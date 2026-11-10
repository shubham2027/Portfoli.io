from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import slugify
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    ProfileForm,
    EducationForm,
    SkillForm,
    ProjectForm
)
from .models import Profile, Portfolio, Education, Skill, Project

def landing_page(request):
    """
    Renders the public landing page for portfoli.io.
    Passes preview data for the three flagship portfolio templates.
    """
    templates_preview = [
        {
            'id': 'minimal',
            'name': 'Minimal Professional',
            'badge': 'Clean & Crisp',
            'description': 'Monochrome typography and executive clarity. Perfect for consultants, researchers, students, and managers seeking clean elegance.',
            'features': ['Distraction-free typography', 'Linear chronological timeline', 'Print-friendly design'],
            'accent_color': '#334155',
            'sample_name': 'Alex Morgan',
            'sample_title': 'Product & Research Lead',
            'preview_type': 'minimal',
        },
        {
            'id': 'modern',
            'name': 'Modern Developer',
            'badge': 'Developer Favorite',
            'description': 'Designed for software engineers and technical builders. Highlights programming stacks, GitHub repos, and interactive project cards.',
            'features': ['Tech stack badge tags', 'Live demo & repo links', 'Dark accent styling'],
            'accent_color': '#4f46e5',
            'sample_name': 'David Chen',
            'sample_title': 'Full-Stack Software Engineer',
            'preview_type': 'developer',
        },
        {
            'id': 'creative',
            'name': 'Creative Showcase',
            'badge': 'Visual & Dynamic',
            'description': 'Crafted for designers, creatives, and digital creators. Features visual gallery cards, rich bio layouts, and vibrant aesthetic touches.',
            'features': ['Visual card showcase', 'Fluid responsive grid', 'Engaging creative highlights'],
            'accent_color': '#0ea5e9',
            'sample_name': 'Sophia Martinez',
            'sample_title': 'UI/UX & Product Designer',
            'preview_type': 'creative',
        },
    ]

    features = [
        {
            'icon': 'bi-lightning-charge-fill',
            'title': 'Instant Setup',
            'description': 'Fill in your education, skills, and projects in an intuitive dashboard. No coding or design skills needed.',
        },
        {
            'icon': 'bi-palette-fill',
            'title': 'Curated Templates',
            'description': 'Choose between Minimal, Developer, and Creative styles. Switch templates anytime with a single click.',
        },
        {
            'icon': 'bi-filetype-html',
            'title': 'Standalone HTML Export',
            'description': 'Download a self-contained HTML portfolio that works offline or can be uploaded to any web server.',
        },
        {
            'icon': 'bi-printer-fill',
            'title': 'Print & PDF Ready',
            'description': 'Generate clean, printable resume layouts ready to save as PDF directly from your browser.',
        },
        {
            'icon': 'bi-markdown-fill',
            'title': 'Markdown & JSON Formats',
            'description': 'Export your portfolio data in raw JSON or formatted Markdown to include in GitHub profiles and applications.',
        },
        {
            'icon': 'bi-shield-lock-fill',
            'title': 'Secure & Private',
            'description': 'Your personal data stays completely private on your account until you choose to download or export it.',
        },
    ]

    steps = [
        {
            'number': '01',
            'step': '01',
            'title': 'Create Your Profile',
            'description': 'Register an account and input your bio, education records, technical skills, and featured projects.',
        },
        {
            'number': '02',
            'step': '02',
            'title': 'Pick a Template Style',
            'description': 'Select from Minimal, Modern Developer, or Creative showcase layouts tailored to your career goals.',
        },
        {
            'number': '03',
            'step': '03',
            'title': 'Export & Share Anywhere',
            'description': 'Download as a standalone HTML website, print to PDF, or export as clean Markdown and JSON files.',
        },
    ]

    return render(request, 'landing.html', {
        'templates_preview': templates_preview,
        'features': features,
        'steps': steps,
    })


