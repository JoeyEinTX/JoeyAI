from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .services.db import init as db_init
from .routes.projects import projects_bp
from .routes.messages import messages_bp
from .routes.search import search_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins=["http://localhost"], supports_credentials=True)
    db_init()
    app.register_blueprint(projects_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(search_bp)

    @app.route('/health', methods=['GET'])

    def create_app():
        app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
        app.config.from_object(Config)

        # DB init (optional, won't crash if missing)
        try:
            from .services import db
            if hasattr(db, "init"):
                db.init()
        except Exception as e:
            app.logger.warning(f"DB init warning: {e}")

        # Blueprints
        try:
            from .routes.health import bp as health_bp
            app.register_blueprint(health_bp)
        except Exception as e:
            app.logger.warning(f"Health route missing: {e}")

        @app.route("/")
        def index():
            from flask import render_template
            return render_template("index.html")

        @app.get("/healthz")
        def healthz():
            return {"status": "ok"}

        return app
