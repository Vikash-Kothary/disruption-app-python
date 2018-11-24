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


class ProductionConfig(BaseConfig):
    """Production configuration using environment variable"""
    ENV = 'production'
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    TESTING = os.getenv('TESTING', 'false').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'ISuckAtTeamNames')
