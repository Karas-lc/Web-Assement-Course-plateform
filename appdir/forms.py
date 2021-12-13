from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo, Email, Regexp


class RegisterForm(FlaskForm):
    id = StringField(label='User ID',
                     validators=[Regexp("^[ST]\d{8}$", message="Enter Correct Student/Teacher ID!"),
                                 DataRequired(message="Valid ID")])
    name = StringField(label='User Name',
                       validators=[
                           Regexp("(^[a-zA-Z]{1}[a-zA-Z\s]{0,20}[a-zA-Z]{1}$)", message="Enter Correct English Name!"),
                           DataRequired(message="valid Name")])
    password = PasswordField(label='User Password', validators=[DataRequired()])
    repassword = PasswordField(label='Check Password',
                             validators=[DataRequired(), EqualTo('password', 'The passwords are inconsistent')])
    email = StringField(label='Email', validators=[DataRequired(), Email(message="Worng Email Format")])
    submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
    id = StringField(label='Student ID/Work ID',
                     validators=[Regexp("^[ST]\d{8}$", message="Enter Correct Student/Teacher ID!"),
                                 DataRequired(message="Valid ID")])
    password = PasswordField(label='Password', validators=[DataRequired()])
    Loginsubmit = SubmitField(label='Log In')


class NewCourseForm(FlaskForm):
    key = StringField(label='Course Key', validators=[DataRequired()])
    name = StringField(label='Course Name', validators=[DataRequired()])
    semester_year = SelectField(label='Semester-Year',
                                validators=[DataRequired()],
                                render_kw={'class': 'form-control'},
                                choices=[('1', '2021-2022'),('2','2022-2023'),('3', '2023-2024')]
                                )
    semester_term = SelectField(label='Semester-Term',
                                validators=[DataRequired()],
                                render_kw={'class':'form-control'},
                                choices=[('1', 'First Term'),('2','Second Term')])
    Introduction = StringField(label='Course Introduction', validators=[DataRequired()])
    NewCoursesubmit = SubmitField(label='Submit')

class  CourseRegisterForm(FlaskForm):
    key = PasswordField(label='Course Key', validators=[DataRequired()])
    CourseRegisterSubmit = SubmitField(label='Submit')
