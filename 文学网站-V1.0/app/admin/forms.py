from flask_wtf import FlaskForm
from wtforms import (StringField, RadioField, SelectField, 
    TextAreaField, SelectMultipleField, PasswordField, BooleanField, 
    URLField, EmailField, IntegerField
    )
from wtforms.validators import DataRequired, Length, URL
from app.blog.models import PostPublishType

class CategoryForm(FlaskForm):
    # 分类表单
    name = StringField('分类名称', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    icon = StringField('分类描述', validators=[ 
        Length(max=256, message="不符合字数要求！")
    ])


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

class TagForm(FlaskForm):
    # 标签表单
    name = StringField('标签', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])


from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed

class CreateUserForm(FlaskForm):
    # 创建表单
    username = StringField('username', validators=[
        DataRequired(message="不能为空"), 
        Length(max=32, message="不符合字数要求！")
        ])
    password = PasswordField('password', validators=[
        Length(max=32, message="不符合字数要求！")
        ], description="修改用户信息时，留空则代表不修改！")
    avatar = FileField("avatar", validators=[
        FileAllowed(['jpg', 'png', 'gif'], message="仅支持jpg/png/gif格式"),
        FileSize(max_size=2048000, message="不能大于2M")],
        description="大小不超过2M，仅支持jpg/png/gif格式，不选择则代表不修改")
    desc = StringField('desc', validators=[Length(max=150, message="字数超限！")])
    gexing = StringField('个性签名', validators=[Length(max=100, message="字数超限！")])
    email = EmailField('邮箱',)
    gender = SelectField('性别', choices=(('man', '男'),('women','女')))
    address = StringField('地址', validators=[Length(max=150, message="字数超限！")])
    is_super_user = BooleanField("是否为管理员")
    is_active = BooleanField("是否活跃", default=True)
    is_first_user = BooleanField("是否为茶余饭后管理员")
    is_second_user = BooleanField("是否为风花雪月管理员")
    is_third_user = BooleanField("是否为校园故事管理员")
    is_fourth_user = BooleanField("是否为以诗会友管理员")
    is_staff = BooleanField("是否锁定")

class BannerForm(FlaskForm):
    # banner表单
    img = FileField("Banner图", validators=[
        FileAllowed(['jpg', 'png', 'gif'], message="仅支持jpg/png/gif格式"),
        FileSize(max_size=3 * 1024 * 1000, message="不能大于3M")],
        description="大小不超过3M，仅支持jpg/png/gif格式，不选择则代表不修改, 尺寸比例：3:1")

    desc = StringField('描述', validators=[
        # DataRequired(message="不能为空"), 
        Length(max=200, message="不符合字数要求！")
        ])

    url = URLField("Url", validators=[
        URL(require_tld=False, message="请输入正确的url"),
        Length(max=300, message="不符合字数要求！")])
    
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
