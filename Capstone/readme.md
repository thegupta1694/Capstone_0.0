# University Project Allocation System

A comprehensive web application for streamlining the final year project allocation process at universities. This system eliminates the chaotic in-person queuing system and provides a structured, transparent environment for team formation, project applications, and slot management.

## 🚀 Features

### For Students
- **Team Formation**: Create teams and invite up to 3 teammates
- **Professor Discovery**: Search and filter professors by name, department, and research domains
- **Application Management**: Submit up to 4 applications simultaneously
- **Status Tracking**: Monitor application status (Pending, Accepted, Rejected)

### For Professors
- **Profile Management**: Update research domains and available slots
- **Application Dashboard**: Review and respond to team applications
- **Slot Management**: Automatic slot tracking and validation

### For Administrators
- **System Overview**: Real-time statistics and allocation progress
- **User Management**: Full CRUD access to all data
- **Conflict Resolution**: Manual override capabilities

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT (JSON Web Tokens)
- **API**: RESTful API with comprehensive filtering and search

### Frontend
- **Framework**: React 18.2.0
- **UI Library**: Material-UI (MUI) 5.14.0
- **State Management**: React Query for server state
- **Routing**: React Router DOM 6.3.0
- **Forms**: Formik with Yup validation

## 📁 Project Structure

```
project-allocation/
├── backend/                     # Django Backend
│   ├── project_allocation/      # Main Django project
│   ├── users/                   # User management app
│   ├── teams/                   # Team formation app
│   ├── applications/            # Application management app
│   ├── requirements.txt         # Python dependencies
│   └── manage.py               # Django management script
├── frontend/                    # React Frontend
│   ├── public/                 # Static files
│   ├── src/                    # Source code
│   │   ├── components/         # Reusable components
│   │   ├── contexts/           # React contexts
│   │   ├── pages/              # Page components
│   │   ├── services/           # API services
│   │   └── App.js              # Main app component
│   └── package.json            # Node.js dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (for production)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**:
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/me/` - Get current user

### User Endpoints
- `GET /api/profile/` - Get/update user profile
- `GET /api/professors/` - List professors
#### 1.3. Target Users
1.  **Students:** All final year students (~1600) who need to form a team and secure a project.
2.  **Teachers (Professors):** Faculty members who guide final year projects.
3.  **Admin:** A university administrator or department head responsible for overseeing the process.

#### 1.4. Core Objectives
*   To eliminate the chaotic, in-person queuing system.
*   To provide a clear and searchable directory of professors and their domains.
*   To streamline the team formation and application process.
*   To give professors an efficient tool to manage applications and slots.
*   To provide administrators with oversight and statistical data on the allocation process.
*   To build a scalable and reliable platform using modern, industry-standard technologies.

---

### 2. Functional Requirements (Scope for Version 1.0)

#### 2.1. Student Profile
*   **Authentication:** Secure login using university portal credentials.
*   **Team Formation:**
    *   A student can create a team, becoming the team leader.
    *   Invite up to 3 teammates via their unique university ID or email.
    *   Invitations are confirmed via an OTP or a unique confirmation link.
    *   View team status and all members.
*   **Professor Discovery:**
    *   View and search a list of all available professors.
    *   Filter professors by name, department, and research domains (tags).
    *   View a professor's detailed profile, including their available project slots.
*   **Application Management:**
    *   A team can submit applications to professors.
    *   A team can have a maximum of **4 live (pending) applications** at any time.
    *   View the status of all submitted applications (Pending, Accepted, Rejected).
    *   Ability to withdraw a pending application.
    *   Once an application is accepted, all other pending applications for that team are automatically withdrawn.

#### 2.2. Teacher (Professor) Profile
*   **Authentication:** Secure login with university credentials.
*   **Profile Management:**
    *   Update personal details and research domains.
    *   Set and dynamically update the number of available project slots.
