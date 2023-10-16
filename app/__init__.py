from flask import Flask
from flask_login import LoginManager
from .db import db, create_collections, insert_user, insert_category

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "random" 

    # create_collections()
    # insert_category()
    # insert_user()

    from app.controllers.auth_controller import auth
    from app.controllers.category_controller import category
    from app.controllers.comment_controller import comment
    from app.controllers.media_controller import media
    from app.controllers.notification_controller import notification
    from app.controllers.post_controller import post
    from app.controllers.user_controller import user
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(category, url_prefix='/categories')
    app.register_blueprint(comment, url_prefix='/comments')
    app.register_blueprint(media, url_prefix='/media')
    app.register_blueprint(notification, url_prefix='/notifications')
    app.register_blueprint(post, url_prefix='/posts')
    app.register_blueprint(user, url_prefix='/users')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return db.User.find()

    return app
