from flask import Flask
from .config import Config  # relative import so it works anywhere

def create_app():
    app = Flask(__name__)
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

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app

# WSGI entrypoint
app = create_app()
