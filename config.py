import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@localhost/emr_db?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
