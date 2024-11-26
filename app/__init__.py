# Base Modules
import os

# Other Modules
from flask import Flask

# ROUTES
from app.routes.base import base 
from app.routes.api import api
from app.routes.player import player
from app.routes.admin import admin

# DOTENV
from dotenv import load_dotenv
load_dotenv()

# DB
from app.configs.db import mongo

# Create flask istance
app = Flask(__name__)

def create_app():
    # Dotenv
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['TEAMS_LOGO_PATH'] = os.getenv('TEAMS_LOGO_PATH')

    # Initialize MongoDB connection
    mongo.init_app(app)

    # Register blueprints
    app.register_blueprint(base)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(player, url_prefix='/player')
    app.register_blueprint(admin, url_prefix='/admin')

    return app