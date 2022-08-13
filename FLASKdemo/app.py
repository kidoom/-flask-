from flask import Flask,request,jsonify,session,g
import config
from blue_prints import qa_bp,user_bp
from exts import db
from flask_mail import Mail,Message
from flask_migrate import Migrate
import string,random
from models import EmailCaptchaModel,UserModel
from datetime import datetime
app = Flask(__name__)
# 配置
app.config.from_object(config)
#绑定数据库
db.init_app(app)
migrate = Migrate(app,db)
#绑定邮箱
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG ']  = True
app.config['MAIL_USERNAME'] = "19836086768@163.com"
app.config['MAIL_PASSWORD'] = "HLQDVUAWJETDYMIF"
app.config['MAIL_DEFAULT_SENDER '] = "19836086768@136.com"
mail = Mail(app)
#注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/captcha',methods=['POST']) #验证码实现
def get_captcha():
    # GET POST
    email = request.form.get("email") #获取前端表单数据
    letters = string.ascii_letters+string.digits #通过使用string库来获得字母库和数字库 通过相加获得数字字母库
    captcha = "".join(random.sample(letters,4)) #这个函数将获得的列表转化为字符串
    if email:
        message = Message(
            subject="测试邮箱",
            recipients=[email],  # 获得数据 发送邮件
            body=f"您的注册码是，{captcha},请不要告诉别人！",
            sender='19836086768@163.com'
        )
        mail.send(message)
        captcha_model=EmailCaptchaModel.query.filter_by(email=email).first() #通过orm查询是否邮箱已经存在
        if captcha_model:
            captcha_model.captcha = captcha  #重新设置验证码
            captcha_model.creat_time = datetime.now()
            db.session.commit()
        else:
            #如果不存在已注册的邮箱 则添加一个邮箱
            captcha_model = EmailCaptchaModel(email=email,captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({"code":200})
    else:
        return jsonify({"code":400,"message":"请先发送邮箱"})
# 钩子函数
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给全局绑定一个user的变量，它的值是user这个变量
            g.user = user
        except:
            g.user = None
# 上下文处理器
# 请求来了——》before——request——》视图函数——》视图函数返回模板——》context——processor
@app.context_processor
def context_processeer():
    if hasattr(g,'user'):
        return {"user": g.user}
    else:
        return {}
if __name__ == '__main__':
    app.run()
