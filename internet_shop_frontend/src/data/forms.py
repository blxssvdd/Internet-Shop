from flask_wtf import FlaskForm
import wtforms


class SignUpForm(FlaskForm):
    first_name = wtforms.StringField("Ім'я")
    last_name = wtforms.StringField("Прізвище")
    email = wtforms.EmailField("Електронна пошта", validators=[wtforms.validators.Email(), wtforms.validators.DataRequired()])
    password = wtforms.PasswordField("Пароль", validators=[wtforms.validators.length(6)])
    submit = wtforms.SubmitField("Зареєструватись")


class LoginForm(FlaskForm):
    email = wtforms.EmailField("Електронна пошта", validators=[wtforms.validators.Email(), wtforms.validators.DataRequired()])
    password = wtforms.PasswordField("Пароль", validators=[wtforms.validators.length(6)])
    submit = wtforms.SubmitField("Увійти")