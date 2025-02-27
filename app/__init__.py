from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

db = SQLAlchemy()
migrate = Migrate()

from dotenv import load_dotenv
def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI') + os.path.join(app.instance_path, 'vocabulary.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views_bp
    # prefixing within the address bar/url info to show a certain string. Leave blank if you dont want.
    app.register_blueprint(views_bp, url_prefix='/')

    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404 - Page Not Found</h1>", 404

    return app