from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import PostForm, EmailPostForm, CommentForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('blog:post_list')
    return render(request, 'blog/post/create.html',{'form':form})

def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts':posts,'page':page})

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                           'comments': comments,
                                           'comment_form': comment_form,
                                           'new_comment': new_comment})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}({cd['email']}), recommends you reading" f"{post.title}"
            message = f'Read "{post.title}" at {post_url}' f'where {cd["name"]} comments {cd["comments"]}'
            send_mail(subject, message, 'admin@gmail.com', [cd['to']])
            sent = True
        
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post': post,
                                                    'form':form,
                                                    'sent': sent})
