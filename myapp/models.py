from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

class Profile(models.Model):
    """
    User professional profile and personal biography.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True, verbose_name="Full Name")
    title = models.CharField(max_length=150, blank=True, verbose_name="Professional Title", help_text="e.g. Full-Stack Developer, UI/UX Designer, Data Analyst")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="Profile Picture")
    email = models.EmailField(blank=True, verbose_name="Public Email", help_text="Contact email displayed on your public portfolio")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Phone Number")
    location = models.CharField(max_length=150, blank=True, verbose_name="Location", help_text="e.g. San Francisco, CA or Remote")
    bio = models.TextField(blank=True, verbose_name="About Me / Biography", help_text="A short summary about your background, expertise, and passions")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL", help_text="https://github.com/yourusername")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL", help_text="https://linkedin.com/in/yourusername")
    website_url = models.URLField(blank=True, verbose_name="Personal Website / Portfolio Link", help_text="https://yourwebsite.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name or self.user.username}'s Profile"

    def get_completion_percentage(self):
        """
        Calculates profile completeness percentage based on essential fields.
        """
        fields = [self.full_name, self.title, self.bio, self.location, self.email, self.profile_picture, self.github_url or self.linkedin_url]
        filled_count = sum(1 for field in fields if bool(field))
        return int((filled_count / len(fields)) * 100)


class Education(models.Model):
    """
    User educational qualifications and academic background.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=200, verbose_name="Institution", help_text="e.g. Stanford University, MIT, State College")
    degree = models.CharField(max_length=150, verbose_name="Degree", help_text="e.g. Bachelor of Science, Master of Arts, High School Diploma")
    field_of_study = models.CharField(max_length=150, blank=True, verbose_name="Field of Study", help_text="e.g. Computer Science, Graphic Design")
    start_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Start Year")
    end_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="End Year", help_text="Leave empty if currently enrolled")
    description = models.TextField(blank=True, verbose_name="Description", help_text="Key achievements, honors, or extracurricular activities")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-end_year', '-start_year']

    def __str__(self):
        return f"{self.degree} at {self.institution} ({self.user.username})"


class Skill(models.Model):
    """
    User technical and professional skills.
    """
    CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Design', 'Design'),
        ('Tools & Others', 'Tools & Others'),
        ('Soft Skills', 'Soft Skills'),
    ]

    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100, verbose_name="Skill Name", help_text="e.g. Python, Figma, React, Docker")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Technical')
    proficiency = models.CharField(max_length=50, choices=PROFICIENCY_CHOICES, default='Intermediate')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.proficiency}) - {self.user.username}"


class Project(models.Model):
    """
    User showcase projects and portfolio items.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200, verbose_name="Project Title")
    description = models.TextField(verbose_name="Description", help_text="Detailed overview of what the project does and your role")
    technologies = models.CharField(max_length=250, verbose_name="Technologies Used", help_text="Comma-separated: e.g. Django, SQLite, Bootstrap 5")
    github_url = models.URLField(blank=True, verbose_name="GitHub Repository URL")
    live_url = models.URLField(blank=True, verbose_name="Live Demo URL")
    image = models.ImageField(upload_to='project_images/', blank=True, null=True, verbose_name="Project Screenshot")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    def tech_list(self):
        """Returns technologies as a cleaned list of tags."""
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


class Portfolio(models.Model):
    """
    Portfolio settings, public slug, active template, and publish status.
    """
    TEMPLATE_CHOICES = [
        ('minimal', 'Minimal Professional'),
        ('modern', 'Modern Developer'),
        ('creative', 'Creative Showcase'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Portfolio Slug", help_text="Unique URL identifier (portfoli.io/u/<slug>/)")
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='minimal', verbose_name="Selected Template")
    is_published = models.BooleanField(default=False, verbose_name="Is Published", help_text="When published, your portfolio is viewable publicly")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio for {self.user.username} (/u/{self.slug}/)"


@receiver(post_save, sender=User)
def create_or_sync_user_profile_and_portfolio(sender, instance, created, **kwargs):
    """
    Signal receiver to automatically create Profile and Portfolio for new Users.
    """
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={
                'email': instance.email,
                'full_name': instance.get_full_name() or instance.username
            }
        )
        base_slug = slugify(instance.username) or f"user-{instance.pk}"
        slug = base_slug
        counter = 1
        while Portfolio.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Portfolio.objects.get_or_create(
            user=instance,
            defaults={
                'slug': slug,
                'template': 'minimal',
                'is_published': False
            }
        )
