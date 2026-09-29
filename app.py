from flask import Flask
from flask_login import LoginManager

from config import Config
from models import db
from models.user import User

from routes.auth import auth
from routes.image import image

app = Flask(__name__)
app.config.from_object(Config)

# Debug - Print configuration
print("=" * 50)
print("UPLOAD_FOLDER     :", app.config.get("UPLOAD_FOLDER"))
print("ENCRYPTED_FOLDER  :", app.config.get("ENCRYPTED_FOLDER"))
print("DECRYPTED_FOLDER  :", app.config.get("DECRYPTED_FOLDER"))
print("KEY_FOLDER        :", app.config.get("KEY_FOLDER"))
print("=" * 50)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth)
app.register_blueprint(image)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)