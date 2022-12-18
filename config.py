import configparser

config = configparser.ConfigParser()
config.read('config.txt')

database_uri = config.get('database', 'con')
