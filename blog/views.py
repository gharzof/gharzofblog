from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post, Category, Tag
import requests
from django.conf import settings

def home(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')

    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    paginator = Paginator(posts.order_by('-created_at'), 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "index.html", {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
    })

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:6]
    return render(request, 'detail.html', {
        'post': post,
        'related_posts': related_posts,
        'request': request
    })

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def add_post(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        tags_ids = request.POST.getlist('tags')

        response = requests.post(
            f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendDocument",
            data={'chat_id': settings.CHAT_ID, 'caption': title},
            files={'document': image}
        )

        if response.status_code == 200:
            file_id = response.json().get('result', {}).get('document', {}).get('file_id')
            file_info = requests.get(f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={file_id}").json()
            file_path = file_info.get('result', {}).get('file_path')
            telegram_file_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file_path}"

            post = Post.objects.create(
                title=title,
                image=telegram_file_url,
                content=content,
                category_id=category_id,
            )
            post.tags.set(tags_ids)
            post.save()

            return redirect('/detail/' + post.slug + '/')

        post = Post.objects.create(
            title=title,
            content=content,
            category_id=category_id,
        )
        post.tags.set(tags_ids)
        post.save()

        return redirect('/detail/' + post.slug + '/')

    return render(request, 'add_post.html', {
        'categories': categories,
        'tags': tags
    })

def about(request):
    return render(request, 'about.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)
