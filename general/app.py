import os

from flask import Flask, render_template

from request_logging import register_request_logging
from routes.auth import auth_bp
from routes.posts import posts_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config.from_mapping(
        MONITOR_URL=os.environ.get("MONITOR_URL", "http://127.0.0.1:5200/api/events")
    )
    if test_config:
        app.config.update(test_config)
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)
    register_request_logging(app)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", message="요청한 페이지를 찾을 수 없습니다."), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5100)
