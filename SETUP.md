# 🚀 Setup & Installation Guide

Welcome to the **Multi-Cloud College Management & Student Services Platform**! This guide will walk you through setting up the project on your local machine for development and testing.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your system:

| Prerequisite | Version | Download Link |
| :--- | :--- | :--- |
| **Python** | 3.11 or higher | [Download Python](https://www.python.org/downloads/) |
| **Node.js** | 20.x or higher | [Download Node.js](https://nodejs.org/) |
| **Git** | Latest | [Download Git](https://git-scm.com/downloads) |
| **Docker** (Optional) | Latest | [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) |

---

## ⚡ Step-by-Step Local Setup

You can run the application either directly on your host machine or using Docker Compose.

### Option A: Local Development (Recommended for Coding)

#### 1. Clone the Repository
```bash
git clone https://github.com/Mrinmoypatratint/multi-cloud-college-platform.git
cd multi-cloud-college-platform
```

#### 2. Backend Setup (Django API)
Open a new terminal window for the backend:

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply database migrations
python manage.py migrate

# 6. Seed the database with demo data (Important!)
python manage.py seed_data

# 7. Start the Django development server (running on port 8000 or 8001)
python manage.py runserver 8001
```

> [!TIP]
> **Why port 8001?** If port 8000 is occupied by another service on your machine, running on 8001 ensures the backend starts successfully.

#### 3. Frontend Setup (React Vite)
Open a second terminal window for the frontend:

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install Node.js dependencies
npm install

# 3. Start the Vite development server
npm run dev
```
> [!NOTE]
> The frontend will typically start on `http://localhost:3000`.

---

### Option B: Docker Compose Setup

If you prefer a fully containerized environment without installing Python and Node locally:

```bash
# 1. Ensure Docker Desktop is running
# 2. Build and start the containers in detached mode
docker-compose -f docker/docker-compose.yml up --build -d
```
> [!NOTE]
> This will start the PostgreSQL database, the Django backend, and the React frontend via Nginx.

---

## 🔑 Demo Accounts

Once the servers are running, access the frontend at `http://localhost:3000` and use the following credentials to explore the different role-based views:

| Role | Username | Password | What they can do |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `superadmin` | `admin123` | Full system access, audit logs, user management. |
| **College Admin** | `collegeadmin` | `admin123` | Manage courses, departments, academic catalog. |
| **Faculty** | `dr_smith` | `admin123` | Mark attendance, view assigned courses. |
| **Staff** | `staff_john` | `admin123` | Manage notices, register students. |
| **Student** | `alice_student` | `admin123` | View attendance, timetable, notices. |

---

## 🛑 Stopping the Servers

- **Local Setup**: Press `Ctrl + C` in both the frontend and backend terminal windows.
- **Docker Setup**: Run `docker-compose -f docker/docker-compose.yml down` to stop and remove the containers.

---

## ❓ Need Help?
If you encounter any issues during setup, please refer to our [Troubleshooting Guide](docs/TROUBLESHOOTING.md) or open an issue on GitHub!
