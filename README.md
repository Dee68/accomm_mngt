# Accommodation Center
[Live demo](https://dimie.dev)

A full-stack platform for managing residential buildings. Tenants are
assigned to apartments, maintenance issues are tracked from report to
resolution, and a community forum lets residents coordinate with each
other. Built with Django, Next.js, PostgreSQL, and Celery.

> **Novel architecture decision:** the frontend was migrated from Redux
> Toolkit to **TanStack Query + Zustand** in November 2026. See the
> [Frontend Migration](#frontend-migration-redux--tanstack-query--zustand)
> section for the before/after, screenshots, and process.

![Accommodation Center home feed](docs/screenshots/home-feed.webp)

## Features

**For tenants**
- Register, activate via email, and sign in with a password or Google OAuth
- View and manage their apartment assignment
- Upload a profile avatar (stored in Cloudinary)
- Report maintenance issues to their building
- Create and interact with community forum posts
- Bookmark and vote on posts
- Rate technicians after a service

![Accommodation Center login user](docs/screenshots/login-user.webp)
![Accommodation Center Email activation](docs/screenshots/activation.webp)

**For technicians**
- Sign in and see issues assigned to them
- Update the status of assigned issues
- Browse the community forum

![Accommodation Center Post forum](docs/screenshots/post-forum.webp)
**For administrators**
- Full Django admin with filters, search, and bulk actions
- Manage apartments, tenants, issues, and technicians
- Assign issues to technicians (with automatic email notification)
- Monitor background tasks via Flower
- Review and act on user reports
- Moderate users (banned after five reports, with automatic account deactivation)

![Accommodation Center Admin Interface](docs/screenshots/admin-interface.webp)



![Accommodation Center Tenant Report Email](docs/screenshots/report.webp)
![Accommodation Center Tenant Warning Email](docs/screenshots/warning.webp)

## Stack

| Layer | Technologies |
|---|---|
| Backend | Django 4.2, Django REST Framework, PostgreSQL |
| Frontend | Next.js, TypeScript, Tailwind CSS, shadcn/ui, **TanStack Query** + **Zustand** (migrated from Redux Toolkit) |
| Authentication | JWT in HttpOnly cookies, Google OAuth |
| Background tasks | Celery, Celerybeat, Redis(Flower for local monitoring) |
| Email | Django templates, CeleryEmailBackend, Mailpit (local), django-anymail + Resend (production) |
| Infrastructure | Docker + nginx (local), Railway (production) |
| API documentation | DRF Spectacular (Swagger, ReDoc) |
| Testing | pytest, pytest-django (333 tests) |

## Quick start

**Prerequisites:** Docker >= 20.10, Docker Compose >= 2.0

```bash
git clone https://github.com/Dee68/accomm_mngt.git
cd accomm_mngt
```

Create the local environment file:

```bash
cp .envs/.env.local.example .envs/.env.local
```

Then build and start the containers:

```bash
make build
make up
```

Once the containers are healthy, the application is available at:

| Service | URL |
|---|---|
| Frontend | http://localhost:8080 |
| API documentation (Swagger) | http://localhost:8080/api/v1/docs/ |
| API documentation (ReDoc) | http://localhost:8080/api/v1/redoc/ |
| Django admin | http://localhost:8080/superuser/ |
| Mailpit (captured emails) | http://localhost:8025 |
| Flower (task monitoring) | http://localhost:5555 |

## Running tests


```bash
docker compose -f local.yml exec api pytest core_apps/ -v
```
The full suite is 333 tests covering models, views, serializers,
permissions, forms, admin configuration, signals, background tasks,
email delivery, and URL routing. The suite runs in approximately 25
seconds.

## Architecture

### Local development

Nine Docker services behind an nginx reverse proxy: `api`, `client`,
`postgres`, `redis`, `celeryworker`, `celerybeat`, `flower`, `mailpit`,
`nginx`.

### Production (Railway)

Three deployable services (`api`, `client`, `celery_workers`) plus managed
Postgres and Redis. No nginx, no Flower, no Mailpit — Railway
terminates TLS and routes by hostname, and Mailpit's role is taken over
by Resend, which receives outbound email through `django-anymail`.

Emails are sent through Celery using `CeleryEmailBackend`, so they don't
block the request cycle. In development, Mailpit intercepts every
outbound message. In production, the SMTP backend points at a
transactional email provider through environment variables.

![Accommodation Center Issue Report Email](docs/screenshots/issue.webp)
![Accommodation Center Issue Assignment Email](docs/screenshots/assignment.webp)
![Accommodation Center Issue Resolution Email](docs/screenshots/resolution.webp)


## Frontend Migration: Redux → TanStack Query + Zustand

The frontend originally used Redux Toolkit (RTK) for global state and RTK Query for server-state caching. To align with modern React patterns, the entire frontend was migrated domain-by-domain to **TanStack Query** for server state and **Zustand** for client state.

### Why the change?
- **Separation of concerns:** Redux mixed server state (fetched data) with client state (UI filters, auth flags). TanStack Query handles server state natively; Zustand handles UI state with minimal boilerplate.
- **Developer experience:** TanStack Query provides built-in caching, background refetching, and optimistic updates without the boilerplate of RTK Query tags.
- **Bundle size:** Removing `react-redux` and `@reduxjs/toolkit` reduced the client bundle significantly.

### What changed (Architecture)

| Concern | Before (Redux) | After (TanStack + Zustand) |
| :--- | :--- | :--- |
| **Server State** | `createApi` slices (`baseApiSlice`, `authApiSlice`, etc.) with `providesTags` / `invalidatesTags` | `lib/query/use-*.ts` hooks powered by TanStack Query |
| **Client State** | `createSlice` (`authSlice`, `userSlice`, `postSlice`) with `useSelector` / `useDispatch` | Zustand stores (`useAuthStore`, `useUserFiltersStore`, `usePostFiltersStore`) |
| **Provider** | `<Provider store={store}>` (react-redux) | `<QueryClientProvider>` (TanStack Query) |
| **Data Fetching** | RTK Query hooks (`useGetAllPostsQuery`) | TanStack hooks (`useAllPosts`) |
| **Cache Invalidation** | `invalidatesTags: ["Post"]` | `queryClient.invalidateQueries({ queryKey: keys.posts.all })` |
| **Optimistic Updates** | `onQueryStarted` | `onMutate` / `onError` / `onSettled` |

---
### Visual Proof
![TanStack Query Devtools — User Profile queries](docs/screenshots/tanstack-profile.webp)
*TanStack Query Devtools showing parallel fetches for user profile, my-posts, my-issues, and my-reports.*

![TanStack Query Devtools — Posts queries](docs/screenshots/tanstack-post.webp)
*TanStack Query Devtools showing cached post lists, popular tags, and top posts.*

![Client deployment — Railway](docs/screenshots/client-railway-deployment.webp)
*Production deploy on Railway: `chore(client): remove Redux, complete TanStack Query + Zustand migration` marked ACTIVE and Deployment Successful.*

### How it was done (The Process)
1. **Auth First:** Ported the auth flow (`useLogin`, `useMe`, `PersistAuth`) to Zustand to establish the new pattern.
2. **Domain-by-Domain:** Ported Posts, Users, Issues, Apartments, Ratings, and Reports one at a time. Each domain received its own API file, Query file, and hooks.
3. **The Final Sweep:** Once all 8 domains were ported, `lib/redux/` was deleted, `react-redux` and `@reduxjs/toolkit` were uninstalled, and `<ReduxProvider>` was removed from the layout.
4. **Rollback Safety:** A git tag (`pre-tanstack-migration`) was created before deletion to guarantee a safe rollback reference.

> **Note on `async-mutex`:** While Redux was removed, `async-mutex` remains in `package.json`. It is still used inside `lib/api/client.ts` to prevent concurrent `/auth/refresh/` requests when multiple API calls fail with a 401 simultaneously.

## Environment variables

The backend reads configuration from `.envs/.env.local`. Required
variables:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_ADMIN_URL=superuser/
POSTGRES_USER=apigolden
POSTGRES_PASSWORD=your-db-password
POSTGRES_DB=apartment
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
EMAIL_HOST=mailpit
EMAIL_PORT=1025
DEFAULT_FROM_EMAIL=noreply@example.com
DOMAIN=localhost:8080
COOKIE_SECURE=False
REDIRECT_URIS=http://localhost:8080
```

The above are local development values. Production additionally requires:

```env
RESEND_API_KEY=your-resend-api-key
ANYMAIL_RESEND_API_KEY=${RESEND_API_KEY}
CORS_ALLOWED_ORIGINS=https://dimie.dev
CSRF_TRUSTED_ORIGINS=https://dimie.dev,https://api.dimie.dev
SESSION_COOKIE_SAMESITE=None
SESSION_COOKIE_SECURE=True
COOKIE_SAMESITE=None
COOKIE_SECURE=True
```

## Project structure

```
accomm_mngt/
├── api/                       # Django backend
│   ├── config/                # Settings (base, local, production)
│   ├── core_apps/
│   │   ├── apartments/        # Apartment management
│   │   ├── common/            # Shared abstractions
│   │   ├── issues/            # Maintenance tickets
│   │   ├── posts/             # Community forum
│   │   ├── profiles/          # User profiles
│   │   ├── ratings/           # User ratings
│   │   ├── reports/           # Moderation reports
│   │   └── users/             # Custom user model
│   ├── requirements/
│   ├── manage.py
│   ├── local.yml              # Docker Compose for development
│   └── Makefile
└── client/                    # Next.js frontend
    ├── app/                   # App router pages
    ├── components/            # Shared UI components
    ├── lib/
    │   ├── api/               # Axios instance + reauth mutex + per-domain API functions
    │   ├── query/             # TanStack Query hooks per domain (use-posts, use-issues, etc.)
    │   └── stores/            # Zustand stores (auth session, UI filters)
    ├── providers/             # QueryClientProvider setup
    └── hooks/                 # Custom React hooks (useAuthNavigation, etc.)
```


> **Historical note:** Before the frontend migration, the client folder
> contained a `lib/redux/` directory holding all Redux Toolkit slices,
> RTK Query API endpoints, and the Redux Provider. That directory was
> fully removed as part of the migration to TanStack Query + Zustand.
> See the [Frontend Migration](#frontend-migration-redux--tanstack-query--zustand)
> section for details on the before/after architecture.

## Deployment

The application is deployed on Railway:

- **api** — Django, gunicorn, connected to managed Postgres and Redis
- **client** — Next.js (TanStack Query + Zustand), deployed from the same repository. The removal of Redux lowered the First Load JS payload.
- **celery_workers** — Celery worker (see `workers.sh`)

External services connected in production:

- **Cloudinary** — avatar storage, keeping the container stateless
- **Resend via django-anymail** — transactional email delivery
- **Google OAuth** — sign-in with Google

Environment variables are set per-service in Railway's dashboard. The
production `DJANGO_SETTINGS_MODULE` is `config.settings.production`.


![Accommodation Center Railway Deployment Dashboard](docs/screenshots/railway-dashboard.webp)


## License

This project is licensed for educational and portfolio purposes. You
are welcome to read, clone, and learn from the code. Commercial use
and republishing as your own work are not permitted.