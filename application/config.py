class Config:
    """Base configuration."""
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:JonJamLil24!@localhost/lesson5_db"
    CACHE_TYPE = "SimpleCache"
    DEBUG = True
    CACHE_DEFAULT_TIMEOUT = 300

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}