def register_view(request):
    """
    Handles user registration.
    Redirects authenticated users to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log user in immediately upon successful registration
            login(request, user)
            messages.success(request, f"Welcome to portfoli.io, {user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below to create your account.")
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """
    Handles user login using session-based authentication.
    Redirects authenticated users to dashboard or requested next URL.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        next_url = request.POST.get('next', '')
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            # Safe redirect validation
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm(request)

    return render(request, 'auth/login.html', {
        'form': form,
        'next': next_url
    })


def logout_view(request):
    """
    Logs out the current user and clears the session.
    Accepts both POST (recommended) and GET requests.
    """
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f"You have been successfully logged out, {username}.")
    return redirect('landing')


@login_required(login_url='login')
def dashboard_view(request):
    """
    User dashboard home.
    Displays user profile status, detailed portfolio completion checklist,
    template selection, publish/unpublish toggle, and module overviews.
    """
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'email': request.user.email,
            'full_name': request.user.get_full_name() or request.user.username
        }
    )

    base_slug = slugify(request.user.username) or f"user-{request.user.pk}"
    portfolio, _ = Portfolio.objects.get_or_create(
        user=request.user,
        defaults={
            'slug': base_slug,
            'template': 'minimal',
            'is_published': False
        }
    )

    educations = request.user.educations.all()
    skills = request.user.skills.all()
    projects = request.user.projects.all()

    educations_count = educations.count()
    skills_count = skills.count()
    projects_count = projects.count()

    # Detailed portfolio readiness checklist
    checklist = {
        'profile_info': bool(profile.full_name and profile.title and profile.location),
        'bio': bool(profile.bio and len(profile.bio.strip()) > 10),
        'photo': bool(profile.profile_picture),
        'education': educations_count >= 1,
        'skills': skills_count >= 3,
        'projects': projects_count >= 1,
    }
    completed_items = sum(1 for v in checklist.values() if v)
    total_items = len(checklist)
    completion_percentage = int((completed_items / total_items) * 100)

    templates_catalog = [
        {
            'id': 'minimal',
            'name': 'Minimal Professional',
            'badge': 'Clean & Crisp',
            'desc': 'Typography-first, structured chronological layout suited for consultants and academics.',
            'accent': '#334155',
            'icon': 'bi-file-earmark-text',
        },
        {
            'id': 'modern',
            'name': 'Modern Developer',
            'badge': 'Developer Favorite',
            'desc': 'Tech-focused dark mode accents, code badges, live repository cards, and demo links.',
            'accent': '#4f46e5',
            'icon': 'bi-code-slash',
        },
        {
            'id': 'creative',
            'name': 'Creative Showcase',
            'badge': 'Visual & Dynamic',
            'desc': 'Vibrant visual cards, project gallery focus, and creative layout for designers and builders.',
            'accent': '#0ea5e9',
            'icon': 'bi-palette',
        },
    ]

    return render(request, 'dashboard.html', {
        'user': request.user,
        'profile': profile,
        'portfolio': portfolio,
        'educations_count': educations_count,
        'skills_count': skills_count,
        'projects_count': projects_count,
        'checklist': checklist,
        'completed_items': completed_items,
        'total_items': total_items,
        'completion_percentage': completion_percentage,
        'templates_catalog': templates_catalog,
        'recent_projects': projects[:3],
        'recent_education': educations[:2],
        'recent_skills': skills[:8],
    })


@login_required(login_url='login')
def portfolio_template_select_view(request):
    """
    Updates the user's active portfolio design template.
    """
    portfolio, _ = Portfolio.objects.get_or_create(
        user=request.user,
        defaults={'slug': slugify(request.user.username) or f"user-{request.user.pk}"}
    )

    if request.method == 'POST':
        selected_template = request.POST.get('template')
        valid_templates = [t[0] for t in Portfolio.TEMPLATE_CHOICES]
        if selected_template in valid_templates:
            portfolio.template = selected_template
            portfolio.save()
            messages.success(request, f"Active template switched to {portfolio.get_template_display()}!")
        else:
            messages.error(request, "Invalid template selection.")

    return redirect('dashboard')