*   **Application Dashboard:**
    *   View all incoming team applications in a clean, filterable list.
    *   Review the details of each applicant team.
    *   **Accept** or **Reject** applications with one click.
    *   Accepting an application decrements the available slot count. The system prevents accepting more applications than available slots.

#### 2.3. Admin Profile
*   **Authentication:** Secure login with admin credentials.
*   **Dashboard & Analytics:**
    *   View key statistics: Total students, teams formed, applications submitted, and the percentage of students successfully allocated.
    *   See a real-time list of professors and their current slot-fill status.
*   **User & System Management:**
    *   Full CRUD (Create, Read, Update, Delete) access to all data (Users, Teams, Applications).
    *   Ability to manually override allocations or resolve conflicts.
    *   Set system-wide parameters like application start/end dates.

---

### 3. Technical Architecture

#### 3.1. Chosen Technology Stack
*   **Frontend:** **React.js** (with a UI library like **Material-UI**)
    *   *Why?* Component-based architecture for a manageable and scalable UI. Massive ecosystem and community support.
*   **Backend:** **Python** with the **Django** framework (using Django Rest Framework for the API).
    *   *Why?* Django's built-in Admin Panel is a massive accelerator for the Admin profile. Its ORM is robust and works perfectly with relational data. Python is a common language in academic environments.
*   **Database:** **PostgreSQL**
    *   *Why?* A powerful, open-source relational database that perfectly models the structured relationships between students, teams, professors, and applications.
*   **Deployment:**
    *   Frontend on **Vercel/Netlify**.
    *   Backend & Database on **Heroku/Render**.

#### 3.2. System Architecture Diagram

```
+----------------+      (HTTPS/API Calls)      +--------------------+      (ORM)      +-----------------+
|                | <--------------------------> |                    | <------------> |                 |
|  React.js      |                              |   Django/DRF API   |                |  PostgreSQL     |
|  (Frontend)    |                              |   (Backend)        |                |  (Database)     |
|                |                              |                    |                |                 |
+----------------+                              +--------------------+                +-----------------+
      ^                                                  ^
      |                                                  |
(User Interaction)                               (Django Admin Panel)
      |                                                  |
+-----------+                                      +-----------+
|           |                                      |           |
|  Student  |                                      |   Admin   |
|  Teacher  |                                      |           |
+-----------+                                      +-----------+
```

#### 3.3. Core Database Schema (PostgreSQL)

*   **`User`** (from `django.contrib.auth.models`)
    *   `id` (PK), `username` (university_id), `email`, `password`, `first_name`, `last_name`.
*   **`Profile`** (extends User)
    *   `user` (OneToOneField to User, PK), `role` (CharField: 'student', 'teacher').
*   **`ProfessorProfile`**
    *   `user` (OneToOneField to User, PK), `department` (CharField), `domains` (TextField), `slots_total` (IntegerField), `slots_filled` (IntegerField).
*   **`Team`**
    *   `id` (PK), `name` (CharField), `leader` (ForeignKey to User).
*   **`TeamMember`**
    *   `team` (ForeignKey to Team), `user` (ForeignKey to User), `status` (CharField: 'pending', 'accepted').
*   **`Application`**
    *   `id` (PK), `team` (ForeignKey to Team), `professor` (ForeignKey to ProfessorProfile), `status` (CharField: 'pending', 'accepted', 'rejected'), `submitted_at` (DateTimeField).

---

### 4. Implementation Plan & Timeline

This project will be executed in 4 main phases over an estimated 10 weeks. We will use a sprint-based approach, with each sprint lasting one week.

**Team Roles (Suggested):**
*   **Project Lead:** Oversees the project, manages tasks, and ensures deadlines are met.
*   **Backend Lead (1-2 members):** Responsible for the Django API and database.
*   **Frontend Lead (1-2 members):** Responsible for the React UI/UX.

---

