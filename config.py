class Config(object):
    pass

class DevConfig():
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProdConfig():
    DEBUG = False

app_config = {
    "development": DevConfig,
    "production": ProdConfig,
}