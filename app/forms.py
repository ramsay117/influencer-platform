from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    FloatField,
    SubmitField,
    SelectField,
    DateField,
)
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=1, max=64)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=1, max=64)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), EqualTo("confirm_password")]
    )
    confirm_password = PasswordField("Confirm Password")
    role = SelectField(
        "Role",
        choices=[("sponsor", "Sponsor"), ("influencer", "Influencer")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")


class CampaignForm(FlaskForm):
    name = StringField("Campaign Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    budget = FloatField("Budget", validators=[DataRequired()])
    visibility = SelectField(
        "Visibility",
        choices=[("public", "Public"), ("private", "Private")],
        validators=[DataRequired()],
    )
    goals = TextAreaField("Goals", validators=[DataRequired()])
    submit = SubmitField("Create Campaign")


class AdRequestForm(FlaskForm):
    influencer_id = SelectField("Influencer", coerce=int, validators=[DataRequired()])
    requirements = TextAreaField("Requirements", validators=[DataRequired()])
    payment_amount = FloatField("Payment Amount", validators=[DataRequired()])
    submit = SubmitField("Send Request")
