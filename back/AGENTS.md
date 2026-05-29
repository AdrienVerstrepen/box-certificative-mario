# AGENTS.md – Back-End

## Project Overview

This is the back-end of the **Travel Planning** application, built with **Python** and **Flask**. It exposes a REST API consumed by the Vue front-end, handles authentication, interacts with the database, and delegates tour computation to the `algorithm/` module.

---

## Directory Structure

```
back/
├── app.py            # Flask application factory and startup
├── connexion.py      # Database connection setup
├── routes/
│   ├── __init__.py   # Blueprint registration
│   ├── tour.py       # Tour endpoints (create, read, share)
│   └── user.py       # User/auth endpoints (register, login, logout)
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container definition
├── venv/             # Python virtual environment
└── README.md         # Back-end specific notes

algorithm/            # Standalone planning algorithm module
├── algorithm_structure.py  # Main algorithm entry point
├── dynamic.py              # Dynamic programming logic
├── graph_locations.py      # Graph construction from locations
├── location.py             # Location data model and distance formula
├── nearest_neighbours.py   # Nearest-neighbour heuristic
└── tests/
    └── location_test.py    # Unit tests for algorithm logic
```

---

## Key Conventions

### Language
All code, comments, docstrings, and variable names must be written in **English**.

### API Design
- All endpoints return **JSON**.
- Use appropriate HTTP status codes: `200`, `201`, `400`, `401`, `403`, `404`, `409`, `500`.
- Prefix all routes with `/api` (e.g., `/api/tours`, `/api/login`, `/api/register`, `/api/places`).
- Routes are grouped in Flask **Blueprints** inside `routes/` (for user management) and in `app.py` for global endpoints.

### Authentication & Passwords
- All passwords are encrypted securely using **Werkzeug's security module** (`generate_password_hash` and `check_password_hash`).
- **Registration**: Passwords are saved as secure pbkdf2/scrypt hashes. Plain text passwords must never be stored.
- **Login/Legacy Migration**: The server supports legacy plain text passwords in the DB (`alice`, `bob`, `charlie` default values) and automatically **upgrades them to secure Werkzeug hashes** in the DB on successful login.
- Every endpoint that accesses user data must verify the identity of the requester.
- A user must only be able to access their own tours.

### Tour Sharing & Deduplication
- Tours have a `visibility` field: `"public"` or `"private"`.
- When custom itineraries are saved, places are **deduplicated** by name and coordinate range prior to insertion to protect database storage space, while maintaining a clean stages sequence history.

---

## Running the Project

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

Or with Docker:

```bash
docker-compose up --build
```

---

## Environment Variables

Sensitive configuration (DB credentials, secret key) must be provided via environment variables, not hard-coded:

```
DB_HOST=...
DB_USER=...
DB_PASSWORD=...
DB_NAME=...
```

---

## Do / Do Not

| Do | Do Not |
|---|---|
| Group routes in Blueprints | Put all routes in `app.py` |
| Validate input before processing | Trust client-supplied data |
| Return structured JSON errors | Return plain-text error strings |
| Hash all passwords securely | Store plain-text passwords in DB |
| Use environment variables for secrets | Hard-code credentials |
| Write docstrings on all functions | Leave functions undocumented |