from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager

# Initialize extensions
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.doctors import doctors_bp
    from routes.patients import patients_bp
    from routes.appointments import appointments_bp
    from routes.beds import beds_bp
    from routes.billing import billing_bp
    from routes.emr import emr_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(doctors_bp, url_prefix='/doctors')
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(beds_bp, url_prefix='/beds')
    app.register_blueprint(billing_bp, url_prefix='/billing')
    app.register_blueprint(emr_bp, url_prefix='/emr')

    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', role='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
