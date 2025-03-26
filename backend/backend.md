# 🖥️ Backend

This is the backend component. It is built with **Python 3.12**, **Flask**, and **PostgreSQL**.

---

## 🚀 Setup Options

You can run the backend in two ways:

---

### 🔁 Option 1: Podman + Docker Setup (Recommended)

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
   ./setup.sh dev
   ```

   This will:
   - Spin up a PostgreSQL container
   - Apply DDLs from `ddl/init_ddl/`
   - Build and run the Flask app in a container
   - Automatically inject environment variables
   - Expose the app on `http://localhost:5000`

---

### 🧪 Option 2: Standalone Setup (Without Containers)

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
