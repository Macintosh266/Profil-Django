from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login



urlpatterns = [
    path('home/', Menu, name='home'),
    path('login/', LoginView, name='login_user'),
    path('profile/', ProfileView, name='profile_view'),
    path('', ProfileDetail, name='profile_detail'),
    path('posts/create/', CreatePost, name='create_post'),
    path("add_comment/", add_comment, name="add_comment"),
    # path("success/", views.success, name="success"),
    path('post/<int:pk>/', PostDetail, name='post_detail'),
    path('delete/post/<int:pk>/', DeletePost, name='delete_post'),
    path('delete/comment/<int:pk>/', DeleteComment, name='delete_comment'),
    path('/posts/<int:pk>/edit/',Post_Update,name='post_update'),
    path('Logout/', LogoutView, name='logout_user'),
    path('password/send/',PasswordChange,name='password_send'),
    # path("cv/download/", download_cv, name="my_cv_download"),
    path("cv/<int:user_id>/download/",download_cv, name="download_cv"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)