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
    ),
    path(
        '<str:notice_id>/update',
        views.UpdateNoticeView.as_view(),
        name='update-notice'
    ),
    path(
        '<str:notice_id>/delete',
        views.DeleteNoticeView.as_view(),
        name='delete-notice'
    )
]
