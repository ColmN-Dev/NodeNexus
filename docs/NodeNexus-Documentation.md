# NodeNexus Documentation

**Last updated:** July 28, 2026

---

# Table of Contents

1. [Overview](#1-overview)
2. [Project Development Summary](#2-project-development-summary)
   - Initial Project Setup
   - Migration From SQLite to PostgreSQL
   - Static Files and Deployment Setup
   - Django Framework Implementation

3. [Current Architecture](#3-current-architecture)
   - Django Project Structure
   - Settings Configuration
   - URL Routing
   - Template System
   - Static File Handling
   - Deployment Architecture

4. [Current Folder Structure](#4-current-folder-structure)

5. [Frontend Implementation](#5-frontend-implementation)
   - Base Template
   - Responsive Navigation
   - Desktop Navigation
   - Mobile Hamburger Menu
   - Mobile Bottom Navigation
   - Dark Mode Toggle
   - Glass UI Design System
   - Branding and Assets

6. [Database Configuration](#6-database-configuration)
   - PostgreSQL Setup
   - Local Development Database
   - Production Database
   - Django Migrations

7. [Django Features Implemented](#7-django-features-implemented)
   - Django Project Configuration
   - Template Inheritance
   - Static Files Management
   - Authentication Foundation
   - Environment Configuration

8. [Completed Features](#8-completed-features)

9. [Current Limitations](#9-current-limitations)

10. [Key Design Decisions](#10-key-design-decisions)
   - Why Django
   - Why PostgreSQL
   - Why Server-Side Rendering
   - Frontend Design Choices

11. [Static Files and Deployment](#11-static-files-and-deployment)
   - STATIC_URL Configuration
   - STATIC_ROOT Configuration
   - collectstatic Process
   - Render Deployment

12. [Responsive Design System](#12-responsive-design-system)
   - Desktop Layout
   - Tablet Layout
   - Mobile Layout
   - Breakpoint Strategy

13. [Branding and Metadata](#13-branding-and-metadata)
   - Logo Implementation
   - Favicon Setup
   - Web Manifest
   - Open Graph Assets

14. [Challenges Faced and Solutions](#14-challenges-faced-and-solutions)

15. [What Was Learned So Far](#15-what-was-learned-so-far)

16. [Testing and Quality Assurance](#16-testing-and-quality-assurance)

17. [Deployment Workflow](#17-deployment-workflow)

18. [Continuous Integration](#18-continuous-integration)

19. [Reflection](#19-reflection)

20. [References](#20-references)

---

# 1. Overview

NodeNexus is a technology intelligence hub built using the Django framework.

The project is designed to provide developers and technology enthusiasts with a central platform for discovering technology news, articles, and updates.

The application uses Django for backend development, PostgreSQL for database management, and a custom responsive frontend built with HTML, CSS, JavaScript, and Bootstrap.

The current development phase focuses on establishing the core Django architecture, frontend design system, responsive navigation, static asset management, and deployment workflow.

---

# 2. Project Development Summary

## Initial Project Setup

NodeNexus was created as a Django-based web application following the standard Django project structure.

The initial setup included:

- Creating the Django project.
- Creating the virtual environment.
- Installing required dependencies.
- Configuring Django settings.
- Preparing the project for PostgreSQL integration.

The project structure was created with future expansion in mind, including authentication, user profiles, article management, and external API integration.

---

## Migration to PostgreSQL

The default SQLite database configuration was replaced with PostgreSQL to provide a more production-ready database environment.

Changes included:

- Installing PostgreSQL dependencies.
- Configuring database connection settings.
- Using environment variables for database credentials.
- Running Django migrations.
- Connecting the project to PostgreSQL locally and on Render.

---

## Django Framework Implementation

NodeNexus uses Django's built-in framework features including:

- URL routing.
- Template inheritance.
- Static file management.
- Settings configuration.
- Database migrations.
- Development and production deployment workflows.

A reusable base template was created to provide shared layout components across pages.

---

# 3. Current Architecture

## Django Project Structure

NodeNexus follows the standard Django architecture pattern.

The project separates configuration, templates, and static assets to maintain a clear development structure.

The main components include:

- Django project configuration.
- URL routing.
- HTML templates.
- Static CSS, JavaScript, and image assets.
- Database configuration.
- Deployment configuration.

This structure allows the application to be expanded with additional features while keeping the codebase organised.

---

## Settings Configuration

The Django settings file was configured for development and production requirements.

Implemented configuration includes:

- PostgreSQL database connection.
- Static file handling.
- Template directory configuration.
- Environment variable support.
- Deployment settings.

Static file configuration:

```python
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"
```

---

## URL Routing

Django URL routing was configured using the project-level `urls.py` file.

The URL configuration acts as the connection point between incoming browser requests and the relevant Django views.

Current routing setup includes:

- Project-level URL management.
- Inclusion of application routes.
- Static file serving during development.
- Future expansion for authentication and content-based pages.

Example structure:

```python
urlpatterns = [
    path("", include("main.urls")),
]
```

The routing system allows NodeNexus features to be separated into individual Django applications as the project grows.

Template System

NodeNexus uses Django's template inheritance system to create reusable layouts.

A central `base.html` template provides shared components including:

- Navigation bar.
- Mobile navigation.
- Footer.
- External stylesheet loading.
- JavaScript loading.
- Metadata configuration.

Individual pages extend the base template instead of duplicating common HTML structures.

Example:

```HTML
{% extends "base.html" %}

{% block content %}

Page content goes here.

{% endblock %}
```

This keeps templates maintainable and ensures consistent styling across the application.

---

## Static File Handling

Static files are managed using Django's built-in staticfiles framework.

The project separates development static assets from collected production assets.

Static files include:

- CSS stylesheets.
- JavaScript files.
- Logos.
- Background images.
- Theme icons.
- Favicons.
- Web manifest files.

Development assets are stored in:

```text
static/
```

During deployment, Django collects these files into:

```text
staticfiles/
```

Which I used:

```Bash
python manage.py collectstatic
```

This was used to generate the staticfiles folder.

---

## Deployment Architecture

The project is configured for deployment on Render using Django's production deployment workflow.

The deployment architecture consists of:

- Render Web Service hosting the Django application.
- PostgreSQL database hosted on Render.
- Gunicorn as the production WSGI server.
- Environment variables for sensitive configuration values.
- Static files collected using Django's `collectstatic` command.
- GitHub integration for automatic deployments after pushing to the main branch.

This deployment setup closely mirrors a real-world production environment while remaining simple enough for development and future expansion.

---

# 4. Current Folder Structure

NodeNexus follows a structured Django project layout separating application logic, configuration, templates, static assets, documentation, and deployment files.

```text
NodeNexus/
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│
├── staticfiles/
│
├── docs/
│   ├── images/
│   ├── NodeNexus-Documentation.md
│   ├── node_nexus_erd.dbml
│   └── planning.md
│
├── manage.py
├── requirements.txt
├── Procfile
├── .python-version
├── .env
├── .gitignore
└── README.md
```

The project structure separates Django configuration (`config`), application functionality (`core`), frontend templates, static resources, and technical documentation. The `docs` directory contains project planning materials, database design files, and documentation resources used throughout development.

The project also includes deployment configuration files such as `Procfile` and `.python-version` to support production deployment on Render.

---

# 5. 

