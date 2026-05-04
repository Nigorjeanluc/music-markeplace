# Music Marketplace

A full-stack web application for discovering, purchasing, and managing digital music albums. Built with FastAPI (backend) and React (frontend), featuring JWT authentication, S3 image storage, playlist management, and an admin dashboard.

## Features

- **User Authentication** — JWT-based auth with access/refresh token rotation
- **Album Marketplace** — Browse, search, and filter albums by genre or artist
- **Digital Purchases** — One-click album purchasing with personal library
- **Ratings & Reviews** — Rate purchased albums (1–5 stars), average rating per album
- **Playlist Management** — Create, rename, and manage playlists with track organization (non-admin users)
- **Admin Dashboard** — Full CRUD management for artists, albums, genres, tracks, and playlists
- **S3 Image Storage** — Album cover art and artist photos via AWS S3 or S3-compatible storage
- **Pagination** — All list endpoints support pagination
- **Responsive UI** — Dark-themed cyber-noir interface built with Tailwind CSS

## Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.12)
- **ORM:** SQLAlchemy 2 + Alembic (migrations)
- **Validation:** Pydantic v2 + pydantic-settings
- **Database:** PostgreSQL 16
- **Auth:** JWT (HS256) with access + refresh tokens
- **Storage:** AWS S3 / S3-compatible (boto3)
- **Testing:** pytest + httpx (both unit and integration tests)

### Frontend
- **Framework:** React 19 with TypeScript
- **Build Tool:** Vite 8
- **Styling:** Tailwind CSS 4
- **Routing:** React Router DOM 7
- **State/Data:** TanStack React Query 5 (caching, pagination, mutations)
- **Forms:** Formik + Yup validation
- **HTTP:** Axios
- **Testing:** Vitest + React Testing Library

## Project Structure

```
music-marketplace/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # API route handlers
│   │   │   ├── auth.py         # POST /auth/register, /auth/login, /auth/refresh, GET /auth/me
│   │   │   ├── artists.py      # CRUD + list for artists
│   │   │   ├── albums.py      # CRUD + list for albums (with ratings & genres)
│   │   │   ├── purchases.py   # POST /purchases/, GET /purchases/me/library
│   │   │   ├── ratings.py     # POST, PUT, GET /ratings/me, GET /ratings/album/:id
│   │   │   ├── genres.py      # CRUD + list for genres
│   │   │   ├── tracks.py      # CRUD + list for tracks
│   │   │   ├── playlists.py   # CRUD + tracks for playlists
│   │   │   └── upload.py      # POST /upload/ (S3 image upload)
│   │   ├── core/              # Config, security, S3 service
│   │   ├── models/            # SQLAlchemy models (User, Artist, Album, etc.)
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/          # Business logic layer
│   │   └── db/               # Session, base, migrations, seed
│   ├── tests/
│   │   ├── unit/             # Unit tests (security, schemas, S3)
│   │   └── integration/       # Integration tests (services + API endpoints)
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/client.ts       # Axios instance + API functions
│   │   ├── hooks/useApi.ts    # TanStack Query hooks
│   │   ├── pages/              # Page components
│   │   ├── components/         # Reusable UI components
│   │   ├── context/            # Auth & Toast context providers
│   │   └── App.tsx            # Router + layout
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.12+ (local backend dev)
- Node.js 20+ (local frontend dev)
- PostgreSQL 16 (or use Docker)
- AWS S3 bucket or S3-compatible storage (for image uploads)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repo-url>
cd music-marketplace

# 1. Configure environment files
cp backend/.env.example backend/.env
# Edit backend/.env with your settings (see Environment Variables below)

cp frontend/.env.example frontend/.env
# Edit frontend/.env if needed

# 2. Start all services
docker compose up --build

# Access:
#   Frontend:  http://localhost:5174
#   Backend API: http://localhost:8001
#   API Docs:  http://localhost:8001/api/v1/docs
```

### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure backend/.env (see Environment Variables below)

# Run migrations + seed + start
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API available at: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Frontend:**
```bash
cd frontend
yarn install

# Configure frontend/.env (see Environment Variables below)

yarn dev

# App available at: http://localhost:5173
```

## Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://musicapp:musicapp123@localhost:5432/musicdb` | Main database URL |
| `DATABASE_URL_TEST` | `postgresql://musicapp:musicapp123@localhost:5432/musicdb_test` | Test database URL |
| `SECRET_KEY` | `your-super-secret-key-change-this-in-production` | JWT secret key |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token expiry (minutes) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token expiry (days) |
| `ENVIRONMENT` | `development` | `development` or `production` |
| `DEBUG` | `True` | Enable debug mode |
| `ALLOWED_ORIGINS` | `["http://localhost:8000", "http://localhost:5173", ...]` | CORS allowed origins (JSON array) |
| `AWS_ACCESS_KEY_ID` | `your-access-key` | AWS S3 access key |
| `AWS_SECRET_ACCESS_KEY` | `your-secret-key` | AWS S3 secret key |
| `AWS_STORAGE_BUCKET_NAME` | `music-marketplace-images` | S3 bucket name |
| `AWS_S3_REGION` | `us-east-1` | S3 region |
| `AWS_S3_CUSTOM_DOMAIN` | _(empty)_ | Optional CDN domain (e.g., CloudFront) |

### Frontend (`frontend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | Backend API base URL |

## Default Credentials (from Seed)

The seed script (`backend/app/db/seed.py`) creates the following users and data:

### Admin User
| Field | Value |
|------|-------|
| Email | `admin@musicmarket.com` |
| Username | `admin` |
| Password | `admin123` |
| Role | Admin |

### Regular Users
| Field | User 1 | User 2 |
|------|--------|--------|
| Email | `john@musicmarket.com` | `jane@musicmarket.com` |
| Username | `john_doe` | `jane_smith` |
| Password | `password123` | `password123` |
| Role | Member | Member |

### Seed Data
- **8 Artists:** John Coltrane, Miles Davis, Pink Floyd, Radiohead, James Brown, Daft Punk, Saleheen, Vishnu
- **8 Albums:** A Love Supreme, Kind of Blue, The Dark Side of the Moon, OK Computer, Kid A, Live at the Apollo, Random Access Memories, Discovery
- **8 Genres:** Jazz, Rock, Classical, Hip Hop, Blues, Electronic, R&B, Pop
- **16 Tracks** across the albums
- **3 Playlists:** My Jazz Collection, Electronic Vibes, Rock Classics
- **6 Purchases** by the two regular users
- **6 Ratings** (1–5 stars)

## API Endpoints

Base URL: `/api/v1`

### Auth (`/auth`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | Public | Register a new user |
| POST | `/auth/login` | Public | Login and receive JWT tokens |
| POST | `/auth/refresh` | Public | Refresh access token |
| GET | `/auth/me` | Authenticated | Get current user profile |

### Artists (`/artists`) — Admin Only for write operations
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/artists/` | Public | List artists (paginated, searchable) |
| GET | `/artists/{id}` | Public | Get artist detail |
| POST | `/artists/` | Admin | Create artist |
| PUT | `/artists/{id}` | Admin | Update artist |
| DELETE | `/artists/{id}` | Admin | Delete artist |

### Albums (`/albums`) — Admin Only for write operations
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/albums/` | Public | List albums (paginated, filter by artist/genre/search) |
| GET | `/albums/{id}` | Public | Get album detail with rating |
| POST | `/albums/` | Admin | Create album |
| PUT | `/albums/{id}` | Admin | Update album |
| DELETE | `/albums/{id}` | Admin | Delete album |

### Purchases (`/purchases`) — Authenticated users
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/purchases/` | Authenticated | Purchase an album |
| GET | `/purchases/me/library` | Authenticated | Get user's purchased albums (paginated) |

### Ratings (`/ratings`) — Authenticated users
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/ratings/` | Authenticated | Rate an album (must be purchased first) |
| PUT | `/ratings/{album_id}` | Authenticated | Update your rating |
| GET | `/ratings/me` | Authenticated | Get your ratings (paginated) |
| GET | `/ratings/album/{album_id}` | Public | Get all ratings for an album (paginated) |

### Genres (`/genres`) — Admin Only for write operations
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/genres/` | Public | List all genres |
| GET | `/genres/{id}` | Public | Get genre detail |
| POST | `/genres/` | Admin | Create genre |
| PUT | `/genres/{id}` | Admin | Update genre |
| DELETE | `/genres/{id}` | Admin | Delete genre |

### Tracks (`/tracks`) — Admin Only for write operations
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/tracks/` | Public | List tracks (paginated, filter by album/search) |
| GET | `/tracks/{id}` | Public | Get track detail |
| POST | `/tracks/` | Admin | Create track |
| PUT | `/tracks/{id}` | Admin | Update track |
| DELETE | `/tracks/{id}` | Admin | Delete track |

