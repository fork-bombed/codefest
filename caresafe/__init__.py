from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

load_dotenv()

bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        bcrypt.init_app(app)
        CORS(app)

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database has been created!")

    @app.cli.command("force-init-db")
    def force_init_db():
        db.drop_all()
        print("Database has been dropped!")
        db.create_all()
        print("Database has been created!")
    
    from caresafe.views import auth, admin, user

    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)

    with app.app_context():
        db.create_all()
    
    return app


app = create_app()
