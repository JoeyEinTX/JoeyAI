
from flask import Flask, render_template
from flask_cors import CORS
from .config import Config
from .services.db import init as db_init
from .routes.projects import projects_bp
from .routes.messages import messages_bp
from .routes.search import search_bp
from .routes.health import bp as health_bp

def create_app():
    import os
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.abspath(os.path.join(base_dir, '..', 'frontend', 'templates'))
    static_dir = os.path.abspath(os.path.join(base_dir, 'static'))
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )
    app.config.from_object(Config)
    CORS(app, origins=["http://localhost"], supports_credentials=True)
    db_init()
    app.register_blueprint(projects_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(health_bp)
    from .routes.conversation_routes import conversations_bp
    from .routes.chat_routes import chat_bp
    app.register_blueprint(conversations_bp)
    app.register_blueprint(chat_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()
