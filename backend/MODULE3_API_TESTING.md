# Module 3 API Testing Guide

Quick reference for testing the Resource Allocation Optimizer endpoints.

## Base URL
```
Production: https://all-wave-project.onrender.com
Local: http://localhost:8000
```

## Quick Start Examples

### 1. Create a Resource with Skills

```bash
curl -X POST "https://all-wave-project.onrender.com/resources" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "role": "Full Stack Developer",
    "capacity_hours": 160,
    "availability_hours": 160,
    "department": "Engineering",
    "location": "Remote",
    "skills": [
      {"skill_name": "React", "proficiency_level": 5},
      {"skill_name": "Python", "proficiency_level": 4},
      {"skill_name": "AWS", "proficiency_level": 3}
    ]
  }'
```

### 2. Add Project Requirements

```bash
curl -X POST "https://all-wave-project.onrender.com/resources/requirements/1" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "skill_name": "React",
    "required_proficiency": 4,
    "required_hours": 120,
    "description": "Frontend development"
  }'
```

### 3. Get Resource Utilization

```bash
# All resources
curl "https://all-wave-project.onrender.com/resources/utilization/all"

# Specific resource
curl "https://all-wave-project.onrender.com/resources/utilization/1"
```

### 4. Detect Conflicts

```bash
# All conflicts
curl "https://all-wave-project.onrender.com/resources/conflicts/detect"

# Project-specific
curl "https://all-wave-project.onrender.com/resources/conflicts/detect?project_id=1"
```

### 5. Get Optimization Recommendations

```bash
curl -X POST "https://all-wave-project.onrender.com/resources/optimize/1"
```

### 6. Create What-If Scenario

```bash
curl -X POST "https://all-wave-project.onrender.com/resources/scenarios" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q1 2026 Plan",
    "description": "Proposed allocation for Q1",
    "allocations": [
      {
        "resource_id": 1,
        "project_id": 1,
        "allocated_hours": 80,
        "start_date": "2026-01-01T00:00:00Z",
        "end_date": "2026-03-31T23:59:59Z"
      }
    ]
  }'
```

### 7. Compare Scenarios

```bash
curl -X POST "https://all-wave-project.onrender.com/resources/scenarios/compare" \
  -H "Content-Type: application/json" \
  -d '[1, 2, 3]'
```

## Test in Python

```python
import requests

BASE_URL = "https://all-wave-project.onrender.com"

# 1. Create resource
resource = requests.post(f"{BASE_URL}/resources", json={
    "name": "Alice Smith",
    "role": "Senior Developer",
    "capacity_hours": 160,
    "availability_hours": 160,
    "department": "Engineering",
    "skills": [
        {"skill_name": "Python", "proficiency_level": 5},
        {"skill_name": "Django", "proficiency_level": 4}
    ]
}).json()

print(f"Created resource: {resource['id']}")

# 2. Check utilization
utilization = requests.get(f"{BASE_URL}/resources/utilization/all").json()
for r in utilization:
    print(f"{r['resource_name']}: {r['utilization_percentage']}% ({r['status']})")

# 3. Get optimization
optimization = requests.post(f"{BASE_URL}/resources/optimize/1").json()
print(f"Optimization score: {optimization['optimization_score']}")
print(f"Top recommendation: {optimization['recommendations'][0]['resource_name']}")
```

## Test with Postman

### Collection Structure
```
Module 3 Tests
├── Resources
│   ├── Create Resource with Skills
│   ├── Get All Resources
│   └── Add Skill to Resource
├── Projects
│   ├── Create Project with Priority
│   └── Add Requirement to Project
├── Utilization
│   ├── Get All Utilization
│   └── Get Single Resource Utilization
├── Conflicts
│   └── Detect All Conflicts
├── Optimization
│   └── Get Recommendations for Project
└── Scenarios
    ├── Create Scenario
    └── Compare Scenarios
```

## Expected Responses

### Utilization Response
```json
[
  {
    "resource_id": 1,
    "resource_name": "John Doe",
    "capacity_hours": 160,
    "allocated_hours": 120,
    "available_hours": 40,
    "utilization_percentage": 75.0,
    "status": "optimal",
    "allocations": [...]
  }
]
```

### Conflict Response
```json
[
  {
    "resource_id": 2,
    "resource_name": "Jane Smith",
    "conflict_type": "over-allocation",
    "description": "Resource is over-allocated by 20 hours",
    "affected_projects": [1, 3],
    "severity": "high",
    "suggested_resolution": "Reduce allocation by 20 hours"
  }
]
```

### Optimization Response
```json
{
  "recommendations": [
    {
      "resource_id": 1,
      "resource_name": "John Doe",
      "match_score": 92.5,
      "skill_match": {
        "React": {"required": 4, "actual": 5, "match": "excellent"}
      },
      "availability_score": 85.0,
      "reasoning": "Excellent skill match; 68.0h available"
    }
  ],
  "conflicts": [],
  "utilization_summary": {
    "total_resources": 10,
    "under_utilized": 2,
    "optimal": 6,
    "over_utilized": 2,
    "avg_utilization": 72.5
  },
  "optimization_score": 85
}
```

## Status Codes

- `200` - Success (GET)
- `201` - Created (POST)
- `400` - Bad Request (validation error)
- `404` - Not Found
- `500` - Internal Server Error

## Common Issues

### Issue: "Resource not found"
**Solution**: Verify resource_id exists
```bash
curl "https://all-wave-project.onrender.com/resources"
```

### Issue: "Project not found"
**Solution**: Create project first
```bash
curl -X POST "https://all-wave-project.onrender.com/projects" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "status": "active", "priority": 5}'
```

### Issue: Empty recommendations
**Solution**: Add project requirements
```bash
curl -X POST "https://all-wave-project.onrender.com/resources/requirements/{project_id}" \
  -d '{"skill_name": "Python", "required_proficiency": 3, "required_hours": 80}'
```

## Full Test Sequence

```bash
# 1. Create project
PROJECT=$(curl -X POST "https://all-wave-project.onrender.com/projects" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mobile App", "priority": 8}' | jq -r '.id')

# 2. Add requirement
curl -X POST "https://all-wave-project.onrender.com/resources/requirements/$PROJECT" \
  -H "Content-Type: application/json" \
  -d '{"project_id": '$PROJECT', "skill_name": "React Native", "required_proficiency": 4, "required_hours": 100}'

# 3. Create resource
RESOURCE=$(curl -X POST "https://all-wave-project.onrender.com/resources" \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob Dev", "role": "Mobile Developer", "capacity_hours": 160, "availability_hours": 160, "skills": [{"skill_name": "React Native", "proficiency_level": 5}]}' | jq -r '.id')

# 4. Get optimization
curl -X POST "https://all-wave-project.onrender.com/resources/optimize/$PROJECT"

# 5. Check utilization
curl "https://all-wave-project.onrender.com/resources/utilization/all"
```

## Automated Testing

Run the comprehensive test suite:

```bash
cd backend
python test_module3.py
```

This will test all Module 3 features end-to-end.
