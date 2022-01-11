import os

class Config(object):

    SECRET_KEY=os.getenv('SECRET_KEY')

    #Upload Config
    UPLOAD_DIR=os.path.curdir+'/static/uploads/'
    
    #Database Config
    file_dir=os.path.dirname(__file__)
    BASE_DIR=os.path.join(file_dir,'blog.db')
    SQLALCHEMY_DATABASE_URI='sqlite:///' + BASE_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    #Mail Config
    MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT= 2525
    MAIL_USERNAME = '6be3fd6d6eca6e'
    MAIL_PASSWORD = '9d268826cdaea7'
    MAIL_USE_TLS= True
    MAIL_USE_SSL= False

    RECAPTCHA_PUBLIC_KEY=os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY=os.getenv('RECAPTCHA_PRIVATE_KEY')



class ProductionConfig(Config):

    pass



class DevelopmentConfig(Config):

    debug=True