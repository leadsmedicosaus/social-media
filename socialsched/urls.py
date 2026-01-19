from django.urls import path
from . import views


urlpatterns = [
    path("", views.calendar, name="calendar"),
    path("schedule/<str:isodate>/", views.schedule_form, name="schedule_form"),
    path("schedule-save/<str:isodate>/", views.schedule_save, name="schedule_save"),
    path("schedule-edit/<int:post_id>/", views.schedule_edit, name="schedule_edit"),
    path("schedule-update-media/<int:post_id>/", views.schedule_update_media, name="schedule_update_media"),
    path(
        "schedule-delete/<int:post_id>/", views.schedule_delete, name="schedule_delete"
    ),
    path("login/", views.login_user, name="login"),
    path("auth/firebase/", views.firebase_auth, name="firebase_auth"),
    path("logout/", views.logout_user, name="logout"),
    path("legal/", views.legal, name="legal"),
    path("blog/", views.blog_articles, name="blog_articles"),
    path("blog/<slug:blog_slug>/", views.blog_article, name="blog_article"),
]
