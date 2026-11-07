from django.contrib import admin
from .models import Profile, Education, Skill, Project, Portfolio

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'title', 'location', 'email', 'updated_at')
    search_fields = ('user__username', 'full_name', 'title', 'email', 'location')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'institution', 'start_year', 'end_year')
    list_filter = ('start_year', 'end_year')
    search_fields = ('user__username', 'institution', 'degree', 'field_of_study')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'category', 'proficiency', 'created_at')
    list_filter = ('category', 'proficiency')
    search_fields = ('user__username', 'name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'technologies', 'created_at')
    search_fields = ('user__username', 'title', 'technologies', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'template', 'is_published', 'updated_at')
    list_filter = ('template', 'is_published')
    search_fields = ('user__username', 'slug')
    readonly_fields = ('created_at', 'updated_at')
