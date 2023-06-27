from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user_id>", views.profile_page, name="profile"),  
    path("following", views.following, name="following"),
    # API Routes
    path("get_post/<int:post_id>", views.get_post, name="get_post"),
    path("get_posts", views.get_posts, name="get_posts"),
    path("update_post/<int:post_id>", views.update_post, name="update_post"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("dislike_post/<int:post_id>", views.dislike_post, name="dislike_post")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # media url path

