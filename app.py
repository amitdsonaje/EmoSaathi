from flask import Flask
from routes.capture import capture_bp
from routes.chat import chat_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(capture_bp)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(debug=True)

