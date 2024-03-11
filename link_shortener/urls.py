from django.urls import path

from link_shortener import views

urlpatterns = [
    path(
        "api/redirections/",
        views.create_redirection,
        name="create-redirection",
    ),
    path(
        "api/redirections/-<str:name>/user-info",
        views.get_user_info,
        name="get-user-info",
    ),
    path(
        "api/redirections/-<str:name>/statistics",
        views.get_statistics,
        name="get-statistics",
    ),
    path(
        "-<str:name>",
        views.redirect,
        name="visit-redirection",
    ),
]
