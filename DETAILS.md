# portfoli.io — Project Development Log

## 1. Project Overview
**portfoli.io** is a clean, modern web application that enables students and professionals to build and export professional personal portfolios without programming knowledge. Users can create a profile, input education, skills, and projects, select from three curated templates, preview their live work, and share their portfolio across multiple file formats (**Standalone HTML**, **Printable PDF**, **Markdown Resume**, and **JSON Data**). Public publishing functionality is safely preserved in the codebase for future implementation.

---

## 2. Technology Stack & Constraints
- **Backend & Rendering:** Python 3.15, Django 6.1.2, Django Template Language (DTL)
- **Database:** SQLite with Django ORM
- **Frontend:** HTML5, CSS3, Bootstrap 5.3.3 (CDN), Bootstrap Icons 1.11.3, Vanilla JavaScript
- **Authentication:** Django built-in session-based authentication
- **Strict Guidelines:**
  - No React / Node.js
  - No Django REST Framework (DRF)
  - No virtual environment (global Python environment)
  - Django handles full-stack rendering and logic

---

## 3. Project Structure
```text
project/
├── config/
│   ├── settings.py       # Configured TEMPLATES, STATICFILES_DIRS, MEDIA_URL/ROOT, Auth URLs
│   ├── urls.py           # Root URL routing, media serving in DEBUG
│   ├── asgi.py
│   └── wsgi.py
├── myapp/
│   ├── migrations/
│   │   └── 0001_initial.py # Profile, Education, Skill, Project, Portfolio models
│   ├── admin.py          # Django admin registration for all 5 models
│   ├── apps.py
│   ├── forms.py          # UserRegistrationForm, UserLoginForm, ProfileForm, EducationForm, SkillForm, ProjectForm
│   ├── models.py         # Profile, Education, Skill, Project, Portfolio + post_save signal
│   ├── tests.py          # Unit & integration tests (49 test cases)
│   ├── urls.py           # Routing: landing, auth, dashboard, templates, exports, preview, CRUD
│   └── views.py          # Controllers for dashboard, templates, exports (HTML/JSON/MD/Print), preview & content CRUD
├── static/
│   ├── css/
│   │   └── style.css     # Modern custom styling, custom cards, buttons, tokens
│   └── js/
│       └── main.js       # Navbar elevation on scroll, smooth anchor navigation, auto-dismiss alerts
├── templates/
│   ├── base.html         # Base layout with navbar, footer, alert messages, auth status
│   ├── landing.html      # Landing page (Hero, Features, Templates, Steps, CTA)
│   ├── dashboard.html    # User dashboard with completion checklist, template switcher & multi-format export cards
│   ├── auth/
│   │   ├── login.html    # Clean session login form with validation & CSRF
│   │   └── register.html # User registration form with email validation & URL slug preview
│   ├── profile/
│   │   └── edit.html     # Comprehensive profile editor with avatar preview, bio, and social links
│   ├── education/
│   │   ├── list.html     # Educational history cards with start/end years and edit/delete actions
│   │   ├── form.html     # Form for adding and updating education records
│   │   └── delete_confirm.html # Confirmation modal/card for deleting education
│   ├── skills/
│   │   └── list.html     # Categorized skill chips with proficiency levels and quick-add form
│   ├── projects/
│   │   ├── list.html     # Project showcase grid with tech tags, screenshots, and live/repo links
│   │   ├── form.html     # Form for adding and editing projects with screenshot upload
│   │   └── delete_confirm.html # Confirmation card for deleting projects
│   └── portfolio/
│       ├── base_portfolio.html # Base template for generated portfolios with interactive preview & export bar
│       ├── print.html          # Clean printable resume/portfolio layout formatted for PDF saving
│       ├── not_published.html  # Friendly status 403 page (reserved for future public publishing)
│       └── templates/
│           ├── minimal.html    # Minimal Professional design layout (monochrome, executive clarity)
│           ├── modern.html     # Modern Developer design layout (dark mode, code badges, tech stack grid)
│           └── creative.html   # Creative Showcase design layout (vibrant visual cards, pill badges)
├── media/                # User uploaded profile pictures & project images
├── db.sqlite3            # SQLite database
├── manage.py
└── DETAILS.md            # Project progress log
```

---

