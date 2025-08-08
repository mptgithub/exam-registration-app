from django.contrib import admin
from .models import ExamSession, Registration

class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'capacity', 'available_seats')
    search_fields = ('title', 'description')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam_session', 'registration_time')
    list_filter = ('exam_session',)
    search_fields = ('student__username', 'exam_session__title')

admin.site.register(ExamSession, ExamSessionAdmin)
admin.site.register(Registration, RegistrationAdmin)
