from ctypes import pointer
from flask import (
    Blueprint, render_template, request, 
    flash, redirect, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db
from app.auth.views.auth import login_required
from app.blog.models import Category, Post, Tag, Comment, inspect_post
from app.auth.models import User
from .models import Banner
from .forms import CategoryForm, PostForm, TagForm, CreateUserForm, InspectPostForm
from flask import Blueprint, flash, render_template, request, redirect, url_for, session, g

bp = Blueprint('admin', __name__, url_prefix='/admin', 
    static_folder='static', template_folder='templates')


@bp.route('/')
@login_required
def index():
    post_count = Post.query.count()
    user_count = User.query.count()
    return render_template('admin/index.html', post_count=post_count, user_count=user_count)

@bp.route('/inspect')
@login_required
def inspect():
    # 文章审核
    post_count = Post.query.count()
    user_count = User.query.count()
    return render_template(
        'admin/inspect.html', post_count=post_count, user_count=user_count)


@bp.route('/article_inspect')
@login_required
def article_inspect():
    # 板块文章审核
    page = request.args.get('page', 1, type=int)
    pagination = inspect_post.query.order_by(-inspect_post.add_date).paginate(
        page=page, per_page=10, error_out=False)
    post_list = pagination.items
    for post in post_list:
        print(post.title)
    print(g.user.inspect)
    return render_template(
        'admin/article_inspect.html', 
        post_list=post_list, pagination=pagination, inspect=g.user.inspect)


@bp.route('/article_detail/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_detail(post_id):
    post = inspect_post.query.get_or_404(post_id)
    form = InspectPostForm(
        title=post.title,
        desc=post.desc,
        category_id=post.category_id,
        content=post.content,
    )
    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    
    if form.validate_on_submit():
        P = Post(
                title=form.title.data,
                desc=form.desc.data,
                category_id=int(form.category_id.data),  # 一对多保存
                content=form.content.data,
                user_id=inspect_post.query.filter(inspect_post.id == post_id).first().user_id
        )

        db.session.add(P)
        post.is_pass = True
        post.is_inspect = True
        db.session.commit()
        flash(f'{form.title.data}审核成功，请为文章添加标签')  

        if g.user.is_super_user:
            return redirect(url_for('admin.article'))
        else:
            return redirect(url_for('admin.article_alter'))  

    return render_template(
        'admin/article_detail.html', 
        post=post, form=form
    )

@bp.route('/article_fail/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_fail(post_id):
    post = inspect_post.query.get_or_404(post_id)
    title = post.title

    post.is_pass = False
    post.is_inspect = True
    db.session.commit()
    flash(f'{title}审核成功')  
    if g.user.is_super_user:
        return redirect(url_for('admin.article'))
    else:
        return redirect(url_for('admin.article_alter')) 

@bp.route('/article_alter')
@login_required
def article_alter():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.category_id==g.user.inspect) \
    .order_by(Post.add_date).paginate(page, per_page=10, error_out=False)
    post_list = pagination.items
    inspect = g.user.inspect
    return render_template(
        'admin/article_alter.html', 
        post_list=post_list, 
        pagination=pagination,
        inspect=inspect
    )


@bp.route('/category')
@login_required
def category():
    # 查看分类
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(
        -Category.add_date).paginate(
            page=page, per_page=10, error_out=False)
    category_list = pagination.items
    return render_template(
        'admin/category.html', 
        category_list=category_list, 
        pagination=pagination
    )


@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def category_add():
    # 新增文章分类
    form = CategoryForm()
    if form.validate_on_submit():
        name = Category.query.filter(Category.name==form.name.data)
        if name is None:
            category = Category(name=form.name.data, icon=form.icon.data)
            db.session.add(category)
            db.session.commit()
            flash(f'{form.name.data}分类添加成功')
            return redirect(url_for('admin.category'))
        else:
            flash(f'{form.name.data} 分类名重复')
            return redirect(url_for('admin.category_add'))
    return render_template('admin/category_form.html', form=form)


@bp.route('/category/edit/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def category_edit(cate_id):
    # 编辑文章分类
    cate = Category.query.get(cate_id)
    form = CategoryForm(name=cate.name, icon=cate.icon)
    if form.validate_on_submit():
        cate.name = form.name.data
        cate.icon = form.icon.data
        db.session.add(cate)
        db.session.commit()
        flash(f'{form.name.data}分类修改成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)


@bp.route('/category/delete/<int:cate_id>')
@login_required
def category_del(cate_id):
    cate = Category.query.get(cate_id)
    try:
        if cate:
            # 级联删除
            Post.query.filter(Post.category_id==cate.id).delete()
            db.session.delete(cate)
            db.session.commit()
            flash(f'{cate.name}分类删除成功')
            return redirect(url_for('admin.category'))
    except:
        flash(f'{cate.name} 分类下有很多文章，请先让版主清理文章后进行删除！')
        return redirect(url_for('admin.category'))

@bp.route('/article')
@login_required
def article():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(
        page=page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template(
        'admin/article.html', 
        post_list=post_list, 
        pagination=pagination
    )


@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    # 新增文章
    form = PostForm()   
    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id, v.name) for v in Tag.query.all()]
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            desc=form.desc.data,
            has_type=form.has_type.data,
            category_id=int(form.category_id.data),  # 一对多保存
            content=form.content.data,
            user_id=g.user.id
        )
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data ]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}添加成功')
        if g.user.is_super_user:
            return redirect(url_for('admin.article'))
        else:
            return redirect(url_for('admin.article_alter'))
    arr = ['none','茶余饭后', '风花雪月', '校园故事', '以诗会友']
    
    if g.user.inspect == None:
        index = 0
    else:
        index = g.user.inspect
    inspect = arr[index]

    return render_template('admin/article_form.html', form=form, flag=g.user.is_super_user,inspect=inspect)


