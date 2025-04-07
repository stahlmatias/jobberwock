# Jobberwocky

Jobberwocky is a lightweight job posting service that aggregates job offers from internal sources and external providers. Companies can register new job opportunities, and candidates can search for relevant jobs based on optional filters. The system is designed with reliability, simplicity, and extensibility in mind.

## Design

- **Tech Stack**: FastAPI (REST), Python, Docker, in-memory storage.
- **Data Storage**: Internal jobs are kept in memory using a singleton storage layer (`memory.py`).
- **External Aggregation**: Supports external job sources with a mocked job API.
- **Caching**: External responses are cached using TTLCache to reduce redundant requests.

### Design Process
- Explored SQLite and CSV-based persistence but opted for in-memory storage to simplify the deployment and testing.
- Used REST for its universality and FastAPI for automatic documentation and ease of development.

### API Design
- RESTful endpoints with JSON payloads.
- OpenAPI schema available at `/docs`.

---

## Development

- **Methodology**: TDD (Test-Driven Development).
- **Tests**: Covered internal CRUD, external source integration, caching, and fallback logic.
- **Best Practices**:
  - Modular services (job, external, cache).
  - Separation of concerns.
  - Clean code using PEP8, SOLID principles.
  - Logging to console and file (`logs/jobberwocky.log`).

To run tests:
```bash
pytest
```

## Deployment

### Quick Start (Dev)
Make sure Docker and Docker Compose are installed.

```bash
docker-compose up --build
```

API will be available at:
```
http://localhost:8000/docs
```

---

## Project Structure

```
.
├── app
│   ├── api/              # API routes
│   ├── logger_config.py  # Logging config
│   ├── main.py           # Entry point
│   ├── schemas.py        # Pydantic models
│   ├── services/
│   │   ├── cache.py
│   │   ├── external_sources.py
│   │   └── job_service.py
│   ├── storage/memory.py # In-memory job store
│   └── utils/xml_parser.py
├── jobberwocky-extra-source-v2/  # Mock external source
├── logs/jobberwocky.log
├── tests/                # Unit tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── ci.yml
└── RELEASE.md
```

## External Job Source
The project includes a mock job source under `jobberwocky-extra-source-v2/`, also Dockerized for integration testing.

