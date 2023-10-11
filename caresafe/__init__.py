from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://spaghetti:@penne23@spaggettihoopos.postgres.database.azure.com/spaggettihoopos'

    bcrypt.init_app(app)

    @app.cli.command("init-db")
    def init_db():
        db = SQLAlchemy(app)
        print("Database has been created!")
    from caresafe.views import auth, admin, user

    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)
    
    return app
