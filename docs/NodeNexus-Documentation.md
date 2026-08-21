# NodeNexus Documentation

**Last updated:** August 21, 2026

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

The application also includes user authentication and account features, allowing users to register, log in, manage their account, manage their profile picture, save articles using bookmarks, and interact with saved articles through comments and replies.

The stack is Django, PostgreSQL, and Django Templates with Bootstrap, custom CSS, and vanilla JavaScript. The project is structured so a React frontend and DRF API layer can be added later without a rewrite, but currently all pages are plain Django templates.

Article data returned by the Currents API is initially treated as temporary API response data. Articles are only persisted in the database when a user bookmarks them, at which point an `Article` record is created and assigned a database ID. Bookmarks and comments can then reference that persistent article record.

The application is deployed on Render, with PostgreSQL used for the database and external services used for news data and user-uploaded media. Comments, nested replies, bookmarks, profiles, authentication, and article interactions are handled through Django's database and template system.

---

# 2. Project Structure

The project splits backend and frontend into separate top-level folders, so Django logic and frontend resources aren't mixed together, and so a React frontend can slot into `frontend/` later without restructuring the backend.

```text
NodeNexus/
│
├── backend/
│   ├── accounts/               # Authentication and account-related views/forms
│   ├── config/                 # Django settings, urls, wsgi/asgi
│   ├── core/                   # General site views and shared functionality
│   ├── news/                   # News, article, and bookmark functionality
│   │   └── services/
│   │       ├── currents.py     # Currents API calls + processing
│   │       ├── cache.py        # API response caching
│   │       └── articles.py     # Article creation/retrieval service logic
│   ├── staticfiles/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── components/         # Reusable template partials
│       ├── pages/              # Page templates
│       └── static/             # CSS, JavaScript, and images
│
├── docs/
├── Procfile
└── README.md
```

The core app handles general site pages and functionality. The news app handles article-related models, views, bookmarks, comments/replies and external news data. The news/services/ package keeps API, caching, and article creation logic separate from the views.

The accounts app handles user registration, authentication, profiles, password management, and profile pictures.

---

# 3. Backend

## Views and URL routing

Django views handle requests from the frontend and connect the templates to the application's backend logic.

Each category page (AI, cybersecurity, gaming, trending) and the search results page uses the relevant service functions to retrieve articles, handle pagination, and render the appropriate template.

Article detail pages can display article data returned by the external API. When an article is bookmarked, its data is stored in the database and can then be retrieved using its database ID.

URL routing is split between the main project URL configuration and the individual Django apps, keeping routes organised by responsibility.

---

## Currents API service

`currents.py` handles communication with the Currents API, including building requests, processing responses, filtering results, and returning article data in a consistent format.

The Currents API does not return a total result count, so pagination cannot use a normal "page X of Y" approach. Instead, the application checks whether another page of results is available and uses this information to control pagination.

In practice, testing showed that results are capped at five pages per query.

```python
        response = requests.get(
            BASE_URL,
            headers={
                "Authorization": API_KEY
            },
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        # Extract articles from the response
        articles = data.get(
            "news",
            []
        )
```

The service sends the request to the Currents API using the API key, query parameters, and a timeout. `raise_for_status()` ensures HTTP errors are detected before the response is processed, while `data.get("news", [])` safely extracts the returned articles.

---

## Caching

`cache.py` provides a TTL-based cache in front of Currents API requests. Repeated requests for the same query and page can therefore use cached data instead of making another external API request.

This reduces API usage and makes the application more resilient to slow or inconsistent API responses.

---

## Content filtering

Before articles are displayed, low-quality or unsuitable results are filtered out.

This includes:

- A domain exclusion list that removes known low-value sources and raw vulnerability database results.
- Filtering auto-generated CVE announcement titles while keeping genuine articles that reference CVE numbers in proper headlines.
- Removing duplicate articles from API results.

---

## Article and bookmark management