**Phase 0: Planning & Foundation (Weeks 1-2)**
*   **Sprint 1: Setup & Design**
    *   **Goal:** Finalize requirements and set up the development environment.
    *   **Tasks:**
        *   Initialize Git repository with the `backend/` and `frontend/` structure.
        *   Set up task management board (Trello, Jira, Notion).
        *   Create detailed UI/UX wireframes in **Figma** for all major screens.
        *   Finalize the detailed database schema.
        *   All members to set up their local development environments (Python/venv, Node.js, PostgreSQL).

**Phase 1: Backend Development (API First) (Weeks 3-5)**
*   **Sprint 2: Core Models & User API**
    *   **Goal:** Build the foundational database models and user authentication.
    *   **Tasks (Backend Lead):**
        *   Set up Django project and create `users` and `api` apps.
        *   Implement User, Profile, ProfessorProfile, Team, and TeamMember models.
        *   Set up the Django Admin to view these models.
        *   Create API endpoints for user registration and login (JWT-based).
*   **Sprint 3: Team & Application Logic**
    *   **Goal:** Implement the core logic for teams and applications.
    *   **Tasks (Backend Lead):**
        *   Create API endpoints for creating a team and inviting members.
        *   Implement OTP/email confirmation logic.
        *   Create models and API endpoints for creating and viewing applications.
        *   Test all endpoints thoroughly with **Postman/Insomnia**.

**Phase 2: Frontend Development (Weeks 4-7) - *Overlaps with Backend***
*   **Sprint 4: Basic Structure & Components**
    *   **Goal:** Build the skeleton of the React app and reusable components.
    *   **Tasks (Frontend Lead):**
        *   Set up React project with React Router.
        *   Build the main layout (Navbar, Footer).
        *   Create reusable UI components (Button, Card, Input) based on Figma designs.
        *   Set up `AuthContext` for managing login state.
*   **Sprint 5: Connecting to the API**
    *   **Goal:** Implement user authentication and display professor data.
    *   **Tasks (Frontend Lead):**
        *   Build Login page and connect to the backend's login endpoint.
        *   Build the Professor List page, fetching data from the backend.
        *   Implement protected routes for logged-in users.
*   **Sprint 6: Student & Teacher Dashboards**
    *   **Goal:** Build the core dashboards for both user roles.
    *   **Tasks (Frontend Lead):**
        *   Build the Student Dashboard for team management and viewing applications.
        *   Build the Teacher Dashboard for viewing and managing applications.

**Phase 3: Integration, Testing & Deployment (Weeks 8-10)**
*   **Sprint 7: Full Feature Integration**
    *   **Goal:** Ensure all frontend and backend features work together seamlessly.
    *   **Tasks (Full Team):**
        *   Connect the application submission flow.
        *   Implement automatic withdrawal of applications upon acceptance.
        *   Conduct thorough end-to-end testing of every user story.
*   **Sprint 8: Deployment & Bug Fixing**
    *   **Goal:** Deploy the application and begin live testing.
    *   **Tasks (Full Team):**
        *   Deploy the Django backend to **Heroku/Render**.
        *   Deploy the React frontend to **Vercel/Netlify**.
        *   Configure environment variables and CORS.
        *   Conduct a round of testing on the live-staging environment and fix bugs.
*   **Sprint 9-10: Final Polish & Documentation**
    *   **Goal:** Prepare the project for final submission.
    *   **Tasks (Full Team):**
        *   Refine the UI based on feedback.
        *   Prepare the final project report and presentation slides.
        *   Ensure the `README.md` is complete with setup and deployment instructions.
        *   Final code cleanup and commenting.

---

### 5. Tools & Best Practices

*   **Version Control:** **Git**. All work must be done on feature branches (`feature/login-page`) and merged into `main` via Pull Requests.
*   **Task Management:** A Kanban board (e.g., **Trello**, **Notion**, or **Jira**) to track the status of all tasks.
*   **Communication:** A dedicated channel on **Slack** or **Discord** for team communication.
*   **Design:** **Figma** for collaborative UI/UX design and wireframing.
*   **API Testing:** **Postman** or **Insomnia** to test backend endpoints independently of the frontend.