# NodeNexus Documentation

**Last updated:** August 13, 2026

---

# Table of Contents

1. [Overview](#1-overview)
2. [Project Structure](#2-project-structure)
3. [Backend](#3-backend)
4. [Frontend](#4-frontend)
5. [Database](#5-database)
6. [Completed Features](#6-completed-features)
7. [Current Limitations](#7-current-limitations)
8. [Key Design Decisions](#8-key-design-decisions)
9. [Deployment](#9-deployment)
10. [Challenges and Solutions](#10-challenges-and-solutions)
11. [What Was Learned](#11-what-was-learned)
12. [Next Steps](#12-next-steps)
13. [References](#13-references)

---

# 1. Overview

NodeNexus is a technology news aggregator built with Django. It pulls articles from the Currents API and displays them across category pages (AI, cybersecurity, gaming, trending), alongside global search, autocomplete, and article detail pages.

The application also includes user authentication and account features, allowing users to register, log in, manage their account, and interact with content. Further user features such as bookmarks, comments, messaging, and account management are being developed as the project progresses.

The stack is Django, PostgreSQL, and Django Templates with Bootstrap, custom CSS, and vanilla JavaScript. The project is structured so a React frontend and DRF API layer can be added later without a rewrite, but currently all pages are plain Django templates.

The application is deployed on Render, with PostgreSQL used for the database and external services used for news data and user-uploaded media.

---

# 2. Project Structure

The project splits backend and frontend into separate top-level folders, so Django logic and frontend resources aren't mixed together, and so a React frontend can slot into `frontend/` later without restructuring the backend.

```text
NodeNexus/
│
├── backend/
│   ├── accounts/               # Authentication and account-related views/forms
│   ├── config/                 # Django settings, urls, wsgi/asgi
│   ├── core/                   # General site views (ai, cybersecurity, gaming, trending)
│   ├── media/                  # Contains the `default.png` file for initial profile picture
│   ├── news/                   # News app: models, views, and services/
│   │   └── services/
│   │       ├── currents.py     # Currents API calls + processing
│   │       └── cache.py        # API response caching
│   ├── staticfiles/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── components/     # Reusable template partials (navbar, footer, article_card, etc.)
│       ├── pages/          # Page templates (index, ai, cybersecurity, gaming, trending, search_results)
│       └── static/         # css, js, images
│
├── docs/
├── Procfile
└── README.md
```

The `core` app handles general site pages. `news` handles article fetching and category logic. The `news/services` package keeps Currents API calls and caching logic out of the views. The `accounts` app handles user registration, login, logout, profile access, password resets, and password changes.

---

# 3. Backend

## Views and URL routing

Each category page (AI, cybersecurity, gaming, trending) and the search results page has a view that: reads the requested page number from the URL, calls the relevant service function, falls back to a valid page if the requested one is empty, and renders the template.

A shared `get_page_articles` helper handles the "requested page has no results, step back until one does" logic so it isn't repeated in every view.

---

## Currents API service

`currents.py` handles all communication with the Currents API: building the request, processing the response into a consistent article format, and returning `has_next` so views know whether another page exists.

The Currents API doesn't return a total result count, so pagination can't use a normal "page X of Y" approach — instead, each request returns whether a next page is available, and the app works page-by-page from there. In practice, and from testing, results are capped at five pages per query.

---

## Caching

`cache.py` provides a TTL-based cache in front of the Currents API calls, so repeated requests for the same query/page don't hit the external API every time. This reduces API usage and makes the app more resilient to slow or inconsistent API responses.

---

## Content filtering

Before articles are shown, low-quality results are filtered out:
- A domain exclusion list removes known low-value sources (forum threads, raw vulnerability database dumps).
- Auto-generated CVE announcement titles are filtered out, while genuine articles that reference a CVE number in a proper headline are kept.
- Duplicate articles are removed.

---

## Authentication

NodeNexus uses Django's built-in authentication system for user registration, password hashing, validation, login, logout, sessions, password resets, and password changes.

The registration form extends Django's `UserCreationForm` and adds an email field. Additional validation requires passwords to contain at least one uppercase letter, lowercase letter, digit, and special character.

The authentication system currently provides:

- User registration
- Login and logout
- Protected profile page
- Profile editing
- Custom profile picture uploads using Cloudinary
- Preset profile picture selection
- Password reset by email
- Password reset confirmation
- Password reset completion
- Change password for authenticated users

Django handles the security-sensitive password hashing and authentication logic rather than implementing these systems manually.

---

## Password Reset and Email

Django's built-in password reset system is used to handle password recovery.

The user enters their email address and Django sends a password reset link. The user can then choose a new password and return to the login page.

During development, Django's console email backend was initially used to print reset emails in the terminal. This was later replaced with SMTP so real emails could be sent.

SMTP settings and the email account password are stored in environment variables rather than the codebase.

The complete reset process was tested successfully using a real email account.

---

# 4. Frontend

## Templates

`base.html` holds the shared site structure (nav, footer, theme switching, static/JS loading). Individual pages extend it. Shared UI pieces (article cards, navbar, footer, search bar, category sections) live in `components/` and get included where needed, so changing one component updates it everywhere it's used.

---

## Styling

Bootstrap handles the responsive grid and base components. Custom CSS on top of that controls the NodeNexus look: a deep-space background with cyan accents, glass-style translucent panels, and dark/light theme support via CSS variables.

---

## Search

- A search bar with live autocomplete, calling a dedicated endpoint that returns matching article titles as JSON.
- Input is debounced to avoid firing a request on every keystroke.
- A stale-response guard tracks the most recent query and discards any autocomplete response that doesn't match it, so a slow earlier request can't overwrite a newer one on screen.

```javascript
if (latestQuery !== query) return; 
```

---

## Pagination

Pagination controls show up to five numbered page buttons (matching the Currents API's five-page cap) plus previous/next arrows, with the current page highlighted.

Layout is responsive:
- **Desktop:** arrows sit on either side of the five page number buttons.
- **Tablet and smaller:** the five page buttons stay on top, with the previous/next arrows moved underneath as their own row.
- Buttons scale down in size on narrower screens to avoid crowding.

The same pagination component is used across the category pages and search results, and search pagination preserves the active query string.

## Homepage and article layout

The homepage article grid is a three-column layout on desktop. On tablet and mobile it switches to a horizontal scrolling carousel instead of stacking into a single column, so users can swipe through articles rather than scroll a long vertical list.

The article detail page has a "related articles" section that uses the same horizontal carousel pattern on tablet and mobile, with related articles matched by comparing the first three words of each article title. This can sometimes return non-tech results, however this is expected when working with external APIs.

```python
related_query = " ".join(title_words[:3])
```

## Responsive Design

Getting Bootstrap and the custom CSS to work consistently across different screen sizes required ongoing testing and adjustments as new features were added. Components such as the mobile navigation, article carousels, pagination, article cards, and article detail layout each required responsive styling to maintain a consistent appearance and layout across desktop, tablet, and mobile devices.

The homepage uses a desktop grid layout that changes to a horizontal carousel on smaller screens, while related articles also use a responsive horizontal carousel. Pagination controls, navigation elements, spacing, card sizes, and typography adjust at different screen sizes to maintain usability.

Responsive testing was carried out across different viewport widths using browser developer tools and physical device testing. This helped identify and resolve layout, spacing, sizing, and overflow issues that were not always visible at standard desktop and mobile breakpoints.

Other responsive features include the mobile bottom navigation bar, off-canvas mobile menu, responsive article cards, and fallback images for articles with missing or broken images.

---

## Password Visibility

The existing password visibility JavaScript was extended to support the password reset and change password forms.

The same `setupPasswordToggle()` function is reused across the authentication pages, allowing users to show or hide password fields without adding separate JavaScript for each form.

---

## Profile and Profile Pictures

The profile page allows authenticated users to edit their account details, change their password, and manage their profile picture.

Users can either upload a custom profile picture through Cloudinary or select from a set of preset images stored locally in the application's static files. Preset images do not use Cloudinary.

The selected profile picture is displayed on the profile page and throughout the application, including the desktop navbar and mobile navigation.

---

# 5. Database

NodeNexus uses PostgreSQL instead of Django's default SQLite, for a more production-realistic setup and to support future features like user accounts, bookmarks, and comments. Credentials are kept in environment variables rather than in the codebase. Development and production use separate PostgreSQL databases, both accessed through the same Django ORM configuration.

The database currently includes Django's default authentication tables and the application's user profile data. User accounts and profile information are stored in PostgreSQL.

Custom profile images are stored through Cloudinary, while preset profile images are stored as static files and referenced by the user's profile.

User features such as bookmarks, comments, and messaging will be added later.

---

# 6. Completed Features

- **News aggregation:** Currents API integration with category pages for AI, cybersecurity, gaming, and trending tech.
- **Search:** global search with a results page, plus live autocomplete with debouncing and stale-response handling.
- **Content filtering:** domain exclusion list, CVE-title filtering, and deduplication.
- **Pagination:** five-button numbered pagination with previous/next arrows, responsive layout, applied across category and search pages.
- **Article detail pages:** full article view with a larger image, a link to the original article, and a related-articles carousel.
- **Responsive frontend:** desktop grid / mobile carousel layouts, mobile bottom nav, off-canvas menu, fallback images.
- **Theming:** dark/light mode via CSS variables.
- **Caching:** TTL cache in front of the Currents API to cut down on repeat requests.
- **User authentication:** Django's built-in authentication system is used for signup, login, logout, password hashing, validation, and sessions.
- **Authentication forms:** Custom signup and login pages with Django form validation, inline errors, and password visibility toggles.
- **Authentication navigation:** Signup, login, and logout links have been added to the desktop and mobile navigation.
- **Password reset:** Users can request a password reset email, set a new password, and return to the login page.
- **Change password:** Logged-in users can change their password from their profile.
- **User profiles:** Authenticated users can view and edit their profile information.
- **Profile pictures:** Users can upload a custom profile picture through Cloudinary or select from preset images stored locally.
- **Profile navigation:** The user's profile picture is displayed in the desktop navbar and mobile hamburger menu.
- **Deployment setup:** Render hosting, PostgreSQL, Gunicorn, WhiteNoise for static files.

Not yet built: bookmarks, comments, and the inbox/messaging system.

---

# 7. Current Limitations

- The app depends entirely on the Currents API — if it's slow, rate-limited, or changes its response format, that directly affects the site. Caching helps but doesn't remove the dependency.
- Article data from the API isn't perfectly consistent (missing fields, occasional thin category results), so some normalisation and filtering will likely need further tuning.
- Related-articles matching (first three words of the title) is a simple heuristic, not true topic matching, so results are sometimes only loosely related.
- Article detail pages currently pass full article metadata (title, description, image, source, published date, URL) through query parameters in the URL, rather than looking articles up by an ID from the database. This works for now but is only temporary until articles are stored with proper IDs once the database models are built.
- User authentication, profile access, profile editing, profile pictures, password reset, and change password are implemented. Bookmarking, comments, and messaging have not been built.

---

# 8. Key Design Decisions

**Why Django** — built-in URL routing, templates, ORM, and authentication meant less to build from scratch compared to Flask, which was used on earlier projects.

**Why Django authentication** — Django handles account creation, password hashing, password validation, login, logout, and sessions out of the box. This avoids having to build security-sensitive authentication features from scratch.

**Why PostgreSQL** — more production-realistic than SQLite, and better suited to the relational data coming later (users, bookmarks, comments).

**Why separate `backend/` and `frontend/`** — keeps Django logic and frontend templates/assets cleanly split, so a future React frontend can be added without reorganising the backend.

**Why previous/next pagination instead of numbered totals** — the Currents API doesn't report a total result count, so a traditional "page X of Y" approach wasn't possible. Since results are capped at five pages, a fixed five-button layout was used instead of calculating a page range.

**Why a service layer for the API** — keeping `currents.py` and `cache.py` separate from the views means the views stay focused on handling requests, and the API/caching logic can be tested and changed independently.

---

# 9. Deployment

NodeNexus is deployed on Render, with Gunicorn as the WSGI server and PostgreSQL as the database, both hosted on Render.

Static files are handled differently depending on environment:
- In development (`DEBUG=True`), Django serves static files directly.
- In production (`DEBUG=False`), WhiteNoise serves collected static files, and `CompressedManifestStaticFilesStorage` generates versioned filenames so updated CSS/JS don't get served from stale browser caches.

User-uploaded profile images are stored using Cloudinary. Cloudinary configuration is provided through environment variables on Render rather than being stored in the codebase.

Deployment flow: push to GitHub → Render pulls the update → installs dependencies → runs `collectstatic` → Gunicorn starts the app → app connects to the production database. Secrets (Django secret key, database credentials, API keys, and Cloudinary credentials) are all set as environment variables on Render, not committed to the repo.

---

# 10. Challenges and Solutions

**Bootstrap vs custom CSS conflicts** — Bootstrap's default grid and component styles sometimes fought with the custom glass UI design. Fixed by using Bootstrap for layout structure only, and custom CSS/media queries for anything branding- or spacing-related.

**Static files not updating after deployment** — CSS changes weren't showing up after deploy because old cached static files were still being served. This came down to understanding how WhiteNoise and `CompressedManifestStaticFilesStorage` version filenames — running `collectstatic` properly and letting the manifest generate new filenames fixed it.

**Currents API has no total result count** — Django's built-in `Paginator` needs a known total, which the API doesn't provide, and using it led to broken/stuck pagination. Solved by switching to a `has_next`-based approach: fetch a page, check if another exists, and let the view decide whether to render or redirect. Since the API caps out around five pages per query, pagination was later simplified further to a fixed five-button layout instead of computing a page range.

**Autocomplete race condition** — Typing quickly could fire multiple autocomplete requests, and a slower earlier request would sometimes resolve after a newer one, overwriting correct results with stale ones. Fixed by tracking the latest submitted query and discarding any response that doesn't match it.

**Autocomplete dropdown rendering behind other content** — despite a high `z-index`, the dropdown appeared behind later page sections. Caused by `backdrop-filter` on sibling elements creating their own stacking contexts, which isolates `z-index` comparisons within that context. Fixed by giving the hero section `position: relative` with an explicit `z-index` so its contents (including the dropdown) stack above later sections.

**Article detail page not loading with just a URL param** — the initial approach passed only the article URL through the query string and tried to look the article back up from that, which didn't work reliably since the API doesn't support fetching a single article by URL. Solved by passing the full article data (title, description, image, published date, source, URL) through query parameters instead, so the detail view builds the article directly from what's in the request rather than re-fetching it. Related articles are then generated by searching on the first three words of the title and filtering out the current article from the results.

**Carousel not activating on mobile landscape** — the homepage still showed the desktop grid instead of the carousel on a mobile device in landscape orientation. Traced to the device's landscape width being wider than the `768px` breakpoint the carousel styling was scoped to. Rather than adding another breakpoint, the carousel rules were moved into the existing `max-width: 992px` section, which already covers tablet and landscape-mobile widths.

**Authentication frontend integration** — Django handled the backend authentication logic, including account creation, password validation, login, logout, and sessions. The main work was integrating the forms into the existing NodeNexus design across signup, login, password reset, and change password, including custom styling, validation errors, password visibility toggles, and responsive authentication links in the navbar.

**Real email setup** — Password reset emails initially used Django's console backend, which printed the email in the terminal. SMTP was later configured so password reset emails could be sent to a real email address. Email credentials are stored in environment variables.

**Initial profile picture implementation** — Profile pictures were initially handled locally through a `media/profile_pics` folder. Both uploaded images and preset images were being stored in this location, with `default.png` used as the initial default profile image. This worked during local development but was not suitable for production on Render because uploaded files should not depend on the application's local filesystem.

**Separating preset and custom profile images** — The profile picture system was redesigned so the two types of images are handled separately. Nine preset images were hand-selected to match the NodeNexus theme and stored in the application's static image files, while custom user uploads are handled by Cloudinary. Two separate fields were added to the `Profile` model to store the selected preset image or custom Cloudinary image.

**Profile picture modal** — The profile picture selection interface required a custom modal allowing users to choose a preset image or upload their own. Initially, placing the modal inside the profile update form caused the form structure and submission behaviour to conflict with the modal. The modal was moved outside the main profile form, which allowed the two interfaces to function independently.

**Profile picture preview and JavaScript integration** — JavaScript was added to control the profile picture modal, handle preset image selection, preview the selected image, and update the displayed profile picture when the user selects a preset or custom upload. This required the frontend to distinguish between the two image sources while keeping the user experience consistent.

**Responsive profile interface** — The profile picture modal and profile editing interface required additional CSS and responsive adjustments to work correctly across desktop, tablet, and mobile screen sizes. The profile picture was also added at a smaller size to the desktop navbar and mobile hamburger menu so the selected image remained visible throughout the application.

**Cloudinary migration** — To make custom profile uploads work reliably in production, the profile image field was changed to `CloudinaryField`. Cloudinary was configured for both development and production, with credentials stored in environment variables. This allowed custom uploads to be stored externally while preset images remained local static assets.

**Cloudinary configuration and Render deployment** — The Cloudinary implementation initially caused deployment problems on Render. The build installed the `cloudinary` package but failed when Django attempted to import `cloudinary_storage`. The unused `cloudinary_storage` configuration was removed and the project was configured to use `CloudinaryField` directly. Cloudinary environment variables were then added to Render so the same profile image system worked in both development and production.

**Development and production consistency** — The profile picture system was tested across both the local development environment and the deployed Render application. The final implementation keeps preset images in static files and custom uploads in Cloudinary, avoiding reliance on the Render filesystem for user-uploaded media.

---

# 11. What Was Learned

- Structuring a Django project using apps, views, templates, and a separate services layer.
- Understanding separation of responsibilities by keeping API requests and caching outside of Django views.
- Working with external APIs and adapting the application around their limitations, including missing total result counts, inconsistent results, and limited ways to identify individual articles.
- Designing pagination around the capabilities of the external API rather than assuming Django's built-in pagination tools would be suitable.
- Combining Bootstrap with custom CSS to create responsive layouts while keeping control over the application's design.
- Understanding how responsive layouts, breakpoints, overflow, and viewport sizes affect different devices.
- Understanding CSS stacking contexts and why `z-index` alone does not always control which elements appear above others.
- Debugging problems by testing different parts of the application and investigating the actual cause rather than assuming the first solution will work.
- Working with temporary solutions while the database structure is still being developed, such as passing article data through URLs.
- Making practical development decisions when a perfect solution is not necessary, such as using relevant title keywords for related articles instead of trying to achieve perfect article matching.
- Gaining a better understanding of how the frontend, Django backend, external APIs, and deployment environment work together as one application.
- Using Django's built-in authentication system for user signup, login, logout, password validation, and sessions.
- Understanding how Django forms handle validation and display errors directly in templates.
- Connecting Django authentication to a custom frontend rather than using Django's default styling.
- Adding custom JavaScript functionality to Django forms, such as password visibility toggles.
- Understanding Django's built-in password reset and change password functionality.
- Configuring SMTP email so the application can send real password reset emails.
- Using environment variables to keep email credentials outside the codebase.
- Building a more complete user profile system with profile editing, password changes, and profile picture management.
- Understanding the difference between static assets and user-uploaded media and why they should be handled separately.
- Using Cloudinary to store user-uploaded images instead of relying on the local filesystem in production.
- Using `CloudinaryField` to connect Django model fields to Cloudinary-hosted images.
- Designing a profile system that supports both preset images and user-uploaded images through separate model fields.
- Using JavaScript to control a custom modal, handle image selection, and preview profile images before submission.
- Understanding how HTML form structure can affect modal behaviour and why separating the modal from the main update form was necessary.
- Keeping development and production media handling consistent through environment-based Cloudinary configuration.

---

# 12. Next Steps

- Bookmarks (saved articles), comments, and the inbox/messaging system required by the assignment brief.
- Account deletion and additional account management features.
- Admin functionality and role-based access control.
- Continued testing and bug fixes on API result consistency (some categories occasionally return fewer than 12 articles).
- Final UI polish, responsive testing, accessibility improvements, and general application refinement.
- Eventual migration to a React frontend with a DRF API layer — models and the service layer are expected to carry over largely unchanged.

---

# 13. References

**Backend**
- Django Documentation — https://docs.djangoproject.com/en/6.0/
- Django Pagination — https://docs.djangoproject.com/en/6.0/topics/pagination/
- Django Models and Migrations — https://docs.djangoproject.com/en/6.0/topics/db/models/
- Django Authentication — https://docs.djangoproject.com/en/6.0/topics/auth/
- Django Messages — https://docs.djangoproject.com/en/6.0/ref/contrib/messages/
- Django Password Management — https://docs.djangoproject.com/en/6.0/topics/auth/passwords/
- Django Email — https://docs.djangoproject.com/en/6.0/topics/email/

**Frontend**
- Bootstrap Documentation — https://getbootstrap.com/docs/
- Bootstrap Modal — https://getbootstrap.com/docs/5.3/components/modal/
- Bootstrap Forms — https://getbootstrap.com/docs/5.3/forms/overview/
- MDN Web Docs — https://developer.mozilla.org/
- MDN File Input — https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file
- MDN File API — https://developer.mozilla.org/en-US/docs/Web/API/File_API
- MDN URL.createObjectURL() — https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static
- CSS Media Queries — https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries

**Database**
- PostgreSQL Documentation — https://www.postgresql.org/docs/
- Django PostgreSQL Notes — https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes

**Media Storage**
- Cloudinary Documentation — https://cloudinary.com/documentation
- Cloudinary Python SDK — https://cloudinary.com/documentation/django_integration
- Cloudinary Image Upload Documentation — https://cloudinary.com/documentation/image_upload_api_reference

**Deployment**
- WhiteNoise Documentation — https://whitenoise.readthedocs.io/en/latest/
- Gunicorn Documentation — https://docs.gunicorn.org/
- Render Documentation — https://render.com/docs

**API**
- Currents API Documentation — https://currentsapi.services/en/docs/
- Requests Documentation — https://requests.readthedocs.io/

**Tools**
- Git Documentation — https://git-scm.com/doc
- GitHub Documentation — https://docs.github.com/