## 🧡 Orange Mittai – Full Stack Application

Orange Mittai is a full-stack e-commerce application built with:

* **Backend**: FastAPI + SQLAlchemy
* **Frontend**: Vue 3 + Vite (JavaScript)
* **Database**:

    * Local: SQLite
    * Production: Cloud SQL (PostgreSQL, IAM authentication)
* **Deployment**: Google Cloud Run

This document explains how to **run the backend and frontend locally**, how environment variables are managed, and how the app runs in **production**.

---

## 📁 Repository Structure

```
orange-mittai/
├── backend/        # FastAPI backend
├── frontend/       # Vue + Vite frontend
└── README.md
```

---

# 🐍 Python Version Management (pyenv)

The backend requires **Python 3.10 or 3.11**.

We strongly recommend using **pyenv** to manage Python versions.

---

## Why pyenv?

* Install multiple Python versions side-by-side
* Match production Python exactly
* Avoid OS Python conflicts
* Per-project Python version control

---

## 1️⃣ Install pyenv

### macOS (Homebrew)

```bash
brew update
brew install pyenv
```

Add pyenv to your shell (`~/.zshrc` or `~/.bashrc`):

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Restart terminal:

```bash
exec "$SHELL"
```

---

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y \
  build-essential curl libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev \
  libffi-dev liblzma-dev
```

Install pyenv:

```bash
curl https://pyenv.run | bash
```

Add to shell config:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Restart shell.

---

## 2️⃣ Install required Python version

```bash
pyenv install 3.11.7
pyenv local 3.11.7
```

Verify:

```bash
python --version
```

---

# 🔧 Backend (FastAPI)

## 📍 Location

```
backend/
```

---

## 1️⃣ Create & activate virtual environment

From the `backend/` directory:

```bash
cd backend
python -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

## 2️⃣ Install backend dependencies

```bash
pip install -r requirements.txt
```

Key dependencies:

* fastapi
* uvicorn
* sqlalchemy
* psycopg2-binary
* cloud-sql-python-connector

---

## 3️⃣ Backend environment variables (Local)

Local development uses **SQLite** by default.

Optional `backend/.env`:

```env
DATABASE_MODE=local
LOCAL_DATABASE_URL=sqlite:///./local.db
```

If not set, SQLite is used automatically.

---

## 4️⃣ Run backend locally

⚠️ Always run uvicorn via Python:

```bash
python -m uvicorn app.main:app --reload
```

Backend URLs:

* API: [http://localhost:8000](http://localhost:8000)
* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* Health: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 5️⃣ Backend – Production (Cloud Run)

In production:

* Database: Cloud SQL (PostgreSQL)
* Auth: IAM (Service Account)
* No DB passwords

### Cloud Run environment variables

```env
DATABASE_MODE=cloud
DB_NAME=orange_mittai
DB_USER=orange-mittai-backend@PROJECT_ID.iam.gserviceaccount.com
INSTANCE_CONNECTION_NAME=PROJECT_ID:REGION:INSTANCE_NAME
```

Backend production URL:

```
https://orange-mittai-backend-xxxxx.a.run.app
```

---

# 🎨 Frontend (Vue + Vite – JavaScript)

## 📍 Location

```
frontend/
```

---

## Requirements

* **Node.js 18+**
* npm

Check:

```bash
node --version
npm --version
```

---

## 1️⃣ Install frontend dependencies

```bash
cd frontend
npm install
```

---

## 2️⃣ Frontend environment variables

### Local development

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Used by:

```bash
npm run dev
```

---

### Production build

Create `frontend/.env.production`:

```env
VITE_API_BASE_URL=https://orange-mittai-backend-xxxxx.a.run.app
```

⚠️ Important:

* Vite injects env vars at **build time**
* Cloud Run runtime env vars do **not** affect static builds

---

## 3️⃣ Run frontend locally

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 4️⃣ Build frontend for production

```bash
npm run build
```

Build output:

```
frontend/dist/
```

---

## 5️⃣ Axios API configuration (example)

```js
import axios from "axios";
import { API_BASE_URL } from "@/config/api";

const axiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
});

export default axiosInstance;
```

---

# 🌍 Local vs Production Overview

| Component | Local                                          | Production             |
| --------- | ---------------------------------------------- | ---------------------- |
| Frontend  | [http://localhost:5173](http://localhost:5173) | Cloud Run frontend URL |
| Backend   | [http://localhost:8000](http://localhost:8000) | Cloud Run backend URL  |
| Database  | SQLite (`local.db`)                            | Cloud SQL (Postgres)   |
| DB Auth   | None                                           | IAM (Service Account)  |

---

# 🧠 Key Notes & Best Practices

* `.env` files must live at **project root** of frontend/backend
* Frontend env vars **must start with `VITE_`**
* Frontend API URL is **build-time only**
* Backend switches DB using `DATABASE_MODE`
* Never hardcode URLs or secrets
* Always use `python -m uvicorn`

---

## ✅ Common Commands Summary

### Backend

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
npm run build
```

---

## 🚀 You’re All Set

This setup provides:

* Clean local development
* Secure production deployment
* IAM-based database access
* Zero secrets in code--platform=linux/amd64
* Zero secrets in code--platform=linux/amd64
* Clear environment separation

Backend – Build with linux/amd64

From repo root (or backend/ if Dockerfile lives there):

docker build \
--platform=linux/amd64 \
-t orange-mittai-backend \
./backend


Or with Google Container Registry / Artifact Registry:

docker build \
--platform=linux/amd64 \
-t REGION-docker.pkg.dev/PROJECT_ID/REPO/orange-mittai-backend:latest \
./backend

✅ Frontend – Build with linux/amd64
docker build \
--platform=linux/amd64 \
-t orange-mittai-frontend \
./frontend


gcloud alpha sql connect orange-mittai-instance \
--database=orange_mittai \
--user=$(gcloud config get account) \
--auto-iam-authn

