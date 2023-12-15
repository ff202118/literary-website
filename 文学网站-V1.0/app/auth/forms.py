from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, URL
from werkzeug.security import check_password_hash
from .models import User
from wtforms import (StringField, RadioField, SelectField, 
    TextAreaField, SelectMultipleField, PasswordField, BooleanField, 
    URLField, EmailField
    )
from app.blog.models import PostPublishType

class LoginForm(FlaskForm):
    # 登陆表单

    def qs_username(username):
        # 对该字段进行在传递之前处理
        u = f'{username}'
        print(u)
        return username

    username = StringField('username', validators=[
        DataRequired(message="不能为空"), 
        Length(max=32, message="不符合字数要求！")
        ], filters=(qs_username,))
    password = PasswordField('password', validators=[
        DataRequired(message="不能为空"),
        Length(max=32, message="不符合字数要求！")
        ])

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is None:
            error = '该用户不存在！'
            raise ValidationError(error)
        elif not check_password_hash(user.password, form.password.data):
            raise ValidationError('用户名或密码不正确!')


class RegisterForm(FlaskForm):
    # 注册表单
    username = StringField('username', validators=[
        DataRequired(message="不能为空"), 
        Length(min=2, max=32, message="超过限制字数！")
        ])
    password = PasswordField('password', validators=[
        DataRequired(message="不能为空"),
        Length(min=2, max=32, message="超过限制字数！"),
        EqualTo('password1', message='两次密码输入不一致！')
        ])
    password1 = PasswordField('password1')

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            error = '该用户名称已存在！'
            raise ValidationError(error)

class PostForm(FlaskForm):
    # 添加文章表单
    title = StringField('标题', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    desc = StringField('描述', validators=[
        DataRequired(message="不能为空"), 
        Length(max=200, message="不符合字数要求！")
    ])
    has_type = RadioField('发布状态', 
        choices=(PostPublishType.draft.name, PostPublishType.show.name), 
        default=PostPublishType.show.name)
    category_id = SelectField(
        '分类', 
        choices=None, 
        coerce=int,
        validators=[
            DataRequired(message="不能为空"),
        ])
    content = TextAreaField('文章详情', 
        validators=[DataRequired(message="不能为空")]
    )
    tags = SelectMultipleField('文章标签', choices=None, coerce=int)

class InspectPostForm(FlaskForm):
    # 添加审核文章表单
    title = StringField('标题', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    desc = StringField('描述', validators=[
        DataRequired(message="不能为空"), 
        Length(max=200, message="不符合字数要求！")
    ])
    category_id = SelectField(
        '分类', 
        choices=None, 
        coerce=int,
        validators=[
            DataRequired(message="不能为空"),
        ])
    content = TextAreaField('文章详情', 
        validators=[DataRequired(message="不能为空")]
    )