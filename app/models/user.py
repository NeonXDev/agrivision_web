from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db, login_manager


class User(UserMixin, db.Model):
    """A registered farmer/grower. UserMixin supplies is_authenticated,
    is_active, is_anonymous, and get_id() for Flask-Login — the same role
    AppUser + AuthService played in the Flutter build, just Python-native
    here instead of wrapping Firebase.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))
