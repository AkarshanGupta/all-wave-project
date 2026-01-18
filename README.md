# PMO Intelligence Platform

A modern, AI-powered Project Management Office (PMO) platform that leverages Large Language Models (LLMs) to automate project insights, risk analysis, meeting summarization, and status reporting.

## 🎯 Project Overview

The PMO Intelligence Platform is a full-stack web application designed to streamline project management workflows by combining traditional PMO capabilities with advanced AI-driven insights. The platform helps project managers and teams track projects, manage risks, schedule meetings, allocate resources, and generate intelligent status reports.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TypeScript)            │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐ │
│  │Dashboard │ Projects │ Meetings │  Risks   │ Resources │ │
│  └──────────┴──────────┴──────────┴──────────┴───────────┘ │
│                    Axios API Client                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API (JSON)
┌─────────────────────────┴───────────────────────────────────┐
│                  Backend (FastAPI + Python)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Layer (Routes)                       │   │
│  │  /projects  /meetings  /risks  /resources  /status   │   │
│  └──────────────────────┬───────────────────────────────┘   │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │              Service Layer (Business Logic)           │   │
│  │  • Meeting Service    • Risk Service                  │   │
│  │  • Status Service     • Resource Service              │   │
│  └──────────────────────┬───────────────────────────────┘   │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │              AI/LLM Integration Layer                 │   │
│  │           Groq API (llama-3.3-70b-versatile)         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────┬───────────────────────────────┐   │
│  │       Models Layer (SQLAlchemy ORM)                   │   │
│  └──────────────────────┴───────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────────┐
│                PostgreSQL Database (Supabase)                │
│  Projects │ Meetings │ Risks │ Resources │ Status Reports   │
└──────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI library with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **React Router v6** - Client-side routing
- **Shadcn/ui** - Accessible component library built on Radix UI
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Hook Form** - Form state management
- **Zod** - Schema validation
- **Axios** - HTTP client for API calls

**Rationale**: React with TypeScript provides a robust foundation for building scalable UIs. Shadcn/ui components are highly customizable and accessible, while Vite offers lightning-fast development experience.

### Backend
- **FastAPI** - High-performance Python web framework
- **Python 3.13** - Latest Python features
- **SQLAlchemy 2.0** - Async ORM for database operations
- **Alembic** - Database migration tool
- **Pydantic v2** - Data validation and settings management
- **AsyncPG** - Asynchronous PostgreSQL driver
- **Uvicorn** - ASGI server
- **Groq API** - LLM provider (llama-3.3-70b-versatile model)

**Rationale**: FastAPI provides automatic API documentation, excellent async support, and type validation. SQLAlchemy's async capabilities ensure high performance under load. Groq offers fast inference speeds for LLM operations.

### Database
- **PostgreSQL** - Relational database
- **Supabase** - Managed PostgreSQL hosting

**Rationale**: PostgreSQL provides ACID compliance, complex querying, and JSON support. Supabase offers a managed solution with easy scaling.

### Deployment
- **Render** - Backend hosting with auto-deployment
- **Vercel** - Frontend hosting with CDN
- **Git** - Version control

## 🤖 AI/ML Approach & Prompt Engineering

### AI Integration Points

The platform uses **Groq's LLM API** with the **llama-3.3-70b-versatile** model for three main features:

#### 1. **Meeting Analysis** (`meeting_service.py`)
**Purpose**: Extract structured information from meeting transcripts

**Prompt Strategy**:
```python
System Prompt: "You are an expert meeting analyst. Always return valid JSON."
User Prompt: Template-based with meeting text injection
```

**Output Schema**:
- Summary (executive overview)
- Decisions made (actionable outcomes)
- Open questions (unresolved items)
- Action items (assignee, due date, description)

**Engineering Approach**:
- Enforces JSON output format
- Uses low temperature (0.3) for consistency
- Structured prompt template loaded from `meeting_prompt.txt`
- Post-processes dates for database compatibility

#### 2. **Risk Analysis** (`risk_service.py`)
**Purpose**: Analyze project data to identify potential risks

**Prompt Strategy**:
```python
Context Aggregation:
- Project overview (name, description, dates)
- Recent status reports (executive summary, risks)
- Team composition (resources, roles, allocations)
- Existing risks (for pattern detection)

Output Format: JSON array of risk objects
```

**Data Compilation**:
- Fetches last 5 status reports
- Includes resource allocation data
- Analyzes team capacity vs. workload
- Temperature: 0.3 for consistent risk assessment

**Engineering Approach**:
- Multi-source data aggregation (status reports, resources, allocations)
- Contextual prompt with project-specific details
- Structured JSON response with risk categories
- Automatic risk score calculation (probability × impact)

