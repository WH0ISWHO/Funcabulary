from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from dotenv import load_dotenv
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI') + os.path.join(app.instance_path, 'vocabulary.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)


    db.init_app(app)
    migrate.init_app(app, db)

    db_path = os.path.join("instance", "vocabulary.db")
    if not os.path.exists(db_path):
        with open(db_path, "w") as f:
            pass
        db.create_all()

    from .views import views_bp
    # prefixing within the address bar/url info to show a certain string. Leave blank if you dont want.
    app.register_blueprint(views_bp, url_prefix='/')

    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404 - Page Not Found</h1>", 404

    return app