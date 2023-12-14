from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.model import Base


db = SQLAlchemy()
db.Model = Base

def create_app(config_filename='instance/config.py'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_pyfile(config_filename)

    # Initialize extensions
    db.init_app(app)

    # Import and register blueprints
    from heatmap import main
    app.register_blueprint(main)

    return app