## 4. Development Roadmap & Status

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Project configuration and landing page | **Completed** |
| **Phase 2** | User registration, login, and logout | **Completed** |
| **Phase 3** | Database models (Profile, Education, Skill, Project, Portfolio) & Profile management | **Completed** |
| **Phase 4** | Education, skills, and project management (CRUD forms) | **Completed** |
| **Phase 5** | User dashboard with completion status, template switcher & module overviews | **Completed** |
| **Phase 6** | Portfolio template selection & dynamic generation (Minimal, Developer, Creative) | **Completed** |
| **Phase 7** | Multi-format portfolio sharing & file exports (HTML, PDF, Markdown, JSON) | **Completed** |
| **Phase 8** | End-to-end verification, quality audit & documentation | **Completed** |
| *Future* | Public URL publishing (`/u/<username>/`) | Preserved for future release |

---

## 5. Phase 1 Implementation Summary
- Configured project settings, root URLs, media serving.
- Built responsive landing page (`landing.html`) with hero, features, template previews, how-it-works, and CTA banner.
- Custom CSS (`static/css/style.css`) and vanilla JS (`static/js/main.js`).

---

## 6. Phase 2 Implementation Summary (Authentication)
- Configured auth settings (`LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`).
- Built `UserRegistrationForm` and `UserLoginForm`.
- Implemented `register_view`, `login_view`, `logout_view`, and protected `dashboard_view`.
- Created templates `templates/auth/login.html` and `templates/auth/register.html`.

---

## 7. Phase 3 Implementation Summary (Database Models & Profile)
- Created 5 models: `Profile`, `Education`, `Skill`, `Project`, `Portfolio`.
- Attached automatic `post_save` receiver provisioning `Profile` and unique `Portfolio` slug on signup.
- Registered all models in `myapp/admin.py`.
- Built `ProfileForm` and `profile_edit_view` with image upload handling and profile strength meter.

---

## 8. Phase 4 Implementation Summary (Education, Skills & Project CRUD)
- Built `EducationForm`, `SkillForm`, `ProjectForm`.
- Strict user isolation in all CRUD querysets (`user=request.user`) preventing unauthorized access.
- Developed list, add, edit, and delete templates and views for Education, Skills, and Projects.

---

## 9. Phase 5 Implementation Summary (User Dashboard)
- Designed full dashboard with dynamic completion percentage (0–100%) and interactive 6-item checklist.
- Integrated template switcher cards allowing instantaneous style change.
- Summary cards and recent item feeds for Education, Skills, and Projects.

---

## 10. Phase 6 & 7 Implementation Summary (Templates & Multi-Format Sharing)

### Multi-Format File Sharing & Exports
Per user request, public URL publishing has been streamlined into direct multi-format file sharing:
1. **Standalone HTML Portfolio (`.html`)**:
   - Route: `/export/html/` (`portfolio_export_html_view`)
   - Generates and downloads a self-contained HTML webpage of the user's active template (Minimal, Developer, or Creative) that opens in any browser offline or can be uploaded anywhere.
2. **Print / Save as PDF (`.pdf`)**:
   - Route: `/export/print/` (`portfolio_print_view`)
   - Renders a clean printable resume layout with print stylesheet (`@media print`) and print-to-PDF button.
3. **Markdown Resume (`.md`)**:
   - Route: `/export/markdown/` (`portfolio_export_markdown_view`)
   - Formats the user's profile, bio, education, skills, and projects into structured Markdown suitable for GitHub profiles or plaintext submission.
4. **Structured JSON Backup (`.json`)**:
   - Route: `/export/json/` (`portfolio_export_json_view`)
   - Exports the complete user portfolio dataset in structured JSON.

### The 3 Dynamic Flagship Templates (Enhanced & Redesigned)
- **Minimal Executive (`templates/portfolio/templates/minimal.html`)**: Redesigned from a narrow single column into a high-density, balanced two-column executive structure (`max-width: 1140px`). Features a sticky profile sidebar with circular avatar, status badge (`Available`), 3-cell metric strip (Projects, Skills, Degrees), stylized bio quote, and icon-based contact rows. The main column features a 2-column project grid with subtle thumbnail/code headers, category-grouped skill cards with proficiency indicators, and an elegant chronological education timeline.
- **Modern Developer (`templates/portfolio/templates/modern.html`)**: Upgraded to a cyber terminal / bento-grid aesthetic (`#07090e` slate background with ambient gradients). Features an IDE/terminal window frame with macOS traffic light dots, branch badge (`git:(main)`), glowing avatar with pulsing status dot (`ready_for_hire: true`), interactive JSON developer specification terminal card, 2-column project cards with git repo headers, code badges, categorized tech stack cards (`📁 Frontend`, `📁 Backend`, etc.) with color-coded proficiency tags, and an academic credentials log.
- **Creative Showcase (`templates/portfolio/templates/creative.html`)**: Enhanced with dynamic mesh gradients (`#3b82f6` to `#6366f1` to `#ec4899`), subtle radial ambient light, floating statistic badges (`Works Shipped`, `Core Skills`, `Credentials`), and rounded pill buttons. Showcases projects in a 2-column bento grid with custom visual art headers or image previews, categorized superpowers cards with pastel proficiency tags, and milestone education journey cards.

