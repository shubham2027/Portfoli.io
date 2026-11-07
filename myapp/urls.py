from django.urls import path
from . import views

urlpatterns = [
    # Landing & Authentication
    path('', views.landing_page, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard & Profile Management
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/template/', views.portfolio_template_select_view, name='portfolio_template_select'),
    path('portfolio/preview/', views.portfolio_preview_view, name='portfolio_preview'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),

    # Portfolio Sharing & File Format Exports
    path('export/html/', views.portfolio_export_html_view, name='portfolio_export_html'),
    path('export/json/', views.portfolio_export_json_view, name='portfolio_export_json'),
    path('export/markdown/', views.portfolio_export_markdown_view, name='portfolio_export_markdown'),
    path('export/print/', views.portfolio_print_view, name='portfolio_print'),

    # Reserved for future public publishing implementation
    path('dashboard/publish/', views.portfolio_publish_toggle_view, name='portfolio_publish_toggle'),
    path('u/<slug:slug>/', views.public_portfolio_view, name='public_portfolio'),

    # Education Management
    path('education/', views.education_list_view, name='education_list'),
    path('education/add/', views.education_create_view, name='education_create'),
    path('education/<int:pk>/edit/', views.education_edit_view, name='education_edit'),
    path('education/<int:pk>/delete/', views.education_delete_view, name='education_delete'),

    # Skills Management
    path('skills/', views.skill_list_view, name='skill_list'),
    path('skills/<int:pk>/delete/', views.skill_delete_view, name='skill_delete'),

    # Project Management
    path('projects/', views.project_list_view, name='project_list'),
    path('projects/add/', views.project_create_view, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit_view, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete_view, name='project_delete'),
]
