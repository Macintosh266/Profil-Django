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
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.colors import HexColor
# from reportlab.platypus import Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO

from .models import UserProfil  # siz UserProfil nomi bilan yozgansiz


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


@login_required(login_url='login_user')
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
            from_email=email,
            recipient_list=["mtosh662@gmail.com"],  # Sizning emailingiz
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

class Custom404View(TemplateView):
    template_name = "404.html"

    def render_to_response(self, context, **response_kwargs):
        """Always return 404 status code with this template."""
        response_kwargs.setdefault("status", 404)
        return super().render_to_response(context, **response_kwargs)

def ProfileDetail(request):
    profil = UserProfil.objects.first()
    skill=Skill.objects.all()
    education=Education.objects.all()
    post=Post.objects.all()
    context = {
        'profil': profil,
        'title': 'Profil ma\'lumotlari',
        'skills':skill,
        'education':education,
        'post':post
        # 'user':user,
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





# def download_cv(request, user_id):
#     profile = UserProfil.objects.get(user__id=user_id)  # Profilni olamiz
#
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#     width, height = A4
#     y = height - 50
#     styles = getSampleStyleSheet()
#
#     def new_page_if_needed(current_y, margin=50):
#         nonlocal p
#         if current_y < margin:
#             p.showPage()
#             p.setFillColor(HexColor("#0f1724"))
#             p.rect(0, 0, width, height, fill=1)
#             return height - 50
#         return current_y
#
#     # Background
#     p.setFillColor(HexColor("#0f1724"))
#     p.rect(0, 0, width, height, fill=1)
#
#     # Header - Username + Bio
#     p.setFont("Helvetica-Bold", 24)
#     p.setFillColor(HexColor("#6EE7B7"))
#     p.drawString(40, y, f"{profile.user.username} — Backend Developer")
#     y -= 30
#
#     if profile.bio:
#         y = new_page_if_needed(y)
#         style = styles["Normal"]
#         style.fontName = "Helvetica"
#         style.fontSize = 12
#         style.textColor = HexColor("#cfeef4")
#         p_obj = Paragraph(profile.bio, style)
#         w, h = p_obj.wrap(width - 80, y)
#         p_obj.drawOn(p, 40, y - h)
#         y -= h + 20
#
#     # Skills
#     if profile.skills.exists():
#         y = new_page_if_needed(y)
#         p.setFont("Helvetica-Bold", 14)
#         p.setFillColor(HexColor("#60A5FA"))
#         p.drawString(40, y, "Ko‘nikmalar:")
#         y -= 20
#
#         for skill in profile.skills.all():
#             y = new_page_if_needed(y)
#             p.setFont("Helvetica", 12)
#             p.setFillColor(HexColor("#e6eef8"))
#             p.drawString(50, y, f"- {skill.name}")
#             y -= 15
#         y -= 10
#
#     # Education
#     if profile.education.exists():
#         y = new_page_if_needed(y)
#         p.setFont("Helvetica-Bold", 14)
#         p.setFillColor(HexColor("#60A5FA"))
#         p.drawString(40, y, "Ta'lim:")
#         y -= 20
#
#         for edu in profile.education.all():
#             y = new_page_if_needed(y)
#             p.setFont("Helvetica-Bold", 12)
#             p.setFillColor(HexColor("#e6eef8"))
#             p.drawString(50, y, f"{edu.degree or ''} - {edu.institution}")
#             y -= 15
#             if edu.description:
#                 style.fontSize = 11
#                 p_obj = Paragraph(edu.description, style)
#                 w, h = p_obj.wrap(width - 100, y)
#                 p_obj.drawOn(p, 60, y - h)
#                 y -= h + 15
#
#     # Projects (Postlardan)
#     posts = profile.user.post_set.all()  # User bilan bog‘langan Postlar
#     if posts.exists():
#         y = new_page_if_needed(y)
#         p.setFont("Helvetica-Bold", 14)
#         p.setFillColor(HexColor("#60A5FA"))
#         p.drawString(40, y, "Loyihalar:")
#         y -= 20
#
#         for post in posts:
#             y = new_page_if_needed(y)
#             p.setFont("Helvetica-Bold", 12)
#             p.setFillColor(HexColor("#e6eef8"))
#             p.drawString(50, y, f"{post.title}")
#             y -= 15
#             style.fontSize = 11
#             p_obj = Paragraph(post.content, style)
#             w, h = p_obj.wrap(width - 100, y)
#             p_obj.drawOn(p, 60, y - h)
#             y -= h + 15
#
#     # Contact info
#     y = new_page_if_needed(y)
#     p.setFont("Helvetica-Bold", 14)
#     p.setFillColor(HexColor("#60A5FA"))
#     p.drawString(40, y, "Aloqa:")
#     y -= 20
#
#     contact_info = [
#         ("Telefon", profile.phone_number),
#         ("Website", profile.website),
#         ("Instagram", profile.instagram),
#         ("Telegram", profile.telegram),
#         ("Manzil", profile.address),
#     ]
#     for label, value in contact_info:
#         if value:
#             y = new_page_if_needed(y)
#             p.setFont("Helvetica", 12)
#             p.setFillColor(HexColor("#e6eef8"))
#             p.drawString(50, y, f"{label}: {value}")
#             y -= 15
#
#     # Finalize PDF
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#
#     return FileResponse(buffer, as_attachment=True, filename=f"{profile.user.username}_cv.pdf")