### Portfolio Preview Engine (`portfolio_preview_view`)
- Floating sticky control bar (`templates/portfolio/base_portfolio.html`) allowing on-the-fly template switching (`?template=minimal|modern|creative`).
- Quick-export dropdown directly in the preview bar.

### Verification & Automated Testing (`myapp/tests.py`)
- Full test suite covering 49 unit and integration tests across Landing, Authentication, Models, Education CRUD, Skills CRUD, Projects CRUD, Dashboard, Templates, and Multi-Format Exports (HTML, JSON, Markdown, Print).
- **Test Results**: All **49 tests** pass cleanly (`Ran 49 tests in 25.178s, OK`).

---

## 11. Portfolio Template Redesign & Visual Enhancement Summary
- **Space Optimization**: Eliminated excessive vertical whitespace and blank page margins by moving to responsive 2-column and bento-grid structures (`max-width: 1120px - 1140px`).
- **Category Grouping**: Leveraged `skills_by_category` across all three templates to replace raw unstructured tag lists with structured domain cards (e.g. Backend, Frontend, Cloud/Tools).
- **Visual Polish**: Added project media frames / styled fallback art banners, metric counters, status indicators (e.g. pulsing green availability light), and micro-interactions on hover.
- **Recruiter-Ready Professionalism**: Preserved clean typographic contrast (Inter + Fira Code), clear hierarchy, and executive readability across all screen sizes.

---

## 12. Project Documentation (`README.md`)
- Authored a comprehensive, recruiter-ready [`README.md`](README.md) covering:
  - Project overview & feature breakdown
  - Technology stack & architecture constraints
  - Project directory structure & layout
  - Step-by-step installation, setup, local server execution, and testing commands
  - Detailed showcase of the 3 flagship portfolio templates (Minimal Executive, Modern Developer, Creative Showcase)
  - Multi-format exports guide (HTML, Print/PDF, Markdown, JSON)
  - Database schema & foreign-key relationships diagram
  - Security, validation, and user isolation policies
  - Future roadmap

---

## 13. System Flow & Architecture Guide (`PROJECT_FLOW.md`)
- Created [`PROJECT_FLOW.md`](PROJECT_FLOW.md) providing a short, clear, beginner-friendly explanation of:
  - What technologies are used and why (Python, Django, SQLite, Bootstrap, DTL, Vanilla JS).
  - Django Model-View-Template (MVT) request-response lifecycle.
  - End-to-end user navigation flow from landing page to export with Mermaid diagram.
  - Complete page connection and routing map for all 18 routes.
  - Exact data flow: Form submission ➔ ORM insertion with strict user isolation ➔ dynamic preview rendering ➔ multi-format file exports (HTML/PDF/MD/JSON).
  - Security policies (CSRF tokens, `@login_required`, PBKDF2 hashing, user data isolation).

---

## 14. Theme Redesign: "Say Briefly" — Creative Agency Sketchbook on Cream Paper
- **Color Palette & Tokens**:
  - `Forest Ink` (`#1a3300`): Structural workhorse carrying 90% of weight for primary text, links, filled buttons, card borders, and nav borders.
  - `Highlighter Yellow` (`#ffe95c`): Editorial text highlight wash (`.highlight-yellow`), tagline eyebrow badges, monogram logo square.
  - `Cream Paper` (`#fcfaf5`): Base canvas across all pages, card surfaces, and navbar.
  - `Pencil Gray` (`#b6b6b6`): Subtle divider hairlines and borders.
  - `Sticky Note Pastels`: Soft Mint (`#d5f5c2`), Teal (`#a8e5e5`), and Blush (`#f6d0ff`) scattered as tactile sticky notes for features, status pills, and alerts.
- **Typography System**:
  - `Bricolage Grotesque 800`: Display headlines with positive tracking (`0.04em-0.05em`), giving a chunky, sticker-book voice.
  - `Inter (400-700)`: Clean humanist sans for body, subheadings, labels, nav links, and form controls.
  - `Roboto Mono`: Technical metadata, chips, and micro-tags.
