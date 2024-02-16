from pyrogram import Client
from configparser import ConfigParser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import db_path

config = ConfigParser()
config.read('config.ini')

api_id = config.get('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')
name_client = config.get('pyrogram', 'name_client')


engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)

db = Session()
app = Client(name_client, api_id=api_id, api_hash=api_hash)
