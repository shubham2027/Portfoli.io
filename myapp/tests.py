from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Profile, Education, Skill, Project, Portfolio

class LandingPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_status_code(self):
        """Landing page should load with HTTP 200 OK."""
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_template_used(self):
        """Landing page should render using base.html and landing.html."""
        response = self.client.get(reverse('landing'))
        self.assertTemplateUsed(response, 'landing.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_landing_page_context_data(self):
        """Context should include templates_preview, features, and steps."""
        response = self.client.get(reverse('landing'))
        self.assertIn('templates_preview', response.context)
        self.assertIn('features', response.context)
        self.assertIn('steps', response.context)
        self.assertEqual(len(response.context['templates_preview']), 3)

    def test_landing_page_content_sections(self):
        """Core sections should be present in rendered HTML."""
        response = self.client.get(reverse('landing'))
        content = response.content.decode('utf-8')
        
        # Check brand and hero
        self.assertIn('portfoli', content)
        self.assertIn('Create Your Professional Portfolio', content)
        
        # Check navigation anchors
        self.assertIn('#features', content)
        self.assertIn('#templates', content)
        self.assertIn('#how-it-works', content)
        
        # Check template names
        self.assertIn('Minimal Professional', content)
        self.assertIn('Modern Developer', content)
        self.assertIn('Creative Showcase', content)

    def test_landing_page_authenticated_user(self):
        """Logged-in users can view landing page and interact with features, templates, and steps."""
        user = User.objects.create_user(username='tester', password='Password123!')
        self.client.login(username='tester', password='Password123!')
        
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Features, templates, and how it works sections should remain present
        self.assertIn('id="features"', content)
        self.assertIn('id="templates"', content)
        self.assertIn('id="how-it-works"', content)

        # Step numbers should display
        self.assertIn('01', content)
        self.assertIn('02', content)
        self.assertIn('03', content)

        # Authenticated CTAs should display
        self.assertIn('Dashboard', content)
        self.assertIn('Live Preview with My Data', content)
        self.assertIn(reverse('portfolio_template_select'), content)


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'johndoe'
        self.email = 'johndoe@example.com'
        self.password = 'ComplexPassword123!'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_register_get_view(self):
        """Register page should return 200 and use auth/register.html."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        self.assertContains(response, 'Create Your Account')

    def test_register_success(self):
        """Valid registration creates a user, logs them in, and redirects to dashboard."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass987!',
            'password2': 'StrongPass987!',
        }, follow=True)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.context['user'].username, 'newuser')

    def test_register_duplicate_username(self):
        """Registration with an already existing username should fail with validation error."""
        response = self.client.post(reverse('register'), {
            'username': self.username,
            'email': 'different@example.com',
            'password1': 'StrongPass987!',
            'password2': 'StrongPass987!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='different@example.com').exists())
        self.assertTrue(response.context['form'].errors)

    def test_register_duplicate_email(self):
        """Registration with an already existing email should fail with validation error."""
        response = self.client.post(reverse('register'), {
            'username': 'uniqueuser',
            'email': self.email,
            'password1': 'StrongPass987!',
            'password2': 'StrongPass987!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='uniqueuser').exists())
        self.assertIn('email', response.context['form'].errors)

    def test_login_get_view(self):
        """Login page should return 200 and use auth/login.html."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(response, 'Welcome Back')

    def test_login_success(self):
        """Valid credentials should authenticate user and redirect to dashboard."""
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        }, follow=True)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_invalid_credentials(self):
        """Invalid credentials should show error message and not authenticate."""
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'WrongPassword123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_logout(self):
        """Logout should clear user session and redirect to landing page."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('landing'))
        self.assertFalse(response.context['user'].is_authenticated)

    def test_dashboard_unauthenticated_redirect(self):
        """Unauthenticated user accessing dashboard should be redirected to login."""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_authenticated_access(self):
        """Authenticated user should be able to view their dashboard."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, 'Welcome,')

    def test_authenticated_user_redirected_from_login_and_register(self):
        """Logged-in users visiting login or register should be redirected to dashboard."""
        self.client.login(username=self.username, password=self.password)
        
        login_res = self.client.get(reverse('login'))
        self.assertRedirects(login_res, reverse('dashboard'))
        
        reg_res = self.client.get(reverse('register'))
        self.assertRedirects(reg_res, reverse('dashboard'))


class Phase3ModelAndProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'alice'
        self.password = 'SecurePassword123!'
        self.user = User.objects.create_user(
            username=self.username,
            email='alice@example.com',
            password=self.password
        )

    def test_profile_and_portfolio_signal_creation(self):
        """Profile and Portfolio should automatically be created when a User is created."""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        self.assertTrue(Portfolio.objects.filter(user=self.user).exists())
        portfolio = self.user.portfolio
        self.assertEqual(portfolio.slug, 'alice')
        self.assertEqual(portfolio.template, 'minimal')
        self.assertFalse(portfolio.is_published)

    def test_education_model(self):
        """Education model creates and formats string representation correctly."""
        edu = Education.objects.create(
            user=self.user,
            institution='Stanford University',
            degree='B.S.',
            field_of_study='Computer Science',
            start_year=2020,
            end_year=2024,
            description='Graduated with Honors.'
        )
        self.assertIn('Stanford University', str(edu))
        self.assertEqual(self.user.educations.count(), 1)

    def test_skill_model(self):
        """Skill model creates with category and proficiency."""
        skill = Skill.objects.create(
            user=self.user,
            name='Django',
            category='Backend',
            proficiency='Advanced'
        )
        self.assertIn('Django', str(skill))
        self.assertEqual(self.user.skills.count(), 1)

    def test_project_model(self):
        """Project model correctly stores fields and parses tech tags."""
        proj = Project.objects.create(
            user=self.user,
            title='E-Commerce Platform',
            description='A modern full-featured shop.',
            technologies='Django, Python, SQLite, Bootstrap 5',
            github_url='https://github.com/alice/shop',
            live_url='https://shop.example.com'
        )
        self.assertEqual(len(proj.tech_list()), 4)
        self.assertIn('Django', proj.tech_list())
        self.assertIn('E-Commerce Platform', str(proj))

    def test_profile_edit_unauthenticated(self):
        """Unauthenticated access to edit profile redirects to login."""
        response = self.client.get(reverse('profile_edit'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile_edit')}")

    def test_profile_edit_get(self):
        """Authenticated user can load edit profile form."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/edit.html')
        self.assertContains(response, 'Personal & Role Information')

    def test_profile_edit_post_success(self):
        """Authenticated user can update profile details."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('profile_edit'), {
            'full_name': 'Alice Wonder',
            'title': 'Senior Python Developer',
            'email': 'alice.public@example.com',
            'phone': '+1 (555) 123-4567',
            'location': 'New York, NY',
            'bio': 'Passionate coder building intuitive web applications.',
            'github_url': 'https://github.com/alicewonder',
            'linkedin_url': 'https://linkedin.com/in/alicewonder',
            'website_url': 'https://alicewonder.dev',
        }, follow=True)

        self.assertRedirects(response, reverse('dashboard'))
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.full_name, 'Alice Wonder')
        self.assertEqual(self.user.profile.title, 'Senior Python Developer')
        self.assertEqual(self.user.profile.location, 'New York, NY')
        self.assertGreater(self.user.profile.get_completion_percentage(), 50)


class Phase4CrudTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='Password123!')
        self.user2 = User.objects.create_user(username='user2', password='Password123!')
        self.client.login(username='user1', password='Password123!')

    # --- Education CRUD & Isolation ---
    def test_education_create_success(self):
        """User can create an education record."""
        response = self.client.post(reverse('education_create'), {
            'institution': 'MIT',
            'degree': 'M.S.',
            'field_of_study': 'AI',
            'start_year': 2021,
            'end_year': 2023,
            'description': 'Thesis on LLMs',
        }, follow=True)
        self.assertRedirects(response, reverse('education_list'))
        self.assertEqual(self.user1.educations.count(), 1)
        self.assertEqual(self.user1.educations.first().institution, 'MIT')

    def test_education_year_validation(self):
        """End year before start year fails validation."""
        response = self.client.post(reverse('education_create'), {
            'institution': 'MIT',
            'degree': 'M.S.',
            'field_of_study': 'AI',
            'start_year': 2024,
            'end_year': 2020,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('end_year', response.context['form'].errors)

    def test_education_edit_success(self):
        """User can edit their own education record."""
        edu = Education.objects.create(user=self.user1, institution='Old Univ', degree='B.A.')
        response = self.client.post(reverse('education_edit', kwargs={'pk': edu.pk}), {
            'institution': 'Updated Univ',
            'degree': 'B.S.',
            'field_of_study': 'Physics',
            'start_year': 2018,
            'end_year': 2022,
        }, follow=True)
        self.assertRedirects(response, reverse('education_list'))
        edu.refresh_from_db()
        self.assertEqual(edu.institution, 'Updated Univ')

    def test_education_user_isolation(self):
        """User1 cannot edit or delete User2's education record."""
        edu2 = Education.objects.create(user=self.user2, institution='Private College', degree='B.A.')
        
        # User1 attempts to edit User2's record
        edit_res = self.client.get(reverse('education_edit', kwargs={'pk': edu2.pk}))
        self.assertEqual(edit_res.status_code, 404)

        # User1 attempts to delete User2's record
        del_res = self.client.post(reverse('education_delete', kwargs={'pk': edu2.pk}))
        self.assertEqual(del_res.status_code, 404)
        self.assertTrue(Education.objects.filter(pk=edu2.pk).exists())

    def test_education_delete(self):
        """User can delete their own education record."""
        edu = Education.objects.create(user=self.user1, institution='To Delete College', degree='B.A.')
        response = self.client.post(reverse('education_delete', kwargs={'pk': edu.pk}), follow=True)
        self.assertRedirects(response, reverse('education_list'))
        self.assertFalse(Education.objects.filter(pk=edu.pk).exists())

    # --- Skills CRUD & Isolation ---
    def test_skill_create_and_delete(self):
        """User can add and delete skills."""
        # Add skill
        response = self.client.post(reverse('skill_list'), {
            'name': 'PostgreSQL',
            'category': 'Backend',
            'proficiency': 'Expert',
        }, follow=True)
        self.assertRedirects(response, reverse('skill_list'))
        skill = self.user1.skills.first()
        self.assertEqual(skill.name, 'PostgreSQL')

        # Delete skill
        del_res = self.client.post(reverse('skill_delete', kwargs={'pk': skill.pk}), follow=True)
        self.assertRedirects(del_res, reverse('skill_list'))
        self.assertEqual(self.user1.skills.count(), 0)

    def test_skill_user_isolation(self):
        """User1 cannot delete User2's skill."""
        skill2 = Skill.objects.create(user=self.user2, name='Kubernetes')
        del_res = self.client.post(reverse('skill_delete', kwargs={'pk': skill2.pk}))
        self.assertEqual(del_res.status_code, 404)
        self.assertTrue(Skill.objects.filter(pk=skill2.pk).exists())

    # --- Projects CRUD & Isolation ---
    def test_project_create_success(self):
        """User can create a showcase project."""
        response = self.client.post(reverse('project_create'), {
            'title': 'AI Code Reviewer',
            'description': 'Automated PR reviewer using LLMs.',
            'technologies': 'Python, Django, Celery',
            'github_url': 'https://github.com/user1/ai-reviewer',
            'live_url': 'https://ai-reviewer.com',
        }, follow=True)
        self.assertRedirects(response, reverse('project_list'))
        self.assertEqual(self.user1.projects.count(), 1)
        self.assertEqual(self.user1.projects.first().title, 'AI Code Reviewer')

    def test_project_edit_success(self):
        """User can update their project."""
        proj = Project.objects.create(user=self.user1, title='Old Title', description='Old desc', technologies='Python')
        response = self.client.post(reverse('project_edit', kwargs={'pk': proj.pk}), {
            'title': 'New Title',
            'description': 'Updated desc',
            'technologies': 'Python, Django',
            'github_url': '',
            'live_url': '',
        }, follow=True)
        self.assertRedirects(response, reverse('project_list'))
        proj.refresh_from_db()
        self.assertEqual(proj.title, 'New Title')

    def test_project_user_isolation(self):
        """User1 cannot edit or delete User2's project."""
        proj2 = Project.objects.create(user=self.user2, title='Secret Project', description='desc', technologies='C++')
        
        edit_res = self.client.get(reverse('project_edit', kwargs={'pk': proj2.pk}))
        self.assertEqual(edit_res.status_code, 404)

        del_res = self.client.post(reverse('project_delete', kwargs={'pk': proj2.pk}))
        self.assertEqual(del_res.status_code, 404)
        self.assertTrue(Project.objects.filter(pk=proj2.pk).exists())

    def test_project_delete(self):
        """User can delete their own project."""
        proj = Project.objects.create(user=self.user1, title='Demo Project', description='desc', technologies='HTML')
        response = self.client.post(reverse('project_delete', kwargs={'pk': proj.pk}), follow=True)
        self.assertRedirects(response, reverse('project_list'))
        self.assertFalse(Project.objects.filter(pk=proj.pk).exists())


class Phase5DashboardAndTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='Password123!')
        self.client.login(username='tester', password='Password123!')

    def test_dashboard_context_metrics(self):
        """Dashboard passes checklist, templates catalog, and completion percentage."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('checklist', response.context)
        self.assertIn('completion_percentage', response.context)
        self.assertIn('templates_catalog', response.context)
        self.assertIn('portfolio', response.context)

    def test_template_select_success(self):
        """User can switch portfolio template."""
        response = self.client.post(reverse('portfolio_template_select'), {
            'template': 'modern'
        }, follow=True)
        self.assertRedirects(response, reverse('dashboard'))
        self.user.portfolio.refresh_from_db()
        self.assertEqual(self.user.portfolio.template, 'modern')

    def test_template_select_invalid(self):
        """Invalid template name does not update the portfolio template."""
        response = self.client.post(reverse('portfolio_template_select'), {
            'template': 'nonexistent_style'
        }, follow=True)
        self.assertRedirects(response, reverse('dashboard'))
        self.user.portfolio.refresh_from_db()
        self.assertNotEqual(self.user.portfolio.template, 'nonexistent_style')

    def test_portfolio_publish_toggle(self):
        """User can toggle publishing status on and off."""
        # Initial is False
        self.assertFalse(self.user.portfolio.is_published)

        # Toggle to True
        response1 = self.client.post(reverse('portfolio_publish_toggle'), follow=True)
        self.assertRedirects(response1, reverse('dashboard'))
        self.user.portfolio.refresh_from_db()
        self.assertTrue(self.user.portfolio.is_published)

        # Toggle back to False
        response2 = self.client.post(reverse('portfolio_publish_toggle'), follow=True)
        self.assertRedirects(response2, reverse('dashboard'))
        self.user.portfolio.refresh_from_db()
        self.assertFalse(self.user.portfolio.is_published)

    def test_portfolio_preview_view(self):
        """Authenticated user can view portfolio preview."""
        response = self.client.get(reverse('portfolio_preview'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_preview'])

    def test_portfolio_preview_template_override(self):
        """User can preview with a specific template via query string."""
        response = self.client.get(f"{reverse('portfolio_preview')}?template=creative")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['active_template'], 'creative')


class Phase6And7PublishingAndTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sarah', password='Password123!')
        self.user.profile.full_name = 'Sarah Connor'
        self.user.profile.title = 'Cybersecurity Engineer'
        self.user.profile.location = 'Los Angeles, CA'
        self.user.profile.bio = 'Leading resilient systems infrastructure.'
        self.user.profile.save()

        # Add sample data
        Education.objects.create(user=self.user, institution='Caltech', degree='M.S.')
        Skill.objects.create(user=self.user, name='Network Defense', category='Technical', proficiency='Expert')
        Project.objects.create(user=self.user, title='Threat Sentinel', description='Intrusion detection system.', technologies='Python, Snort')

    def test_public_portfolio_published_access(self):
        """Anonymous visitor can view published portfolio."""
        self.user.portfolio.is_published = True
        self.user.portfolio.save()

        response = self.client.get(reverse('public_portfolio', kwargs={'slug': 'sarah'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sarah Connor')
        self.assertContains(response, 'Cybersecurity Engineer')
        self.assertContains(response, 'Threat Sentinel')
        self.assertContains(response, 'Network Defense')

    def test_public_portfolio_unpublished_anonymous_denied(self):
        """Anonymous visitor receives not_published page with status 403 when portfolio is unpublished."""
        self.user.portfolio.is_published = False
        self.user.portfolio.save()

        response = self.client.get(reverse('public_portfolio', kwargs={'slug': 'sarah'}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'portfolio/not_published.html')
        self.assertContains(response, 'Portfolio is in Draft Mode', status_code=403)

    def test_public_portfolio_unpublished_owner_allowed_draft_preview(self):
        """Owner logged in can view their unpublished portfolio with a draft notice."""
        self.user.portfolio.is_published = False
        self.user.portfolio.save()

        self.client.login(username='sarah', password='Password123!')
        response = self.client.get(reverse('public_portfolio', kwargs={'slug': 'sarah'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_owner_draft'])
        self.assertContains(response, 'Draft Mode:')

    def test_public_portfolio_nonexistent_slug(self):
        """Non-existent portfolio slug returns 404."""
        response = self.client.get(reverse('public_portfolio', kwargs={'slug': 'nobody-here'}))
        self.assertEqual(response.status_code, 404)

    def test_templates_dynamic_rendering_across_styles(self):
        """All 3 templates render user information dynamically."""
        self.user.portfolio.is_published = True

        for tmpl in ['minimal', 'modern', 'creative']:
            self.user.portfolio.template = tmpl
            self.user.portfolio.save()

            response = self.client.get(reverse('public_portfolio', kwargs={'slug': 'sarah'}))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Sarah Connor')
            self.assertContains(response, 'Threat Sentinel')

class PortfolioSharingAndExportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alex', password='Password123!')
        self.user.profile.full_name = 'Alex Morgan'
        self.user.profile.title = 'Full-Stack Developer'
        self.user.profile.bio = 'Experienced engineer specializing in web systems.'
        self.user.profile.email = 'alex@example.com'
        self.user.profile.location = 'San Francisco, CA'
        self.user.profile.save()

        Education.objects.create(user=self.user, institution='UC Berkeley', degree='B.S.', field_of_study='EECS', start_year=2018, end_year=2022)
        Skill.objects.create(user=self.user, name='Python', category='Backend', proficiency='Expert')
        Project.objects.create(user=self.user, title='TaskFlow', description='Distributed async orchestrator.', technologies='Python, Django, Redis')

    def test_export_html_success(self):
        """User can export and download their portfolio as standalone HTML."""
        self.client.login(username='alex', password='Password123!')
        response = self.client.get(reverse('portfolio_export_html'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response['Content-Type'])
        self.assertIn('attachment; filename="alex_portfolio.html"', response['Content-Disposition'])
        content = response.content.decode('utf-8')
        self.assertIn('Alex Morgan', content)
        self.assertIn('TaskFlow', content)

    def test_export_json_success(self):
        """User can export structured portfolio data as JSON."""
        self.client.login(username='alex', password='Password123!')
        response = self.client.get(reverse('portfolio_export_json'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])
        self.assertIn('attachment; filename="alex_portfolio.json"', response['Content-Disposition'])
        data = response.json()
        self.assertEqual(data['username'], 'alex')
        self.assertEqual(data['profile']['full_name'], 'Alex Morgan')
        self.assertEqual(len(data['educations']), 1)
        self.assertEqual(len(data['skills']), 1)
        self.assertEqual(len(data['projects']), 1)

    def test_export_markdown_success(self):
        """User can export formatted Markdown resume."""
        self.client.login(username='alex', password='Password123!')
        response = self.client.get(reverse('portfolio_export_markdown'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/markdown', response['Content-Type'])
        self.assertIn('attachment; filename="alex_resume.md"', response['Content-Disposition'])
        content = response.content.decode('utf-8')
        self.assertIn('# Alex Morgan', content)
        self.assertIn('UC Berkeley', content)
        self.assertIn('TaskFlow', content)

    def test_portfolio_print_view_success(self):
        """User can view clean print/PDF layout."""
        self.client.login(username='alex', password='Password123!')
        response = self.client.get(reverse('portfolio_print'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/print.html')
        self.assertContains(response, 'Print / Save as PDF')
        self.assertContains(response, 'Alex Morgan')

    def test_export_unauthenticated_redirect(self):
        """Unauthenticated requests to export endpoints redirect to login."""
        endpoints = ['portfolio_export_html', 'portfolio_export_json', 'portfolio_export_markdown', 'portfolio_print']
        for ep in endpoints:
            response = self.client.get(reverse(ep))
            self.assertRedirects(response, f"{reverse('login')}?next={reverse(ep)}")
