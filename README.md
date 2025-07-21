# CG Stewart Developer Blog

A modern, full-stack developer blog built with Django REST Framework and Next.js, featuring elegant design, secure file handling, and smooth animations.

## 🚀 Features

### Frontend (Next.js)
- **Elegant Design**: Beautiful, responsive UI with smooth animations using Framer Motion
- **Modern Architecture**: Next.js 15 with TypeScript, TanStack Query, and Tailwind CSS
- **Dynamic Routing**: Slug-based routing for posts, projects, and videos
- **Interactive Filtering**: Category-based filtering for blog posts
- **Optimized Images**: Next.js Image component with S3 integration
- **Responsive Layout**: Mobile-first design that works on all devices

### Backend (Django)
- **REST API**: Django REST Framework with versioned API endpoints
- **Admin CMS**: Django admin interface with modern theme (django-jazzmin)
- **Secure File Storage**: AWS S3 integration with signed URLs for private files
- **Content Management**: Full CRUD operations for posts, projects, videos, and bio
- **Flexible Content**: Support for markdown content and rich media

### Content Types
- **Bio**: Personal information, social links, resume, and profile image
- **Posts**: Blog posts with categories (General, Tech, Book Reviews)
- **Projects**: Portfolio projects with tech stack, live links, and GitHub repos
- **Videos**: Video content with YouTube integration and thumbnails

## 🏗️ Architecture

This is a monorepo containing two main applications:

```
cgstewart-django/
├── apps/
│   ├── api/          # Django REST API backend
│   └── web/          # Next.js frontend
├── packages/
│   └── ui/           # Shared UI components (shadcn/ui)
└── README.md
```

### Backend (`apps/api`)
- **Framework**: Django 5.x with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Storage**: AWS S3 with django-storages
- **Authentication**: Django admin authentication
- **API**: RESTful endpoints at `/api/v1/`

### Frontend (`apps/web`)
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: TanStack Query for server state
- **Animations**: Framer Motion for smooth transitions

## 🛠️ Tech Stack

### Backend
- Django 5.x
- Django REST Framework
- django-storages (S3 integration)
- django-jazzmin (admin theme)
- boto3 (AWS SDK)
- python-dotenv
- UV (package manager)

### Frontend
- Next.js 15
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Framer Motion
- Lucide React (icons)

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- UV (Python package manager)
- pnpm (Node.js package manager)
- AWS S3 bucket (for file storage)

### Backend Setup

1. Navigate to the API directory:
   ```bash
   cd apps/api
   ```

2. Install dependencies with UV:
   ```bash
   uv sync
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Configure environment variables in `.env`:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   AWS_STORAGE_BUCKET_NAME=your-s3-bucket
   AWS_S3_REGION_NAME=your-aws-region
   ```

5. Run migrations:
   ```bash
   uv run python manage.py migrate
   ```

6. Create superuser:
   ```bash
   uv run python manage.py createsuperuser
   ```

7. Start development server:
   ```bash
   uv run python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the web directory:
   ```bash
   cd apps/web
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Create environment file:
   ```bash
   cp .env.local.example .env.local
   ```

4. Configure environment variables in `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```

5. Start development server:
   ```bash
   pnpm dev
   ```

## 📝 Content Management

### Django Admin
Access the Django admin at `http://localhost:8000/admin/` to manage content:

- **Bio**: Update personal information and social links
- **Posts**: Create and manage blog posts with categories
- **Projects**: Add portfolio projects with tech stacks and links
- **Videos**: Manage video content with YouTube URLs

### API Endpoints
The REST API is available at `http://localhost:8000/api/v1/`:

- `GET /bio/` - Get bio information
- `GET /posts/` - List all posts
- `GET /posts/{slug}/` - Get specific post
- `GET /projects/` - List all projects
- `GET /projects/{slug}/` - Get specific project
- `GET /videos/` - List all videos
- `GET /videos/{slug}/` - Get specific video

## 🎨 Design Features

### Homepage
- **Elegant Headers**: "I write about tech and books here" and "I like to showcase my art here"
- **Recent Content**: Shows 3 most recent posts and projects
- **Smooth Animations**: Staggered animations using Framer Motion
- **Responsive Navigation**: Clean header with section links

### List Pages
- **Posts**: Category filtering with elegant card design
- **Projects**: Clean grid layout with tech stack badges
- **Videos**: YouTube thumbnail integration with play overlays

### Detail Pages
- **Rich Content**: Full content display with images and metadata
- **Navigation**: Back buttons for easy navigation
- **Responsive**: Optimized for all screen sizes

## 🔒 Security Features

- **Signed URLs**: S3 files use temporary signed URLs for secure access
- **Private Storage**: Files are stored privately in S3 with controlled access
- **CORS Configuration**: Proper CORS setup for API access
- **Environment Variables**: Sensitive data stored in environment files

## 🚀 Deployment

### Backend Deployment
- Configure production database (PostgreSQL recommended)
- Set up AWS S3 bucket with proper permissions
- Configure environment variables for production
- Use a WSGI server like Gunicorn

### Frontend Deployment
- Build the Next.js application: `pnpm build`
- Deploy to Vercel, Netlify, or similar platform
- Configure environment variables for production API URL

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**CG Stewart** - Developer & Designer

---

*Built with ❤️ using Django, Next.js, and modern web technologies.*

This template is for creating a monorepo with shadcn/ui.

## Usage

```bash
pnpm dlx shadcn@latest init
```

## Adding components

To add components to your app, run the following command at the root of your `web` app:

```bash
pnpm dlx shadcn@latest add button -c apps/web
```

This will place the ui components in the `packages/ui/src/components` directory.

## Tailwind

Your `tailwind.config.ts` and `globals.css` are already set up to use the components from the `ui` package.

## Using components

To use the components in your app, import them from the `ui` package.

```tsx
import { Button } from "@workspace/ui/components/button"
```
