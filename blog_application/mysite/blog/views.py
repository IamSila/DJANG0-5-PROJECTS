from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

# Create your views here.
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 3
    context_object_name = 'posts'
    template_name = "blog/post/list.html"

def post_list(request):

    posts_list = Post.published.all()
    # pagination with 3 posts per page
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get("page", 10)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
# If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
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
