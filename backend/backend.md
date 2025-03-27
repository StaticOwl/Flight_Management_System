# 🖥️ Backend

This is the backend component. It is built with **Python 3.12**, **Flask**, and **PostgreSQL**.

---

## 🚀 Setup Options

You can run the backend in two ways:

---

### 🖁 Option 1: Podman + Docker Setup (Recommended)

This method uses **Podman** to create isolated containers for PostgreSQL and the Flask backend.

#### ✅ Prerequisites
- [Podman](https://podman.io/getting-started/installation)
- PostgreSQL is handled in a container, no need for a native install
- Docker-compatible CLI via Podman

#### ⚙️ Steps

1. **Clone the repository** (if not done):
   ```bash
   git clone <repo_url>
   cd backend
   ```

2. **Create a `.env` file if it's not present already**
   Inside `backend/envs/dev.env`, add:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=flight_db
   POSTGRES_HOST=flight_db
   POSTGRES_PORT=5432
   FLASK_ENV=dev
   ```

3. **Run setup:**
   ```bash
   ./setup.sh full
   ```

   This will:
   >- Spin up a PostgreSQL container
   >- Apply DDLs from `ddl/init_ddl/`
   >- Build and run the Flask app in a container
   >- Automatically inject environment variables
   >- Expose the app on `http://localhost:5000`

#### ⚡ Run Specific Parts
If you want to **skip some steps** and only run specific parts, you can use:

| Command | Action |
|---------|--------|
| `./setup.sh podman` | Setup Podman & Network |
| `./setup.sh db` | Setup PostgreSQL Database |
| `./setup.sh seed` | Apply database schema |
| `./setup.sh backend` | Deploy Flask backend |
| `./setup.sh status` | Check running containers |

---

### 🤖 Option 2: Standalone Setup (Without Containers)

You can run the backend directly using native **Python** and **PostgreSQL** — no containers involved.

---

### ✅ Prerequisites

- [Miniforge](https://github.com/conda-forge/miniforge) / Miniconda / Anaconda
- PostgreSQL installed and running locally

---

### ⚙️ Steps

1. **Create a Conda environment using `environment.yml`:**
   ```bash
   conda env create -f environment.yml
   conda activate flights
   ```

2. **Set up PostgreSQL database:**
   - Create a database (e.g., `flight_db`)
   - Apply the schema:
     ```bash
     psql -U postgres -d flight_db -f ddl/init_ddl/MAKE_TABLES.sql
     psql -U postgres -d flight_db -f ddl/init_ddl/DDL.sql
     ```

3. **Setup environment Variables**
   ```bash
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=postgres
   export POSTGRES_DB=flight_db
   export POSTGRES_HOST=flight_db
   export POSTGRES_PORT=5432
   export FLASK_ENV=dev
   ```

4. **Run the backend app:**
   ```bash
   python app.py
   ```

---

### 🧪 Run Backend Tests

```bash
cd backend/src/tests
pytest -s
```

## 🔗 Available API Endpoints

Below is a list of key backend API routes and their purposes:

### 🧑‍🎓 User APIs
| Endpoint | Method | Description |
|--------------------------|--------|--------------------------------|
| `/createuser` | POST | Register a new user |
| `/login` | POST | Log in and receive JWT token |
| `/users` | GET | Get current user profile (Auth) |
| `/users` | PUT | Update user profile (Auth) |
| `/users/<user_id>/delete` | DELETE | Delete a user |
| `/token` | GET | Get user ID from token |
| `/gettoken/<user_id>` | GET | Generate token for user ID |

---

### 🛋 Booking APIs
| Endpoint | Method | Description |
|----------------------|------------|-------------------------------|
| `/createbooking` | POST | Create a new booking |
| `/bookings/<booking_id>` | PUT, DELETE | Modify or cancel a booking |
| `/users/bookings` | GET | Get booking history for user |

---

### ✈️ Flight APIs
| Endpoint | Method | Description |
|--------------------------|------------|--------------------------------|
| `/createflights` | POST | Create new flight entry |
| `/flights/search` | GET | Search flights |
| `/flights` | GET | Fetch all flights |
| `/flights/<flight_id>/crew` | GET, PUT | Get or update assigned crew members |
| `/flights_by_airlines/<airline_id>` | GET | Get flights for specific airline |

---

### 🏢 Airline APIs
| Endpoint | Method | Description |
|------------------|--------|--------------------------------|
| `/airlines` | GET | Fetch all airlines |
| `/airlines/<airline_id>` | GET | Get airline dashboard data |

---

### 🤝 Crew & Role APIs
| Endpoint | Method | Description |
|----------------|--------|--------------------------------|
| `/getCrew` | GET | Get all crew members |
| `/addCrew` | POST | Add new crew member |
| `/update-crew/<crew_id>` | PUT | Update crew member details |
| `/roles` | GET | Get all crew roles |

---

### 🧪 System & Utility
| Endpoint | Method | Description |
|-----------------|--------|------------------------------------|
| `/dbstatus` | GET | Run auto-checks for all `/api/<Model>` |
| `/api/<Model>` | GET | Generic fetch for model data |

