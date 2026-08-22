# Python VPS Deployment Cookiecutter

A highly optimized, production-ready CI/CD and Docker setup for deploying Python apps (Django or FastAPI) + Celery + PgBouncer + Redis on ANY VPS (AWS EC2, DigitalOcean Droplet, Hostinger, etc.). 

Instead of configuring Docker, Nginx, Let's Encrypt, and GitHub Actions from scratch for every new project, this Starter Kit generates the entire architecture in seconds.

## 🚀 Features

* **Framework Agnostic:** Supports both **Django** and **FastAPI** projects out of the box.
* **Flexible Package Managers:** Choose between **uv**, **poetry**, or **pip** to match your existing workflow.
* **Zero-Downtime Deployments:** Docker containers gracefully recreate on GitHub Actions pushes.
* **Auto-SSL & Reverse Proxy:** Pre-configured Nginx templates with automatic Let's Encrypt SSL provisioning.
* **Built for Scale:** Includes `PgBouncer` for database connection pooling, and `Redis` + `Celery` for background tasks.
* **Multi-Tenant Ready:** Dynamically sets host ports so you can run multiple apps on the same VPS without port conflicts.
* **Safe Bind Mounts:** Maps static and media files to `/var/www/` instead of opaque Docker volumes to prevent Nginx permission issues.

## 📦 Prerequisites

You need `cookiecutter` installed on your machine:
```bash
pip install cookiecutter
```

You also need a VPS instance (Ubuntu recommended — e.g., AWS EC2, DigitalOcean, Hostinger) and a DockerHub account.

## 🛠️ Usage

This template can be used to start a new project from scratch or to add a deployment pipeline to an existing one.

### For a New Project

Run the command in the directory where you want your new project folder to be created. It will generate a new folder containing your deployment files, ready for you to start developing.

```bash
cookiecutter https://github.com/Nwafor6/vps-deployment-cookiecutter.git --checkout develop
```

### For an Existing Project

1.  Navigate (`cd`) into your project's root directory (the one with your `pyproject.toml` or `requirements.txt`).
2.  Run the `cookiecutter` command below. It will create a **new sub-folder** inside your project (e.g., `my-awesome-app/`).
3.  Move the generated files from this new sub-folder up into your project root.

```bash
cookiecutter https://github.com/Nwafor6/vps-deployment-cookiecutter.git --checkout develop
```

After it runs, move the generated files. For a `project_slug` of `my-awesome-app`, you would run:

```bash
# This moves all files (including hidden ones like .github) into your current directory
mv my-awesome-app/.[!.]* . && mv my-awesome-app/* . && rmdir my-awesome-app
```

You will be prompted to provide several variables:

* **`project_slug`**: The name of your project (e.g., `my-awesome-app`). This will be used for network names, container names, and Nginx configs.
* **`framework`**: Choose between `django` or `fastapi`.
* **`package_manager`**: Choose between `uv`, `poetry`, or `pip`.
* **`use_redis`**: Include Redis container? (`y` or `n`)
* **`use_celery`**: Include Celery worker and beat containers? (`y` or `n`)
* **`use_pgbouncer`**: Include PgBouncer connection pooler? (`y` or `n`)
* **`python_app_folder`**: The exact name of the folder containing your `settings.py` and `asgi.py` (e.g., `backend`, `core`, or `my_app`). Leave as default if using FastAPI.
* **`dev_domain`**: The domain for your development environment (e.g., `api-dev.example.com`).
* **`prod_domain`**: The domain for your production environment (e.g., `api.example.com`).
* **`email_for_ssl`**: The email address Let's Encrypt will use for SSL certificate expiration notices.
* **`dev_host_port`**: The port exposed to the VPS host for the DEV environment (e.g., `8002`).
* **`prod_host_port`**: The port exposed to the VPS host for the PROD environment (e.g., `8001`).

### What gets generated?
```
your_project/
├── .github/
│   └── workflows/
│       ├── deploy-dev.yml
│       └── deploy-prod.yml
├── Dockerfile
├── docker-compose.<slug>.dev.yml
├── docker-compose.<slug>.prod.yml
├── nginx-<slug>-dev.conf
└── nginx-<slug>-prod.conf
```

## ⚙️ GitHub Secrets Required

To make the CI/CD pipeline work automatically, add the following Secrets to your GitHub repository:

* **DockerHub**: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
* **VPS Access**: `EC2_HOST`, `EC2_HOST_PROD`, `EC2_USERNAME` (e.g., `ubuntu` or `root`), `SSH_PRIVATE_KEY` *(Note: The variable names contain 'EC2', but they work perfectly for any cloud provider)*
* **App Secrets**: `SECRET_KEY`, `DATABASE_URL` (Dev), `DATABASE_PROD_URL` (Prod)
* **Optional Integrations**: Any other environment variables your app requires (e.g., AWS S3 keys, AI provider keys). Edit the `.yml` files to pass these through to the `.env` generation step.

## 📖 Deployment Flow

1. Push your code to the `develop` or `main` branches.
2. GitHub Actions will build the Docker image using `uv` and push it to DockerHub.
3. The Action SSHs into your VPS instance.
4. It dynamically generates a `.env` file on the server.
5. It pulls the latest image and runs `docker compose up -d` (zero-downtime recreation).
6. It runs Django migrations and collects static files.
7. *Optional:* If you set `SETUP_SSL: true` in the GitHub workflow, it will automatically configure Nginx and generate Let's Encrypt certificates.
