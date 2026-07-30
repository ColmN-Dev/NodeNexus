# NodeNexus Documentation

**Last updated:** July 28, 2026

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
   - React Preparation
   - Asset Organisation
   - Template Structure
   - Responsive Design System
   - Branding and Assets

6. [Database Configuration](#6-database-configuration)
   - PostgreSQL Setup
   - Development Database
   - Production Database
   - Django Migrations

7. [Django Features Implemented](#7-django-features-implemented)
   - Django Project Configuration
   - URL Routing
   - Static File Management
   - Environment Configuration
   - Backend Foundation

8. [Completed Features](#8-completed-features)

9. [Current Limitations](#9-current-limitations)

10. [Key Design Decisions](#10-key-design-decisions)
   - Why Django
   - Why PostgreSQL
   - Why Frontend Separation
   - Frontend Design Choices

11. [Deployment](#11-deployment)
   - Static Files Configuration
   - collectstatic Process
   - Gunicorn Configuration
   - Render Deployment

12. [Challenges Faced and Solutions](#12-challenges-faced-and-solutions)

13. [What Was Learned So Far](#13-what-was-learned-so-far)

14. [Next Steps](#14-next-steps)

15. [References](#15-references)

---

# 1. Overview

NodeNexus is a technology intelligence hub built using the Django framework.

The project is designed as a platform for discovering technology news and content across areas including artificial intelligence, cybersecurity, gaming, and trending technology topics.

The application currently uses Django for backend development, PostgreSQL for database management, and Django templates with custom CSS and JavaScript for the frontend.

The current development phase focuses on establishing the Django project structure, database integration, responsive frontend design, static asset management, and deployment workflow.

The project architecture has been organised to allow future expansion into a larger full-stack application with additional features and a possible React frontend.

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

The project was structured with future expansion in mind, including authentication, article management, API integration, and additional user functionality.

---

## Migration to PostgreSQL

The default SQLite database configuration was replaced with PostgreSQL to provide a more production-ready database environment.

Changes included:

- Installing PostgreSQL dependencies.
- Configuring Django database settings.
- Using environment variables for database credentials.
- Running Django migrations.
- Preparing the project for local and production database usage.

---

## Project Structure Reorganisation

The project structure was reorganised to improve separation between backend functionality and frontend resources.

Changes included:

- Moving Django project files into the backend directory.
- Organising frontend templates and assets separately.
- Creating dedicated locations for static files.
- Preparing the project structure for future React development.

This organisation improves maintainability while allowing future frontend expansion.

---

## Django Framework Implementation

NodeNexus uses Django framework features including:

- URL routing.
- Template rendering.
- Settings configuration.
- Static file management.
- Database migrations.
- Development and production deployment configuration.

The Django backend provides the foundation for future features including authentication, article management, and external API integration.

---

# 3. Current Architecture

## Backend Structure

NodeNexus currently uses Django as the backend framework.

The backend is responsible for:

- Django project configuration.
- URL routing.
- Database communication.
- Application logic.
- Future API development.

The Django project is contained inside the backend directory to separate server-side functionality from frontend resources.

---

## Settings Configuration

The Django settings file has been configured for development and deployment requirements.

Current configuration includes:

- PostgreSQL database integration.
- Environment variable support.
- Static file configuration.
- Allowed hosts configuration.
- Deployment settings.

Sensitive configuration values are stored using environment variables rather than being directly stored in the source code.

---

## URL Routing

Django URL routing is managed through the project-level `urls.py` configuration.

The routing system connects incoming browser requests to the appropriate Django views.

Current routing provides the foundation for future expansion including:

- Authentication routes.
- Article pages.
- API endpoints.
- User functionality.

---

## Template Structure

NodeNexus currently uses Django template inheritance.

A reusable `base.html` template provides shared components including:

- Navigation.
- Footer.
- Metadata.
- Static file loading.
- JavaScript loading.
- Theme functionality.

Individual pages extend the base template instead of duplicating common HTML structures.

---

## Static Asset Management

Static files are managed using Django's built-in staticfiles system.

Current assets include:

- CSS stylesheets.
- JavaScript files.
- Images.
- Logos.
- Branding assets.

The project uses Django static configuration to collect assets for production deployment.

---

## Deployment Architecture

NodeNexus is configured for deployment using Render.

The deployment setup includes:

- Render Web Service hosting the Django application.
- PostgreSQL database integration.
- Gunicorn as the production WSGI server.
- Environment variables for configuration.
- GitHub-based deployment workflow.

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
│   ├── staticfiles/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── assets/
│       │   ├── css/
│       │   ├── js/
│       │   └── images/
│       │
│       ├── components/
│       └── pages/
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

- Django backend functionality.
- Frontend resources.
- Documentation and planning files.
- Deployment configuration.

The backend directory contains Django configuration and application files, while frontend resources are organised separately for future expansion.

---