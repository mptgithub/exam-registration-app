from django.test import TestCase
from django.contrib.auth.models import User
from .models import ExamSession, Registration
from django.urls import reverse
from django.utils import timezone
import datetime

class PortalTestCase(TestCase):

    def setUp(self):
        # Create users
        self.student1 = User.objects.create_user('student1', 'student1@example.com', 'password')
        self.student2 = User.objects.create_user('student2', 'student2@example.com', 'password')

        # Create exam sessions
        self.session1 = ExamSession.objects.create(
            title='Math Exam',
            description='A test of your math skills.',
            start_time=timezone.now() + datetime.timedelta(days=1),
            end_time=timezone.now() + datetime.timedelta(days=1, hours=2),
            capacity=1
        )
        self.session2 = ExamSession.objects.create(
            title='History Exam',
            description='A test of your history knowledge.',
            start_time=timezone.now() + datetime.timedelta(days=2),
            end_time=timezone.now() + datetime.timedelta(days=2, hours=2),
            capacity=10
        )
        self.session3 = ExamSession.objects.create(
            title='Science Exam',
            description='A test of your science knowledge.',
            start_time=timezone.now() + datetime.timedelta(days=3),
            end_time=timezone.now() + datetime.timedelta(days=3, hours=2),
            capacity=10
        )
        self.session4 = ExamSession.objects.create(
            title='Art Exam',
            description='A test of your art skills.',
            start_time=timezone.now() + datetime.timedelta(days=4),
            end_time=timezone.now() + datetime.timedelta(days=4, hours=2),
            capacity=10
        )

    def test_exam_session_available_seats(self):
        """Test the available_seats property of the ExamSession model."""
        self.assertEqual(self.session1.available_seats, 1)
        Registration.objects.create(student=self.student1, exam_session=self.session1)
        self.assertEqual(self.session1.available_seats, 0)

    def test_exam_session_list_view(self):
        """Test the exam session list view."""
        response = self.client.get(reverse('portal:exam_session_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.session1.title)
        self.assertContains(response, self.session2.title)

    def test_my_registrations_view_authenticated(self):
        """Test the my_registrations view for an authenticated user."""
        self.client.login(username='student1', password='password')
        Registration.objects.create(student=self.student1, exam_session=self.session1)
        response = self.client.get(reverse('portal:my_registrations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.session1.title)

    def test_my_registrations_view_unauthenticated(self):
        """Test the my_registrations view for an unauthenticated user."""
        response = self.client.get(reverse('portal:my_registrations'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('portal:my_registrations')}")

    def test_register_for_session_success(self):
        """Test successful registration for a session."""
        self.client.login(username='student1', password='password')
        response = self.client.get(reverse('portal:register_for_session', args=[self.session2.id]))
        self.assertRedirects(response, reverse('portal:my_registrations'))
        self.assertTrue(Registration.objects.filter(student=self.student1, exam_session=self.session2).exists())

    def test_register_for_session_no_seats(self):
        """Test registration for a session with no available seats."""
        Registration.objects.create(student=self.student2, exam_session=self.session1)
        self.client.login(username='student1', password='password')
        response = self.client.get(reverse('portal:register_for_session', args=[self.session1.id]))
        self.assertRedirects(response, reverse('portal:exam_session_list'))
        self.assertFalse(Registration.objects.filter(student=self.student1, exam_session=self.session1).exists())

    def test_register_for_session_duplicate(self):
        """Test registering for the same session twice."""
        self.client.login(username='student1', password='password')
        Registration.objects.create(student=self.student1, exam_session=self.session2)
        response = self.client.get(reverse('portal:register_for_session', args=[self.session2.id]))
        self.assertRedirects(response, reverse('portal:my_registrations'))
        # Check that only one registration exists
        self.assertEqual(Registration.objects.filter(student=self.student1, exam_session=self.session2).count(), 1)

    def test_register_for_session_max_limit(self):
        """Test registering for more than three sessions."""
        self.client.login(username='student1', password='password')
        Registration.objects.create(student=self.student1, exam_session=self.session1)
        Registration.objects.create(student=self.student1, exam_session=self.session2)
        Registration.objects.create(student=self.student1, exam_session=self.session3)

        response = self.client.get(reverse('portal:register_for_session', args=[self.session4.id]))
        self.assertRedirects(response, reverse('portal:exam_session_list'))
        self.assertFalse(Registration.objects.filter(student=self.student1, exam_session=self.session4).exists())
