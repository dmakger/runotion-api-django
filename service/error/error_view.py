from .error import ErrorHelper


class TaskError(ErrorHelper):
    def is_not_found(self):
        return self.get_error(error="Такой задачи не существует", status=self.NOT_FOUND)


class ProjectError(ErrorHelper):
    def is_not_found(self):
        return self.get_error(error="Такого проекта не существует", status=self.NOT_FOUND)
