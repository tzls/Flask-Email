import os
from os import *
from flask import *
from flask_mail import Mail
from flask_mail import  Message
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap

basedir = os.path.abspath(os.path.dirname(__file__))
#创建Flask类的对象，__name__是程序主模块或包的名字
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zhou123@localhost/flaskuser'
app.config['SQLALCHEMY_COMMIT_ON_TRAEDOWN'] = True
app.config['MAIL_USE_TLS'] = False
app.config['SECRET_KEY']='guess'
#连接到要处理的数据库
db = SQLAlchemy(app)

#对应于数据库中的表和变量
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique = True)
    #返回一个具有可读性的字符串表示模型，可在调试和测试时使用
    def __repr__(self):
        return '<Role %r>'% self.name
    users = db.relationship('User',backref ='role')
class User(db.Model):
    __tablename__ ='users'
    id =db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String(64),unique =True,index= True)
    # 返回一个具有可读性的字符串表示模型，可在调试和测试时使用
    def __repr__(self):
        return '<User u'%r'>'% self.username
    role_id =db.Column(db.Integer,db.ForeignKey('roles.id'))

class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[Required()])
    submit = SubmitField('Submit')

def send_mail(to,subject,template,**kwargs):
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = '#####'
    app.config['MAIL_PASSWORD'] = '######'
    app.config.from_object('config')
    # 邮件主题
    app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
    # 发件人
    app.config['FLASKY_MAIL_SENDER'] = 'tong<1213951064@qq.com>'
    mail = Mail(app)
    #三个参数以此是邮件主题、发送者的邮箱，收件人的邮箱地址
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender = app.config['FLASKY_MAIL_SENDER'],recipients= [to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    mail.send(msg)

#初始化Flask-Script，在程序中使用一个包含所有Bootstrap文件的基模版
bootstrap = Bootstrap(app)
@app.route('/',methods =['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            #if app.config['FLASKY_ADMIN']:
            app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
            send_mail('######@hotmail.com','New User','user',user = user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    #参数依次是模板的文件名，键值对
    return render_template('index.html',form=form,name = session.get('name'),known = session.get('known',False))

# if __name__=='__main__':
#     admin_role = Role(name='Admin')
#     user_tong =User(username='tong',role=admin_role)
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zhou123@localhost/flaskuser'
#     app.config['SQLALCHEMY_COMMIT_ON_TRAEDOWN'] = True
#     db = SQLAlchemy(app)
#     db.session.add(admin_role)
#     db.session.add(user_tong)
#     db.session.commit()
#     print('admin_role',user_tong.id)
if __name__=='__main__':
    app.run(debug=True)



