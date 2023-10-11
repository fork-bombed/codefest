from flask import Flask
from caresafe.views.admin import bp as admin_bp
from caresafe.views.user import bp as user_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    
    return app
