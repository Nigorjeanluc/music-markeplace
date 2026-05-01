# Music Marketplace API - Endpoints & Services Documentation

## Overview

The backend provides a RESTful API for a music marketplace with authentication, artist/album/track management, playlists, purchases, and ratings. All endpoints are prefixed with `/api/v1`.

---

## 1. Authentication Endpoints (`/api/v1/auth/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/register` | POST | Public | Register a new user |
| `/login` | POST | Public | Login and get JWT tokens |
| `/refresh` | POST | Public | Refresh access token |
| `/me` | GET | Authenticated | Get current user profile |

### AuthService Logic

| Method | Logic |
|--------|-------|
| `register(user_in)` | Checks if email/username exists → hashes password with bcrypt → creates user → returns (user, tokens) |
| `login(user_in)` | Verifies email/password → returns (user, tokens) or None if invalid |
| `refresh_token(token_in)` | Decodes refresh token → validates type is "refresh" → creates new (access, refresh) tokens |
| `get_current_user_response(user)` | Converts User model to UserResponse schema (id as string) |

### Schemas
- `UserCreate`: email, username, password, avatar_url (optional)
- `UserLogin`: email, password
- `UserResponse`: id (str), email, username, avatar_url, is_admin, is_active, created_at
- `Token`: access_token, refresh_token, token_type
- `TokenRefresh`: refresh_token

---

## 2. Artists Endpoints (`/api/v1/artists/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | GET | Public | List artists with optional search |
| `/{artist_id}` | GET | Public | Get artist detail + album count |
| `/` | POST | Admin only | Create new artist |
| `/{artist_id}` | PUT | Admin only | Update artist |
| `/{artist_id}` | DELETE | Admin only | Delete artist |

### ArtistService Logic

| Method | Logic |
|--------|-------|
| `get_artists(skip, limit, search)` | Queries all artists → optional search by `performing_name` → returns list of (artist, album_count) tuples |
| `get_artist(artist_id)` | Finds artist by ID → returns (artist, album_count) tuple or None |
| `create_artist(artist_in)` | Checks for duplicate `performing_name` → creates artist → returns artist or None if duplicate |
| `update_artist(artist_id, artist_in)` | Gets artist tuple → extracts artist obj → updates fields using `model_dump(exclude_unset=True)` |
| `delete_artist(artist_id)` | Finds and deletes artist → returns True/False |

### Schemas
- `ArtistCreate`: real_name, performing_name, date_of_birth, photo_url (optional)
- `ArtistUpdate`: real_name (optional), performing_name (optional), date_of_birth (optional)
- `ArtistResponse`: id, real_name, performing_name, date_of_birth, photo_url, created_at, album_count

---

## 3. Albums Endpoints (`/api/v1/albums/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | GET | Public | List albums with filters (artist, genre, search) |
| `/{album_id}` | GET | Public | Get album detail + average rating + genre names |
| `/` | POST | Admin only | Create album with genre associations |
| `/{album_id}` | PUT | Admin only | Update album + genre associations |
| `/{album_id}` | DELETE | Admin only | Delete album |

### AlbumService Logic

| Method | Logic |
|--------|-------|
| `get_albums(skip, limit, artist_id, genre, search)` | Queries albums with filters → computes average rating (from purchasers only) using subquery joining Rating + Purchase → gets genre names via AlbumGenre → returns (album, avg_rating, genre_names, artist) tuples |
| `get_album(album_id)` | Same as above for single album |
| `create_album(album_in)` | Verifies artist exists → creates album → flushes to get ID → adds genre associations to AlbumGenre table |
| `update_album(album_id, album_in)` | Updates album fields → replaces genre associations if provided |
| `delete_album(album_id)` | Deletes album (cascade deletes AlbumGenre entries) → returns True/False |

### Schemas
- `AlbumCreate`: name, price, release_date (optional), artist_id, genre_ids (list), cover_image_url (optional)
- `AlbumUpdate`: name (optional), price (optional), release_date (optional), genre_ids (optional)
- `AlbumResponse`: id, name, price, release_date, artist_id, artist_name, rating, genre_names, cover_image_url, created_at, updated_at

---

## 4. Tracks Endpoints (`/api/v1/tracks/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | GET | Public | List tracks with album/genre filters |
| `/{track_id}` | GET | Public | Get track detail |
| `/` | POST | Admin only | Create track |
| `/{track_id}` | PUT | Admin only | Update track |
| `/{track_id}` | DELETE | Admin only | Delete track |

### TrackService Logic

| Method | Logic |
|--------|-------|
| `get_tracks(skip, limit, album_id, search)` | Queries tracks → filters by album_id (validates UUID) or search term → returns track list |
| `get_track(track_id)` | Finds track by ID → returns track or None |
| `create_track(track_in)` | Verifies album exists → creates track → returns track or None |
| `update_track(track_id, track_in)` | Updates track fields using `model_dump(exclude_unset=True)` |
| `delete_track(track_id)` | Deletes track → returns True/False |

