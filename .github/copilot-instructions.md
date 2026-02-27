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
- App: `destinations/` (to be created)

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

## Models (to be created in `destinations` app)

- **Trip** - name, description, timestamps
- **Destination** - FK to Trip, name, description, address, lat, lon, timestamps
- **DestinationImage** - FK to Destination, image file, is_primary, caption, sort_order
- **DestinationDistance** - from_destination, to_destination, haversine_distance_km, driving_distance_km, driving_duration_minutes, directions_json (JSONField)

## Code Style

- **Linting/formatting**: ruff
- **Testing**: pytest with pytest-django
- **Configuration**: django-environ, all secrets in `.env`

## Development Commands

Use `make <target>` - see Makefile for all targets.

