from flask import Blueprint, render_template, request, g, flash, redirect, url_for
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from RealProject import db

bp = Blueprint('blog', __name__, url_prefix='/blog', 
    static_folder='static', template_folder='templates')


def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page=page, per_page=9, error_out=False)
    post_list = pagination.items

    import random
    imgs = [
        'https://scpic.chinaz.net/files/default/imgs/2023-06-08/d781fa28b7aa7db0.jpg', 
        'https://scpic.chinaz.net/files/pic/pic9/201406/apic4293.jpg', 
        'https://scpic.chinaz.net/files/pic/pic9/201909/zzpic20201.jpg']

    for post in post_list:
        post.img = random.sample(imgs, 1)[0]

    import json
    from app.admin.models import Banner
    banners = Banner.query.all()
    banners_list = [{'img': f'/admin/static/{banner.img}', 'url': banner.url} for banner in banners]
    banners_json = json.dumps(banners_list, ensure_ascii=False)
    return render_template('index.html', posts=post_list, pagination=pagination, banners=banners_json)


@bp.route('/category/<int:cate_id>')
def cates(cate_id):
    # 文章列表页
    cate = Category.query.get(cate_id)
    page = request.args.get('page', default=1, type=int)

    pagination = Post.query.filter(Post.category_id==cate_id).paginate(
        page=page, per_page=10, error_out=False)
    
    post_list = pagination.items

    return render_template(
        'cate_list.html', 
        post_list=post_list, 
        cate=cate,
        cate_id=cate_id,
        pagination=pagination)


@bp.route('/category/<int:cate_id>/<int:post_id>', methods=['GET', 'POST'])
def detail(cate_id, post_id):
    cate = Category.query.get(cate_id)
    post = Post.query.get_or_404(post_id)
    # 上一篇
    prev_post = Post.query.filter(Post.id < post_id).order_by(-Post.id).first()
    # 下一篇
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id).first()

    # 留言列表
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter(Comment.post_id==post.id).order_by(-Comment.add_date).paginate(
        page=page, per_page=10, error_out=False)
    comment_list = pagination.items
    
    # 留言功能
    form = CommentForm()
    # 验证表单数据
    if form.validate_on_submit():
        # 保存留言到数据库
        comment = Comment(
            content=form.content.data,
            post_id=post.id,
            user_id=g.user.id
        )
        db.session.add(comment)
        db.session.commit()
        # 传递成功信息
        flash(f'留言成功！')
        # 留言成功跳转到留言列表区
        return redirect(f"{url_for('blog.detail', cate_id=cate.id, post_id=post.id)}#comment")
    
    return render_template(
        'detail.html', cate=cate, post=post, 
        prev_post=prev_post, next_post=next_post, 
        pagination=pagination, comment_list=comment_list,
        form=form
    )


@bp.context_processor
def inject_archive():
    # 文章归档日期注入上下文
    posts = Post.query.order_by(-Post.add_date)
    dates = set([post.add_date.strftime("%Y年%m月") for post in posts])
    
    # 标签
    tags = Tag.query.all()
    for tag in tags:
        tag.style = ['is-success', 'is-danger', 'is-black', 'is-light', 'is-primary', 'is-link', 'is-info', 'is-warning']

    # 最新文章
    new_posts = posts.limit(6)
    return dict(dates=dates, tags=tags, new_posts=new_posts)


@bp.route('/category/<string:date>')
def archive(date):
    # 归档页
    import re
    # 正则匹配年月
    regex = re.compile(r'\d{4}|\d{2}')
    dates = regex.findall(date)
    
    from sqlalchemy import extract, and_, or_
    page = request.args.get('page', 1, type=int)
    # 根据年月获取数据
    archive_posts = Post.query.filter(
        and_(extract('year', Post.add_date) == int(dates[0]), 
            extract('month', Post.add_date) == int(dates[1])
            )
        )
    # 对数据进行分页
    pagination = archive_posts.paginate(page=page, per_page=5, error_out=False)
    return render_template('archive.html', 
        post_list=pagination.items,  pagination=pagination, date=date)


@bp.route('/tags/<int:tag_id>')
def tags(tag_id):
    # 标签页
    tag = Tag.query.get(tag_id)
    return render_template('tags.html', post_list=tag.post, tag=tag)


@bp.route('/search')
def search():
    # 搜索页
    words = request.args.get("words")
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(
        Post.title.like("%"+words+"%")).paginate(
            page=page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('search.html', post_list=post_list, words=words, pagination=pagination)