@bp.route('/article/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_edit(post_id):
    # 修改文章
    post = Post.query.get(post_id)
    tags = [tag.id for tag in post.tags]
    form = PostForm(
        title=post.title,
        desc=post.desc,
        category_id=post.category.id,
        has_type=post.has_type.value,
        content=post.content,
        tags=tags,
    )

    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id, v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        # 这里才是修改的逻辑
        print(type(form.has_type.data))
        # 一个,引起的bug  StatementError
        post.title=form.title.data
        post.desc=form.desc.data
        post.has_type=form.has_type.data
        post.category_id=int(form.category_id.data)  # 一对多保存
        post.content=form.content.data
        post.tags=[Tag.query.get(tag_id) for tag_id in form.tags.data ]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}修改成功')
        if g.user.is_super_user:
            return redirect(url_for('admin.article'))
        else:
            return redirect(url_for('admin.article_alter'))
    return render_template('admin/article_form.html', form=form, post=post, flag=g.user.is_super_user)


@bp.route('/article/delete/<int:post_id>')
@login_required
def article_del(post_id):
    # 删除文章
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.title}删除成功')
        if g.user.is_super_user:
            return redirect(url_for('admin.article'))
        else:
            return redirect(url_for('admin.article_alter'))


@bp.route('/tag')
@login_required
def tag():
    # 查看标签列表
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(-Tag.add_date).paginate(page=page, per_page=10, error_out=False)
    tag_list = pagination.items
    return render_template('admin/tag.html', tag_list=tag_list, pagination=pagination)


@bp.route('/tag/add', methods=['GET', 'POST'])
@login_required
def tag_add():
    # 增加标签
    form = TagForm()
    if form.validate_on_submit():
        try:
            tag = Tag(name=form.name.data)
            db.session.add(tag)
            db.session.commit()
            flash(f'{form.name.data}添加成功')
            return redirect(url_for('admin.tag'))
        except:
            flash(f'{form.name.data} 重复标签名!')
            return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_form.html', form=form)


