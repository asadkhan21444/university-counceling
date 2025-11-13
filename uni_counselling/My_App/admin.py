# my_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from .models import (
    CustomUser, Student, Counsellor, CounsellorAvailability,
    Appointment, CounsellingSession, SessionDocument,
    EmergencyContact, CounsellorReview
)

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {
            'fields': ('role', 'phone_number', 'date_of_birth', 'profile_picture')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': ('role', 'phone_number', 'date_of_birth', 'profile_picture')
        }),
    )
    
    actions = ['make_admin', 'make_counsellor', 'make_student']
    
    def make_admin(self, request, queryset):
        queryset.update(role='admin', is_staff=True, is_superuser=True)
        self.message_user(request, "Selected users have been assigned Admin role with full permissions.")
    make_admin.short_description = "Assign Admin role to selected users"
    
    def make_counsellor(self, request, queryset):
        queryset.update(role='counsellor', is_staff=True, is_superuser=False)
        self.message_user(request, "Selected users have been assigned Counsellor role.")
    make_counsellor.short_description = "Assign Counsellor role to selected users"
    
    def make_student(self, request, queryset):
        queryset.update(role='student', is_staff=False, is_superuser=False)
        self.message_user(request, "Selected users have been assigned Student role.")
    make_student.short_description = "Assign Student role to selected users"

# Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user_full_name', 'faculty', 'department', 'academic_year', 'enrollment_date')
    list_filter = ('faculty', 'department', 'academic_year', 'enrollment_date')
    search_fields = ('student_id', 'user__username', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('user_full_name',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_full_name')
        }),
        ('Academic Information', {
            'fields': ('student_id', 'enrollment_date', 'faculty', 'department', 'academic_year')
        }),
        ('Contact Information', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'address')
        }),
    )
    
    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Full Name'

# Counsellor Availability Inline
class CounsellorAvailabilityInline(admin.TabularInline):
    model = CounsellorAvailability
    extra = 1
    fields = ('day_of_week', 'start_time', 'end_time', 'is_active')

# Counsellor Admin
@admin.register(Counsellor)
class CounsellorAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'user_full_name', 'specialization', 'area_of_expertise', 'experience_years', 'is_available')
    list_filter = ('area_of_expertise', 'is_available', 'specialization')
    search_fields = ('license_number', 'user__username', 'user__first_name', 'user__last_name', 'specialization')
    readonly_fields = ('user_full_name', 'total_appointments', 'average_rating')
    inlines = [CounsellorAvailabilityInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_full_name')
        }),
        ('Professional Information', {
            'fields': ('license_number', 'specialization', 'area_of_expertise', 'experience_years', 'qualifications')
        }),
        ('Additional Information', {
            'fields': ('bio', 'is_available', 'max_students')
        }),
        ('Statistics', {
            'fields': ('total_appointments', 'average_rating'),
            'classes': ('collapse',)
        }),
    )
    
    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Full Name'
    
    def total_appointments(self, obj):
        return obj.appointment_set.count()
    total_appointments.short_description = 'Total Appointments'
    
    def average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            avg_rating = sum(review.rating for review in reviews) / reviews.count()
            return f"{avg_rating:.1f}/5"
        return "No ratings yet"
    average_rating.short_description = 'Average Rating'

