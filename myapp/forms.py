from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Profile, Education, Skill, Project

class UserRegistrationForm(UserCreationForm):
    """
    User registration form with email validation and Bootstrap 5 styling.
    """
    email = forms.EmailField(
        required=True,
        help_text="A valid email address is required for your account and portfolio contact info.",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com',
            'autocomplete': 'email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. This will be your portfolio URL slug (e.g. /u/username/).',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styling to all fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a unique username',
            'autocomplete': 'username'
        })
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Create a secure password',
                'autocomplete': 'new-password'
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Confirm your password',
                'autocomplete': 'new-password'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email


class UserLoginForm(AuthenticationForm):
    """
    User login form with Bootstrap 5 input styling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autocomplete': 'username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })


class ProfileForm(forms.ModelForm):
    """
    Profile management form for updating personal and professional details.
    """
    class Meta:
        model = Profile
        fields = [
            'full_name',
            'title',
            'profile_picture',
            'email',
            'phone',
            'location',
            'bio',
            'github_url',
            'linkedin_url',
            'website_url',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Alex Morgan'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Full-Stack Developer & UI/UX Specialist'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. alex.morgan@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. +1 (555) 234-5678'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. San Francisco, CA or Remote'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a brief professional overview about yourself, your areas of expertise, and what drives you...'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/yourusername'
            }),
            'website_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com or blog'
            }),
        }


class EducationForm(forms.ModelForm):
    """
    Form for adding and modifying educational records.
    """
    class Meta:
        model = Education
        fields = [
            'institution',
            'degree',
            'field_of_study',
            'start_year',
            'end_year',
            'description',
        ]
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Stanford University or MIT'
            }),
            'degree': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Bachelor of Science, Master of Science'
            }),
            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Computer Science, Software Engineering'
            }),
            'start_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2020',
                'min': 1950,
                'max': 2035
            }),
            'end_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2024 (leave blank if currently enrolled)',
                'min': 1950,
                'max': 2035
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notable coursework, honors, GPA, research projects, or extracurricular achievements...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_year = cleaned_data.get('start_year')
        end_year = cleaned_data.get('end_year')
        if start_year and end_year and end_year < start_year:
            self.add_error('end_year', "End year cannot be earlier than start year.")
        return cleaned_data


class SkillForm(forms.ModelForm):
    """
    Form for creating and managing skills.
    """
    class Meta:
        model = Skill
        fields = ['name', 'category', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python, Docker, Figma, React'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'proficiency': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class ProjectForm(forms.ModelForm):
    """
    Form for adding and editing featured projects.
    """
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'technologies',
            'github_url',
            'live_url',
            'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Distributed Task Orchestrator'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide a comprehensive overview of the problem solved, your technical approach, architecture, and key outcomes...'
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comma-separated, e.g. Python, Django, PostgreSQL, Docker'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername/project'
            }),
            'live_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://project-demo.example.com'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
