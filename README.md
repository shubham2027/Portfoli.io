# portfoli.io — Personal Portfolio Generator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.x-092e20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap_5.3.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Tests](https://img.shields.io/badge/Tests-49_Passing-brightgreen)](https://docs.djangoproject.com/en/stable/topics/testing/)

**portfoli.io** is a clean, modern web application built with Python and Django that enables students, software engineers, designers, and professionals to build, preview, and share recruiter-ready personal portfolios without requiring any programming knowledge.

Users can register, enter their personal background, academic credentials, categorized skills, and featured projects, choose from three distinct portfolio styles, preview their live portfolio, and export it across multiple file formats (**Standalone HTML**, **Printable PDF**, **Markdown Resume**, and **JSON Data**).

---

## Table of Contents

- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Architecture & Directory Structure](#project-architecture--directory-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Running the Development Server](#running-the-development-server)
  - [Running Tests](#running-tests)
- [Portfolio Templates](#portfolio-templates)
- [Multi-Format Sharing & Exports](#multi-format-sharing--exports)
- [Database Models & Architecture](#database-models--architecture)
- [Security & Validation](#security--validation)
- [Future Enhancements](#future-enhancements)

---

## Key Features

### 1. Modern Landing Page
- Engaging hero section introducing the platform with direct calls to action.
- Feature breakdown highlighting ease of use, instant exports, and responsive design.
- Interactive template showcase displaying previews of all three design styles.
- Step-by-step workflow guide ("Create Profile", "Add Highlights", "Pick Style & Share").
- Professional navigation bar and footer with platform links.

### 2. User Authentication & Session Security
- User registration with unique username and email validation.
- Secure session-based authentication (Login, Logout) powered by Django's built-in auth system.
- Strict route protection ensuring all dashboard, management, and preview routes require authentication.

### 3. Interactive User Dashboard
- Personalized welcome banner and quick-action buttons.
- Dynamic completion percentage meter ($0\%$ to $100\%$) paired with an interactive 6-step setup checklist.
- Quick summary widgets for Education records, Skills catalog, and Project items.
- In-place template switcher allowing instant default style selection.

### 4. Comprehensive Profile Management
- Full name, professional title, and customizable avatar upload with automated fallbacks.
- Contact details: Email, phone number, and geographic location.
- Detailed biography / executive summary.
- Social links: GitHub, LinkedIn, and personal website URLs.

### 5. Education & Academic Background (Full CRUD)
- Add, view, edit, and delete academic milestones.
- Fields: Institution, degree, field of study, start year, end year (or "Present"), and description.
- Chronological timeline ordering across all generated portfolios.

### 6. Categorized Skills Management (Full CRUD)
- Add, update, and remove skills with domain categories (e.g., *Frontend*, *Backend*, *DevOps*, *Design*, *General*).
- Proficiency ratings: *Beginner*, *Intermediate*, *Advanced*, and *Expert*.
- Automatically grouped and presented in structured competency matrices on portfolios.

### 7. Featured Projects Management (Full CRUD)
- Add, update, and delete showcase projects.
- Fields: Project title, description, comma-separated technologies, GitHub repository URL, live preview URL, and optional screenshot image upload.
- Automated parsing of technologies into individual badges.

### 8. Live Portfolio Preview Engine
- Interactive top control bar sticky at the top of the preview window.
- Instant template switcher allowing users to switch styles on the fly (`?template=minimal`, `?template=modern`, or `?template=creative`).
- Quick export menu directly accessible within the preview mode.
- Button to set any template as the user's permanent default.

---

## Technology Stack

The project adheres strictly to standard, clean Django full-stack practices without unnecessary external dependencies:

| Layer | Technology |
|---|---|
| **Backend Framework** | Python 3.10+ / Django 6.x |
| **Rendering Engine** | Django Template Language (DTL) |
| **Database** | SQLite via Django ORM |
| **Frontend Styling** | Bootstrap 5.3.3 (CDN), Bootstrap Icons 1.11.3, Custom CSS tokens |
| **Client-Side Scripting** | Vanilla JavaScript (ES6+) |
| **Authentication** | Django Session Authentication & Password Hashers |

> **Architecture Constraints:**
> - Strictly **no** React, Node.js, or complex client build pipelines.
> - Strictly **no** Django REST Framework (DRF) — Django handles both rendering and backend logic.
> - Relies on native Django ORM, CSRF protection, and form validation.

---

## Project Architecture & Directory Structure

```text
project/
├── config/
│   ├── settings.py         # Configured TEMPLATES, STATIC, MEDIA, Auth routes
│   ├── urls.py             # Root URL routing & media serving in DEBUG mode
│   ├── asgi.py             # ASGI deployment configuration
│   └── wsgi.py             # WSGI deployment configuration
├── myapp/
│   ├── migrations/
│   │   └── 0001_initial.py # Initial migration for Profile, Education, Skill, Project, Portfolio
│   ├── admin.py            # Admin registration for all 5 models
│   ├── apps.py             # App configuration with signal loading
│   ├── forms.py            # Registration, Login, Profile, Education, Skill, Project forms
│   ├── models.py           # Database models + post_save user provisioning signal
│   ├── tests.py            # 49 unit and integration tests
│   ├── urls.py             # Complete URL routing for all modules & exports
│   └── views.py            # View controllers for dashboard, CRUD, preview, exports
├── static/
│   ├── css/
│   │   └── style.css       # Custom design tokens, card styles, and animations
│   └── js/
│       └── main.js         # Navbar scroll elevation, dismissible alerts, smooth scroll
├── templates/
│   ├── base.html           # Main base template (navbar, flash alerts, footer)
│   ├── landing.html        # Public landing page
│   ├── dashboard.html      # User dashboard & progress checklist
│   ├── auth/
│   │   ├── login.html      # User login form
│   │   └── register.html   # Registration form with dynamic username preview
│   ├── profile/
│   │   └── edit.html       # Profile editor with avatar upload & preview
│   ├── education/
│   │   ├── list.html       # Education history management
│   │   ├── form.html       # Add / Edit education form
│   │   └── delete_confirm.html
│   ├── skills/
│   │   └── list.html       # Categorized skills list & quick add
│   ├── projects/
│   │   ├── list.html       # Project grid management
│   │   ├── form.html       # Add / Edit project with screenshot upload
│   │   └── delete_confirm.html
│   └── portfolio/
│       ├── base_portfolio.html # Shared base with sticky preview bar & export menu
│       ├── print.html          # Clean printable resume layout formatted for PDF
│       ├── not_published.html  # Status 403 page for unpublished portfolios
│       └── templates/
│           ├── minimal.html    # Minimal Executive template (2-column editorial)
│           ├── modern.html     # Modern Developer template (terminal & cyber bento)
│           └── creative.html   # Creative Showcase template (mesh gradient & bento)
├── media/                  # Uploaded profile photos and project screenshots
├── db.sqlite3              # SQLite database file
├── manage.py               # Django management script
├── DETAILS.md              # Project implementation log across all phases
└── README.md               # Project documentation
```

---

## Getting Started

### Prerequisites

- **Python 3.10** or higher installed on your system.
- **Django 5.x / 6.x** installed.

Verify your Python and Django installations:
```bash
python --version
python -m django --version
```

### Installation & Setup

1. **Navigate to the project root directory**:
   ```bash
   cd project
   ```

2. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

3. **(Optional) Create a superuser for Django Admin**:
   ```bash
   python manage.py createsuperuser
   ```

### Running the Development Server

Start the Django built-in local development server:
```bash
python manage.py runserver
```

Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```

- **Landing Page**: `http://127.0.0.1:8000/`
- **Register Account**: `http://127.0.0.1:8000/register/`
- **Login**: `http://127.0.0.1:8000/login/`
- **Dashboard**: `http://127.0.0.1:8000/dashboard/`
- **Django Admin**: `http://127.0.0.1:8000/admin/`

### Running Tests

The application includes an extensive automated test suite covering authentication, forms, CRUD operations, template rendering, and exports:

```bash
python manage.py test
```

Expected result:
```text
Found 49 test(s).
Creating test database for alias 'default'...
.................................................
----------------------------------------------------------------------
Ran 49 tests in ~25s

OK
Destroying test database for alias 'default'...
```

---

## Portfolio Templates

Each template is carefully styled to eliminate awkward whitespace and deliver a balanced, professional presentation:

### 1. Minimal Executive (`minimal.html`)
- **Layout**: Balanced asymmetric 2-column editorial structure (`max-width: 1140px`).
- **Sidebar**: Sticky profile card with circular avatar / monogram, availability pill (`● Available`), 3-cell metric strip (Projects, Skills, Degrees), stylized bio quote, and icon-based contact rows.
- **Main Section**: 2-column project cards with subtle thumbnail or code headers, domain-categorized skills with proficiency chips, and an academic timeline with milestone dots.
- **Ideal for**: Consultants, managers, analysts, executives, and academics.

### 2. Modern Developer (`modern.html`)
- **Layout**: Dark mode cyber-terminal & bento-grid aesthetic (`#07090e` slate canvas with ambient indigo glow).
- **Hero Frame**: Terminal window header with macOS traffic light dots (`red`, `yellow`, `green`), active branch badge (`git:(main) ✓`), pulsing green beacon (`ready_for_hire: true`), and an interactive `developer_spec.json` card.
- **Main Section**: 2-column project cards with `origin/main` commit headers, monospace syntax tags, categorized tech stack cards (`📁 Frontend`, `📁 Backend`, etc.) with color-coded proficiency tags, and an academic credentials log.
- **Ideal for**: Full-stack engineers, backend developers, devops specialists, and data scientists.

### 3. Creative Showcase (`creative.html`)
- **Layout**: Dynamic multi-stop mesh gradient header (`#3b82f6` to `#6366f1` to `#ec4899`) with rounded bento cards.
- **Header**: Avatar with glowing ring, location pill, bio lead text, live stat counters (*Works Shipped*, *Core Skills*, *Credentials*), and pill action buttons.
- **Main Section**: Bento grid of projects with screenshot frames or decorative geometric art banners, categorized superpowers cards with pastel badges, and milestone journey cards.
- **Ideal for**: UI/UX designers, creative technologists, frontend developers, and multimedia creators.

---

## Multi-Format Sharing & Exports

Users can share and archive their generated portfolios in multiple convenient formats:

| Format | Endpoint | Description |
|---|---|---|
| **Standalone HTML** | `/export/html/` | Downloads a self-contained `.html` webpage of the active template that can be opened locally in any browser or uploaded to any hosting service. |
| **Print / PDF** | `/export/print/` | Opens a clean, dedicated printable resume layout configured with `@media print` styling to easily **Save as PDF** or print directly. |
| **Markdown Resume** | `/export/markdown/` | Generates a clean `.md` resume document with Markdown headers, lists, and links, perfect for GitHub READMEs or plaintext job portals. |
| **JSON Data Backup** | `/export/json/` | Exports the user's entire portfolio record (profile, educations, skills, projects) as structured `.json` for backup and portability. |

*(Note: Public URL publishing functionality at `/u/<username>/` remains safely preserved in the backend for future public deployment).*

---

## Database Models & Architecture

All models are linked to Django's built-in `User` model using `OneToOneField` or `ForeignKey` with `on_delete=models.CASCADE`:

```text
User (Django Built-in)
  ├── Profile (OneToOneField)
  │     ├── full_name, title, profile_picture, bio
  │     └── email, phone, location, github_url, linkedin_url, website_url
  │
  ├── Portfolio (OneToOneField)
  │     ├── slug (unique), template ('minimal', 'modern', 'creative'), is_published
  │
  ├── Education (ForeignKey -> User, related_name='educations')
  │     ├── institution, degree, field_of_study, start_year, end_year, description
  │
  ├── Skill (ForeignKey -> User, related_name='skills')
  │     ├── name, category, proficiency
  │
  └── Project (ForeignKey -> User, related_name='projects')
        ├── title, description, technologies, github_url, live_url, image
```

### Automatic Provisioning Signal
When a new `User` is registered, a `post_save` Django signal automatically creates:
1. An empty `Profile` instance ready for completion.
2. A `Portfolio` instance with a unique slug derived from the username.

---

## Security & Validation

- **Strict User Isolation**: All CRUD queries filter explicitly by `user=request.user`, preventing users from reading or modifying another user's records.
- **CSRF Protection**: All POST forms include Django's `{% csrf_token %}` tag.
- **Form Validation**: Strict validation on URLs, email formats, and file uploads.
- **Password Security**: Uses Django's default PBKDF2 password hashing algorithm with SHA-256.
- **Media Safety**: Uploaded images are stored in designated `media/` subdirectories (`avatars/` and `projects/`).

---

## Future Enhancements

The following capabilities are architected for seamless future addition:
- **AI-Powered Biography Generator**: Automated professional summary generation based on skills and projects.
- **Resume PDF Parser**: Extract profile, education, and project records automatically from an uploaded PDF.
- **Direct PDF Rendering**: Server-side PDF generation using WeasyPrint or ReportLab.
- **Custom Color Palettes**: Allow users to select accent colors for each template.
- **Public Domain Publishing**: One-click publishing to `/u/<username>/` with custom vanity domains.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

