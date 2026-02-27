# Copilot Instructions - TripDetails

> **Maintain this file** - update it whenever new features are added or architecture changes.

## Project Overview

TripDetails is a Django application for managing sightseeing trips with destinations, photos, and driving directions.

## Tech Stack

- **Django 6.0** on **Python 3.14+**
- **Poetry** for dependency management
- **SQLite** database
- **Bootstrap 5.3** vendored locally in `static/vendor/bootstrap/` (NO CDN links)
- **OpenRouteService** API for geocoding and routing
- **WhiteNoise** for static file serving
- **django-environ** for configuration via `.env` file

## Project Structure

- Repo directory: `trip-details/` (hyphen - filesystem only)
- Django settings package: `trip_details/` (underscore - Python import)
- App: `destinations/` ✅ created
- All templates go in the **project-level** `templates/` directory (NOT inside the app)
- Migrations are excluded from ruff linting (`*/migrations/*.py`)

## Key Design Decisions

- **Single-user app** - no authentication required
- **Class-based views** throughout
- **All distances stored in kilometers** in the database (3 decimal places for precision)
- **Display unit** controlled by `settings.DISTANCE_UNIT` (`km` or `miles`)
- **Conversion** uses `settings.KM_TO_MILES = 0.621371`
- **UI rounding**: 1 decimal place for all displayed distances
- **Template tag** `format_distance` handles the km-to-miles conversion and rounding for display
- **Template tag** `format_duration` formats minutes into human-readable strings
- **Bootstrap is vendored locally** - never use CDN links; reference via `{% static 'vendor/bootstrap/...' %}`
- **Offline-first**: all data persisted in SQLite; only geocoding and route fetching need internet
- **Images stored locally** in `MEDIA_ROOT`
- **Destinations ordered** by `sort_order` then `created_at`; drag-and-drop reordering deferred

## Models ✅ Created in `destinations` app

- **Trip** - `name`, `description`, `created_at`, `updated_at`
  - `__str__`: returns `name`
  - Default ordering: `-created_at`
- **Destination** - FK to Trip (`related_name='destinations'`), `name`, `description`, `address`, `latitude`, `longitude`, `sort_order`, `created_at`, `updated_at`
  - `__str__`: returns `name`
  - Default ordering: `['sort_order', 'created_at']`
- **DestinationImage** - FK to Destination (`related_name='images'`), `image` (ImageField, `upload_to='destinations/'`), `is_primary`, `caption`, `sort_order`
  - `__str__`: returns caption or `"Image for {destination.name}"`
- **DestinationDistance** - `from_destination` FK (`related_name='distances_from'`), `to_destination` FK (`related_name='distances_to'`), `haversine_distance_km`, `driving_distance_km`, `driving_duration_minutes`, `directions_json` (JSONField)
  - `UniqueConstraint` on `(from_destination, to_destination)` named `unique_destination_pair`
  - `__str__`: returns `"From → To"`

## Settings Notes

- `STATIC_ROOT = BASE_DIR / 'staticfiles'` — required by WhiteNoise's `CompressedManifestStaticFilesStorage`
- `staticfiles/` and `media/` are in `.gitignore`
- WhiteNoise does **not** serve media files; dev media serving uses `django.conf.urls.static`

## Code Style

- **Linting/formatting**: ruff
- **Testing**: pytest with pytest-django
- **Configuration**: django-environ, all secrets in `.env`
- Migrations are excluded from ruff lint rules

## Development Commands

Use `make <target>` - see Makefile for all targets.

