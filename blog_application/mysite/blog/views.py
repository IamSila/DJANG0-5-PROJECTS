from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.
from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request,year, month, day, post):
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug = post,
                            publish_month = month,
                            publish_year = year
    )
    return render(request, "blog/post/detail.html", {"post": post})
