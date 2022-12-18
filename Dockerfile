#
FROM python:3.9
#
COPY . /app

#
WORKDIR /app

#
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#
CMD ["waitress-serve", "--listen=0.0.0.0:5000" ,"app:app"]