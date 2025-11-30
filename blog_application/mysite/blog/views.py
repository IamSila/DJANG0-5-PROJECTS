from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.
from .models import Post


def post_list(request):

    posts_list = Post.published.all()
    # pagination with 3 posts per page
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.page(page_number)
    return render(request, "blog/post/list.html", {"posts": posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    return render(request, "blog/post/detail.html", {"post": post})
