# SkillPoints Africa 🚀

SkillPoints Africa is an AI-powered, full-stack upskilling and resource-redemption platform designed to empower youth across the African tech startup ecosystem. By combining localized micro-learning modules with a gamified ledger system, the platform transforms educational milestones into real-world utility—directly eliminating the opportunity cost of education.

Students complete high-demand digital skills tracks, submit practical contextual workflows, and earn SkillPoints (SP) redeemable for data vouchers, vendor rewards, or operational tools.

---

## 📺 MVP Video Walkthroughs & Demos

Great execution speaks louder than pitch slides. Watch the functional prototype in action below, where I detail the backend code workflows, demonstrate the AI generation cockpit, and show how to run the system:

* 🎥 **[Watch Part 1: SkillPoints Africa MVP Demo & Functional Overview](https://youtu.be/qOsSjAitHYI)**
* 💻 **[Watch Part 2: Technical Deep Dive & Code Architecture Walkthrough](https://youtu.be/GKYU7YG2xOo)**

---
---
## 🌐 Live Application

The SkillPoints Africa MVP is now live. Explore the platform here:

👉 <u>[SkillPoints Africa Live Platform](https://skill-points-africa.vercel.app/)</u>

---

## 🚀 Join the Closed Beta & Community Pool

We are actively onboarding early students, tech mentors, and local retail/vendor partners in Accra and across West Africa. Sign up to join our ecosystem:

👉 **[SkillPoints Africa Community & Beta Registration Form](https://forms.gle/kstGyHw4G4aTTkTz5)**

---

## ✨ Core Features

### 👨‍🎓 Student Ecosystem
* **Interactive Workspace:** Tightly designed task interfaces offering structured instructional lessons mapped with Practical African Market Context Studies.
* **Dynamic Portfolios:** Support for multiple-choice quizzes, validation checkboxes, and long-form narrative workflow assignment inputs.
* **Wallet & Reward Ledger:** A secure tracking dashboard showing total point balances (SP), real-time completion percentages, and valid voucher access codes.

### 🛠️ Operations Cockpit (Admin Interface)
* **AI-Powered Track Generation:** Utilizes the cutting-edge `google-genai` SDK to dynamically create localized educational modules on demand.
* **Evaluation Loop:** Comprehensive tracking panel for administrators to review active text submissions, deliver structured feedback, and release milestone tokens.

---

## 🛠️ Tech Stack & Architecture

* **Backend Framework:** Django (Python 3.10+)
* **Database Pipeline:** SQLite (Development) / PostgreSQL (Production ready)
* **Frontend Architecture:** Clean HTML5 Semantics, Vanilla JavaScript ES6, and Modularized Native CSS Grid/Flexbox pipelines (`static/core/`)
* **Third-Party Integrations:** Google GenAI SDK (`google-genai>=1.0.0`), FontAwesome v6 (Iconography)

---

## 🚀 Local Installation & Deployment Pipeline

This repository is optimized for seamless collaboration across different development environments. All outdated platform-specific dependencies (such as `pywin32`) have been stripped to ensure flawless initialization.

Follow these step-by-step instructions to spin up the MVP workspace locally:

### 1. Clone the repository
```bash
git clone https://github.com/Tidjani-Adeniran/SkillPoints-Africa.git
cd SkillPoints-Africa
```

### 2. Isolate with a Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Package Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
The application relies on secure environment parameters to process user data and run the generative tracking modules. Create a file named `.env` in your root project directory (same folder as `manage.py`) and paste your keys:

```env
DEBUG=True
SECRET_KEY=your-django-super-secret-key
GEMINI_API_KEY=your-google-gemini-api-access-token
```

### 5. Run Database Migrations & Seed Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an Administrator Profile
```bash
python manage.py createsuperuser
```

### 7. Launch the Local Development Server
```bash
python manage.py runserver
```
Open your preferred web browser and navigate to `http://127.0.0.1:8000/` to explore the student workspace. Access the management cockpit at `http://127.0.0.1:8000/admin/`.

---

## 📂 Targeted File System Layout

To ensure Django's template loaders and static engines register paths properly, the repository must match this clean modular structure:

```text
SkillPoints-Africa/           # Git Repository Root Folder
│
├── accounts/                 # User Accounts, Authentication, Wallet Profile States
│   ├── migrations/
│   ├── templates/            # Plural name namespace configuration
│   │   └── accounts/
│   │       ├── login.html
│   │       └── signup.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── core/                     # Learning Engines, Course Tracks, Submissions & Marketplace
│   ├── migrations/
│   ├── static/
│   │   └── core/
│   │       ├── accounts.css
│   │       ├── script.js
│   │       └── styles.css
│   ├── templates/
│   │   ├── about.html
│   │   ├── admin_dashboard.html   
│   │   ├── ai_demo.html
│   │   ├── dashboard.html
│   │   ├── home.html
│   │   ├── layout.html
│   │   ├── marketplace.html
│   │   ├── tracks.html
│   │   └── workspace.html
│   ├── templatetags/         # Custom template tag registry (singular 'templatetags')
│   │   ├── __init__.py
│   │   └── custom_tags.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── api/                      # Planned Enterprise Integration Layer
│   ├── serializers.py        # Handles JSON verification mapping
│   ├── urls.py               # SaaS Webhook Portals (/api/v1/rewards/)
│   └── views.py              # Cryptographic HMAC Endpoint Verification
│
├── SkillPoint/               # Central Project Management & Routing Configurations Only
│   ├── __init__.py
│   ├── settings.py           # Master Project Configuration 
│   ├── urls.py               # Master Routing Gateway Matrix
│   └── wsgi.py
│
├── .gitignore                # Security protocols blocking cache/secrets/local DBs
├── manage.py                 # Django entrypoint script
├── README.md                 # Documentation
└── requirements.txt          # Frozen dependency manifest
```

---

## 💡 Engineering Roadmap

* **Cloud Infrastructure Deployment:** Migrating settings to support production-ready PostgreSQL running on Vercel Serverless architectures.
* **SaaS B2B University Integration Gateway:** Exposing protected API endpoints utilizing HMAC cryptographic secret keys, allowing external higher-education School Management Systems (SMS) to issue SkillPoints automatically based on internal portal achievements.
* **Sybil Defense Layer:** Implementing behavioral biometric telemetry engines (typing acceleration, click arrays) within Django to protect the voucher liquidation pool from automated bot farming.
