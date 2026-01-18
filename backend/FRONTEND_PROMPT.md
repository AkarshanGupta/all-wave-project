# Frontend Generation Prompt

Create a professional React/Next.js frontend for a PMO Intelligence Platform with the following specifications:

## BACKEND INFORMATION:
- Base URL: http://localhost:8000
- API Endpoints:
  - GET /health - Health check
  - GET / - API info
  - /projects - Project management endpoints
  - /meetings - Meeting management endpoints  
  - /risks - Risk management endpoints
  - /resources - Resource management endpoints
  - /status - Status report endpoints

## FRONTEND REQUIREMENTS:

### 1. Environment Configuration (.env.local):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=PMO Intelligence Platform
```

### 2. Dashboard Layout:
- Header with app title "PMO Intelligence Platform"
- Navigation sidebar with menu items:
  - Dashboard (overview)
  - Projects
  - Meetings
  - Risks
  - Resources
  - Status Reports
- Main content area
- Footer

### 3. Dashboard Page (/dashboard):
- Health status card (call GET /health)
- Display "Connected to Backend" if healthy
- Show backend version from GET /
- Quick stats cards for:
  - Total Projects
  - Total Meetings
  - Total Risks
  - Total Resources

### 4. Pages to Create:
- /dashboard - Main dashboard
- /projects - List projects with add/edit/delete
- /meetings - List meetings with add/edit/delete
- /risks - List risks with add/edit/delete
- /resources - List resources with add/edit/delete
- /status-reports - List status reports

### 5. API Integration:
- Create API service layer (lib/api.ts) with axios
- Implement all CRUD operations
- Add loading and error states
- Display toast notifications for success/error

### 6. UI Requirements:
- Use TailwindCSS for styling
- Add shadcn/ui components for forms and dialogs
- Responsive design (mobile, tablet, desktop)
- Dark/light mode toggle (optional)
- Professional color scheme (blue/green theme)

### 7. Data Display:
- Tables with sorting and pagination
- Modal dialogs for create/edit operations
- Form validation
- Confirmation dialogs for delete operations

### 8. Testing Support:
- Add demo data buttons to populate sample data
- Test connection button on dashboard
- API response logging for debugging
- Loading skeletons for better UX

## TECH STACK:
- Framework: Next.js 14+
- UI: React with TailwindCSS
- Component Library: shadcn/ui
- HTTP Client: axios
- State Management: React hooks (useState, useEffect)
- Form Handling: React Hook Form

## FOLDER STRUCTURE:
```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   ├── projects/
│   │   └── page.tsx
│   ├── meetings/
│   │   └── page.tsx
│   ├── risks/
│   │   └── page.tsx
│   ├── resources/
│   │   └── page.tsx
│   └── status-reports/
│       └── page.tsx
├── components/
│   ├── Sidebar.tsx
│   ├── Header.tsx
│   ├── Footer.tsx
│   └── ...
├── lib/
│   ├── api.ts (API service)
│   └── utils.ts
├── .env.local
└── package.json
```

## PRIORITY FEATURES:
1. Working backend connection
2. Dashboard with health check
3. CRUD operations for all entities
4. Error handling and user feedback
5. Responsive UI

Create a production-ready, clean, and maintainable frontend application.
