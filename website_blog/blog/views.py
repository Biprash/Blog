from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

from users.models import User
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm, ProfileUpdateForm

# Create your views here.

def index(request):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-created_date')
    users = User.objects.all()
    paginator = Paginator(posts_list, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {'posts':posts, 'home_page':'active', 'users':users}
    return render(request, 'index.html', context)

def search_view(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        posts = Post.objects.filter(title__icontains=url_parameter)
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:4]

    ctx["posts"] = posts
    if request.is_ajax():
        html = render_to_string(
            template_name="main_post_lists.html", 
            context={"posts": posts}
        )

    data_dict = {"html_from_view": html}

    return JsonResponse(data=data_dict, safe=False)

def About(request):
    context = {'about_page':'active', 'title':'About'}
    return render(request, 'about.html', context)

class NewPost(LoginRequiredMixin,View):
    def get(self,request):
        form = PostForm()
        context = {'form':form, 'new_post_page':'active', 'title':'New Post'}
        return render(request,'new_post.html', context)

    def post(self,request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.author_id = request.user.id
            if 'add_post' in request.POST:
                form.published_date = post.publish()
                form.save(commit=True)                
                messages.success(request, f'Post Published')
            elif 'draft' in request.POST:
                form.save(commit=True)
                messages.success(request, f'Post Saved as Draft')
            else:
                print('error')
        return redirect('blog:home')

def DetailViewPost(request,pk):
    posts = get_list_or_404(Post, pid=pk)
    comments = Comment.objects.filter(post_id=pk).exclude(approved_comment__isnull=True).order_by('-created_date')
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                content = form.save(commit=False)
                content.post_id = pk
                content.author_id = request.user.id
                form.save()
                messages.success(request, f'Your comment has been posted but not been Approved')
                return redirect('blog:post_detail', pk=pk)
        else:
            form = CommentForm()
    else:
        form = CommentForm()
    context = {'posts':posts,'comments':comments,'form':form}
    return render(request, 'post_detail.html', context)

def UserDetailView(request,pk):
    posts_list = Post.objects.filter(author_id=pk).exclude(published_date__isnull=True).order_by('-created_date')
    user = User.objects.filter(id=pk).first()
    
    paginator = Paginator(posts_list, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {'posts':posts, 'user':user}
    return render(request, 'user_detail.html', context)

@login_required
def DraftPost(request,pk):    
    posts_list = Post.objects.filter(author_id=pk).exclude(published_date__lte=timezone.now()).order_by('-created_date')

    paginator = Paginator(posts_list, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {'posts':posts, 'draft_list_page':'active', 'title':'Draft'}
    return render(request, 'draft_list.html', context)

@login_required
def DeletePost(request,pk):
    posts = get_list_or_404(Post, pid=pk)
    if posts[0].author_id == request.user.id:
        Post.objects.filter(pid=pk).delete()
        messages.success(request, f'%s has been Deleated' %posts[0].title)
    return redirect('blog:home')

@login_required
def EditPost(request,pk):
    posts = get_object_or_404(Post, pid=pk)
    if posts.author_id == request.user.id:
        if request.method == 'POST':
            form = PostForm(request.POST or None, instance=posts)
            if form.is_valid():
                posts = form.save(commit=False)
                posts.save()
                return redirect('blog:post_detail', pk=pk)
        else:
            form = PostForm(instance=posts)
            context = {'title':'Edit Post', 'form':form}
    else:
        return redirect('blog:home')
    return render(request, 'new_post.html', context)
    
@login_required
def PublishDraftPost(request,pk):
    posts = get_object_or_404(Post, pid=pk)
    if posts.author_id == request.user.id:
        posts.published_date = timezone.now()
        posts.save()
        messages.success(request, f'%s has been Published' %posts.title)
        return redirect('blog:home')

@login_required
def UserProfile(request,pk):
    user = get_object_or_404(User, id=pk)
    if user.id == request.user.id:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, f'Profile has been Updated!')
                return redirect('blog:profile', pk=pk)
        else:
            # posts = Post.objects.filter(author_id=pk).exclude(published_date__lte=timezone.now()).order_by('-created_date')
            form = ProfileUpdateForm(instance=request.user)
            # query doesnot give right output to right user
            comments = Comment.objects.exclude(approved_comment__lte=timezone.now()).order_by('-created_date')
            context = {'title':'Profile', 'profile_page':'active', 'user':user, 'comments':comments, 'form':form}
        return render(request, 'profile.html', context)
    else:
        return redirect('blog:home')

@login_required
def ApproveComment(request,pk):
    comment = get_object_or_404(Comment, cid=pk)
    user_id = request.user.id
    comment.approved_comment = timezone.now()
    comment.save()
    messages.success(request, f'%s has been Published' %comment.comment_text)
    return redirect('blog:profile', pk=user_id)


@login_required
def DeleteComment(request,pk):
    comment = get_object_or_404(Comment, cid=pk)
    user_id = request.user.id
    comment.delete()
    messages.warning(request, f'%s has been Deleated' %comment.comment_text)
    return redirect('blog:profile', pk=user_id)

