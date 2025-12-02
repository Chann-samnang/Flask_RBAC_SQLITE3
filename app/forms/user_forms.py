# forms/user_forms.py

import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Optional,
)
from app.models import User
from extensions import db

# ----- helpers -----

def strong_password(form, field):
    """Require: min 8 chars, upper, lower, digit, special"""
    password = field.data or ""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search("[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search("[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search("[0-9]", password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        raise ValidationError("Password must contain at least one special character.")

# ----- create form (password required) -----

class UserCreateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "Username"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "Email"},
    )
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(max=120)],
        render_kw={"placeholder": "Full name"},
    )
    is_active = BooleanField("Active", default=True)

    password = PasswordField(
        "Password",
        validators=[DataRequired(), strong_password],
        render_kw={"placeholder": "Strong password"},
    )

    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password don't match!"),
        ],
        render_kw={"placeholder": "Confirm password"},
    )

    submit = SubmitField("Save")

    # ---- server-side uniqueness checks ----

    def validate_username(self, field):
        exists = db.session.scalar(
            db.select(User).filter(User.username == field.data)
        )
        if exists:
            raise ValidationError("This username is already taken.")

    def validate_email(self, field):
        exists = db.session.scalar(
            db.select(User).filter(User.email == field.data)
        )
        if exists:
            raise ValidationError("This email is already registered.")

# ---- edit form (password optional) ----

class UserEditForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    full_name = StringField(
        "Full name",
        validators=[Length(max=120)],
    )
    is_active = BooleanField("Active")

    # optional password - only change if filled
    password = PasswordField(
        "New Password (leave blank to keep current)",
        validators=[Optional(), strong_password, Length(min=6)],
    )
    password2 = PasswordField(
        "Confirm New Password",
        validators=[EqualTo("password", message="Password don't match!")],
    )

    submit = SubmitField("Update")

    def __init__(self, original_user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_user = original_user

    def validate_username(self, field):
        if (
            field.data != self.original_user.username
            and User.query.filter_by(username=field.data).first()
        ):
            raise ValidationError("This username is already taken.")

    def validate_email(self, field):
        if (
            field.data != self.original_user.email
            and User.query.filter_by(email=field.data).first()
        ):
            raise ValidationError("This email is already registered.")

# ---- delete confirmation form ----

class ConfirmDeleteForm(FlaskForm):
    submit = SubmitField("Confirm Delete")