Articles returned by the Currents API are initially handled as API response data rather than being stored in the database.

When a user views an article, its data can be displayed directly from the API response. When the user chooses to bookmark an article, the relevant article data is passed to the article service.

The service checks whether the article already exists in the `Article` table. If it does not, the article is created and assigned a database ID. A `Bookmark` record is then created linking the authenticated user to that article.

This keeps the database limited to articles that users have actually saved instead of storing every article returned by the external API.

When a user removes a bookmark, the bookmark is deleted. If the article is no longer bookmarked by any user, the associated article record can also be removed so unused article records do not remain in the database.

```python
def get_or_create_article(article_data):
    article, created = Article.objects.get_or_create(
        url=article_data.get("url"),
        defaults={
            "title": article_data.get("title", ""),
            "description": article_data.get("description", ""),
            "image": article_data.get("image", ""),
            "published": article_data.get("published"),
            "source": article_data.get("source", ""),
        },
    )

    return article, created
```

The article service uses the API article URL to find an existing database record or create one from the supplied API data. This keeps the conversion from temporary API data to a persistent `Article` record in one place.

```python
# Create the Article database record only when the user bookmarks it
article, created = get_or_create_article(article_data)

# Create the bookmark linking the article to the logged-in user
bookmark, bookmark_created = Bookmark.objects.get_or_create(
    user=request.user,
    article=article
)
```

The bookmark view first passes the submitted API article data to the article service, which creates or retrieves the persistent `Article` record. The bookmark is then created using `get_or_create()`, linking the article to the authenticated user without creating duplicate bookmark records.

---

## Comments

NodeNexus supports comments on articles, including nested replies. When an authenticated user adds a comment to an article that has not yet been persisted, the article data is first stored in the `Article` table and assigned an article ID. The new `Comment` record is then associated with that article. This means commenting can persist an API article in the same way that bookmarking can.

Comments are stored in the database and associated with the corresponding `Article` and `User` records. A self-referencing parent relationship allows a comment to act as a reply to another comment and supports replies being nested further.

The article detail view retrieves top-level comments separately from all comments. Top-level comments are used for the main comment display, while the complete collection is used for actions such as editing and deleting the current user's comments.

The comment markup was separated into a reusable `comment.html` component instead of keeping the entire comment structure inside the article detail template. The component uses recursive rendering so each comment can render its replies, including further nested replies, without requiring separate templates for different reply levels.

Authenticated users can add comments and replies, edit their own comments, and delete their own comments. Edit and delete actions use Bootstrap modals, with the modal forms kept separate from the main comment submission form so the different forms do not interfere with each other.

The article detail view initializes the comment collections before checking whether the article is persisted. This allows the same template to safely handle articles before and after they are persisted.

Comment timestamps are displayed using the same local-time formatting system as article publication dates. UTC timestamps are converted into the user's local timezone in JavaScript before being displayed in a human-readable format.

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

```django
{% for reply in comment.replies.all %}

    {% include "comment.html" with comment=reply %}

{% endfor %}
```

The comment interface is kept in a reusable `comment.html` component, which recursively includes itself for replies. This allows the same template structure to render comments and nested replies at any depth without duplicating the markup.

---

## Styling

Bootstrap handles the responsive grid and base components. Custom CSS on top of that controls the NodeNexus look: a deep-space background with cyan accents, glass-style translucent panels, and dark/light theme support via CSS variables.

---

## Search

- A search bar with live autocomplete, calling a dedicated endpoint that returns matching article titles as JSON.
- Input is debounced to avoid firing a request on every keystroke.
- A stale-response guard tracks the most recent query and discards any autocomplete response that doesn't match it, so a slow earlier request can't overwrite a newer one on screen.

