class Config():
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123@localhost:3306/assignment'
    SQLALCHEMY_TRACK_MODIFICATIONS=False



config_dict={
    'config': Config,
}