@login_required(login_url='login')
def portfolio_publish_toggle_view(request):
    """
    Toggles public visibility of the user's portfolio.
    """
    portfolio, _ = Portfolio.objects.get_or_create(
        user=request.user,
        defaults={'slug': slugify(request.user.username) or f"user-{request.user.pk}"}
    )

    if request.method == 'POST':
        portfolio.is_published = not portfolio.is_published
        portfolio.save()

        if portfolio.is_published:
            messages.success(
                request,
                f"🎉 Your portfolio is now LIVE and viewable publicly at /u/{portfolio.slug}/!"
            )
        else:
            messages.info(
                request,
                "Your portfolio has been set to Draft mode and is now hidden from public visitors."
            )

    return redirect('dashboard')


@login_required(login_url='login')
def portfolio_preview_view(request):
    """
    Preview mode for the portfolio generator.
    Allows logged-in users to preview their portfolio under the active template
    with an interactive switcher bar.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    portfolio, _ = Portfolio.objects.get_or_create(
        user=request.user,
        defaults={'slug': slugify(request.user.username) or f"user-{request.user.pk}"}
    )

    # Allow on-the-fly preview template override via query param ?template=modern
    active_template = request.GET.get('template', portfolio.template)
    if active_template not in ['minimal', 'modern', 'creative']:
        active_template = portfolio.template

    educations = request.user.educations.all()
    skills = request.user.skills.all()
    projects = request.user.projects.all()

    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        skills_by_category.setdefault(skill.category, []).append(skill)

    context = {
        'portfolio_user': request.user,
        'profile': profile,
        'portfolio': portfolio,
        'educations': educations,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'projects': projects,
        'active_template': active_template,
        'is_preview': True,
    }

    # Render template according to selection
    template_file = f"portfolio/templates/{active_template}.html"
    return render(request, template_file, context)


@login_required(login_url='login')
def portfolio_export_html_view(request):
    """
    Exports and downloads the user's portfolio as a standalone HTML document.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
    educations = request.user.educations.all()
    skills = request.user.skills.all()
    projects = request.user.projects.all()

    skills_by_category = {}
    for skill in skills:
        skills_by_category.setdefault(skill.category, []).append(skill)

    context = {
        'portfolio_user': request.user,
        'profile': profile,
        'portfolio': portfolio,
        'educations': educations,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'projects': projects,
        'active_template': portfolio.template,
        'is_preview': False,
        'is_standalone': True,
    }

    template_file = f"portfolio/templates/{portfolio.template}.html"
    html_content = render_to_string(template_file, context, request=request)

    response = HttpResponse(html_content, content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_portfolio.html"'
    return response


@login_required(login_url='login')
def portfolio_export_json_view(request):
    """
    Exports the complete portfolio data as a structured JSON file.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)

    data = {
        'username': request.user.username,
        'export_date': timezone.now().isoformat(),
        'active_template': portfolio.template,
        'profile': {
            'full_name': profile.full_name or request.user.get_full_name(),
            'title': profile.title,
            'email': profile.email or request.user.email,
            'phone': profile.phone,
            'location': profile.location,
            'bio': profile.bio,
            'github_url': profile.github_url,
            'linkedin_url': profile.linkedin_url,
            'website_url': profile.website_url,
        },
        'educations': [
            {
                'institution': e.institution,
                'degree': e.degree,
                'field_of_study': e.field_of_study,
                'start_year': e.start_year,
                'end_year': e.end_year,
                'description': e.description,
            }
            for e in request.user.educations.all()
        ],
        'skills': [
            {
                'name': s.name,
                'category': s.category,
                'proficiency': s.proficiency,
            }
            for s in request.user.skills.all()
        ],
        'projects': [
            {
                'title': p.title,
                'description': p.description,
                'technologies': p.tech_list(),
                'github_url': p.github_url,
                'live_url': p.live_url,
            }
            for p in request.user.projects.all()
        ],
    }

    response = JsonResponse(data, json_dumps_params={'indent': 2})
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_portfolio.json"'
    return response


@login_required(login_url='login')
def portfolio_export_markdown_view(request):
    """
    Exports the portfolio content as a formatted Markdown resume document (.md).
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)

    lines = []
    name = profile.full_name or request.user.username
    lines.append(f"# {name}")
    if profile.title:
        lines.append(f"### {profile.title}")
    lines.append("")

    contact_parts = []
    if profile.email:
        contact_parts.append(f"Email: {profile.email}")
    if profile.phone:
        contact_parts.append(f"Phone: {profile.phone}")
    if profile.location:
        contact_parts.append(f"Location: {profile.location}")
    if contact_parts:
        lines.append(" • ".join(contact_parts))
        lines.append("")

    links = []
    if profile.github_url:
        links.append(f"[GitHub]({profile.github_url})")
    if profile.linkedin_url:
        links.append(f"[LinkedIn]({profile.linkedin_url})")
    if profile.website_url:
        links.append(f"[Portfolio/Website]({profile.website_url})")
    if links:
        lines.append(" • ".join(links))
        lines.append("")

    if profile.bio:
        lines.append("## About Me")
        lines.append(profile.bio)
        lines.append("")

    edus = request.user.educations.all()
    if edus.exists():
        lines.append("## Education")
        for e in edus:
            period = f"{e.start_year or ''} – {e.end_year or 'Present'}"
            study = f" in {e.field_of_study}" if e.field_of_study else ""
            lines.append(f"- **{e.degree}{study}**, *{e.institution}* ({period})")
            if e.description:
                lines.append(f"  {e.description}")
        lines.append("")

    skills = request.user.skills.all()
    if skills.exists():
        lines.append("## Skills")
        for s in skills:
            lines.append(f"- **{s.name}** ({s.category}) — *{s.proficiency}*")
        lines.append("")

    projs = request.user.projects.all()
    if projs.exists():
        lines.append("## Featured Projects")
        for p in projs:
            lines.append(f"### {p.title}")
            if p.technologies:
                lines.append(f"*Technologies: {p.technologies}*")
            lines.append(p.description)
            plinks = []
            if p.github_url:
                plinks.append(f"[GitHub Repository]({p.github_url})")
            if p.live_url:
                plinks.append(f"[Live Demo]({p.live_url})")
            if plinks:
                lines.append(" • ".join(plinks))
            lines.append("")

    content = "\n".join(lines)
    response = HttpResponse(content, content_type='text/markdown; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_resume.md"'
    return response


@login_required(login_url='login')
def portfolio_print_view(request):
    """
    Renders a clean printable view of the portfolio formatted for printing or saving to PDF.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
    educations = request.user.educations.all()
    skills = request.user.skills.all()
    projects = request.user.projects.all()

    skills_by_category = {}
    for skill in skills:
        skills_by_category.setdefault(skill.category, []).append(skill)

    return render(request, 'portfolio/print.html', {
        'portfolio_user': request.user,
        'profile': profile,
        'portfolio': portfolio,
        'educations': educations,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'projects': projects,
    })


def public_portfolio_view(request, slug):
    """
    Publicly accessible portfolio view at /u/<slug>/.
    Accessible without authentication when portfolio is published.
    If unpublished, only the authenticated owner can preview it.
    """
    portfolio = get_object_or_404(Portfolio, slug=slug)

    # Check publication status & permissions
    is_owner = request.user.is_authenticated and request.user == portfolio.user
    if not portfolio.is_published and not is_owner:
        return render(request, 'portfolio/not_published.html', {
            'portfolio': portfolio,
            'slug': slug
        }, status=403)

    profile = getattr(portfolio.user, 'profile', None)
    educations = portfolio.user.educations.all()
    skills = portfolio.user.skills.all()
    projects = portfolio.user.projects.all()

    skills_by_category = {}
    for skill in skills:
        skills_by_category.setdefault(skill.category, []).append(skill)

    context = {
        'portfolio_user': portfolio.user,
        'profile': profile,
        'portfolio': portfolio,
        'educations': educations,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'projects': projects,
        'active_template': portfolio.template,
        'is_preview': False,
        'is_owner_draft': (not portfolio.is_published and is_owner),
    }

    template_file = f"portfolio/templates/{portfolio.template}.html"
    return render(request, template_file, context)


@login_required(login_url='login')
def profile_edit_view(request):
    """
    Handles viewing and editing the user's personal and professional profile details.
    """
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'email': request.user.email,
            'full_name': request.user.get_full_name() or request.user.username
        }
    )

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been successfully updated!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please review and fix the errors highlighted below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile/edit.html', {
        'form': form,
        'profile': profile
    })


# ==========================================================================
# Education Management (CRUD)
# ==========================================================================

@login_required(login_url='login')
def education_list_view(request):
    """
    Displays the user's educational history.
    """
    educations = request.user.educations.all()
    return render(request, 'education/list.html', {
        'educations': educations
    })


@login_required(login_url='login')
def education_create_view(request):
    """
    Creates a new education record for the authenticated user.
    """
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            messages.success(request, f"Education at '{education.institution}' was added.")
            return redirect('education_list')
        else:
            messages.error(request, "Please correct the errors in the education form.")
    else:
        form = EducationForm()

    return render(request, 'education/form.html', {
        'form': form,
        'action_title': 'Add Education Record',
        'is_edit': False
    })


@login_required(login_url='login')
def education_edit_view(request, pk):
    """
    Edits an existing education record belonging to the authenticated user.
    """
    education = get_object_or_404(Education, pk=pk, user=request.user)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, f"Education at '{education.institution}' was updated.")
            return redirect('education_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EducationForm(instance=education)

    return render(request, 'education/form.html', {
        'form': form,
        'education': education,
        'action_title': f"Edit Education — {education.institution}",
        'is_edit': True
    })


@login_required(login_url='login')
def education_delete_view(request, pk):
    """
    Deletes an education record belonging to the authenticated user.
    """
    education = get_object_or_404(Education, pk=pk, user=request.user)
    if request.method == 'POST':
        institution = education.institution
        education.delete()
        messages.info(request, f"Education record at '{institution}' was removed.")
        return redirect('education_list')

    return render(request, 'education/delete_confirm.html', {
        'education': education
    })


# ==========================================================================
# Skills Management (CRUD)
# ==========================================================================

@login_required(login_url='login')
def skill_list_view(request):
    """
    Displays the user's skills and provides a quick-add form.
    """
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, f"Skill '{skill.name}' was added.")
            return redirect('skill_list')
        else:
            messages.error(request, "Please correct the skill form errors.")
    else:
        form = SkillForm()

    skills = request.user.skills.all()
    # Group skills by category for neat display
    categories = {}
    for skill in skills:
        categories.setdefault(skill.category, []).append(skill)

    return render(request, 'skills/list.html', {
        'skills': skills,
        'categories': categories,
        'form': form
    })


@login_required(login_url='login')
def skill_delete_view(request, pk):
    """
    Deletes a skill record belonging to the authenticated user.
    """
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        name = skill.name
        skill.delete()
        messages.info(request, f"Skill '{name}' has been removed.")
    return redirect('skill_list')


# ==========================================================================
# Project Management (CRUD)
# ==========================================================================

@login_required(login_url='login')
def project_list_view(request):
    """
    Displays all showcase projects belonging to the authenticated user.
    """
    projects = request.user.projects.all()
    return render(request, 'projects/list.html', {
        'projects': projects
    })


@login_required(login_url='login')
def project_create_view(request):
    """
    Creates a new showcase project for the authenticated user.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, f"Project '{project.title}' was added successfully.")
            return redirect('project_list')
        else:
            messages.error(request, "Please correct the errors in the project form.")
    else:
        form = ProjectForm()

    return render(request, 'projects/form.html', {
        'form': form,
        'action_title': 'Add Showcase Project',
        'is_edit': False
    })


@login_required(login_url='login')
def project_edit_view(request, pk):
    """
    Edits an existing project belonging to the authenticated user.
    """
    project = get_object_or_404(Project, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f"Project '{project.title}' was updated.")
            return redirect('project_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/form.html', {
        'form': form,
        'project': project,
        'action_title': f"Edit Project — {project.title}",
        'is_edit': True
    })


@login_required(login_url='login')
def project_delete_view(request, pk):
    """
    Deletes a project record belonging to the authenticated user.
    """
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.info(request, f"Project '{title}' has been removed.")
        return redirect('project_list')

    return render(request, 'projects/delete_confirm.html', {
        'project': project
    })
