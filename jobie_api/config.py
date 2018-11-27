#/usr/bin/python3
"""  
config.py - Configuration for Flask application  
"""

import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Default configuration"""
    ENV = 'production'
    database_path = os.path.join(basedir, 'database.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(database_path)


class DevelopmentConfig(BaseConfig):
    """Development configuration using config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(basedir, 'config.ini')
    config.read(config_path)

    ENV = 'development'
    DEBUG = config.get('DEFAULT', 'DEBUG').lower() == 'true'
    TESTING = config.get('DEFAULT', 'TESTING').lower() == 'true'
    SECRET_KEY = config.get('DEFAULT', 'SECRET_KEY')
    FACE_API_KEY = config.get('DEFAULT', 'FACE_API_KEY')
    VISION_API_KEY = config.get('DEFAULT', 'VISION_API_KEY')
    TEXT_API_KEY = config.get('DEFAULT', 'TEXT_API_KEY')
    FB_USERNAME = config.get('DEFAULT', 'FB_USERNAME')
    FB_PASSWORD = config.get('DEFAULT', 'FB_PASSWORD')

    def save():
        with open(config_path, 'w') as write_file:
            config.write(write_file)


class ProductionConfig(BaseConfig):
    """Production configuration using environment variable"""
    ENV = 'production'
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    TESTING = os.getenv('TESTING', 'false').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'ISuckAtTeamNames')
    FACE_API_KEY = os.getenv('FACE_API_KEY', None)
    VISION_API_KEY = os.getenv('VISION_API_KEY', None)
    TEXT_API_KEY = os.getenv('TEXT_API_KEY', None)
    FB_USERNAME = os.getenv('FB_USERNAME', None)
    FB_PASSWORD = os.getenv('FB_USERNAME', None)