#### 3. **Status Report Generation** (`status_service.py`)
**Purpose**: Generate executive status reports from project data

**Prompt Strategy**:
```python
Aggregated Context:
- Project metadata
- Risk summary (count, severity distribution)
- Recent meetings (last 5)
- Resource allocation stats
- Total allocated hours

Output: Four-section report
```

**Sections Generated**:
1. Executive Summary - Overall project health
2. Risks Summary - Top concerns and mitigation
3. Meetings Summary - Recent decisions and action items
4. Resources Summary - Team allocation and capacity

**Engineering Approach**:
- Structured template from `status_prompt.txt`
- Data preprocessing (counting, summarizing)
- Low temperature for professional tone
- Separate sections for easy parsing

### Prompt Engineering Best Practices Used

1. **Structured Outputs**: All prompts request JSON format for reliable parsing
2. **Low Temperature (0.3)**: Ensures consistent, focused responses
3. **Context Injection**: Dynamic data insertion into prompt templates
4. **System Prompts**: Sets AI behavior and expectations upfront
5. **Template-based**: Prompts stored in `/app/ai/prompts/` for easy iteration
6. **Error Handling**: Graceful fallback when GROQ_API_KEY is missing
7. **Data Preprocessing**: Clean, relevant data compilation before LLM call

### Model Selection Rationale

**llama-3.3-70b-versatile** was chosen for:
- Strong JSON generation capabilities
- Good balance of speed and accuracy
- Cost-effectiveness via Groq's fast inference
- 70B parameter size handles complex context
- "Versatile" variant optimized for varied tasks

## 📦 Module Status

### ✅ Fully Implemented & Working

#### Projects Module
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Fields: name, description, status, priority (1-10), start_date, deadline
- ✅ Display: Project list with ID, dates, priority
- ✅ AI Integration: Used as context in risk analysis

#### Meetings Module
- ✅ CRUD operations
- ✅ Fields: title, date, time, duration, attendees, status, raw_text
- ✅ AI-powered transcript analysis
- ✅ Automatic extraction of summary, decisions, open questions, action items
- ✅ Attendees input (supports comma-separated names)

#### Risks Module
- ✅ CRUD operations
- ✅ Fields: title, description, category, probability, impact, severity
- ✅ Automatic risk score calculation (probability × impact)
- ✅ Color-coded severity display
- ✅ **AI Risk Analysis** (Brain icon) - Analyzes project data to identify risks

#### Resources Module
- ✅ CRUD operations (including delete endpoint)
- ✅ Fields: name, role, capacity, availability, department, location
- ✅ Skills tracking with proficiency levels
- ✅ Resource allocation tracking

#### Status Reports Module
- ✅ View existing reports
- ✅ AI-powered report generation
- ✅ Aggregates data from projects, risks, meetings, resources
- ✅ Four-section report structure

#### Dashboard
- ✅ Real-time statistics (project count, meeting count, risk count, resource count)
- ✅ Dynamic recent activity feed (shows last 5 updates across modules)
- ✅ Health status indicator
- ✅ Quick action buttons

### ⚠️ Partially Implemented

#### Allocations
- ⚠️ Backend: Create and list allocations
- ❌ Frontend: No dedicated page (used in backend calculations)
- 📝 Status: Data model exists, used for resource analysis, needs UI

#### Search Functionality
- ⚠️ UI component exists in header
- ❌ Not wired to actual search logic
- 📝 Status: Visual placeholder

### 🚧 Planned / Not Implemented

- ❌ User authentication & authorization
- ❌ Role-based access control (RBAC)
- ❌ Real-time notifications
- ❌ Document/file attachments
- ❌ Email integration
- ❌ Calendar integration
- ❌ Gantt chart visualization
- ❌ Resource workload charts
- ❌ Export to PDF/Excel
- ❌ Audit logs
- ❌ Multi-project portfolio view

