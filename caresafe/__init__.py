from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caresafe.db'

    db.init_app(app)
    bcrypt.init_app(app)

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database has been created!")
    
    from caresafe.views import auth, admin, user

    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)
    
    return app
