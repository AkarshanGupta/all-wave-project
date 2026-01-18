# Module 3: Resource Allocation Optimizer

## Overview
The Resource Allocation Optimizer provides intelligent resource management capabilities including optimal allocation recommendations, conflict detection, utilization analysis, and what-if scenario planning.

## Key Features

### 1. Resource Profiles
Resources now include:
- **Skills**: Each resource can have multiple skills with proficiency levels (1-5)
- **Department**: Organizational unit
- **Location**: Physical or virtual location
- **Capacity**: Total available hours
- **Availability**: Current available hours

### 2. Project Requirements
Projects can define:
- **Required Skills**: Skills needed with minimum proficiency levels
- **Required Hours**: Hours needed for each skill
- **Priority**: Project priority (1-10 scale, 10 being highest)
- **Timeline**: Start date and deadline

### 3. Utilization Analysis
Monitor resource utilization across the organization:
- **Under-utilized**: < 60% capacity used
- **Optimal**: 60-90% capacity used
- **Over-utilized**: > 90% capacity used

### 4. Scheduling Conflict Detection
Automatically detect:
- **Over-allocation**: Resources allocated beyond capacity
- **Date overlaps**: Same resource on multiple projects simultaneously
- **Skill mismatches**: Resources without required skills

### 5. Optimal Allocation Recommendations
AI-powered recommendations based on:
- **Skill Matching** (70% weight): Match resource skills to project requirements
- **Availability** (30% weight): Current resource availability
- **Development Opportunities**: Consider skill growth
- **Match Score**: 0-100 score for each resource-project pair

### 6. What-If Scenario Analysis
Test allocation strategies without affecting actual data:
- Create multiple scenarios
- Compare scenarios side-by-side
- Analyze metrics (hours, resources, efficiency)
- Get recommendations for best approach

## Database Schema Changes

### New Tables

#### resource_skills
```sql
- id (PK)
- resource_id (FK -> resources)
- skill_name (string, indexed)
- proficiency_level (1-5)
```

#### project_requirements
```sql
- id (PK)
- project_id (FK -> projects)
- skill_name (string, indexed)
- required_proficiency (1-5)
- required_hours (decimal)
- description (text)
```

#### allocation_scenarios
```sql
- id (PK)
- name (string)
- description (text)
- scenario_data (JSON)
- metrics (JSON)
- created_at, updated_at
```

### Modified Tables

#### projects (added)
```sql
- priority (integer, default 5)
- start_date (datetime)
- deadline (datetime)
```

#### resources (added)
```sql
- department (string)
- location (string)
```

## API Endpoints

### Resource Management

#### GET /resources/utilization/all
Get utilization metrics for all resources.
```json
Response: [
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

#### GET /resources/utilization/{resource_id}
Get utilization for a specific resource.

#### GET /resources/conflicts/detect?project_id={id}
Detect scheduling conflicts (optionally filtered by project).
```json
Response: [
  {
    "resource_id": 2,
    "resource_name": "Jane Smith",
    "conflict_type": "over-allocation",
    "description": "Resource is over-allocated by 20 hours",
    "affected_projects": [1, 3, 5],
    "severity": "high",
    "suggested_resolution": "Reduce allocation or increase capacity by 20 hours"
  }
]
```

#### POST /resources/optimize/{project_id}
Get optimal allocation recommendations for a project.
```json
Response: {
  "recommendations": [
    {
      "resource_id": 1,
      "resource_name": "John Doe",
      "project_id": 5,
      "project_name": "Mobile App",
      "match_score": 92.5,
      "skill_match": {
        "React": {"required": 4, "actual": 5, "match": "excellent"},
        "TypeScript": {"required": 3, "actual": 4, "match": "excellent"}
      },
      "availability_score": 85.0,
      "reasoning": "Excellent skill match; 68.0h available"
    }
  ],
  "conflicts": [...],
  "utilization_summary": {
    "total_resources": 10,
    "under_utilized": 2,
    "optimal": 6,
    "over_utilized": 2,
    "avg_utilization": 72.5
  },
  "optimization_score": 75
}
```

### Skills & Requirements

#### POST /resources/skills/{resource_id}
Add a skill to a resource.
```json
Request: {
  "skill_name": "Python",
  "proficiency_level": 4
}
```

#### POST /resources/requirements/{project_id}
Add a skill requirement to a project.
```json
Request: {
  "project_id": 5,
  "skill_name": "Python",
  "required_proficiency": 3,
  "required_hours": 80,
  "description": "Backend API development"
}
```

### Scenario Planning

#### POST /resources/scenarios
Create a what-if scenario.
```json
Request: {
  "name": "Q1 2026 Allocation",
  "description": "Proposed allocation for Q1",
  "allocations": [
    {
      "resource_id": 1,
      "project_id": 5,
      "allocated_hours": 80,
      "start_date": "2026-01-01T00:00:00Z",
      "end_date": "2026-03-31T23:59:59Z"
    }
  ]
}

