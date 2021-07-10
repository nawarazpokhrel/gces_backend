from django.urls import path

from apps.materials import views

urlpatterns = [
path(
        'add',
        views.AddMaterialView.as_view(),
        name='add-material'
    ),
    path(
        'list',
        views.ListMaterialView.as_view(),
        name='list-material'
    ),
    path(
        '<str:material_id>/update',
        views.UpdateMaterialView.as_view(),
        name='update-material'
    ),
    path(
        '<str:material_id>/delete',
        views.DeleteMaterialView.as_view(),
        name='delete-material'
    )
]
