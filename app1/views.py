from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.views.generic import TemplateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from django.http import FileResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def LoginView(request):
    if request.method == 'POST':
        form = LoginUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Login yoki parol noto‘g‘ri.')
    else:
        form = LoginUser()

    return render(request, 'login_user.html', {'form': form})


@login_required(login_url='login_user')
def Menu(request):
    posts = Post.objects.filter(author=request.user)
    comments = Comment.objects.filter(author=request.user)
    profil = get_object_or_404(UserProfil, user=request.user)

    context = {
        'posts': posts,
        'comments': comments,
        'profil': profil,
    }
    return render(request, 'index.html', context=context)


@login_required(login_url='login_user')
def ProfileView(request):
    if request.method == 'GET':
        profil = get_object_or_404(UserProfil, user=request.user)
        form = UserProfilForm(instance=profil)
        context = {
            'title': 'Profilni tahrirlash',
            'form': form,
            'profil': profil,
        }
    else:
        profil = get_object_or_404(UserProfil, user=request.user)
        form = UserProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('home')
        context = {
            'form': form,

            'profil': profil,
        }
    return render(request, 'profil_update.html', context=context)


@login_required(login_url='login_user')
def CreatePost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def add_comment(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        full_message = f"""
        Yangi xabar:
        Ism: {first_name}
        Familiya: {last_name}
        Email: {email}
        Xabar: {message}
        """
        send_mail(
            subject=f"Portfolio contact: {first_name} {last_name}",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["mtosh662@gmail.com"],
        )
        return redirect('profile_detail')

    return render(request, "profil_detail.html")


@login_required(login_url='login_user')
def PostDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


@login_required(login_url='login_user')
@require_POST
def DeletePost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('home')
    post.delete()
    return redirect('home')


@login_required(login_url='login_user')
def DeleteComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect('home')
    comment.delete()
    return redirect('home')

def custom_404(request, exception=None):
    """Custom 404 handler API uchun"""
    # API so'rov ekanligini tekshiring
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Not Found',
            'message': 'The requested resource was not found.',
            'status_code': 404
        }, status=404)
    
    # Web sahifa uchun oddiy 404
    return render(request, '404.html', status=404)

def custom_500(request):
    """Custom 500 handler"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred.',
            'status_code': 500
        }, status=500)
    
    return render(request, '500.html', status=500)

def ProfileDetail(request):
    profil = UserProfil.objects.all().first()
    skill=Skill.objects.all()
    education=Education.objects.all()
    post=Post.objects.all()
    user=User.objects.all().first()
    context = {
        'profil': profil,
        'title': 'Profil ma\'lumotlari',
        'skills':skill,
        'education':education,
        'post':post,
        'user':user,
    }

    return render(request, 'profil_detail.html', context=context)


@login_required(login_url='login_user')
def Post_Update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    context = {
        'title': 'Postni tahrirlash',
        'form': form,
        'post': post,
    }
    return render(request, 'post_update.html', context=context)


@login_required(login_url='login_user')
def LogoutView(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='login_user')
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            if not request.user.check_password(old_password):
                form.add_error('old_password', 'Eski parol noto‘g‘ri.')
            else:
                new_password = form.cleaned_data.get('new_password1')
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Parolingiz muvaffaqiyatli o‘zgartirildi.')
                return redirect('home')
    else:
        form = PasswordChangeForm()
    return render(request, 'password_change.html', {'form': form})

