from apps.assignment import usecases


class AssignmentMixin:
    def get_assignment(self):
        return usecases.GetAssignmentUseCase(
            assignment_id=self.kwargs.get('assignment_id')
        ).execute()
