from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContactForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired("Please tell me your name."), Length(max=120)])
    email = EmailField(
        "Email",
        validators=[DataRequired("I need an email address to reply."), Email("That email address doesn't look right."), Length(max=200)],
    )
    company = StringField("Business name", validators=[Optional(), Length(max=160)])
    message = TextAreaField(
        "What's slowing your business down?",
        validators=[
            DataRequired("A sentence or two is enough."),
            Length(min=10, max=5000, message="Please write between 10 and 5,000 characters."),
        ],
    )
    # Honeypot. Hidden from people; bots fill it in.
    website = StringField("Leave this empty", validators=[Optional()])
