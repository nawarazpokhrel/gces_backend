from apps.materials import usecases


class MaterialMixin:
    def get_material(self):
        return usecases.GetMaterialUseCase(
            material_id=self.kwargs.get('material_id')
        ).execute()