## 🚀 Setup Instructions

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.10+ (3.13 recommended)
- **PostgreSQL** database (or Supabase account)
- **Groq API Key** (get from [console.groq.com](https://console.groq.com))

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create `.env` file in `backend/` directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
   GROQ_API_KEY=gsk_your_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   GROQ_TEMPERATURE=0.3
   ```

   **For Supabase**:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

5. **Run database migrations**:
   ```bash
   # On Windows
   migrate.bat
   
   # On macOS/Linux
   chmod +x migrate.sh
   ./migrate.sh
   ```

6. **Start development server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will run at: `http://localhost:8000`
   
   API docs available at: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**:
   Create `.env` file in `frontend/` directory:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

   **For production**:
   ```env
   VITE_API_URL=https://your-backend.onrender.com
   ```

4. **Start development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

   Frontend will run at: `http://localhost:5173`

### Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

**Existing Migrations**:
- `001_initial_migration.py` - Base schema (projects, meetings, risks, resources)
- `002_add_risk_analytics.py` - Risk metrics table
- `003_add_allocation_optimizer.py` - Resource allocations and scenarios
- `004_add_meeting_fields.py` - Meeting date/time/duration/attendees/status

## 📊 Sample Data Formats

### Project Creation
```json
{
  "name": "iOS and Android App",
  "description": "Mobile app for customers",
  "status": "Active",
  "priority": 8,
  "start_date": "2026-01-20",
  "deadline": "2026-06-30"
}
```

### Meeting Upload (AI Analysis)
```json
{
  "project_id": 1,
  "title": "Sprint Planning Meeting",
  "raw_text": "Meeting started at 10am. John discussed the new authentication feature. Sarah raised concerns about API rate limits. Decision: We'll implement OAuth 2.0. Action: Mike to research rate limiting solutions by Friday. Open question: Should we support biometric auth?"
}
```

**AI Output**:
```json
{
  "summary": "Sprint planning focused on authentication implementation",
  "decisions": "Implement OAuth 2.0 for authentication",
  "open_questions": "Should we support biometric authentication?",
  "action_items": [
    {
      "description": "Research rate limiting solutions",
      "assignee": "Mike",
      "due_date": "2026-01-24"
    }
  ]
}
```

### Risk Creation
```json
{
  "project_id": 1,
  "title": "API Integration Delay",
  "description": "Third-party API may not be ready on time",
  "category": "Technical",
  "probability": 7,
  "impact": 8,
  "severity": "High",
  "mitigation_plan": "Develop mock API for testing"
}
```

### Resource Creation
```json
{
  "name": "Sarah Johnson",
  "role": "Senior Developer",
  "capacity_hours": 160,
  "availability_hours": 120,
  "department": "Engineering",
  "location": "Remote",
  "skills": [
    {"skill_name": "React", "proficiency_level": 5},
    {"skill_name": "Python", "proficiency_level": 4},
    {"skill_name": "AWS", "proficiency_level": 3}
  ]
}
```

### Status Report Generation Input
**Endpoint**: `POST /status-reports/generate/{project_id}`

**AI Output**:
```json
{
  "executive_summary": "Project is 60% complete, on track for Q2 delivery. Key milestone: API integration completed this week.",
  "risks_summary": "3 high-priority risks identified: API delays, resource constraints, scope creep. Mitigation plans in place.",
  "meetings_summary": "5 meetings held this month. Key decisions: Architecture finalized, OAuth implementation approved.",
  "resources_summary": "Team of 5 engineers, 85% allocated. Total capacity: 800 hours, utilized: 680 hours."
}
```

## 🔌 API Endpoints

### Projects
- `GET /projects` - List all projects
- `POST /projects` - Create project
- `GET /projects/{id}` - Get project by ID
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### Meetings
- `GET /meetings` - List all meetings
- `POST /meetings` - Create meeting (manual)
- `POST /meetings/upload` - Upload meeting transcript (AI analysis)
- `PUT /meetings/{id}` - Update meeting
- `DELETE /meetings/{id}` - Delete meeting

### Risks
- `GET /risks` - List all risks
- `POST /risks` - Create risk
- `POST /risks/analyze-project/{project_id}` - AI risk analysis (Brain icon)
- `PUT /risks/{id}` - Update risk
- `DELETE /risks/{id}` - Delete risk

### Resources
- `GET /resources` - List all resources
- `POST /resources` - Create resource
- `PUT /resources/{id}` - Update resource
- `DELETE /resources/{id}` - Delete resource

### Status Reports
- `GET /status` - List all status reports
- `POST /status-reports/generate/{project_id}` - Generate AI status report
- `DELETE /status/{id}` - Delete status report

### Health
- `GET /health` - Backend health check

## 🎨 UI Features

### Design System
- **Color Scheme**: Blue primary (#1D7FC2), green accent, dark mode ready
- **Typography**: Inter font family
- **Spacing**: Tailwind's 8px base unit
- **Components**: Shadcn/ui (Radix primitives + Tailwind)
- **Animations**: Framer Motion for smooth transitions

### Key UX Patterns
- **Modal Dialogs**: For create/edit operations (scrollable)
- **Toast Notifications**: Success/error feedback
- **Loading States**: Skeleton loaders and spinners
- **Responsive Design**: Mobile-first approach
- **Color-coded Severity**: Visual risk/status indicators
- **Relative Timestamps**: "2 hours ago" format

## ⚠️ Known Limitations

### Current Limitations

1. **No Authentication**: Platform is open access (no login required)
   - **Impact**: Not suitable for multi-tenant production use
   - **Mitigation**: Add JWT authentication + RBAC in future

2. **AI Requires Data**: Risk analysis needs existing status reports/resources
   - **Impact**: New projects won't generate AI insights immediately
   - **Mitigation**: Add sample data or improve prompts for sparse data

3. **Single Workspace**: No multi-organization support
   - **Impact**: All users see all projects
   - **Mitigation**: Add organization/workspace separation

4. **Limited File Upload**: No document attachments
   - **Impact**: Meeting transcripts are text-only
   - **Mitigation**: Integrate S3/cloud storage for files

5. **No Real-time Updates**: Manual refresh needed to see changes
   - **Impact**: Multiple users may see stale data
   - **Mitigation**: Add WebSocket support for live updates

6. **Groq API Dependency**: AI features require external API
   - **Impact**: Fails if Groq is down or rate-limited
   - **Mitigation**: Add fallback to local models or graceful degradation

7. **Meeting Attendees**: Simple comma-separated text field
   - **Impact**: No validation, typos possible
   - **Mitigation**: Add user management and autocomplete

8. **No Pagination**: All records loaded at once
   - **Impact**: Performance degrades with >1000 records
   - **Mitigation**: Implement cursor-based pagination

9. **Basic Search**: Header search is non-functional
   - **Impact**: Must manually scan lists
   - **Mitigation**: Implement full-text search with filters

10. **Date Timezone**: Assumes UTC, no user timezone handling
    - **Impact**: Dates may appear off for international teams
    - **Mitigation**: Add timezone detection and conversion

### Browser Compatibility

- ✅ Chrome/Edge (Chromium) 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ❌ Internet Explorer (not supported)

## 🚀 Future Improvements

### High Priority
1. **User Authentication** (JWT + OAuth2)
   - Login/signup flows
   - Password reset
   - Session management

2. **Role-Based Access Control**
   - Admin, Manager, Team Member roles
   - Permission-based feature access
   - Project-level access control

3. **Real-time Notifications**
   - WebSocket integration
   - Email notifications
   - In-app notification center

4. **Enhanced AI Features**
   - Sentiment analysis on meeting transcripts
   - Predictive project delays
   - Resource optimization recommendations
   - Auto-tagging and categorization

### Medium Priority
5. **Data Visualization**
   - Gantt charts for project timelines
   - Burn-down charts
   - Resource utilization heatmaps
   - Risk trend analysis

6. **Export & Reporting**
   - PDF export for status reports
   - Excel export for data
   - Custom report templates
   - Scheduled report delivery

7. **Integrations**
   - Calendar sync (Google/Outlook)
   - Slack/Teams notifications
   - Jira/GitHub issue tracking
   - Email parsing for meeting notes

8. **Advanced Search & Filtering**
   - Full-text search across all modules
   - Saved filter presets
   - Bulk operations
   - Advanced query builder

### Low Priority
9. **Mobile Apps**
   - React Native iOS/Android apps
   - Push notifications
   - Offline mode

10. **Analytics Dashboard**
    - Executive KPI dashboard
    - Team performance metrics
    - Project health scoring
    - Predictive analytics

## 📝 Development Notes

### Code Structure

**Backend** (`backend/app/`):
```
app/
├── ai/                  # LLM integration
│   ├── llm_client.py    # Groq API wrapper
│   └── prompts/         # Prompt templates
├── api/                 # FastAPI routes
├── core/                # Config & database
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── services/            # Business logic
└── utils/               # Helper functions
```

**Frontend** (`frontend/src/`):
```
src/
├── components/          # React components
│   ├── dashboard/       # Dashboard-specific
│   ├── dialogs/         # Modal forms
│   ├── layout/          # App shell
│   ├── shared/          # Reusable components
│   └── ui/              # Shadcn components
├── hooks/               # Custom React hooks
├── lib/                 # Utilities
│   ├── api.ts           # API client & types
│   └── utils.ts         # Helper functions
└── pages/               # Route pages
```

### Coding Standards

- **Backend**: PEP 8, type hints, async/await
- **Frontend**: ESLint, TypeScript strict mode
- **Commits**: Conventional commits (feat:, fix:, docs:)
- **API**: RESTful conventions, JSON responses

### Testing

**Backend**:
```bash
# Unit tests (if implemented)
pytest
```

**Frontend**:
```bash
# Vitest unit tests
npm run test

# Watch mode
npm run test:watch
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is private and proprietary.

## 👥 Team

- **Developer**: PMO Intelligence Team
- **AI Integration**: Groq API (llama-3.3-70b-versatile)
- **Deployment**: Render (backend) + Vercel (frontend)

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Contact: admin@pmo.com

---

**Built with ❤️ using FastAPI, React, and AI**
