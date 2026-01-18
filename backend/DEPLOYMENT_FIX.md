# Deployment Fix for Meeting 500 Error

## Issue
The `/meetings` endpoint returns a 500 error because the database migration for new meeting fields hasn't been applied.

## What Was Fixed

### 1. Database Migration (004_add_meeting_fields.py)
- Changed `attendees` from JSON to Text for database compatibility
- Made `status` nullable with default value
- Stores attendees as JSON string for SQLite/PostgreSQL compatibility

### 2. Meeting Model
- Added property getter/setter for `attendees` to handle JSON serialization
- Stores attendees internally as JSON string
- Automatically converts between list and JSON string

### 3. Meeting API
- Added date parsing to convert string dates to date objects
- Handles date conversion errors gracefully
- Properly serializes dates back to strings in responses

### 4. Meeting Schema  
- Added custom field serializer for date conversion
- Ensures dates are returned as "YYYY-MM-DD" strings

## How to Fix on Render

### Option 1: Trigger Redeploy (Recommended)
1. Push these changes to your repository
2. Go to Render dashboard
3. Click "Manual Deploy" → "Deploy latest commit"
4. The `start.sh` script will automatically run migrations

### Option 2: Manual Migration (If needed)
If the automatic migration fails, run manually:
```bash
# SSH into your Render instance or use Shell tab
cd /opt/render/project/src/backend
python run_migrations.py
```

## Verification
After redeployment, test:
```bash
curl https://all-wave-project.onrender.com/meetings
```

Should return `[]` (empty array) instead of 500 error.

## Files Changed
- `backend/alembic/versions/004_add_meeting_fields.py` - Migration file
- `backend/app/models/meeting.py` - Model with JSON property
- `backend/app/schemas/meeting.py` - Schema with date serializer
- `backend/app/api/meeting.py` - API with date parsing
