# 一.Flask渲染Jinja2模板和传参

## 1如何渲染模板

1. - 模板放在`templates`文件夹下
   - 从`flask`中导入`render_template`函数。
   - 在视图函数中，使用`render_template`函数，渲染模板。注意：只需要填写模板的名字，不需要填写`templates`这个文件夹的路径。(仅仅限html直接在template文件夹下)

## 2.模板传参

- 如果只有一个或者少量参数，直接在`render_template`函数中添加关键字参数就可以了。
  如：

```python
@app.route('/')
def index():
    return render_template('index.html',usename=u'lzh')#传参
```

*如果有多个参数的时候，那么可以先把所有的参数放在字典中，然后在`render_template`中，*
*使用两个星号，把字典转换成关键参数传递进去，这样的代码更方便管理和使用。*

*在模板中，如果要使用一个变量，语法是：`{{params}}`*

*访问模型中的属性或者是字典，可以通过`{{params.property}}`的形式，或者是使用`{{params['age']}}`.*

## 3.Jinja2模板内置的过滤器

1. **abs(value):返回一个数值的绝对值，例如`{{ -1|abs }}`。如果给的参数类型不为数字，就会报错。**
2. **default(value,default_value,boolean=False):如果当前变量没有值，则会使用参数中的值来代替。**
3. **first(value): 返回序列的第一个元素**
4. **last(value): 返回序列的最后一个元素**

```python
# 传入参数为
names = ['小明','小红']
# 模板中使用
{{ names|first }}
{{ names|last }}

```

*注意:*

- *如果是一个字典，那么返回的是`key`的值*

## 4.模板继承

**继承作用和语法：**
**python中的继承**
**\* 作用：可以把一些公共的代码放在父模板中，避免每个模板写同样的代码。**
**\* 语法：**
**`子模板写 {% extends 'base.html' %}`**
**在父模板中写**

> {% block main%}{% endblock %}

**在HTML文件中可以使用模板继承的方式来继承base模板的htmml文件**

**url链接：**
**使用url_for(视图函数名称)可以反转成url。**
**url_for(‘login’)**

**等价于’/login/’**

**加载静态文件：**
**语法：url_for('static',filename='路径')**
**静态文件，flask会从static文件夹中开始寻找，所以不需要再写static这个路径了。**
**可以加载css文件，可以加载js文件，还有image文件。(CSS内放一些背景 字体的设置 js放警告框之类**

```html
#第一个：加载css文件
<link rel="stylesheet" href="{{ url_for('static',filename='css/index.css') }}">
#第二个：加载js文件
<script src="{{ url_for('static',filename='js/index.js') }}"></script>
#第三个：加载图片文件
<img src="{{ url_for('static',filename='images/zhiliao.png') }}" alt="">


```

# 二.Flask-SQLAlchemy

1. **ORM：Object Relationship Mapping（模型关系映射）。**
2. **flask-sqlalchemy是一套ORM框架。**
3. **ORM的好处：可以让我们操作数据库跟操作对象是一样的，非常方便。因为一个表就抽象成一个类，一条数据就抽象成该类的一个对象。**

**配置信息：**

```python
# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'db_demo1'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST
                                             ,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

```

**在主`app`文件中，添加配置文件,也可以通过init_app来绑定app**

```python
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

```

### 1.使用Flask-SQLAlchemy创建模型与表的映射：

***模型需要继承自db.Model，然后需要映射到表中的属性，必须写成db.Column的数据类型。***
***数据类型：***
***db.Integer代表的是整形.***
***db.String代表的是varchar，需要指定最长的长度。***
***db.Text代表的是text。***
***其他参数：***
***primary_key：代表的是将这个字段设置为主键。***
***autoincrement：代表的是这个主键为自增长的。***
***nullable：代表的是这个字段是否可以为空，默认可以为空，可以将这个值设置为False，在数据库中，这个值就不能为空了。***

**创建实例**：

```python
   class Article(db.Model):
    __tablename__='article'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)

db.create_all()

```

*最后需要调用`db.create_all`来将模型真正的创建到数据库中。*

## 2.CURD

### 通过session字段来进行curd 基本的curd函数都在flask文档中

## 3.Flask-SQLAlchemy外键及其关系

```python
​```
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref=db.backref('articles'))#重点新加的 为了方便访问谋篇文章的作者
​```

```

*通过`ForeignKey`方法来创建外键 将不同的模型产生联系 此时可以满足多种模型关系  比如一对多，一对一，多对一*

**` author = db.relationship('User',backref=db.backref('articles'))`解释：**
**给`Article`这个模型添加一个`author`属性，可以访问这篇文章的作者的数据，像访问普通模型一样。 第一个参数`User`是模型名字，他会关联到`Article`中和`User`中有关的外键。**
**`backre`是定义反向引用，可以通过`User.articles`访问这个模型所写的所有文章。即可以用过`author`访问这个作者的所有文章**


