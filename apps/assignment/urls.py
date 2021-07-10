from django.urls import path

from apps.assignment import views

urlpatterns = [
    path(
        'add',
        views.AddAssignmentView.as_view(),
        name='add-assignment'
    ),
    path(
        'list',
        views.ListAssignmentView.as_view(),
        name='list-assignment'
    ),
    path(
        '<str:assignment_id>/update',
        views.UpdateAssignmentView.as_view(),
        name='update-assignment'
    ),
    path(
        '<str:assignment_id>/delete',
        views.DeleteAssignmentView.as_view(),
        name='delete-assignment'
    )
]
