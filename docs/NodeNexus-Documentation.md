# NodeNexus Documentation

**Last updated:** August 4, 2026

---

# Table of Contents

1. [Overview](#1-overview)

2. [Project Development Summary](#2-project-development-summary)
   - Initial Project Setup
   - Migration From SQLite to PostgreSQL
   - Project Structure Reorganisation
   - Django Framework Implementation

3. [Current Architecture](#3-current-architecture)
   - Backend Structure
   - Settings Configuration
   - URL Routing
   - Template Structure
   - Static Asset Management
   - Deployment Architecture

4. [Current Folder Structure](#4-current-folder-structure)

5. [Frontend Implementation](#5-frontend-implementation)
   - Django Templates
   - Bootstrap Layout System
   - Reusable Components
   - Responsive Design
   - Custom CSS and Theme System
   - JavaScript Functionality

6. [Database Configuration](#6-database-configuration)
   - PostgreSQL Setup
   - Development Database
   - Production Database
   - Django ORM and Migrations

7. [Django Features Implemented](#7-django-features-implemented)
   - Project Configuration
   - URL Routing
   - Template Rendering
   - Static File Management
   - Environment Configuration
   - Application Structure

8. [Completed Features](#8-completed-features)
   - News Aggregation
   - Search Functionality
   - Search Autocomplete
   - Content Quality Filtering
   - Pagination
   - Frontend Interface
   - API Reliability Features
   - Development Foundation

9. [Current Limitations](#9-current-limitations)

10. [Key Design Decisions](#10-key-design-decisions)
   - Why Django
   - Why PostgreSQL
   - Why Frontend Separation
   - Why Bootstrap and Custom CSS
   - Service Layer Design

11. [Deployment](#11-deployment)
   - Production Settings
   - WhiteNoise Configuration
   - collectstatic Process
   - Gunicorn Configuration
   - Render Deployment

12. [Challenges Faced and Solutions](#12-challenges-faced-and-solutions)
   - Frontend Layout and Bootstrap Integration
   - Responsive Design Challenges
   - Static Files, collectstatic, and CSS Caching
   - External API Integration
   - API Usage and Caching
   - Search System Development
   - Autocomplete Race Conditions
   - CSS Stacking Context Issues
   - Pagination Implementation
   - Deployment Configuration
   - Project Structure and Code Organisation

13. [What Was Learned So Far](#13-what-was-learned-so-far)

14. [Next Steps](#14-next-steps)

15. [References](#15-references)

---

# 1. Overview

NodeNexus is a technology intelligence hub built using the Django framework.

The project is designed as a platform for discovering technology news and content across areas including artificial intelligence, cybersecurity, gaming, and trending technology topics. News content is retrieved from external APIs and presented through a responsive, category-based interface.

The application currently uses Django for backend development, PostgreSQL for database management, and Django Templates with Bootstrap, custom CSS, and JavaScript for the frontend.

The current development phase focuses on establishing the Django project structure, database integration, API integration, responsive frontend design, static asset management, and deployment workflow.

The project architecture has been organised to allow future expansion into a larger full-stack application with features including user authentication, personalised article bookmarking, user profiles, and a future React frontend.

---

# 2. Project Development Summary

## Initial Project Setup

NodeNexus was created as a Django-based web application.

The initial setup included:

- Creating the Django project.
- Creating the virtual environment.
- Installing required dependencies.
- Configuring Django settings.
- Preparing PostgreSQL integration.
- Creating the initial application structure.
- Creating the frontend templates and static asset structure.
- Setting up Git version control and GitHub.
- Preparing the project for deployment on Render.

The project was structured with future expansion in mind, including authentication, article management, external API integration, user profiles, bookmarking functionality, and a future React frontend.

---

## Migration to PostgreSQL

The default SQLite database configuration was replaced with PostgreSQL to provide a more production-ready database environment.

Changes included:

- Installing PostgreSQL dependencies.
- Configuring Django database settings.
- Using environment variables for database credentials.
- Running Django migrations.
- Preparing the project for local and production database usage.

At the current stage, PostgreSQL has been successfully configured and connected to the application, with the database prepared for future model implementation as additional features are developed.

---

## Project Structure Reorganisation

The project structure was reorganised to improve separation between backend functionality and frontend resources.

Changes included:

- Moving Django project files into the backend directory.
- Organising frontend templates and assets separately.
- Creating dedicated locations for static files.
- Preparing the project structure for future React development.

This organisation improves maintainability by separating server-side logic from presentation assets while also providing a smoother transition to a future React frontend.

---

## Django Framework Implementation

NodeNexus currently uses several core Django framework features including:

- URL routing.
- View rendering.
- Template inheritance.
- Settings configuration.
- Static file management.
- Database migrations.
- Development and production deployment configuration.

The Django backend provides the foundation for future features including authentication, article management, external API integration, bookmarking functionality, and personalised user features.

---

# 3. Current Architecture

## Backend Structure

NodeNexus currently uses Django as the backend framework.

The backend is responsible for:

- Django project configuration.
- URL routing.
- Database communication.
- Application logic.
- API development.

The Django project is contained inside the backend directory to separate server-side functionality from frontend resources.

---

## Settings Configuration

The Django settings file has been configured for both development and deployment requirements.

Current configuration includes:

- PostgreSQL database integration.
- Environment variable support using `.env`.
- Static file configuration.
- Allowed hosts configuration.
- Deployment settings for Render.
- Environment-based DEBUG configuration.

Sensitive configuration values such as secret keys, database credentials, API keys, and debug settings are stored using environment variables rather than directly within the source code.

The application uses different static file behaviour depending on the environment. During development, Django handles static files normally while `DEBUG=True`. In production, when `DEBUG=False`, WhiteNoise middleware is enabled and Django uses compressed manifest static file storage to improve performance and provide cache-safe static asset versioning.

---

## URL Routing

Django URL routing is managed through the project-level `urls.py` configuration.

The routing system connects incoming browser requests to the appropriate Django views.

Current routes include:

- Homepage
- AI
- Cybersecurity
- Gaming
- Trending
- Search Results

The routing structure has been designed to support future expansion including authentication routes, user profiles, bookmarking functionality, and additional API endpoints.

---

## Template Structure

NodeNexus uses Django template inheritance combined with reusable template partials.

A reusable `base.html` template provides the shared site structure, including:

- Navigation.
- Footer.
- Metadata.
- Static file loading.
- JavaScript loading.
- Theme functionality.
- Bootstrap CSS and JavaScript.

Individual pages extend the `base.html` template instead of duplicating common HTML structures. Shared UI elements are organised as reusable template components within the `components/` directory and included where required.

Reusable components include the hero section, search bar, article cards, navbar, footer, and mobile navigation. This structure improves maintainability by allowing shared interface elements to be updated from a single location.

---

## Static Asset Management

Static files are managed using Django's built-in `staticfiles` framework alongside Bootstrap and custom frontend assets.

Current assets include:

- CSS stylesheets.
- JavaScript files.
- Images.
- Logos.
- Branding assets.

During development, static files are served using Django's development static file handling.

For production deployment, the project enables WhiteNoise when `DEBUG=False`. Django runs the `collectstatic` process to gather frontend assets, and `CompressedManifestStaticFilesStorage` generates versioned filenames for improved caching behaviour and reliable updates after deployment.

The main custom stylesheet controls the application's glass UI, theme variables, homepage hero section, responsive navigation, article cards, typography, and overall branding, while Bootstrap provides the responsive grid system and base components.

---

## Deployment Architecture

NodeNexus is configured for deployment using Render.

The deployment setup includes:

- Render Web Service hosting the Django application.
- PostgreSQL database integration.
- Gunicorn as the production WSGI server.
- WhiteNoise for serving static files.
- Environment variables for configuration.
- Django's `collectstatic` process during deployment.
- GitHub-based continuous deployment workflow.

---

# 4. Current Folder Structure

NodeNexus follows a separated backend and frontend structure.

Current project structure:

```text
NodeNexus/
│
├── backend/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── core/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── news/
│   │   ├── migrations/
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── cache.py
│   │   │   └── currents.py
│   │   │
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   │
│   ├── staticfiles/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── article_card.html
│       │   ├── category_section.html
│       │   ├── footer.html
│       │   ├── mobile_nav.html
│       │   ├── navbar.html
│       │   └── search_bar.html
│       │
│       ├── pages/
│       │   ├── ai.html
│       │   ├── base.html
│       │   ├── cybersecurity.html
│       │   ├── gaming.html
│       │   ├── index.html
│       │   ├── search_results.html
│       │   └── trending.html
│       │
│       └── static/
│           ├── css/
│           ├── images/
│           └── js/
│
├── docs/
│   ├── images/
│   ├── NodeNexus-Documentation.md
│   ├── node_nexus_erd.dbml
│   └── planning.md
│
├── Procfile
├── .python-version
├── .gitignore
└── README.md
```

The project structure separates:

- Django project configuration.
- Core application functionality.
- News functionality and external API integrations.
- Frontend templates and static resources.
- Documentation and planning files.
- Deployment configuration.

The `core` application provides the foundation for general site functionality, while the `news` application manages technology news features and category-based content.

The `news/services` package separates external API communication and supporting logic from Django views:

- `currents.py` handles communication with the Currents API and processes external news data.
- `cache.py` provides caching functionality to reduce unnecessary external API requests and improve reliability.

This separation keeps Django views focused on handling requests and rendering responses while allowing API integrations and utility logic to be maintained independently.

The frontend directory currently organises Django template resources and static assets separately from backend logic. This structure also prepares the project for a future React frontend migration while allowing Django Templates to remain the current presentation layer.

---

# 5. Frontend Implementation

NodeNexus uses Django Templates as the current presentation layer, with Bootstrap providing the responsive grid system, layout utilities, and base component structure.

Custom CSS and JavaScript are used alongside Bootstrap to create the NodeNexus visual identity, interactive elements, and responsive behaviour.

Current frontend implementation includes:

- A shared `base.html` layout extended by all pages.
- Reusable template components for navigation, footer, search, article cards, and category sections.
- A homepage hero section containing the project branding, description, and search functionality.
- Category pages for AI, cybersecurity, gaming, and trending technology content.
- A search results page displaying matching articles using shared article card components.
- Bootstrap-powered article layouts with responsive behaviour across desktop, tablet, and mobile devices.
- A custom glass UI design system for cards, navigation, search components, and content sections.
- A deep-space background theme with cyan technology-inspired accents.
- Dark/light theme support using custom CSS variables.
- Mobile navigation using a bottom navigation bar and an off-canvas menu system.
- Responsive horizontal article carousels were added for smaller screen sizes on homepage category sections, allowing users to horizontally scroll through category articles on tablet and mobile devices while maintaining the desktop grid layout.

The frontend combines Bootstrap's layout system with custom styling. Bootstrap handles general spacing, grid behaviour, and responsive utilities, while custom CSS controls the NodeNexus branding, component styling, and theme appearance.

Responsive behaviour is handled through a combination of Bootstrap utilities and custom CSS media queries. The responsive system supports desktop, tablet, and mobile layouts while maintaining consistent spacing, navigation behaviour, and content presentation.

The frontend structure uses reusable components and shared layouts to reduce duplication between pages. Article cards, category sections, navigation elements, and search components are reused across different views to maintain consistency.

The frontend resources are organised separately from backend logic, allowing the current Django Template implementation to remain maintainable while preparing the project for a future React frontend migration.

---

# 6. Database Configuration

NodeNexus uses PostgreSQL as the primary database system.

PostgreSQL was selected to provide a production-ready relational database environment and to support future expansion of the application.

## PostgreSQL Setup

The project was migrated from Django's default SQLite database to PostgreSQL.

Configuration includes:

- PostgreSQL database integration through Django settings.
- Environment variables for database credentials.
- Database connection management through Django ORM.
- Separate development and production database configuration.

Sensitive database information is stored outside the source code using environment variables.

---

## Development Database

During development, NodeNexus uses a local PostgreSQL database for testing and building application functionality.

The development environment allows:

- Running Django migrations.
- Testing database connections.
- Developing models and application logic.
- Verifying backend functionality before deployment.

---

## Production Database

The production environment uses PostgreSQL hosted through Render.

The deployed application connects to the production database using environment variables configured through the hosting platform.

This keeps database credentials secure while allowing the same Django configuration structure to be used across development and production environments.

---

## Django Migrations

Django migrations are used to manage database schema changes.

Current migration workflow includes:

- Creating migrations when models are updated.
- Applying migrations through Django management commands.
- Keeping database structure synchronised with application changes.

The current database foundation is prepared for future NodeNexus features including articles, categories, user profiles, bookmarks, and other application models.

---

# 7. Django Features Implemented

NodeNexus currently uses Django features to provide the application foundation and connect backend functionality with the frontend presentation layer.

## Django Application Structure

The project is organised using separate Django applications:

- `core` handles general site functionality.
- `news` handles technology news features and external API integration.

This separation keeps different areas of functionality organised into independent Django applications.

---

## Django Views

Django views handle incoming requests and prepare data before rendering templates.

Current views provide:

- Homepage content.
- Technology category pages.
- Search functionality.
- News data processing through service modules.

The views remain focused on handling requests and responses, while external API communication and utility logic are separated into the `services` package.

---

## News Service Integration

The `news` application contains service modules responsible for external data processing.

Current services include:

- Currents API integration.
- API response handling.
- Caching functionality.

This allows external API logic to remain separate from Django views and improves maintainability.

---

## Template Rendering

Django's template engine is used to render dynamic pages.

Implemented features include:

- Passing backend data into templates.
- Rendering category-specific content.
- Reusing shared template components.
- Displaying API-generated article data through the frontend.

---

# 8. Completed Features

The current NodeNexus implementation includes the following completed features:

## News Aggregation

- Integration with the Currents API for retrieving technology news content.
- Processing of external API responses into a consistent article format.
- Category-based news sections for:
  - Artificial Intelligence.
  - Cybersecurity.
  - Gaming.
  - Trending technology.

---

## Search Functionality

- Global search functionality available from the main interface.
- Search results page displaying matching articles.
- Reusable article cards used for displaying search results.

---

## Search Autocomplete

- Live search suggestions implemented through a dedicated `auto_complete` endpoint, returning matching article titles as JSON.
- Debounced input handling to reduce unnecessary requests while typing.
- A stale-response guard was added to discard out-of-order API replies, preventing earlier partial queries from overwriting more recent search results.
- Category pages (AI, Cybersecurity, Gaming, Trending) now render live articles fetched directly from the Currents API, replacing the previous placeholder templates.

---

## Content Quality Filtering

- Low-quality and duplicate articles are filtered from API results before display.
- A domain exclusion list removes known low-value sources such as forum
  threads and raw vulnerability database dumps.
- Articles with titles that are auto-generated CVE announcements are
  filtered out, while genuine journalism that references a CVE number
  within a proper headline is retained.

---

## Pagination

- Custom pagination system implemented to handle article results returned
  from external news APIs across the AI, Cybersecurity, Gaming, Trending,
  and Search Results pages.
- Pagination controls display the current page with previous and next
  navigation, rather than a fully numbered page list, reflecting the
  Currents API's lack of a reliable indicator for whether further pages
  of results exist.
- `currents.py` was updated to support page-based API requests and return
  `has_next` pagination information, alongside the existing filtering,
  deduplication, and caching logic.
- `core/views.py` and `news/views.py` were updated to retrieve the
  requested page, validate page requests, and redirect users to the last
  valid page when an unavailable page is requested.
- Pagination templates preserve the active search query when navigating
  between search result pages.
- Pagination styling was added to `style.css`, including navigation
  buttons, active page indicators, hover states, and responsive behaviour
  consistent with the NodeNexus theme.

---

## Frontend Interface

- Responsive homepage layout.
- Category pages for different technology topics.
- Fallback placeholder image displayed when article images are missing or fail to load.
- Reusable template components.
- Article card components.
- Search bar component.
- Navigation components.
- Mobile navigation system.
- Active page indication on the mobile bottom navigation bar, based on the currently matched URL route
- Dark/light theme support.
- Glass-style UI design.

---

## API Reliability Features

- API response caching implemented to reduce unnecessary external requests.
- Dedicated service layer created for external API communication.
- External API data processing separated from Django views.

---

## Development Foundation

- Django project configured with environment-based settings.
- PostgreSQL integration completed.
- Render deployment configuration prepared.
- Production static file handling configured using WhiteNoise.

---

# 9. Current Limitations

The current NodeNexus implementation provides the core foundation for a technology news platform; however, some areas may require further refinement as development continues.

## External API Dependency

The application currently relies on external APIs for retrieving news content.

Potential challenges include:

- API availability and response reliability.
- Changes to external API structures.
- Rate limits and request restrictions.
- Ensuring consistent article formatting when processing external data.

The service layer and caching system reduce dependency issues, but external data sources remain outside of direct application control.

---

## Article Data Processing

External news data may vary between sources and requires normalisation before being displayed.

Potential improvements include:

- More advanced duplicate detection.
- Better handling of missing article fields.
- Improved filtering of low-quality or irrelevant content.

---

## Responsive Frontend Refinement

The frontend currently supports desktop, tablet, and mobile layouts; however, maintaining consistent behaviour across different screen sizes requires ongoing testing.

Potential challenges include:

- Bootstrap component interactions with custom CSS.
- Managing complex responsive layouts.
- Preventing styling conflicts between framework utilities and custom designs.

---

## Frontend and Backend Scaling

The current Django Template architecture provides a maintainable foundation, but larger application growth may require additional architectural changes.

Potential considerations include:

- Increasing separation between frontend and backend logic.
- Optimising API requests as content volume increases.
- Maintaining reusable components as more features are introduced.

---

## Static Asset Management

Production static file handling is configured using Django staticfiles and WhiteNoise, but deployment environments require careful management of asset updates.

Potential challenges include:

- Ensuring updated CSS and JavaScript files are correctly collected during deployment.
- Avoiding stale cached assets after changes.
- Maintaining reliable static file versioning.

---

# 10. Key Design Decisions

## Why Django

Django was selected as the backend framework because it provides a structured development environment with built-in features including URL routing, template rendering, authentication support, security features, and database management through the Django ORM.

Using Django allows NodeNexus to be developed with a clear separation between backend logic, database functionality, and frontend presentation while providing a strong foundation for future expansion.

---

## Why PostgreSQL

PostgreSQL was selected instead of Django's default SQLite database because it provides a more production-ready relational database system.

PostgreSQL offers better scalability, reliability, and support for future application features including user accounts, article storage, bookmarks, comments, and personalised content.

---

## Why Frontend Separation

Frontend resources are organised separately from backend functionality to improve maintainability and project structure.

The current application uses Django Templates as the presentation layer, while frontend assets are organised independently to allow future migration to React without requiring a complete project restructure.

This approach keeps backend logic, templates, styling, and JavaScript responsibilities separated.

---

## Frontend Design Choices

NodeNexus uses a technology-focused visual identity based around a deep-space theme with cyan accents and glass-style interface elements.

The design choices include:

- A responsive layout system supporting desktop, tablet, and mobile devices.
- Reusable UI components to maintain consistency across pages.
- Bootstrap for responsive layout utilities and component structure.
- Custom CSS for branding, themes, animations, and unique interface styling.
- JavaScript for interactive frontend behaviour such as theme switching and navigation features.

The frontend design aims to create a modern developer-focused interface while maintaining usability and consistency across the application.

---

# 11. Deployment

NodeNexus is configured for deployment using Render as the hosting platform.

The deployment architecture includes:

- Render Web Service hosting the Django application.
- PostgreSQL database hosted through Render.
- Gunicorn as the production WSGI server.
- WhiteNoise for production static file serving.
- Environment variables for production configuration.
- GitHub integration for deployment updates.

---

## Static Files Configuration

Static files are managed using Django's staticfiles framework.

During development, Django serves static assets normally through the development server.

For production deployment:

- `DEBUG=False` enables production static file handling.
- WhiteNoise middleware serves collected static files.
- `CompressedManifestStaticFilesStorage` creates versioned static filenames to improve caching and asset reliability.

---

## collectstatic Process

The Django `collectstatic` command is used during deployment to gather all static assets into the production static directory.

This process collects:

- Custom CSS files.
- JavaScript files.
- Images.
- Branding assets.
- Third-party static resources.

A key deployment consideration was understanding how static file caching affects updates. Changes to CSS and frontend assets may not appear immediately if previous cached versions are still being served. Updating the collected static files and ensuring new manifest versions are generated resolves these issues.

---

## Gunicorn Configuration

Gunicorn is used as the production WSGI server to run the Django application.

The deployment configuration uses:

- Django WSGI application entry point.
- Gunicorn worker process management.
- Render start commands for production execution.

---

## Render Deployment Workflow

The deployment workflow follows:

1. Code changes are pushed to GitHub.
2. Render detects repository updates.
3. Dependencies are installed from `requirements.txt`.
4. Django collects static files using `collectstatic`.
5. Gunicorn starts the Django application.
6. The application connects to the production PostgreSQL database.

Environment variables are configured through Render to provide:

- Django secret key.
- Database credentials.
- API keys.
- Production configuration values.

This deployment structure provides a production-ready workflow while maintaining separate development and production environments.

---

# 12. Challenges Faced and Solutions

During the development of NodeNexus, several technical challenges were encountered across backend development, frontend implementation, static file management, API integration, and deployment.

---

## Frontend Layout and Bootstrap Integration

One of the main frontend challenges was balancing Bootstrap's built-in layout system with custom CSS styling.

Bootstrap provided useful responsive utilities and grid functionality, but some default behaviours conflicted with the custom NodeNexus design system. This required adjustments to:

- Container sizing.
- Grid behaviour.
- Component spacing.
- Navigation layouts.
- Card positioning.
- Responsive breakpoints.

Custom CSS media queries were introduced alongside Bootstrap utilities to provide more control over desktop, tablet, and mobile layouts.

The final approach was to use Bootstrap for general structure while allowing custom CSS to control branding, appearance, and specific component behaviour.

---

## Responsive Design Challenges

Creating a consistent experience across different screen sizes required additional testing and refinement.

Challenges included:

- Mobile navigation positioning.
- Preventing content from being hidden behind the bottom navigation bar.
- Maintaining article card layouts across screen sizes.
- Adjusting typography and spacing for smaller displays.
- Handling unusual viewport widths.

These issues were resolved through custom media queries, responsive spacing adjustments, and testing across different device sizes.

---

## Static Files, collectstatic, and CSS Caching

Static file management created challenges during development and deployment.

A major issue occurred where CSS changes appeared not to update after deployment because previously collected static files were still being served from cache.

The solution involved understanding Django's static file pipeline:

- Development static handling when `DEBUG=True`.
- Production static collection through `collectstatic`.
- WhiteNoise static file serving when `DEBUG=False`.
- Manifest-based static file versioning through `CompressedManifestStaticFilesStorage`.

This highlighted the importance of understanding how browsers, Django staticfiles, and production asset handling interact.

---

## External API Integration

Integrating external news APIs required handling differences between external data sources and the NodeNexus application structure.

Challenges included:

- Processing external API responses.
- Converting API data into a consistent article format.
- Handling missing or inconsistent data fields.
- Reducing unnecessary API requests.

The solution was creating a dedicated services layer separate from Django views.

The `news/services` package separates API communication and supporting logic:

- `currents.py` handles external API requests and data processing.
- `cache.py` manages temporary API response caching.

This keeps views focused on handling requests and rendering responses.

---

## API Usage and Caching

External APIs introduced challenges around request limits, reliability, and repeated calls.

A caching system was introduced to:

- Reduce unnecessary API requests.
- Improve response times.
- Protect API usage limits.
- Provide more reliable behaviour during repeated searches.

The caching system will continue to be refined as more API functionality is added.

---

## Search System Development

Building a unified search system required additional planning because different search queries may require different handling.

The search system required:

- Processing user search input.
- Determining the correct API pipeline.
- Normalising API responses.
- Displaying results through reusable components.

The current structure separates search-related logic from views, allowing the system to be expanded and improved.

---

## Autocomplete Race Conditions

Implementing live search suggestions introduced a race condition: multiple autocomplete requests could be in flight simultaneously as a user typed, and slower earlier requests occasionally resolved after faster, more recent ones. This caused outdated results to visually overwrite correct ones.

The solution was tracking the most recently submitted query and discarding any response that did not match it upon arrival, ensuring only the latest keystroke's results are ever rendered.

---

## CSS Stacking Context Issues

The autocomplete dropdown initially rendered behind other page sections despite having a high `z-index`. This was caused by `backdrop-filter` properties on sibling elements creating independent stacking contexts, which isolate `z-index` comparisons to within that context rather than the whole page. The fix involved explicitly establishing a stacking context on the hero section with `position: relative` and an appropriate `z-index`, allowing its contents, including the dropdown, to render above later sections.

---

## Pagination Implementation

Prior pagination experience came from a previous Flask project using the Google Books API, where the `start_index` parameter allowed simple offset-based pagination. Django's built-in `Paginator` class was used in an initial attempt at pagination for NodeNexus, alongside a similar numbered pagination system.

The Currents API had no reliable way to indicate whether a next page of results existed. `Paginator` expects a known total count to calculate page numbers, which the API could not consistently provide. This caused several issues:

- Invalid page requests returning errors instead of failing gracefully
- Empty responses on out-of-range pages
- Pagination buttons remaining active on pages with no data, letting users navigate to empty or broken pages and breaking the page layout
- Inconsistent navigation state, with next/previous controls not accurately reflecting whether further results were actually available

`Paginator` was dropped in favour of a simpler current-page indicator with previous/next navigation, deriving page availability directly from the API response rather than a known total. `currents.py` was updated to support page-based requests and expose `has_next`, while views validate requested pages and redirect to the last valid page using `HttpResponseRedirect` when an invalid or empty page is requested.

---

## Deployment Configuration

Deployment introduced challenges around configuring Django correctly for a production environment.

Issues included:

- Managing environment variables.
- Configuring allowed hosts.
- Preparing Gunicorn.
- Handling static files correctly.
- Separating development and production settings.

These were resolved by introducing environment-based configuration and separating development behaviour from production deployment requirements.

---

## Project Structure and Code Organisation

As NodeNexus expanded, maintaining a clean structure became increasingly important.

The project was reorganised to separate:

- Django configuration.
- Core application functionality.
- News and API functionality.
- Frontend templates and static resources.

Creating dedicated service modules helped prevent API logic and utility functions from becoming mixed with Django views.

---

# 13. What Was Learned So Far

Developing NodeNexus has strengthened understanding of building a full-stack Django application and the relationship between backend systems, frontend design, databases, APIs, and deployment.

Key areas learned include:

- Structuring a Django project using apps, views, templates, services, and reusable components.
- Using PostgreSQL with Django ORM and preparing applications for scalable database development.
- Integrating external APIs and separating API communication from application logic.
- Implementing caching strategies to improve API reliability and reduce unnecessary requests.
- Evaluating and moving away from Django's built-in `Paginator` when working with externally sourced, unreliable-total data, in favour of a simpler API-driven pagination approach.
- Managing static files, production configuration, and deployment workflows using Render and WhiteNoise.
- Combining Bootstrap with custom CSS to create responsive layouts and maintain a consistent design system.
- Debugging real-world issues involving frontend layouts, static assets, deployment configuration, and external services.

The project has improved understanding of building maintainable applications by focusing on separation of concerns, reusable structures, and preparing the codebase for future expansion.

---

# 14. Next Steps

The next stages of NodeNexus development will focus on completing the core application functionality and improving the overall user experience.

Planned next steps include:

- Adding article detail pages for expanded article information and user interactions.
- Implementing database models and migrations for articles, categories, users, bookmarks, and related features.
- Developing authentication and user profile functionality.
- Adding bookmarking and personalised user features.
- Expanding frontend interactivity using JavaScript.
- Testing application functionality and improving reliability.
- Preparing the project for future React frontend migration.

Development will continue incrementally, prioritising core functionality before adding additional features.

---

# 15. References

The following documentation sources were used throughout the development of NodeNexus:

## Frameworks and Backend

- Django Documentation  
  https://docs.djangoproject.com/en/6.0/

- Django Static Files Documentation  
  https://docs.djangoproject.com/en/6.0/howto/static-files/

- Django Templates Documentation  
  https://docs.djangoproject.com/en/6.0/topics/templates/

- Django Pagination Documentation  
  https://docs.djangoproject.com/en/6.0/topics/pagination/

- Django Models and Migrations Documentation  
  https://docs.djangoproject.com/en/6.0/topics/db/models/

- Django Authentication Documentation  
  https://docs.djangoproject.com/en/6.0/topics/auth/

---

## Frontend Development

- Bootstrap Documentation  
  https://getbootstrap.com/docs/

- MDN Web Documentation (HTML, CSS, JavaScript references)  
  https://developer.mozilla.org/

- CSS Media Queries Documentation  
  https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries

- JavaScript Documentation  
  https://developer.mozilla.org/en-US/docs/Web/JavaScript

---

## Database

- PostgreSQL Documentation  
  https://www.postgresql.org/docs/

- Django PostgreSQL Database Backend Documentation  
  https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes

---

## Deployment and Production Configuration

- WhiteNoise Documentation  
  https://whitenoise.readthedocs.io/en/latest/

- Gunicorn Documentation  
  https://docs.gunicorn.org/

- Render Documentation  
  https://render.com/docs

---

## API Integration

- Currents API Documentation  
  https://currentsapi.services/en/docs/

- HTTP Requests Documentation  
  https://requests.readthedocs.io/

---

## Version Control and Development Tools

- Git Documentation  
  https://git-scm.com/doc

- GitHub Documentation  
  https://docs.github.com/

---