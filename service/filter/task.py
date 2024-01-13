from service.filter.filter import Filter


class TaskFilter(Filter):
    COMPLETED = 'completed'
    PROJECT_ID = 'project_id'

    def full(self):
        super().full()
        self.completed()
        self.project()

    def completed(self):
        if self.COMPLETED not in self.request.data.keys():
            return None
        self.result['completed_at__isnull'] = not self.request.data[self.COMPLETED]

    def project(self):
        if self.PROJECT_ID not in self.request.data.keys():
            return None
        self.result['project__id'] = self.request.data[self.PROJECT_ID]
