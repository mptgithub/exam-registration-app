from django.db import models
from django.contrib.auth.models import User

class ExamSession(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    @property
    def registered_students_count(self):
        return self.registration_set.count()

    @property
    def available_seats(self):
        return self.capacity - self.registered_students_count

class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exam_session')

    def __str__(self):
        return f"{self.student.username} registered for {self.exam_session.title}"
