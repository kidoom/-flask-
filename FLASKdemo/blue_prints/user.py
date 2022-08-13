from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from models import UserModel
from .forms import RegisterForm,LoginForm
from exts import db
bp = Blueprint('user',__name__,url_prefix="/user")

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and user.password == password:
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("邮箱或密码错误")
                return redirect(url_for("user.login"))
        else:
            flash("邮箱或密码格式错误")
            return redirect(url_for("user.register"))

@bp.route("/logout")
def logout():
    #清除session所有数据
    session.clear()
    return redirect(url_for("user.login"))


@bp.route('/register',methods=['GET','POST'])
def register():
   if request.method == "GET":
       return render_template("register.html")
   else:
       form = RegisterForm(request.form)
       if form.validate():  #如果表单验证成功 则重定向进入登陆页面
           email = form.email.data
           username = form.username.data
           password = form.password.data

           user = UserModel(email=email, username=username, password=password)
           db.session.add(user)   #同时储存用户信息
           db.session.commit()
           return redirect(url_for("user.login"))  #重定向url路由
       else:
           return redirect(url_for("user.register"))