```javascript
let timeout;
let latestQuery = "";

searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim();
    latestQuery = query;

    clearTimeout(timeout);

    if (query.length < 2) return;

    timeout = setTimeout(async () => {
        const response = await fetch(
            `/auto-complete/?q=${encodeURIComponent(query)}`
        );

        const results = await response.json();

        // Ignore outdated results
        if (latestQuery !== query) return;

        const limitedResults = results.slice(0, 8);
    }, 250);
}); 
```

The autocomplete uses a 250ms debounce so requests are not sent for every keystroke. `latestQuery` ensures that results from an earlier search are ignored if the user has already entered a newer query, preventing outdated suggestions from replacing the current results.

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
        # Use the first three words of the title to find related articles
        title_words = article["title"].split()
        related_query = " ".join(title_words[:3])

        related_articles, _ = search_articles(related_query)

        # Remove the current article and limit results to 12 articles
        related_articles = [
            item for item in related_articles
            if item.get("url") != article["url"]
        ]
        
        # Broaden the search if no related articles are found
        if not related_articles:
            related_query = " ".join(title_words[:2])
            related_articles, _ = search_articles(related_query)
            
            related_articles = [
            item for item in related_articles
            if item.get("url") != article["url"]
        ]
```

The related articles system uses the current article's title to generate a simple search query rather than requiring a separate recommendation system. It first searches using the first three words of the title, removes the current article from the results, and falls back to the first two words if no results are found. This provides a lightweight way of finding potentially related content while working within the limitations of the external API.

## Bookmarks

Users can bookmark articles from the article detail page and remove them again from their saved articles.

The bookmark interface uses SVG icons rather than text-only controls, keeping the interface compact and consistent with the rest of the NodeNexus design.

When an article is bookmarked, its data is stored in the `Article` table and a `Bookmark` record links it to the user's account. Saved articles are displayed on the user's profile page.

Removing a bookmark deletes the bookmark record. If the article is no longer bookmarked by any user, the associated article record is also removed to keep the database clean.

---

## Comments and Replies

The article detail page includes a comment interface for authenticated users. Comments are displayed using a reusable `comment.html` component rather than keeping the complete comment markup inside the article detail template.

The comment component supports nested replies by recursively including itself for child comments. This allows replies to replies to be displayed using the same component structure without creating separate templates for each nesting level.

Users can edit and delete their own comments through Bootstrap modals. The edit and delete modals are generated for the user's comments and are kept separate from the main comment form so that the form and modal structures do not interfere with each other.

The comment interface was tested with top-level comments, replies, nested replies, editing, and deletion to ensure the recursive structure and modal actions worked correctly.

---

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

NodeNexus uses PostgreSQL instead of Django's default SQLite, for a more production-realistic setup and to support relational features such as user accounts, articles, and bookmarks. Credentials are kept in environment variables rather than in the codebase. Development and production use separate PostgreSQL databases, both accessed through the same Django ORM configuration.

The database includes Django's default authentication tables, the application's user profile data, and the custom `Article`, `Bookmark`, and `Comment` models.

The `Article` model stores article information when an article is bookmarked, including its title, description, image, source, published date, and URL. The `Bookmark` model connects saved articles to individual users.

The `Comment` model stores comments made on articles and links each comment to the user who created it. Comments can optionally reference another comment as their parent, allowing replies and nested replies to be stored using the same model.

An article can therefore be persisted either when a user bookmarks it or when a user adds a comment to it. In both cases, the article data is stored in the `Article` table and receives a database ID that can be referenced by related records.

When a bookmark is removed, the bookmark record is deleted. If no other user has bookmarked the associated article, the article record is also removed. This also applies to comments.

Custom profile images are stored through Cloudinary, while preset profile images are stored as static files and referenced by the user's profile.

User features such as messaging and notifications will be added later.

---

# 6. Completed Features

- **News aggregation:** Currents API integration with category pages for AI, cybersecurity, gaming, and trending tech.
- **Search:** global search with a results page, plus live autocomplete with debouncing and stale-response handling.
- **Content filtering:** domain exclusion list, CVE-title filtering, and deduplication.
- **Pagination:** five-button numbered pagination with previous/next arrows, responsive layout, applied across category and search pages.
- **Article detail pages:** full article view with a larger image, a link to the original article, and a related-articles carousel.
- **Bookmarks:** Users can save articles to their profile, view their saved articles, and remove bookmarks. Articles are only added to the database when bookmarked, and unused article records are removed when no users have them bookmarked. Saved articles can also be commented on and replied to.
- **Comments and replies:** Authenticated users can add comments to articles, reply to comments, create nested replies, edit their own comments, and delete their own comments. Adding a comment to an unsaved API article persists the article in the database before creating the associated `Comment` record. Comments are rendered recursively through a reusable template component.
- **Article management:** Saved articles are stored using `Article` and `Bookmark` database models, allowing bookmarked content to be associated with individual users. Comments are associated with persisted articles through the `Comment` model, with support for nested replies.
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

Not yet built: notifications and the inbox/messaging system.

---

# 7. Current Limitations

- The app depends entirely on the Currents API — if it's slow, rate-limited, or changes its response format, that directly affects the site. Caching helps but doesn't remove the dependency.
- Article data from the API isn't perfectly consistent (missing fields, occasional thin category results), so some normalisation and filtering will likely need further tuning.
- Related-articles matching (first three words of the title) is a simple approximation, not true topic matching, so results are sometimes only loosely related.
- Article detail pages currently receive the full article metadata through query parameters rather than looking the article up by a database ID. This is intentional for unsaved articles because API articles are not stored in the database until a user bookmarks them.
- Bookmarked articles are stored in the database, but the application does not currently store every article returned by the API. This means an article only receives a database ID after it has been saved.
- Bookmarking currently depends on the article data supplied by the API response. If the API changes or provides incomplete article data, this can affect the information stored when an article is bookmarked.

---

# 8. Key Design Decisions

**Why Django** — built-in URL routing, templates, ORM, and authentication meant less to build from scratch compared to Flask, which was used on earlier projects.

**Why Django authentication** — Django handles account creation, password hashing, password validation, login, logout, and sessions out of the box. This avoids having to build security-sensitive authentication features from scratch.

**Why PostgreSQL** — more production-realistic than SQLite, and better suited to the relational data coming later (users, bookmarks, comments).

**Why separate `backend/` and `frontend/`** — keeps Django logic and frontend templates/assets cleanly split, so a future React frontend can be added without reorganising the backend.

**Why previous/next pagination instead of numbered totals** — the Currents API doesn't report a total result count, so a traditional "page X of Y" approach wasn't possible. Since results are capped at five pages, a fixed five-button layout was used instead of calculating a page range.

**Why a service layer for the API** — keeping `currents.py` and `cache.py` separate from the views means the views stay focused on handling requests, and the API/caching logic can be tested and changed independently.

**Why articles are not stored immediately** — Articles returned by the Currents API are initially treated as API response data rather than being stored in the database. Storing every article returned by the API would create unnecessary database records for content users may never interact with. An article is only created in the database when a user chooses to bookmark it.

**Why bookmarks use separate Article and Bookmark models** — The `Article` model stores the article data itself, while the `Bookmark` model connects an article to a specific user. This keeps article data separate from the user's saved relationship and allows the same article to be bookmarked by multiple users without duplicating the article record.

**Why the Article record is created when bookmarked** — When a user saves an API article, the application uses the article data already available in the API response to create or retrieve the corresponding `Article` record. The database then assigns the article its own ID, which the bookmark can reference.

**Why unused articles are removed** — When a user removes a bookmark, the bookmark record is deleted. If no other users have bookmarked that article, the associated `Article` record is also removed. This prevents the database from accumulating article records that are no longer being used.

**Why commenting can persist an article** — Comments need a persistent `Article` record so they can be stored and associated with the article. If a user comments on an article that only exists as API response data, the application first creates the `Article` record from the available article data. The resulting database ID is then used by the new `Comment` record.

**Why comments use a self-referencing relationship** — Comments and replies use the same `Comment` model. A comment can optionally reference another comment as its parent, allowing the same structure to represent both top-level comments and replies without creating separate models for each level of nesting.

**Why comments are rendered recursively** — The comment structure is handled by a reusable `comment.html` component that can render a comment and then recursively render its replies. This allows the same template to support nested conversations at multiple levels without duplicating markup for each reply level.

**Why comment actions use separate modals** — Edit and delete actions use Bootstrap modals rather than placing additional forms directly into the main comment form. Keeping the modal forms separate prevents nested or overlapping form structures from interfering with comment submission.

**Why API response data is used for unsaved articles** — The Currents API does not provide a reliable way to retrieve an individual article by its URL or another permanent database identifier. Passing the article data through to the detail page allows unsaved articles to be displayed without unnecessarily storing them in the database.

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

**Bootstrap and custom CSS integration** — Bootstrap's grid and component styles sometimes conflicted with the custom NodeNexus design. The solution was to use Bootstrap mainly for layout and component structure while keeping branding, spacing, responsive behaviour, and visual styling in custom CSS.

**Static files and deployment caching** — CSS and JavaScript changes were sometimes not immediately visible after deployment because previously collected static files were still being served. Understanding WhiteNoise and `CompressedManifestStaticFilesStorage`, then running `collectstatic` correctly, ensured updated files received new versioned filenames.

**Currents API limitations and pagination** — The Currents API does not provide a total result count, making Django's standard `Paginator` unsuitable. Pagination was redesigned around checking whether another page exists, with the API's five-page limit eventually allowing a fixed five-button pagination layout. API results also required filtering, deduplication, and handling inconsistent or incomplete article data.

**API caching and rate limits** — Repeated Currents API requests could contribute to rate limiting and inconsistent response times. A TTL-based cache was introduced so repeated searches could reuse recent results rather than making unnecessary external requests.

**Autocomplete race condition** — Rapid typing could produce multiple autocomplete requests where an older, slower response overwrote a newer result. A latest-query check was added so stale responses are ignored.

**Autocomplete stacking issue** — The autocomplete dropdown could appear behind later sections despite having a high `z-index`. This was caused by `backdrop-filter` creating separate stacking contexts. The containing hero section was given its own positioning and `z-index` so the dropdown could stack correctly.

**Responsive layout issues** — The homepage and article carousels required several responsive adjustments. One issue occurred on mobile devices in landscape orientation because their width exceeded the original `768px` carousel breakpoint. The carousel rules were moved into the existing `max-width: 992px` section so tablet and landscape-mobile layouts were handled consistently. Similar responsive adjustments were required for navigation, pagination, article cards, profile interfaces, spacing, and typography.

**Article detail and API article handling** — Article detail pages initially attempted to retrieve an article using only its URL, but Currents does not provide a reliable individual-article lookup. The solution was to pass the full article data through query parameters for unsaved API articles. This allowed the detail page to work without creating a database record for every article.

**Bookmark database design** — Bookmarks required deciding how temporary API article data should become persistent database data. The final design keeps unsaved articles as API response dictionaries while they are being viewed. When a user bookmarks an article, the article service uses that data to get or create an `Article` record, allowing Django to assign it a database ID. A `Bookmark` record then connects the article to the user. This keeps the `Article` and `Bookmark` responsibilities separate and prevents every API result from being stored unnecessarily.

**Bookmark state and cleanup** — The article detail page needed to determine whether the current user had already bookmarked an article while still supporting articles that did not yet exist in the database. The bookmark flow was therefore designed to work with both API data and persisted articles. When a bookmark is removed, the application checks whether another user still references the article and deletes the unused `Article` record when necessary.

**Bookmark implementation and testing** — Adding bookmarks required migrations, a dedicated article service for persistence, bookmark creation and deletion logic, and testing across the article detail page and profile. The complete flow was tested to ensure articles could be saved, displayed as saved, removed, and correctly cleaned up from the database.

**Authentication frontend integration** — Django's authentication system handled account creation, password validation, login, logout, sessions, and password management, while the frontend required custom integration into the NodeNexus design. This included custom forms, validation errors, responsive navigation links, password visibility controls, password reset pages, and change-password functionality.

**Password reset email setup** — Password reset initially used Django's console email backend, which displayed emails in the development terminal. SMTP was later configured so real password reset emails could be sent. Email credentials were kept in environment variables and the complete reset process was tested using a real email account.

**Profile picture storage and Cloudinary** — Profile pictures initially used the local filesystem for both uploads and preset images. This was unsuitable for production on Render because uploaded files should not depend on the application's local filesystem. The system was redesigned so nine preset images remain permanent static assets while custom uploads use Cloudinary through `CloudinaryField`. Separate profile fields distinguish between the two sources.

**Profile picture modal and frontend integration** — The profile picture selector required a custom modal for choosing presets or uploading an image. Initially, placing the modal inside the main profile form caused form and modal structures to interfere with each other. Moving the modal outside the main form resolved the conflict. JavaScript was then used to control selection, previews, and the displayed profile image, with additional responsive styling for desktop, tablet, and mobile.

**Cloudinary deployment configuration** — Cloudinary initially caused a Render deployment error because the project attempted to import `cloudinary_storage` even though it was not required by the final implementation. The unused configuration was removed, `CloudinaryField` was used directly, and the required Cloudinary credentials were added as Render environment variables.

**Comment persistence for unsaved articles** — Comments introduced a new requirement because a `Comment` must reference a database `Article`, while an article being viewed may still only exist as an API dictionary. The solution was to make commenting itself persist the article. When a logged-in user comments on an unsaved article, the article data is used to create the `Article` record, Django assigns its ID, and the new `Comment` is then linked to that article. This means users do not need to bookmark an article before commenting.

**Comment view and data handling** — Adding comments exposed an issue in the article detail view where comment collections were not available consistently across the API-article and persisted-article paths, resulting in a 500 error. The view was reorganised so the required comment collections are initialized before the article persistence logic, allowing both article states to use the same template. Top-level comments are retrieved separately using `parent__isnull=True`, while the complete comment collection remains available for nested comments and user actions.

**Nested replies and recursive rendering** — Replies required a self-referencing relationship on the `Comment` model so each comment can optionally reference another comment as its parent. This allows top-level comments, replies, and replies to replies to use the same model. As the comment structure became recursive, the comment markup was moved from `article_detail.html` into a reusable `comment.html` component. The component recursively includes itself for child comments, allowing nested replies at any depth without duplicating the template structure.

**Comment editing and deletion** — Edit and delete actions had to work for comments at any level of the nested conversation. The application therefore retains access to the complete set of comments while the recursive component handles their display. Controls are only shown for comments belonging to the authenticated user, with the backend responsible for enforcing ownership.

**Comment forms and Bootstrap modals** — Comment creation, editing, and deletion introduced multiple forms and Bootstrap modals on the same article page. The initial modal placement caused form/modal overlap and submission conflicts. The modal structures were separated from the main comment form and each edit/delete action was associated with its correct form, allowing the different comment operations to work independently.

**Comment database integration** — The comment system required a new `Comment` model, relationships to users and articles, a self-referencing parent relationship, migrations, view logic, template components, and testing. The implementation connected these pieces so comments and nested replies could be created, edited, deleted, and displayed correctly for persisted articles.

**Date and timestamp handling** — Article and comment timestamps could arrive in formats that JavaScript did not always parse consistently. The frontend converts the UTC timestamp into a JavaScript `Date` and validates it before formatting it using `Intl.DateTimeFormat`. Invalid values are ignored rather than causing the entire timestamp script to fail with an `Invalid time value` error.

**Development and production consistency** — Features involving external storage and deployment were tested in both local development and the Render environment. Environment variables were used for secrets and external services, while static assets remained part of the application and user-uploaded media was stored externally through Cloudinary.

---

# 11. What Was Learned

- Structuring a Django application using separate apps, views, templates, models, and services while keeping API and caching logic outside the views.

- Understanding how Django's ORM, PostgreSQL database, external APIs, templates, JavaScript, and deployment environment work together as one application.

- Working with external APIs and adapting application design around their limitations, including inconsistent results, missing result counts, rate limits, and limited individual-article lookup.

- Designing pagination and caching around the capabilities of an external API rather than assuming Django's built-in tools will always be appropriate.

- Combining Bootstrap with custom CSS and understanding responsive layouts, breakpoints, overflow, stacking contexts, and `z-index`.

- Debugging by tracing the actual execution path, checking console and server errors, and identifying which part of the application is responsible instead of repeatedly changing unrelated code.

- Using Django's built-in authentication and form systems for registration, validation, password hashing, login, logout, sessions, password resets, and password changes.

- Integrating Django authentication into a custom frontend and extending it with JavaScript functionality such as password visibility controls.

- Configuring SMTP and environment variables for real password reset emails without exposing credentials in the codebase.

- Understanding the difference between static assets and user-uploaded media and why production applications should not rely on the local filesystem for uploaded files.

- Using Cloudinary and `CloudinaryField` for custom user uploads while keeping permanent preset profile images as static assets.

- Understanding how HTML form structure affects Bootstrap modal behaviour and why separate forms and modal structures are sometimes necessary.

- Designing database-backed features around the difference between temporary API data and persistent Django model data.

- Understanding why API articles should not automatically be stored in the database and how user actions such as bookmarking or commenting can intentionally transition an API article into a persistent `Article` record.

- Understanding the relationship between `Article` and `Bookmark` models, using `get_or_create()` to avoid unnecessary duplicates, and cleaning up unused records after bookmark removal.

- Understanding how a self-referencing Django model can represent comments, replies, and nested replies without requiring separate models.

- Using reusable Django template components and recursive template inclusion to render hierarchical data at arbitrary nesting levels.

- Managing multiple forms and Bootstrap modals on the same page without allowing their structures to interfere with one another.

- Handling ownership and permissions for user-generated content such as comment editing and deletion.

- Understanding how Django views need to initialise and pass consistent data to templates when the same page supports multiple data sources and execution paths.

- Handling and validating timestamps in JavaScript when external API and database data can use different date formats.

- Using migrations to evolve the PostgreSQL schema as features such as bookmarks, profiles, and comments are introduced.

- Understanding the importance of testing features across different article states, users, screen sizes, and development/production environments.

- Reviewing documentation against the actual implementation to identify missing functionality, outdated descriptions, and inconsistencies.
---

# 12. Next Steps

- The inbox/messaging system required by the assignment brief.
- Account deletion and additional account management features.
- Admin functionality and role-based access control.
- Continued testing and bug fixes on API result consistency (some categories occasionally return fewer than 12 articles).
- Final UI polish, responsive testing, accessibility improvements, and general application refinement.
- Continued testing of existing features as new functionality is added.
- Eventual migration to a React frontend with a DRF API layer — models and the service layer are expected to carry over largely unchanged.

---

# 13. References

**Backend**
- Django Documentation — https://docs.djangoproject.com/en/6.0/
- Django Pagination — https://docs.djangoproject.com/en/6.0/topics/pagination/
- Django Models and Migrations — https://docs.djangoproject.com/en/6.0/topics/db/models/
- Django Model Relationships — https://docs.djangoproject.com/en/6.0/topics/db/examples/
- Django QuerySet API — https://docs.djangoproject.com/en/6.0/ref/models/querysets/
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
- MDN Date — https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date
- MDN Intl.DateTimeFormat — https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat
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