# 🏠 NestMate — Student Accommodation & Roommate Finder

A Django-based CRUD web application for students to find accommodation and connect with potential roommates, deployed on AWS with a full CI/CD pipeline.

---

## 📋 Assignment Info

- **Module:** H9CDOS — Cloud DevOpsSec
- **Application:** Student Accommodation & Roommate Finder
- **Stack:** Django, PostgreSQL (AWS RDS), Docker, AWS Elastic Beanstalk, GitHub Actions, SonarQube

---

## 🚀 Features

- **Listings** — Create, read, update, delete room listings
- **Profiles** — Student profiles with course and college info
- **Requests** — Send, manage, accept/reject roommate requests
- **Search & Filter** — Search by city, type, max rent
- **Input Validation** — Server-side validation on all forms
- **Authentication** — Django built-in user auth

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 (Python 3.11) |
| Database | PostgreSQL (AWS RDS) |
| Hosting | AWS Elastic Beanstalk |
| Containers | Docker → AWS ECR |
| Secrets | AWS Secrets Manager |
| Monitoring | AWS CloudWatch |
| CI/CD | GitHub Actions |
| Static Analysis | Bandit + Flake8 + SonarQube |

---

## 📁 Project Structure

```
accommodation_finder/
├── accommodation_finder/    # Django project config
│   ├── settings.py          # Settings (AWS Secrets Manager integration)
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py
├── core/                    # Main application
│   ├── models.py            # StudentProfile, Listing, RoommateRequest
│   ├── views.py             # All CRUD views
│   ├── forms.py             # Forms with validation
│   ├── urls.py              # App URL patterns
│   ├── migrations/          # Database migrations
│   └── templates/core/      # HTML templates
├── templates/
│   └── base.html            # Base layout
├── .github/workflows/
│   └── cicd.yml             # GitHub Actions CI/CD pipeline
├── Dockerfile               # Docker container definition
├── requirements.txt         # Python dependencies
├── sonar-project.properties # SonarQube config
├── .env.example             # Environment variable template
└── manage.py
```

---

## ⚙️ Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/nestmate.git
cd nestmate
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your local settings
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser
```bash
python manage.py createsuperuser
```

### 7. Run development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🐳 Docker

### Build and run locally
```bash
docker build -t nestmate .
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-key \
  -e DEBUG=True \
  nestmate
```

---

## ☁️ AWS Deployment

### Prerequisites
- AWS CLI configured
- AWS account with permissions for: ECR, Elastic Beanstalk, RDS, Secrets Manager, IAM

### Step 1: Create ECR Repository
```bash
aws ecr create-repository --repository-name nestmate-app --region eu-west-1
```

### Step 2: Create RDS PostgreSQL Instance
```bash
aws rds create-db-instance \
  --db-instance-identifier nestmate-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20 \
  --region eu-west-1
```

### Step 3: Store credentials in AWS Secrets Manager
```bash
aws secretsmanager create-secret \
  --name nestmate/db/credentials \
  --secret-string '{"username":"postgres","password":"YOUR_PASSWORD","host":"YOUR_RDS_ENDPOINT","dbname":"accommodation_db","port":"5432"}' \
  --region eu-west-1
```

### Step 4: Create Elastic Beanstalk Application
```bash
eb init nestmate-accommodation --platform docker --region eu-west-1
eb create nestmate-accommodation-prod
```

### Step 5: Add GitHub Secrets
In your GitHub repo → Settings → Secrets → Actions, add:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `SONAR_TOKEN`
- `SONAR_HOST_URL`
- `DB_SECRET_NAME` → `nestmate/db/credentials`

### Step 6: Push to main branch
```bash
git push origin main
# GitHub Actions will automatically build, test, and deploy
```

---

## 🔄 CI/CD Pipeline

```
Developer pushes code
        ↓
GitHub Actions triggered
        ↓
    ┌── CI ──────────────────────────────────┐
    │  1. Flake8 — style & syntax check      │
    │  2. Bandit — security scan             │
    │  3. SonarQube — code quality           │
    │  4. Django unit tests                  │
    │  5. Coverage report                    │
    └────────────────────────────────────────┘
        ↓ (if CI passes & branch = main)
    ┌── CD ──────────────────────────────────┐
    │  1. Login to AWS ECR                   │
    │  2. Build & push Docker image          │
    │  3. Create EB deployment package       │
    │  4. Deploy to Elastic Beanstalk        │
    └────────────────────────────────────────┘
        ↓
Live application on AWS
```

---

## 🔒 Security

- Django CSRF protection on all forms
- SQL injection prevention via Django ORM
- Passwords hashed with PBKDF2
- Secrets stored in AWS Secrets Manager (never in code)
- Environment variables for all sensitive config
- Input validation on all user-facing forms
- Bandit security scanning in CI pipeline

---

## 📊 CRUD Summary

| Model | Create | Read | Update | Delete |
|-------|--------|------|--------|--------|
| Listing | ✅ | ✅ | ✅ | ✅ |
| StudentProfile | ✅ | ✅ | ✅ | — |
| RoommateRequest | ✅ | ✅ | ✅ (status) | ✅ (withdraw) |

---

## 📚 References

- Django Documentation: https://docs.djangoproject.com/
- AWS Elastic Beanstalk: https://docs.aws.amazon.com/elasticbeanstalk/
- AWS ECR: https://docs.aws.amazon.com/ecr/
- AWS Secrets Manager: https://docs.aws.amazon.com/secretsmanager/
- GitHub Actions: https://docs.github.com/en/actions
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Bandit: https://bandit.readthedocs.io/
- SonarQube: https://docs.sonarqube.org/
