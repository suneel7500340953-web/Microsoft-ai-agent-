from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    DateField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from .models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=128)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValueError("Email already registered.")


class SampleForm(FlaskForm):
    sample_code = StringField(
        "Sample Code", validators=[DataRequired(), Length(max=50)]
    )
    collection_date = DateField("Collection Date", validators=[DataRequired()])
    status = SelectField(
        "Status",
        choices=[
            ("received", "Received"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ],
        default="received",
        validators=[DataRequired()],
    )
    organism = StringField("Organism", validators=[Optional(), Length(max=100)])
    result = TextAreaField("Result", validators=[Optional()])
    submit = SubmitField("Save")