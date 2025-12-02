# app/__init__.py

from flask import Flask, redirect, url_for
from extensions import db, csrf
from config import Config
from app.routes.user_routes import user_bp

def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    app.register_blueprint(user_bp)

    # Define root route
    @app.route("/")
    def root():
        return redirect(url_for("users.index"))
    # Create database tables
    with app.app_context():
        db.create_all()
        print ("Database tables created.")

    return app
