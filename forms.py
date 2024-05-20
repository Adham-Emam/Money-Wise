from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from models import User, Income, Expenses


class IncomeForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(
        min=0.01)], render_kw={"placeholder": "Amount"})
    source = StringField('Source', validators=[DataRequired()], render_kw={
                         "placeholder": "Source"})
    submit = SubmitField('Add Income')


class ExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(
        min=0.01)], render_kw={"placeholder": "Amount"})
    description = StringField('Description', validators=[
                              DataRequired()], render_kw={"placeholder": "Description"})
    submit = SubmitField('Add Expense')


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[DataRequired()], render_kw={
        "placeholder": "Password"})
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo(
        'password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={
        "placeholder": "Username"})
    password = PasswordField(validators=[DataRequired()], render_kw={
        "placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
