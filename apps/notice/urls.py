from django.urls import path

from apps.notice import views

urlpatterns = [
    path(
        'add',
        views.AddNoticeView.as_view(),
        name='add-notice'
    ),
    path(
        'list',
        views.ListNoticeView.as_view(),
        name='list-notice'
    )
]