### Schemas
- `TrackCreate`: name, date, album_id
- `TrackUpdate`: name (optional), date (optional), album_id (optional)
- `TrackResponse`: id, name, date, album_id, created_at

---

## 5. Genres Endpoints (`/api/v1/genres/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | GET | Public | List all genres |
| `/{genre_id}` | GET | Public | Get genre detail |
| `/` | POST | Admin only | Create new genre |
| `/{genre_id}` | PUT | Admin only | Update genre |
| `/{genre_id}` | DELETE | Admin only | Delete genre |

### GenreService Logic

| Method | Logic |
|--------|-------|
| `get_genres(skip, limit, search)` | Queries genres → optional search by name → ordered by name |
| `get_genre(genre_id)` | Finds genre by ID → returns genre or None |
| `create_genre(genre_in)` | Creates genre → returns genre |
| `update_genre(genre_id, genre_in)` | Updates fields using `model_dump(exclude_unset=True)` |
| `delete_genre(genre_id)` | Deletes genre → returns True/False |

### Schemas
- `GenreCreate`: name, description (optional)
- `GenreUpdate`: name (optional), description (optional)
- `GenreResponse`: id, name, description, created_at, updated_at

---

## 6. Playlists Endpoints (`/api/v1/playlists/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | GET | Authenticated | List user's playlists |
| `/{playlist_id}` | GET | Owner only | Get playlist + tracks |
| `/` | POST | Authenticated | Create playlist with optional tracks |
| `/{playlist_id}` | PUT | Owner only | Update playlist name |
| `/{playlist_id}` | DELETE | Owner only | Delete playlist |
| `/{playlist_id}/tracks` | POST | Owner only | Add track to playlist |
| `/{playlist_id}/tracks/{track_id}` | DELETE | Owner only | Remove track from playlist |

### PlaylistService Logic

| Method | Logic |
|--------|-------|
| `get_playlists(user_id)` | Gets all playlists for a user |
| `get_playlist(playlist_id, user_id)` | Gets playlist by ID, ensuring it belongs to the user |
| `create_playlist(playlist_in, user_id)` | Creates playlist → optionally adds tracks (validates UUIDs, checks track exists) → rolls back if any track invalid |
| `update_playlist(playlist_id, playlist_in, user_id)` | Updates playlist name only |
| `delete_playlist(playlist_id, user_id)` | Deletes playlist (cascade deletes PlaylistTrack entries) |
| `add_track_to_playlist(playlist_id, track_id, user_id)` | Checks track not already in playlist → adds to PlaylistTrack table |
| `remove_track_from_playlist(playlist_id, track_id, user_id)` | Removes track from PlaylistTrack table |
| `build_playlist_response(playlist, include_tracks)` | Builds response with track count or full track details |

### Schemas
- `PlaylistCreate`: name, track_ids (list)
- `PlaylistUpdate`: name (optional)
- `PlaylistResponse`: id, name, created_at, track_count
- `PlaylistDetailResponse`: id, name, created_at, track_count, tracks
- `PlaylistTrackAdd`: track_id
- `TrackInPlaylist`: id, name, date, album_name, artist_name

---

## 7. Purchases Endpoints (`/api/v1/purchases/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | POST | Authenticated | Purchase an album |
| `/me/library` | GET | Authenticated | Get user's purchased albums |

### PurchaseService Logic

| Method | Logic |
|--------|-------|
| `create_purchase(user_id, purchase_in)` | Verifies album exists → creates purchase record with album price → handles duplicate purchase (IntegrityError) → returns purchase or None |
| `get_user_purchases(user_id)` | Gets all user's purchases → joins album + artist info → gets user's rating + average rating for each album |
| `build_purchase_response(purchase, album, artist)` | Builds PurchaseResponse from purchase + album + artist |
| `build_purchase_response_with_ratings(...)` | Extended response including user's rating and average rating |

### Schemas
- `PurchaseCreate`: album_id
- `PurchaseResponse`: id, album_id, album_name, artist_name, purchase_date, amount_paid

---

## 8. Ratings Endpoints (`/api/v1/ratings/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | POST | Authenticated | Rate album (must have purchased) |
| `/{album_id}` | PUT | Authenticated | Update your rating |
| `/me` | GET | Authenticated | Get your ratings |
| `/album/{album_id}` | GET | Public | Get all ratings for album |

### RatingService Logic

