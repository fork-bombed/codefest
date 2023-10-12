from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from flask_apscheduler import APScheduler

load_dotenv()

bcrypt = Bcrypt()
db = SQLAlchemy()
scheduler = APScheduler()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
    db.init_app(app)
    bcrypt.init_app(app)
    if scheduler.state == 0:
        scheduler.init_app(app)
        scheduler.start()
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