Response: {
  "id": 1,
  "name": "Q1 2026 Allocation",
  "metrics": {
    "total_allocated_hours": 480,
    "resources_involved": 6,
    "projects_involved": 3,
    "allocations_count": 12
  }
}
```

#### POST /resources/scenarios/compare
Compare multiple scenarios.
```json
Request: [1, 2, 3]

Response: {
  "scenarios": [...],
  "comparison_metrics": {
    "total_hours": [480, 520, 450],
    "resources_used": [6, 8, 5],
    "projects_covered": [3, 4, 3]
  },
  "recommendations": "Scenario 'Q1 2026 Allocation' appears most efficient with 450 total hours allocated."
}
```

### Resource Creation (Enhanced)

#### POST /resources
Create a resource with skills.
```json
Request: {
  "name": "John Doe",
  "role": "Senior Developer",
  "capacity_hours": 160,
  "availability_hours": 160,
  "department": "Engineering",
  "location": "Remote",
  "skills": [
    {"skill_name": "Python", "proficiency_level": 5},
    {"skill_name": "React", "proficiency_level": 4},
    {"skill_name": "AWS", "proficiency_level": 3}
  ]
}
```

## Migration

Run the migration to update your database:

```bash
# Windows
migrate.bat

# Linux/Mac
./migrate.sh
```

The migration file `003_add_allocation_optimizer.py` will:
1. Add new columns to `projects` and `resources` tables
2. Create `resource_skills`, `project_requirements`, and `allocation_scenarios` tables
3. Add appropriate indexes for performance

## Usage Examples

### Example 1: Setup Resource with Skills
```python
# 1. Create resource with skills
POST /resources
{
  "name": "Alice Johnson",
  "role": "Full Stack Developer",
  "capacity_hours": 160,
  "availability_hours": 160,
  "department": "Engineering",
  "skills": [
    {"skill_name": "React", "proficiency_level": 5},
    {"skill_name": "Node.js", "proficiency_level": 4},
    {"skill_name": "PostgreSQL", "proficiency_level": 4}
  ]
}
```

### Example 2: Define Project Requirements
```python
# 1. Add requirements to project
POST /resources/requirements/5
{
  "skill_name": "React",
  "required_proficiency": 4,
  "required_hours": 80,
  "description": "Frontend development"
}

POST /resources/requirements/5
{
  "skill_name": "Node.js",
  "required_proficiency": 3,
  "required_hours": 60,
  "description": "Backend API"
}
```

### Example 3: Get Optimization Recommendations
```python
# Get recommendations for project 5
POST /resources/optimize/5

# Returns top-matching resources with skill analysis
```

### Example 4: Detect and Resolve Conflicts
```python
# 1. Check for conflicts
GET /resources/conflicts/detect

# 2. Review conflicts and suggested resolutions
# 3. Adjust allocations based on recommendations
```

### Example 5: Compare Allocation Strategies
```python
# 1. Create scenario A
POST /resources/scenarios
{
  "name": "Conservative Approach",
  "allocations": [...]
}

# 2. Create scenario B
POST /resources/scenarios
{
  "name": "Aggressive Approach",
  "allocations": [...]
}

# 3. Compare
POST /resources/scenarios/compare
[1, 2]
```

## Key Algorithms

### Skill Match Score
```
For each project requirement:
  if resource_proficiency >= required_proficiency:
    score = 100 (perfect match)
  else if resource_proficiency > 0:
    score = (resource_proficiency / required_proficiency) * 80
  else:
    score = 0

overall_score = average(all_requirement_scores)
```

### Resource Match Score
```
match_score = (skill_match_score * 0.7) + (availability_score * 0.3)
```

### Utilization Status
```
if utilization < 60%: "under-utilized"
elif utilization <= 90%: "optimal"
else: "over-utilized"
```

### Conflict Severity
- **High**: Over-allocation > 20% capacity
- **Medium**: Date overlaps, over-allocation < 20%
- **Low**: Minor skill mismatches

## Benefits

1. **Efficiency**: Optimize resource allocation to maximize productivity
2. **Visibility**: Real-time view of resource utilization across organization
3. **Risk Mitigation**: Detect and resolve conflicts before they impact projects
4. **Data-Driven**: Make allocation decisions based on skills, availability, and metrics
5. **Planning**: Test different strategies with what-if scenarios
6. **Development**: Consider skill growth opportunities in allocations
7. **Scalability**: Handle complex multi-project, multi-resource environments

## Future Enhancements

- Machine learning for predictive allocation
- Cost optimization based on resource rates
- Team dynamics and collaboration patterns
- Automated conflict resolution suggestions
- Integration with calendar systems
- Resource forecasting and demand prediction
- Skills gap analysis
- Training recommendations