| Method | Logic |
|--------|-------|
| `create_or_update_rating(user_id, rating_in)` | Verifies album exists → verifies user purchased album → validates rating 1-5 → upserts (updates if exists, creates if not) → computes average rating from all purchasers |
| `update_rating(user_id, album_id, rating_in)` | Finds existing rating → validates 1-5 → updates → computes average |
| `get_user_ratings(user_id)` | Gets all user's ratings → joins album info + average rating |
| `get_album_ratings(album_id)` | Gets all ratings for album → computes average → returns with album info |
| `build_rating_response(rating, album_name, avg_rating)` | Builds RatingResponse |

### Schemas
- `RatingCreate`: album_id, rating (1-5)
- `RatingUpdate`: rating (1-5)
- `RatingResponse`: album_id, album_name, user_rating, avg_rating, created_at

---

## 9. Upload Endpoint (`/api/v1/upload/`)

### Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | POST | Admin only | Upload image to S3 |

### Upload Logic

| Method | Logic |
|--------|-------|
| `upload_image(file, folder, current_user)` | Validates file is image (content_type starts with "image/") → generates unique filename using UUID → uploads to S3 via S3Service → returns `{"url": s3_url}` |

### S3Service Logic

| Method | Logic |
|--------|-------|
| `upload_file(file_obj, file_name, content_type)` | Uploads file to S3 bucket → returns public URL (custom domain or S3 URL) or None on failure |
| `delete_file(file_name)` | Deletes file from S3 bucket → returns True/False |

### Schemas
- No request schema (uses `UploadFile` and `File` from FastAPI)
- Response: `{"url": str}` - the S3 public URL of the uploaded image

### S3 Configuration (in `.env`)
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=music-marketplace-images
AWS_S3_REGION=us-east-1
AWS_S3_CUSTOM_DOMAIN=  # Optional CDN URL
```

---

## Key Patterns Used

### 1. UUID Validation
All endpoints validate UUIDs before querying the database using `is_valid_uuid()` from `app/core/uuid_utils.py`. Invalid UUIDs return `None` or `404` early.

### 2. Upsert Pattern (Ratings)
The rating service checks for existing records before inserting:
```python
existing = self.db.query(Rating).filter(...).first()
if existing:
    existing.rating = rating_in.rating
else:
    # create new
```

### 3. Tuple Returns
Services return tuples like `(model, related_data)` to avoid extra queries:
- Artist service: `(artist, album_count)`
- Album service: `(album, avg_rating, genre_names, artist)`
- Rating service: `(rating, avg_rating)`

### 4. Subquery for Aggregates
Album rating uses SQLAlchemy subquery joining Rating + Purchase (only purchasers can rate):
```python
select(func.avg(Rating.rating))
    .join(Purchase, ...)
    .where(Rating.album_id == Album.id)
    .correlate(Album)
    .scalar_subquery()
```

### 5. Partial Updates
Update methods use `model_dump(exclude_unset=True)` to only change provided fields:
```python
update_data = schema.model_dump(exclude_unset=True)
for field, value in update_data.items():
    setattr(obj, field, value)
```

### 6. Cascade Deletes
- Playlist → PlaylistTrack (via SQLAlchemy relationships)
- Album → AlbumGenre (via SQLAlchemy relationships)

### 7. Admin-Only Protection
Endpoints that modify data use `get_current_admin_user` dependency:
```python
current_user = Depends(get_current_admin_user)
```

### 8. Owner-Only Access (Playlists)
Playlist endpoints verify the playlist belongs to the authenticated user:
```python
playlist = self.db.query(Playlist).filter(
    Playlist.id == playlist_id,
    Playlist.user_id == user_id
).first()
```

---

## Database Models

| Model | Key Fields | Relationships |
|-------|------------|---------------|
| User | id, email, username, avatar_url, hashed_password, is_admin, is_active | purchases, ratings, playlists |
| Artist | id, real_name, performing_name, date_of_birth, photo_url | albums |
| Album | id, name, price, release_date, artist_id, cover_image_url | artist, ratings, purchases, genres |
| Track | id, name, date, album_id | album |
| Genre | id, name, description | albums (via AlbumGenre) |
| AlbumGenre | album_id, genre_id | links albums to genres |
| Playlist | id, name, user_id | user, tracks (via PlaylistTrack) |
| PlaylistTrack | playlist_id, track_id | links playlists to tracks |
| Purchase | id, user_id, album_id, amount_paid | user, album |
| Rating | id, user_id, album_id, rating | user, album |

---

## Test Coverage

- **171 tests passing** (148 integration + 23 unit) with 0 warnings
- **Unit tests**: Schema validation, security (password hashing, JWT tokens), S3Service
- **Integration tests**: Service layer (CRUD operations), API endpoints (HTTP responses), upload endpoint
- **Fixtures**: `db_session` (function-scoped), `client` (TestClient), `normal_user`, `admin_user`, `user_token`, `admin_token`
