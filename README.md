# TripDetails

A Django application for managing sightseeing trips. Organize destinations with photos, view driving distances and step-by-step directions between sites. All distances are stored in kilometers and can be displayed in either km or miles via a configuration setting. Data is stored locally in SQLite for offline access after initial setup. The Bootstrap UI is vendored locally so no internet connection is required to use the application once set up.

## Features

- **Trip Management** - Create and organize trips with names and descriptions
- **Destination Management** - Add destinations with addresses, GPS coordinates, and geocoding support
- **Photo Gallery** - Upload multiple photos per destination with primary photo selection
- **Distance Calculation** - Automatic driving distance and straight-line (haversine) calculation between all destinations in a trip
- **Turn-by-Turn Directions** - Step-by-step driving directions stored locally for offline viewing
- **Configurable Units** - Display distances in kilometers or miles
- **Offline Capable** - All data persisted locally; works without internet after initial data entry

## Tech Stack

- Python 3.14+ / Django 6.0 / SQLite / Bootstrap 5.3 (vendored locally)
- OpenRouteService API / Poetry / WhiteNoise

## Prerequisites

- Python 3.14+
- [Poetry](https://python-poetry.org/docs/#installation)
- [OpenRouteService API key](https://openrouteservice.org/dev/#/signup) (free tier)

## Quick Start

```bash
git clone git@github.com:<your-username>/trip-details.git
cd trip-details
make setup
cp .env.example .env
# Edit .env and set ORS_API_KEY, optionally DISTANCE_UNIT=miles
make superuser
make run
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | (insecure default) | Django secret key |
| `DJANGO_DEBUG` | `True` | Debug mode |
| `ORS_API_KEY` | (empty) | OpenRouteService API key |
| `DISTANCE_UNIT` | `km` | Display unit: `km` or `miles` |

## Offline Usage

Internet is only needed for: initial `make bootstrap` (once), geocoding addresses, and fetching driving directions. Once data is saved, the app works fully offline.

## Development Notes

### Makefile Commands

| Command | Description |
|---|---|
| `make setup` | Install deps, download Bootstrap, migrate |
| `make run` | Start dev server |
| `make test` | Run tests (pytest) |
| `make lint` | Lint (ruff) |
| `make format` | Format (ruff) |
| `make migrate` | Apply migrations |
| `make makemigrations` | Generate migrations |
| `make shell` | Django shell |
| `make superuser` | Create admin user |
| `make clean` | Remove cache files |

## Technical Details

*To be expanded as the project develops.*

## License

MIT License - see [LICENSE](LICENSE) for details.

