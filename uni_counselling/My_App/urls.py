from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # root route
    path('services/', views.ServicesView.as_view(), name='services'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('system_user_home/',views.system_user_home,name='system_user_home'),
########################################################################################
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
###########################################################################################################################################################
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    ####################################################################################################
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/update/<str:pk>/', views.student_update, name='student_update'),
    path('students/delete/<str:pk>/', views.student_delete, name='student_delete'),
    ############################################################################################
    path("counsellors/", views.counsellor_list, name="counsellor_list"),
    path("counsellors/add/", views.counsellor_add, name="counsellor_add"),
    path("counsellors/update/<str:pk>/", views.counsellor_update, name="counsellor_update"),
    path("counsellors/delete/<str:pk>/", views.counsellor_delete, name="counsellor_delete"),
    ####################################################################################################
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    ######################################################################################################
    path('availability/', views.availability_list, name="availability_list"),
    path('availability/add/', views.availability_add, name="availability_add"),
    path('availability/update/<int:pk>/', views.availability_update, name="availability_update"),
    path('availability/delete/<int:pk>/', views.availability_delete, name="availability_delete"),
    #################################################################################################
    path("admin_session_list/", views.admin_session_list, name="admin_session_list"),
    path("sessions/add/", views.admin_session_add, name="session_add"),
    path("sessions/update/<int:pk>/", views.admin_session_update, name="admin_session_update"),
    path("sessions/delete/<int:pk>/", views.admin_session_delete, name="admin_session_delete"),
    #######################################################################################################
    path('documents/', views.session_document_list, name='session_document_list'),
    path('documents/add/', views.session_document_add, name='session_document_add'),
    path('documents/<int:pk>/edit/', views.session_document_edit, name='session_document_edit'),
    path('documents/<int:pk>/delete/', views.session_document_delete, name='session_document_delete'),
    #######################################################################################################
    path('emergency-contacts/', views.emergency_contact_list, name='emergency_contact_list'),
    path('emergency-contacts/add/', views.emergency_contact_add, name='emergency_contact_add'),
    path('emergency-contacts/update/<int:pk>/', views.emergency_contact_update, name='emergency_contact_update'),
    path('emergency-contacts/delete/<int:pk>/', views.emergency_contact_delete, name='emergency_contact_delete'),
    ###################################################################################################################
    path("reviews/", views.review_list, name="review_list"),
    path("reviews/add/", views.review_add, name="review_add"),
    path("reviews/update/<int:pk>/", views.review_update, name="review_update"),
    path("reviews/delete/<int:pk>/", views.review_delete, name="review_delete"),
    ######################################################################################################################
    path("reports/students/", views.student_report, name="student_report"),
    path("reports/students/pdf/", views.export_student_pdf, name="export_student_pdf"),
    path("reports/students/excel/", views.export_student_excel, name="export_student_excel"),

    path("reports/counselling/", views.counselling_report, name="counselling_report"),
    path("reports/counselling/pdf/", views.export_counselling_pdf, name="export_counselling_pdf"),
    path("reports/counselling/excel/", views.export_counselling_excel, name="export_counselling_excel"),

    path("reports/appointments/", views.appointment_report, name="appointment_report"),
    path("reports/appointments/pdf/", views.export_appointment_pdf, name="export_appointment_pdf"),
    path("reports/appointments/excel/", views.export_appointment_excel, name="export_appointment_excel"),
    ######################################################################################################################
    # Role management
    path("roles/", views.role_list, name="role_list"),
    path("roles/add/", views.role_add, name="role_add"),
    path("roles/edit/<int:pk>/", views.role_edit, name="role_edit"),
    path("roles/delete/<int:pk>/", views.role_delete, name="role_delete"),
    # User management (System Settings)
    path("settings/users/", views.user_list, name="user_list"),
    path("settings/users/add/", views.user_add, name="user_add"),
    path("settings/users/edit/<int:pk>/", views.user_edit, name="user_edit"),
    path("settings/users/delete/<int:pk>/", views.user_delete, name="user_delete"),
#########################################################################################################################################################################
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    ###################################################################################
    path('student_appointment_list/',views.student_appointment_list,name='student_appointment_list'),
    path('Student_appointment_create/',views.Student_appointment_create,name='Student_appointment_create'),
    ############################################################################################################
    path('student_session_list/',views.student_session_list,name='student_session_list'),
    #############################################################################################
    path('student_session_document_list/',views.student_session_document_list,name='student_session_document_list'),
    ##################################################################################################################
    path('student_emergency_contact_list/',views.student_emergency_contact_list,name='student_emergency_contact_list'),
    ########################################################################################################################
    path("student_review_list/", views.student_review_list, name="student_review_list"),
    path("student_review_add/add/", views.student_review_add, name="student_review_add"),
    path("student_review_update/update/<int:pk>/", views.student_review_update, name="student_review_update"),
    ######################################################################################################################
    path('student_user_list/',views.student_user_list,name='student_user_list'),
#########################################################################################################################################################################
    path('counsellor/dashboard/', views.counsellor_dashboard, name='counsellor_dashboard'),
    ########################################################################################################
    path('counseller_appointment_list/',views.counseller_appointment_list,name='counseller_appointment_list'),
    ###################################################################################################################
    path("availability/manage/", views.manage_availability, name="manage_availability"),
    path("availability/add/", views.add_availability, name="add_availability"),
    path("availability/update/<int:pk>/", views.update_availability, name="update_availability"),
    path("availability/delete/<int:pk>/", views.delete_availability, name="delete_availability"),
    path("availability/view/", views.view_availability, name="view_availability"),
    #####################################################################################
    path('my_sessions_list/', views.session_list, name='my_sessions_list'),
    path('my_sessions_list/add/', views.session_create, name='my_session_create'),
    path('sessions/<int:pk>/edit/', views.session_update, name='my_session_update'),
    path('sessions/<int:pk>/delete/', views.session_delete, name='my_session_delete'),
    ######################################################################################################################
    path('counseller_session_document_list/',views.counseller_session_document_list,name='counseller_session_document_list'),
    path('counseller_session_document_add/',views.counseller_session_document_add,name='counseller_session_document_add'),
    path('counseller_session_document_edit/<int:pk>/edit/',views.counseller_session_document_edit,name='counseller_session_document_edit'),
    #####################################################################################################
    path('counseller_student_list/',views.counseller_student_list,name='counseller_student_list'),
    ###############################################################################################################
    path('counseller_review_list/',views.counseller_review_list,name='counseller_review_list'),
    ###############################################################################################################
    path('counseller_user_list/',views.counseller_user_list,name='counseller_user_list'),
]