# Appointment Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_name', 'counsellor_name', 'appointment_date', 'status', 'duration_minutes', 'created_at')
    list_filter = ('status', 'appointment_date', 'counsellor', 'created_at')
    search_fields = ('student__user__username', 'student__user__first_name', 'student__user__last_name',
                    'counsellor__user__username', 'counsellor__user__first_name', 'counsellor__user__last_name',
                    'purpose')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'appointment_date'
    list_editable = ('status',)
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('student', 'counsellor', 'appointment_date', 'duration_minutes', 'status')
        }),
        ('Appointment Information', {
            'fields': ('purpose', 'concerns')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'
    student_name.admin_order_field = 'student__user__first_name'
    
    def counsellor_name(self, obj):
        return obj.counsellor.user.get_full_name()
    counsellor_name.short_description = 'Counsellor'
    counsellor_name.admin_order_field = 'counsellor__user__first_name'

# Session Document Inline
class SessionDocumentInline(admin.TabularInline):
    model = SessionDocument
    extra = 1
    fields = ('document_type', 'file', 'file_name', 'description', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

# Counselling Session Admin
@admin.register(CounsellingSession)
class CounsellingSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment_info', 'session_date', 'follow_up_required', 'follow_up_date', 'rating')
    list_filter = ('session_date', 'follow_up_required', 'rating', 'follow_up_date')
    search_fields = ('appointment__student__user__username', 'appointment__student__user__first_name',
                    'appointment__counsellor__user__username', 'appointment__counsellor__user__first_name')
    readonly_fields = ('session_date',)
    inlines = [SessionDocumentInline]
    
    fieldsets = (
        ('Session Information', {
            'fields': ('appointment', 'session_date')
        }),
        ('Session Details', {
            'fields': ('session_notes', 'counsellor_observations', 'recommendations')
        }),
        ('Follow-up Information', {
            'fields': ('follow_up_required', 'follow_up_date')
        }),
        ('Feedback', {
            'fields': ('rating', 'student_feedback')
        }),
    )
    
    def appointment_info(self, obj):
        return f"{obj.appointment.student.user.get_full_name()} with {obj.appointment.counsellor.user.get_full_name()}"
    appointment_info.short_description = 'Appointment'

# Session Document Admin
@admin.register(SessionDocument)
class SessionDocumentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'document_type', 'session_info', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('file_name', 'session__appointment__student__user__username', 
                    'session__appointment__counsellor__user__username')
    readonly_fields = ('uploaded_at', 'file_preview')
    
    fieldsets = (
        ('Document Information', {
            'fields': ('session', 'document_type', 'file_name', 'description')
        }),
        ('File Details', {
            'fields': ('file', 'uploaded_at', 'file_preview')
        }),
    )
    
    def session_info(self, obj):
        return f"{obj.session.appointment.student.user.get_full_name()} - {obj.session.session_date.strftime('%Y-%m-%d')}"
    session_info.short_description = 'Session'
    
    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file uploaded"
    file_preview.short_description = 'File Preview'

# Emergency Contact Admin
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_name', 'relationship', 'phone_number', 'is_primary')
    list_filter = ('relationship', 'is_primary')
    search_fields = ('name', 'student__user__username', 'student__user__first_name', 'phone_number')
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'

# Counsellor Review Admin
@admin.register(CounsellorReview)
class CounsellorReviewAdmin(admin.ModelAdmin):
    list_display = ('counsellor_name', 'student_name', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('counsellor__user__username', 'counsellor__user__first_name',
                    'student__user__username', 'student__user__first_name', 'review_text')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Review Information', {
            'fields': ('counsellor', 'student', 'rating', 'is_approved')
        }),
        ('Review Content', {
            'fields': ('review_text',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def counsellor_name(self, obj):
        return obj.counsellor.user.get_full_name()
    counsellor_name.short_description = 'Counsellor'
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'

# Custom Admin Actions
def approve_reviews(modeladmin, request, queryset):
    queryset.update(is_approved=True)
approve_reviews.short_description = "Approve selected reviews"

def mark_appointments_completed(modeladmin, request, queryset):
    queryset.update(status='completed')
mark_appointments_completed.short_description = "Mark selected appointments as completed"

def make_counsellors_available(modeladmin, request, queryset):
    queryset.update(is_available=True)
make_counsellors_available.short_description = "Mark selected counsellors as available"

# Add custom actions to respective admins
CounsellorReviewAdmin.actions = [approve_reviews]
AppointmentAdmin.actions = [mark_appointments_completed]
CounsellorAdmin.actions = [make_counsellors_available]

# Group Permission Setup Function
def setup_default_groups():
    """Function to set up default groups with permissions"""
    from django.contrib.auth.models import Group, Permission
    
    # Admin Group - Full permissions
    admin_group, created = Group.objects.get_or_create(name='Administrators')
    if created:
        # Add all model permissions to admin group
        for content_type in ContentType.objects.all():
            permissions = Permission.objects.filter(content_type=content_type)
            admin_group.permissions.add(*permissions)
    
    # Counsellor Group - Limited permissions
    counsellor_group, created = Group.objects.get_or_create(name='Counsellors')
    if created:
        # Add counsellor-specific permissions
        counsellor_permissions = Permission.objects.filter(
            codename__in=[
                'can_view_student_records', 'can_manage_schedule', 
                'can_write_session_notes', 'can_view_all_appointments',
                'can_manage_own_availability', 'can_write_session_notes',
                'can_view_session_history', 'can_upload_documents',
                'can_view_documents', 'can_change_appointment_status'
            ]
        )
        counsellor_group.permissions.add(*counsellor_permissions)
    
    # Student Group - Basic permissions
    student_group, created = Group.objects.get_or_create(name='Students')
    if created:
        student_permissions = Permission.objects.filter(
            codename__in=[
                'can_view_own_appointments', 'can_book_appointment',
                'can_view_own_records', 'can_cancel_appointment',
                'can_write_review'
            ]
        )
        student_group.permissions.add(*student_permissions)
    
    print("Default groups created successfully!")

# Unregister default Group admin if you want custom group management
admin.site.unregister(Group)