from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.entities import User


class LoginForm(FlaskForm):
    
    '''Класс наследуется от FlaskForm и содержит поля формы входа пользователя

    Четыре класса, которые представляют типы полей, которые я использую для этой 
    формы, импортируются непосредственно из пакета WTForms, поскольку расширение 
    Flask-WTF не предоставляет настраиваемые версии. Для каждого поля объект 
    создается как переменная класса в классе LoginForm. Каждому полю присваивается 
    описание или метка в качестве первого аргумента.
    '''

    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
   
    '''Класс наследуется от FlaskForm и содержит поля формы регистрации пользователя

    Пять классов, которые представляют типы полей, которые я использую для этой 
    формы, импортируются непосредственно из пакета WTForms, поскольку расширение 
    Flask-WTF не предоставляет настраиваемые версии. Для каждого поля объект 
    создается как переменная класса в классе LoginForm. Каждому полю присваивается 
    описание или метка в качестве первого аргумента.
    '''

    login = StringField('Login', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        '''Метод класса RegistrationForm(FlaskForm)

        Метод возвращает ошибку ValidationError() в случае, если логин, введённый
        пользователем not None, то есть логин уже содержится в базе данных.
        
        Аргументы функции:
        username -- строка
        '''
        user = User.query.filter_by(login=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        '''Метод класса RegistrationForm(FlaskForm)

        Метод возвращает ошибку ValidationError() в случае, если email, введённый
        пользователем not None, то есть email уже содержится в базе данных.

        Аргументы функции:
        email -- строка
        '''
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')