# NodeNexus Documentation

**Last updated:** July 28, 2026

---

# Table of Contents

1. [Overview](#1-overview)

2. [Project Development Summary](#2-project-development-summary)
   - Initial Project Setup
   - Migration From SQLite to PostgreSQL
   - Frontend and Backend Separation
   - Django Framework Implementation

3. [Current Architecture](#3-current-architecture)
   - Backend Structure
   - Settings Configuration
   - URL Routing
   - Frontend Architecture
   - Static Asset Management
   - Deployment Architecture

4. [Current Folder Structure](#4-current-folder-structure)

5. [Frontend Implementation](#5-frontend-implementation)
   - React Preparation
   - Asset Organisation
   - Component Structure
   - Page Structure
   - Responsive Design System
   - Branding and Assets

6. [Database Configuration](#6-database-configuration)
   - PostgreSQL Setup
   - Local Development Database
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

NodeNexus is a technology intelligence hub built using Django as the backend framework.

The project is designed to provide developers and technology enthusiasts with a central platform for discovering technology news, articles, and updates.

The application uses Django for backend development, PostgreSQL for database management, and a separated frontend architecture prepared for future React implementation.

The current development phase focuses on establishing the Django backend architecture, database integration, frontend separation, asset organisation, responsive design system, and deployment workflow.

The project structure separates backend responsibilities from frontend development to allow future expansion into a full-stack application with a dedicated React frontend communicating with Django services.

---

# 2. Project Development Summary

## Initial Project Setup

NodeNexus was created as a Django-based web application following Django's standard project structure.

The initial setup included:

- Creating the Django project.
- Creating the virtual environment.
- Installing required dependencies.
- Configuring Django settings.
- Preparing the project for PostgreSQL integration.
- Creating the initial frontend structure.

The project structure was created with future expansion in mind, including authentication, user profiles, article management, external API integration, and a dedicated frontend application.

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

## Frontend and Backend Separation

The project architecture was reorganised to separate backend and frontend responsibilities.

The Django backend was moved into its own directory:

- Django configuration.
- Application logic.
- Database handling.
- Backend services.

A dedicated frontend structure was created to prepare for future React development:

- Frontend assets.
- Page structure.
- Reusable components.
- Client-side functionality.

This separation allows NodeNexus to transition towards a modern full-stack architecture while keeping Django responsible for backend functionality.

---

## Django Framework Implementation

NodeNexus uses Django's built-in framework features including:

- URL routing.
- Settings configuration.
- Static file management.
- Database migrations.
- Development and production deployment workflows.

The Django backend provides the foundation for future features including authentication, API endpoints, article management, and user functionality.

---

# 3. Current Architecture

## Backend Structure

NodeNexus uses a separated backend and frontend architecture.

The backend is built using Django and is responsible for:

- Project configuration.
- URL routing.
- Database communication.
- Application logic.
- Future API development.
- Authentication and user management.

The Django backend is contained inside the backend directory to keep server-side functionality separate from frontend development.

---

## Settings Configuration

The Django settings file is configured for development and production requirements.

Current configuration includes:

- PostgreSQL database integration.
- Environment variable support.
- Static file configuration.
- Deployment settings.
- Allowed hosts configuration.

Sensitive values such as database credentials and API keys are stored using environment variables.

---

## URL Routing

Django URL routing is managed through the project-level urls.py file.

The URL configuration acts as the connection between incoming requests and backend functionality.

The routing system will allow NodeNexus to expand with additional features including:

- Authentication routes.
- Article management.
- API endpoints.
- User functionality.

---

## Frontend Architecture

The frontend structure has been separated from the Django backend to prepare for future React implementation.

The frontend directory contains:

- Page structures.
- Reusable components.
- Static assets.
- Client-side functionality.

This separation allows the frontend and backend to be developed independently while communicating through future API endpoints.

---

## Static Asset Management

Frontend assets are organised separately from Django backend files.

Current frontend assets include:

- CSS files.
- JavaScript files.
- Images.
- Branding assets.

Django's staticfiles system remains responsible for collecting and serving production static resources during deployment.

---

## Deployment Architecture

NodeNexus is configured for deployment using Render.

The deployment architecture consists of:

- Render Web Service hosting the Django application.
- PostgreSQL database integration.
- Gunicorn as the production WSGI server.
- Environment variables for configuration.
- GitHub integration for deployment workflow.

The project structure is organised to support future expansion into a full-stack application with a dedicated frontend and Django backend.

---

# 4. Current Folder Structure

NodeNexus follows a separated backend and frontend project structure.

The backend contains Django configuration, application logic, database configuration, and deployment requirements.

The frontend directory has been created to organise client-side development and prepare for future React implementation.

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
- Frontend development resources.
- Documentation and planning files.
- Deployment configuration.

The backend directory contains the Django project and application files, while the frontend directory contains assets and future client-side components.

The docs directory contains technical documentation, database planning files, and project design resources.

Deployment files such as Procfile and .python-version remain at the repository root to support Render deployment.

---

