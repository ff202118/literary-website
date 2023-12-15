from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    # 分类表单
    content = TextAreaField('分类名称', validators=[
        DataRequired(message="不能为空"), 
        Length(max=200, message="不符合字数要求！")
    ])