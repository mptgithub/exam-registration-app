from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExamSession, Registration
from django.contrib import messages
from django.core.mail import send_mail

def exam_session_list(request):
    sessions = ExamSession.objects.all()
    return render(request, 'portal/exam_session_list.html', {'sessions': sessions})

@login_required
def register_for_session(request, session_id):
    session = get_object_or_404(ExamSession, pk=session_id)
    student = request.user

    # 1. Check for available seats
    if session.available_seats <= 0:
        messages.error(request, f"Sorry, there are no available seats for {session.title}.")
        return redirect('portal:exam_session_list')

    # 2. Prevent duplicate registration for the same session
    if Registration.objects.filter(student=student, exam_session=session).exists():
        messages.warning(request, f"You are already registered for {session.title}.")
        return redirect('portal:my_registrations')

    # 3. Limit total registrations per student
    if Registration.objects.filter(student=student).count() >= 3:
        messages.error(request, "You cannot register for more than three exam sessions.")
        return redirect('portal:exam_session_list')

    # If all checks pass, create the registration
    Registration.objects.create(student=student, exam_session=session)
    messages.success(request, f"You have successfully registered for {session.title}.")

    # Send confirmation email
    if student.email:
        send_mail(
            'Exam Registration Confirmation',
            f'Dear {student.first_name or student.username},\n\nYou have successfully registered for the exam: {session.title}.\n\nThank you!',
            'no-reply@example.com',
            [student.email],
            fail_silently=False,
        )

    return redirect('portal:my_registrations')

@login_required
def my_registrations(request):
    registrations = Registration.objects.filter(student=request.user)
    return render(request, 'portal/my_registrations.html', {'registrations': registrations})
