# SkillPoints Africa 🚀

SkillPoints Africa is a full-stack Learn-to-Earn (L2E) platform built with Django to incentivize skill development and empower African youth through education. The platform enables users to enroll in structured skill tracks, complete practical assignments, earn SkillPoints (SP) for verified progress, and redeem those points through a rewards marketplace. By connecting learning with tangible incentives, SkillPoints Africa aims to bridge the gap between education, employability, and economic opportunity across Africa.

The current MVP includes user authentication, a personalized dashboard, skill enrollment, task management, a points-based reward system, and a marketplace redemption workflow. Future development will focus on integrating artificial intelligence (AI) to generate personalized learning pathways, recommend skill tracks, and automate task creation based on individual learner profiles and career goals.

---

## 🏗️ System Architecture

The project utilizes a decoupled, multi-app Django architecture designed for modularity, clean separation of concerns, and ease of scaling:

```text
SkillPointsAfrica/ (Root)
│
├── core/            # Global Configuration: Master settings, WSGI/ASGI layout, and global routing (urls.py).
│
├── accounts/        # Identity & Ledger: User authentication, registration, profiles, and wallet balances.
│
└── SkillPoints/             # Core Core Engine: Learning tracks, milestone assignments, enrollments, and reward redemptions.

✨ Core Features
👤 1. Advanced Authentication & Wallets (accounts)
Custom user registration and login pipelines with success messaging.
Automated provisioning of a digital User Wallet upon account registration.
Real-time balance ledger tracking active Skill Points (SP).

📚 2. Dynamic Course Workspace (skillPoints)
  Admin-Driven Curriculum: Administrators can instantly add new Tracks and Milestone Tasks via the /admin dashboard panel without writing code.
  Enrollment Engine: One-click registration for active tracks that securely hooks the user profile to the learning sequence.
  Interactive Workspace: A responsive, live lab environment that dynamically loops through specific track assignments, displaying clear PENDING or COMPLETED visual milestones.

💰 3. Automated Point Accrual & Redemption Loop
  Instant Verification: Task submissions route through an optimized background workflow that flags assignments as passed and calculates point value metrics.
  Wallet Hydration: Points are automatically injected into the student’s profile wallet ledger immediately upon task completion.
  Marketplace Exchange: A built-in storefront where users can exchange accrued points for mock operational reward vouchers, modifying balances instantly.
🛠️ Local Development & Installation Setup
Because local database records (db.sqlite3) and dependencies (venv/) are excluded via the project .gitignore policy to secure local information, follow these steps to initialize the project from scratch:

Prerequisites
  Python 3.10 or higher installed on your local machine.
  Git version control client.
Step 1: Clone the Repository (

git clone [https://github.com/Tidjani-Adeniran/SkillPoints-Africa.git](https://github.com/Tidjani-Adeniran/SkillPoints-Africa.git)
cd SkillPoints-Africa
code .

# In the terminal of your code editor Enter these commands
# Create the environment
    python -m venv venv
# Install the required architectural packages using the dependency mapping file
    pip install -r requirements.txt
#Execute Django migrations to inspect structural files and build your local database file system
    python manage.py makemigrations
    python manage.py migrate
#Generate administrative login credentials to access the backend control panel layout
    python manage.py createsuperuser
#Launch the Development Server
    python manage.py runserver

Open your browser and navigate to http://127.0.0.1:8000/ to interact with the platform.
Access http://127.0.0.1:8000/admin/ to manually seed initial tracks, milestones, and marketplace rewards.

🔒 Security & Git Configuration
This project enforces strict environment boundaries using a local .gitignore policy:

db.sqlite3 is explicitly ignored to ensure local user testing data, credentials, and structural tokens never leak to public repositories.

venv/ and all compiled __pycache__/ modules are ignored to ensure the cloud repository remains lightweight, optimized, and fast to download.

🚀 Future Roadmap
Phase 2: Advanced interactive UI components with responsive CSS Grid dashboard statistics card layouts.
Phase 3: Integration of secure, automated code/text verification models to systematically audit deliverables before points distribution.
Phase 4: Live integration with African micro-reward API services for automated digital voucher fulfillment.
