import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres1:password@192.168.1.33:5432/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '4bff634f62da0165ccaaf031e4daed83ca43b1697c0756564d416aad6d6a4586')