### Playlists (`/playlists`) — Authenticated users (non-admin)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/playlists/` | Authenticated | List user's playlists |
| GET | `/playlists/{id}` | Authenticated | Get playlist detail with tracks |
| POST | `/playlists/` | Authenticated | Create playlist |
| PUT | `/playlists/{id}` | Authenticated | Rename playlist |
| POST | `/playlists/{id}/tracks` | Authenticated | Add track to playlist |
| DELETE | `/playlists/{id}/tracks/{track_id}` | Authenticated | Remove track from playlist |
| DELETE | `/playlists/{id}` | Authenticated | Delete playlist |

### Upload (`/upload`) — Admin Only
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/upload/` | Admin | Upload image to S3 |

> Full interactive API documentation available at `/api/v1/docs` (Swagger UI) when the backend is running.

## Frontend Pages & Routing

| Route | Page | Access | Description |
|-------|------|--------|-------------|
| `/login` | `LoginPage` | Public | Login/register form |
| `/` | `MarketplacePage` | Public | Browse albums, search, filter by genre, spotlight artists |
| `/library` | `LibraryPage` | Authenticated (non-admin) | View purchased albums, rate albums, pagination |
| `/playlists` | `PlaylistsPage` | Authenticated (non-admin) | Manage playlists, add/remove tracks |
| `/artists` | `ArtistsPage` | Public | Browse all artists with search and pagination |
| `/artists/:id` | `ArtistDetailPage` | Public | Artist profile, discography, stats |
| `/albums/:id` | `AlbumDetailPage` | Public | Album detail, tracklist, purchase, rate |
| `/management` | `ManagementPage` | Admin only | Full CRUD for artists, albums, genres, tracks, playlists |
| `/profile` | `ProfilePage` | Authenticated | User profile, stats, ratings, playlists (accessed via UI) |

**Navigation:** Sidebar (`Sidebar.tsx`) shows Marketplace, Library, Playlists (non-admin), Artists, and Management (admin only). Library and Playlists are hidden from admin users.

## Database Schema

- **User** — id, email, username, hashed_password, is_admin, is_active, created_at, updated_at
- **Artist** — id, real_name, performing_name, date_of_birth, photo_url, created_at, updated_at
- **Genre** — id, name, description, created_at, updated_at
- **Album** — id, name, price, release_date, artist_id, cover_image_url, created_at, updated_at
- **AlbumGenre** — album_id, genre_id (many-to-many)
- **Track** — id, name, date, album_id, created_at
- **Playlist** — id, user_id, name, created_at
- **PlaylistTrack** — id, playlist_id, track_id, created_at (many-to-many with ordering)
- **Purchase** — id, user_id, album_id, purchase_date, amount_paid
- **Rating** — id, user_id, album_id, rating (1–5), created_at, updated_at

## Running Tests

### Backend Tests (pytest)
```bash
cd backend
pytest                          # Run all tests
pytest tests/unit/               # Unit tests only
pytest tests/integration/         # Integration tests only
pytest --cov=app                  # With coverage
```

**Test coverage:**
- Unit: security, schemas, S3 service
- Integration: auth, artists, albums, tracks, genres, playlists, purchases, ratings, upload endpoints

### Frontend Tests (Vitest)
```bash
cd frontend
yarn test                         # Run all tests
yarn test --run                    # Run once (CI mode)
```

**Test coverage:**
- `LoginPage.test.tsx` — Login/register form validation and submission
- `useApi.test.ts` — API hook tests
- `client.test.ts` — HTTP client tests
- `AuthContext.test.tsx` — Auth context provider tests
- `Logo.test.tsx` — Logo component tests
- `ImageUpload.test.tsx` — Image upload component tests

## S3 Image Upload

Admin users can upload artist photos and album cover images via the Management page. Images are stored in the configured S3 bucket. The `folder` parameter in the upload endpoint determines the S3 key prefix (e.g., `artists/`, `albums/`).

**Configuration:**
1. Create an S3 bucket (e.g., `music-marketplace-images`)
2. Add your AWS credentials to `backend/.env`
3. Uploaded images return a public URL stored in the database

## Developer
Igor J.L. Ndiramiye