- **Components & Layout**:
  - Floating pill-shaped navbar on Cream Paper with 16px radius, Pencil Gray border, and two-part lockup (Yellow square `po` monogram + `portfoli.io` wordmark).
  - 6px border radius strictly applied to all buttons (`.btn-primary-custom`, `.btn-outline-custom`, etc.).
  - 12-16px border radius for cards with flat color separations and 1px borders instead of heavy drop shadows.
  - All application pages redesigned and harmonized: Base layout, Landing page, User Dashboard, Authentication (Login/Register), Profile Editor, Education CRUD, Skills CRUD, Projects CRUD, Portfolio Preview bar, and Printable Resume view.
- **Verification**: All **49 unit & integration tests** pass with 100% success (`Ran 49 tests in 18.262s, OK`).

---

## 15. Authenticated Navigation & Interaction Verification
- **Global Anchor Routing**:
  - Updated navbar and footer navigation links (`Features`, `Templates`, `How It Works`) from relative `#anchor` to `{% url 'landing' %}#anchor` (`/#features`, `/#templates`, `/#how-it-works`).
  - Allows authenticated users on `/dashboard/`, `/profile/edit/`, `/education/`, `/skills/`, or `/projects/` to click navbar links and jump smoothly back to that section on the landing page.
- **Enhanced Smooth Scroll Engine (`static/js/main.js`)**:
  - Handles same-page smooth scroll on `/#anchor` without reloading the page.
  - Automatically compensates for sticky navbar height (`offsetPosition = elementPosition + window.pageYOffset - navHeight - 20`) both on click and when arriving at the page with an anchor hash in the URL.
- **Landing Page Template Modal for Authenticated Users**:
  - Previously, clicking "Use [Template]" in the preview modal simply closed the modal and redirected to the dashboard without switching the template.
  - Upgraded modal footer for logged-in users to provide:
    1. A **"Use [Template] &rarr;"** form button that immediately updates their portfolio template to the chosen style via `portfolio_template_select`.
    2. A **"Live Preview with My Data"** button (`portfolio_preview?template=<id>`) to immediately inspect their actual portfolio data in that template.
- **Step Number Rendering**:
  - Added `'step'` key to `steps` in `landing_page` view and updated template to `{{ step.number }}` so step numbers ("01", "02", "03") render with full fidelity.
- **Automated Testing**:
  - Added `test_landing_page_authenticated_user` to `myapp/tests.py`.
  - All **50 unit & integration tests** pass cleanly (`Ran 50 tests in 17.724s, OK`).

---

## 16. Visual Enhancement: Light Green Wash for Cards & Boxes
- **Context & Motivation**:
  - The sketchbook theme's original palette used Cream Paper (`#fcfaf5`) for both page canvas and card surfaces, which produced a slightly flat, pale appearance without sufficient dimensional hierarchy.
  - Applied a delicate, organic light green wash across all cards, step blocks, frames, and feature boxes to make the interface visually appealing, tactile, and lively.
- **CSS Color Tokens (`static/css/style.css`)**:
  - `--color-mint-wash: #edf6ea;` — Primary card/box fill: a soft, muted sage-mint tint that sits comfortably between Cream Paper (`#fcfaf5`) and saturated sticky mint (`#d5f5c2`).
  - `--color-mint-wash-subtle: #f4f9f1;` — Secondary inner container wash for mockups, code headers, and subtle dividers.
  - `--color-mint-wash-hover: #e2f0dd;` — Interactive hover state for cards and list items.
  - `--color-mint-wash-banner: #e4f2de;` — Bottom CTA banner surface fill.
  - `--bg-card: var(--color-mint-wash);` — Global semantic card background token.
- **Components Styled with Light Green Tint**:
  - `.card-sketch`: Dashboard metric cards, section panels, form containers, profile info boxes.
  - `.step-card-sketch`: "How It Works" 3-step workflow cards on the landing page.
  - `.hero-mockup-frame` & `.hero-mockup-bar`: Hero illustration and interactive portfolio preview card frames.
  - `.cta-sketch-banner`: Bottom call-to-action banner on the landing page.
  - `.card-sticky-cream`: Secondary utility cards.
  - `.backed-by-item`: Tech stack credibility pills in the hero section.
  - Crisp white (`#ffffff`) tag backgrounds (`.mono-tag`) and form inputs (`.form-control`) provide high-contrast readability against the light green surface.
- **Accessibility & Verification**:
  - Forest Ink text (`#1a3300`) on `--color-mint-wash` (`#edf6ea`) provides an **11.8:1 contrast ratio**, well exceeding WCAG 2.1 AAA requirements (7:1).
  - All **50 unit and integration tests** pass cleanly (`Ran 50 tests in 18.525s, OK`).






