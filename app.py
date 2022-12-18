import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from waitress import serve
from config import database_uri
from models import db, Announcement
from form import AnnouncementForm
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.secret_key = os.urandom(15)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
ma = Marshmallow(app)

db.init_app(app)
path = os.getcwd()


class AnnouncementSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "date", "title", "media")


UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def post_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        file = form.upload.data
        title = form.title.data
        date = form.date.data.strftime('%B %d, %Y')
        ext = secure_filename(file.filename)[-4:]
        filename = '-'.join(title.split()) + '-' + form.date.data.strftime('%B-%d-%Y') + ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        post = Announcement(date, title, filename)
        db.session.add(post)
        db.session.commit()
        flash('File successfully uploaded')
        return redirect('/')
    return render_template('upload.html', form=form)


@app.route('/api/v1/announcements', methods=['GET'])
def get_all():
    announcement = Announcement.query.order_by(desc(Announcement.id)).all()
    announcement_schema = AnnouncementSchema(many=True)
    return announcement_schema.dump(announcement)


@app.route('/api/v1/announcement/<announcement_id>', methods=['GET'])
def get_article(announcement_id):
    announcement = Announcement.query.filter_by(id=announcement_id).first()
    return send_from_directory(app.config['UPLOAD_FOLDER'], announcement.media)


if __name__ == "__main__":
    #    app.run(host='0.0.0.0', port=5000)
    serve(app, host='0.0.0.0', port=5000)