@bp.route('/tag/edit/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_edit(tag_id):
    # 修改标签
    try:    
        tag = Tag.query.get(tag_id)
        form = TagForm(name=tag.name)
        if form.validate_on_submit():
            tag.name = form.name.data
            db.session.add(tag)
            db.session.commit()
            flash(f'{form.name.data}修改成功')
            return redirect(url_for('admin.tag'))
    except:
            flash(f'{form.name.data} 重复标签名!')
            return redirect(url_for('admin.tag_add'))    
    return render_template('admin/tag_form.html', form=form)


@bp.route('/tag/del/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_del(tag_id):
    # 删除标签
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        flash(f'{tag.name}删除成功')
        return redirect(url_for('admin.tag'))

    
@bp.route('/user')
@login_required
def user():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(-User.add_date).paginate(
        page=page, per_page=10, error_out=False)
    user_list = pagination.items
    return render_template(
        'admin/user.html', 
        user_list=user_list, 
        pagination=pagination)


@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    # 添加用户
    form = CreateUserForm()
    form.gender.data='man'
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                is_super_user=form.is_super_user.data,
                is_active=form.is_active.data,
                is_staff=form.is_staff.data,
                is_first_user=form.is_first_user.data,
                is_second_user=form.is_second_user.data,
                is_third_user=form.is_third_user.data,
                is_fourth_user=form.is_fourth_user.data
            )
            if user.is_first_user:
                user.inspect=1
            elif user.is_second_user:
                user.inspect=2
            elif user.is_third_user:
                user.inspect=3
            elif user.is_fourth_user:
                user.inspect=4
            db.session.add(user)
            db.session.commit()
            flash(f'{form.username.data}添加成功！')
            return redirect(url_for('admin.user'))
        except:
            flash(f'{form.username.data}重复的用户名！')
            return redirect(url_for('admin.user_add'))
    return render_template('admin/user_form.html', form=form)


@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    # 修改用户信息
    user = User.query.get(user_id)
    form = CreateUserForm(
        username=user.username,
        password=user.password,
        avatar=user.avatar,
        gender='man',
        is_super_user=user.is_super_user,
        is_active=user.is_active,
        is_staff=user.is_staff,
        is_first_user=user.is_first_user,
        is_second_user=user.is_second_user,
        is_third_user=user.is_third_user,
        is_fourth_user=user.is_fourth_user
    )
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            if not form.password.data:
                user.password = user.password
            else:
                user.password = generate_password_hash(form.password.data)
            user.is_super_user = form.is_super_user.data
            user.is_active = form.is_active.data
            user.is_staff = form.is_staff.data
            user.is_first_user = form.is_first_user.data
            user.is_second_user = form.is_second_user.data
            user.is_third_user = form.is_third_user.data
            user.is_fourth_user = form.is_fourth_user.data
            if user.is_first_user:
                user.inspect=1
            elif user.is_second_user:
                user.inspect=2
            elif user.is_third_user:
                user.inspect=3
            elif user.is_fourth_user:
                user.inspect=4

            db.session.add(user)
            db.session.commit()
            flash(f'{user.username}修改成功！')
            return redirect(url_for('admin.user'))
        except:
            flash(f'{form.username.data}重复用户名！')
            return redirect(url_for('admin.user_edit',user_id=user_id))
    return render_template('admin/user_form.html', form=form, user=user)


@bp.route('/user/del/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_del(user_id):
    # 删除用户
    user = User.query.get(user_id)
    if not user.is_staff:
        db.session.delete(user)
        db.session.commit()
        flash(f'{user.username}删除成功')
        return redirect(url_for('admin.user'))
    else:
        flash(f'{user.username}已锁定')
        return redirect(url_for('admin.user'))

@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    # 上传图片
    if request.method == 'POST':
        # 获取一个文件类型 request.files
        f = request.files.get('upload')
        file_size = len(f.read())
        f.seek(0)  # reset cursor position to beginning of file

        if file_size > 2048000:  # 限制上传大小为2M
            return {
                'code':'err',
                'message': '文件超过限制2048000字节',
            }
        
        from .utils import upload_file_path
        upload_path, filename = upload_file_path('upload', f)
        f.save(upload_path)
        return {
            'code':'ok',
            'url':f'/admin/static/upload/{filename}'
        }


@bp.route('/comment')
@login_required
def comment():
    # 留言列表
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(-Comment.add_date).paginate(
        page=page, per_page=10, error_out=False)
    comment_list = pagination.items
    return render_template(
        'admin/comment.html', 
        comment_list=comment_list, 
        pagination=pagination
    )


@bp.route('/comment/del/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def comment_del(comment_id):
    # 删除留言
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        flash(f'{comment.content}删除成功')
        return redirect(url_for('admin.comment'))