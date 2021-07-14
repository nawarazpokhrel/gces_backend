from django.urls import path

from apps.result import views

urlpatterns = [
    path(
        'user/<str:user_id>/add',
        views.AddResultView.as_view(),
        name='add-result'

    ),
    path(
        'user/<str:user_id>/list',
        views.ListResultView.as_view(),
        name='list-result'

    )

]
