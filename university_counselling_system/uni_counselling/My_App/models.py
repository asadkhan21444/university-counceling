# my_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
###############################################################################################################################
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('counsellor', 'Counsellor'),
        ('admin', 'Administrator'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ("can_access_admin_panel", "Can access admin panel"),
            ("can_manage_users", "Can manage users"),
            ("can_manage_appointments", "Can manage appointments"),
            ("can_view_reports", "Can view reports"),
            ("can_manage_counsellors", "Can manage counsellors"),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def is_student(self):
        return self.role == 'student'
    
    def is_counsellor(self):
        return self.role == 'counsellor'
    
    def is_admin(self):
        return self.role == 'admin'
###############################################################################################################################
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(max_length=20, unique=True)
    enrollment_date = models.DateField()
    FACULTY_CHOICES = (
        ('engineering', 'Engineering'),
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('business', 'Business'),
        ('medicine', 'Medicine'),
        ('law', 'Law'),
    )
    
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES)
    department = models.CharField(max_length=100)
    academic_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    
    class Meta:
        permissions = [
            ("can_view_own_appointments", "Can view own appointments"),
            ("can_book_appointment", "Can book appointment"),
            ("can_view_own_records", "Can view own records"),
            ("can_cancel_appointment", "Can cancel appointment"),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"
###############################################################################################################################
class Counsellor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField(default=0)
    qualifications = models.TextField()
    bio = models.TextField(blank=True, null=True)
    
    AREA_OF_EXPERTISE_CHOICES = (
        ('academic', 'Academic Counselling'),
        ('career', 'Career Counselling'),
        ('personal', 'Personal Counselling'),
        ('mental_health', 'Mental Health'),
        ('crisis', 'Crisis Intervention'),
    )
    
    area_of_expertise = models.CharField(max_length=50, choices=AREA_OF_EXPERTISE_CHOICES)
    is_available = models.BooleanField(default=True)
    max_students = models.IntegerField(default=20)
    
    class Meta:
        permissions = [
            ("can_view_student_records", "Can view student records"),
            ("can_manage_schedule", "Can manage schedule"),
            ("can_write_session_notes", "Can write session notes"),
            ("can_view_all_appointments", "Can view all appointments"),
            ("can_manage_own_availability", "Can manage own availability"),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"
###############################################################################################################################
class CounsellorAvailability(models.Model):
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['counsellor', 'day_of_week']
        verbose_name_plural = 'Counsellor Availabilities'
    
    def __str__(self):
        return f"{self.counsellor.user.username} - {self.get_day_of_week_display()}"
###############################################################################################################################
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    purpose = models.TextField()
    concerns = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date']
        unique_together = ['counsellor', 'appointment_date']
        permissions = [
            ("can_change_appointment_status", "Can change appointment status"),
            ("can_view_all_appointments", "Can view all appointments"),
        ]
    
    def __str__(self):
        return f"Appointment: {self.student.user.username} with {self.counsellor.user.username} on {self.appointment_date}"
###############################################################################################################################
class CounsellingSession(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    session_date = models.DateTimeField(auto_now_add=True)
    session_notes = models.TextField()
    counsellor_observations = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True, null=True
    )
    student_feedback = models.TextField(blank=True, null=True)
    
    class Meta:
        permissions = [
            ("can_write_session_notes", "Can write session notes"),
            ("can_view_session_history", "Can view session history"),
        ]
    
    def __str__(self):
        return f"Session for {self.appointment.student.user.username} - {self.session_date}"
###############################################################################################################################
class SessionDocument(models.Model):
    DOCUMENT_TYPES = (
        ('assessment', 'Assessment Form'),
        ('consent', 'Consent Form'),
        ('progress', 'Progress Notes'),
        ('report', 'Report'),
        ('other', 'Other'),
    )
    
    session = models.ForeignKey(CounsellingSession, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='session_documents/')
    file_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = [
            ("can_upload_documents", "Can upload documents"),
            ("can_view_documents", "Can view documents"),
        ]
    
    def __str__(self):
        return f"{self.file_name} - {self.session}"
###############################################################################################################################
class EmergencyContact(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'phone_number']
    
    def __str__(self):
        return f"{self.name} ({self.relationship}) - {self.student.user.username}"
###############################################################################################################################
class CounsellorReview(models.Model):
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['counsellor', 'student']
        permissions = [
            ("can_write_review", "Can write review"),
            ("can_moderate_reviews", "Can moderate reviews"),
        ]
    
    def __str__(self):
        return f"Review for {self.counsellor.user.username} by {self.student.user.username}"
###############################################################################################################################
# Signal to create user profile when user is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            Student.objects.create(
                user=instance, 
                student_id=f"STU{instance.id:06d}",
                enrollment_date=timezone.now().date()
            )
        elif instance.role == 'counsellor':
            Counsellor.objects.create(
                user=instance, 
                license_number=f"LIC{instance.id:06d}"
            )

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'student' and hasattr(instance, 'student'):
        instance.student.save()
    elif instance.role == 'counsellor' and hasattr(instance, 'counsellor'):
        instance.counsellor.save()