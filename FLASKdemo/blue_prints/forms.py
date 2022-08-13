import wtforms
from wtforms.validators import length,email,EqualTo,InputRequired
from models import EmailCaptchaModel,UserModel

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6,max=20)])





class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3,max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6,max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model and captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("验证码错误！")


    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("邮箱已存在")

class QiestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3,max=20)])
    content = wtforms.StringField(validators=[length(min=5)])

class CommentForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])