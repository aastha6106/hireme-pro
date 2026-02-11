from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship(
        "Resume", backref="owner", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False, default="Untitled Resume")
    summary = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    educations = db.relationship(
        "Education", backref="resume", lazy=True, cascade="all, delete-orphan"
    )
    experiences = db.relationship(
        "Experience", backref="resume", lazy=True, cascade="all, delete-orphan"
    )
    skills = db.relationship(
        "Skill", backref="resume", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Resume {self.title}>"


class Education(db.Model):
    __tablename__ = "educations"

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    school = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200), default="")
    start_date = db.Column(db.String(50), default="")
    end_date = db.Column(db.String(50), default="")
    description = db.Column(db.Text, default="")

    def __repr__(self):
        return f"<Education {self.school}>"


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(50), default="")
    end_date = db.Column(db.String(50), default="")
    description = db.Column(db.Text, default="")

    def __repr__(self):
        return f"<Experience {self.role} at {self.company}>"


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), default="")

    def __repr__(self):
        return f"<Skill {self.name}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))