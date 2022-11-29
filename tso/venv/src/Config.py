class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin123'
    MYSQL_DB = 'entidadbancaria'


config = {
    'development': DevelopmentConfig
}
