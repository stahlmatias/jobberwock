# Jobberwocky Deployment Guide

## Requirements
- Docker
- Docker Compose

## How to Deploy (Local Dev)

```bash
# Step 1: Clone the repository
$ git clone https://github.com/stahlmatias/jobberwock.git
$ cd jobberwocky

# Step 2: Build and run with Docker Compose
$ docker-compose up --build
```

Once running, the API will be available at:
```
http://localhost:8000/docs
```

---

## Logs
- Console output
- File: `logs/jobberwocky.log`

---

## Stopping Services
To shut down all containers:
```bash
docker-compose down
```

---

## Deployment Strategy

This project is prepared for local deployment using Docker Compose. For cloud deployment:

- **Platform**: Any Docker-compatible platform (e.g., AWS ECS, DigitalOcean, GCP Cloud Run).
- **Options**:
  - Use container registry (e.g., Docker Hub or GitHub Container Registry).
  - Add CI/CD with GitHub Actions to build and deploy.
  - Extend `docker-compose.yml` or translate to `k8s` manifests for production scale.

---

## Tests

To run all tests inside the container:
```bash
docker-compose exec jobberwocky pytest
```

For local (non-Docker) testing:
```bash
pip install -r requirements.txt
pytest
```



