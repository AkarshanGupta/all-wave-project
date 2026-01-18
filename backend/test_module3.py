"""
Test script for Module 3: Resource Allocation Optimizer
Demonstrates all key features of the optimizer.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://all-wave-project.onrender.com"
# BASE_URL = "http://localhost:8000"  # Use this for local testing

def print_json(data, title="Response"):
    """Pretty print JSON data."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print('='*60)
    print(json.dumps(data, indent=2, default=str))
    print('='*60)

def test_create_project_with_requirements():
    """Test 1: Create a project with requirements."""
    print("\n📋 TEST 1: Creating project with requirements...")
    
    # Create project
    project_data = {
        "name": "E-Commerce Platform Rewrite",
        "description": "Modernize legacy e-commerce system",
        "status": "active",
        "priority": 9,
        "start_date": "2026-02-01T00:00:00Z",
        "deadline": "2026-06-30T23:59:59Z"
    }
    
    response = requests.post(f"{BASE_URL}/projects", json=project_data)
    project = response.json()
    print_json(project, "Created Project")
    
    project_id = project["id"]
    
    # Add requirements
    requirements = [
        {
            "project_id": project_id,
            "skill_name": "React",
            "required_proficiency": 4,
            "required_hours": 200,
            "description": "Frontend development with React and TypeScript"
        },
        {
            "project_id": project_id,
            "skill_name": "Node.js",
            "required_proficiency": 4,
            "required_hours": 160,
            "description": "Backend API development"
        },
        {
            "project_id": project_id,
            "skill_name": "PostgreSQL",
            "required_proficiency": 3,
            "required_hours": 80,
            "description": "Database design and optimization"
        },
        {
            "project_id": project_id,
            "skill_name": "AWS",
            "required_proficiency": 3,
            "required_hours": 60,
            "description": "Cloud infrastructure and deployment"
        }
    ]
    
    for req in requirements:
        response = requests.post(f"{BASE_URL}/resources/requirements/{project_id}", json=req)
        print(f"✅ Added requirement: {req['skill_name']}")
    
    return project_id

def test_create_resources_with_skills():
    """Test 2: Create resources with skills."""
    print("\n👥 TEST 2: Creating resources with skills...")
    
    resources = [
        {
            "name": "Sarah Chen",
            "role": "Senior Full Stack Developer",
            "capacity_hours": 160,
            "availability_hours": 160,
            "department": "Engineering",
            "location": "San Francisco",
            "skills": [
                {"skill_name": "React", "proficiency_level": 5},
                {"skill_name": "Node.js", "proficiency_level": 4},
                {"skill_name": "TypeScript", "proficiency_level": 5},
                {"skill_name": "AWS", "proficiency_level": 3}
            ]
        },
        {
            "name": "Michael Rodriguez",
            "role": "Backend Developer",
            "capacity_hours": 160,
            "availability_hours": 160,
            "department": "Engineering",
            "location": "Austin",
            "skills": [
                {"skill_name": "Node.js", "proficiency_level": 5},
                {"skill_name": "PostgreSQL", "proficiency_level": 4},
                {"skill_name": "Python", "proficiency_level": 4},
                {"skill_name": "AWS", "proficiency_level": 4}
            ]
        },
        {
            "name": "Emily Watson",
            "role": "Frontend Developer",
            "capacity_hours": 160,
            "availability_hours": 160,
            "department": "Engineering",
            "location": "Remote",
            "skills": [
                {"skill_name": "React", "proficiency_level": 4},
                {"skill_name": "Vue.js", "proficiency_level": 4},
                {"skill_name": "CSS", "proficiency_level": 5},
                {"skill_name": "TypeScript", "proficiency_level": 3}
            ]
        },
        {
            "name": "David Kim",
            "role": "DevOps Engineer",
            "capacity_hours": 160,
            "availability_hours": 160,
            "department": "Infrastructure",
            "location": "Seattle",
            "skills": [
                {"skill_name": "AWS", "proficiency_level": 5},
                {"skill_name": "Docker", "proficiency_level": 5},
                {"skill_name": "Kubernetes", "proficiency_level": 4},
                {"skill_name": "Python", "proficiency_level": 3}
            ]
        },
        {
            "name": "Lisa Martinez",
            "role": "Database Administrator",
            "capacity_hours": 160,
            "availability_hours": 160,
            "department": "Data",
            "location": "Chicago",
            "skills": [
                {"skill_name": "PostgreSQL", "proficiency_level": 5},
                {"skill_name": "MySQL", "proficiency_level": 4},
                {"skill_name": "MongoDB", "proficiency_level": 4},
                {"skill_name": "SQL", "proficiency_level": 5}
            ]
        }
    ]
    
    resource_ids = []
    for resource_data in resources:
        response = requests.post(f"{BASE_URL}/resources", json=resource_data)
        resource = response.json()
        resource_ids.append(resource["id"])
        print(f"✅ Created resource: {resource_data['name']} (ID: {resource['id']})")
    
    return resource_ids

def test_resource_utilization():
    """Test 3: Check resource utilization."""
    print("\n📊 TEST 3: Checking resource utilization...")
    
    response = requests.get(f"{BASE_URL}/resources/utilization/all")
    utilization = response.json()
    
    print_json(utilization, "Resource Utilization Summary")
    
    # Print summary
    print("\n📈 Utilization Summary:")
    for resource in utilization:
        status_emoji = "🟢" if resource["status"] == "optimal" else "🔴" if resource["status"] == "over-utilized" else "🟡"
        print(f"{status_emoji} {resource['resource_name']}: {resource['utilization_percentage']}% ({resource['status']})")

def test_detect_conflicts():
    """Test 4: Detect scheduling conflicts."""
    print("\n⚠️  TEST 4: Detecting scheduling conflicts...")
    
    response = requests.get(f"{BASE_URL}/resources/conflicts/detect")
    conflicts = response.json()
    
    if conflicts:
        print_json(conflicts, "Detected Conflicts")
        print(f"\n⚠️  Found {len(conflicts)} conflicts")
    else:
        print("✅ No conflicts detected!")

def test_optimal_allocation(project_id):
    """Test 5: Get optimal allocation recommendations."""
    print("\n🎯 TEST 5: Getting optimal allocation recommendations...")
    
    response = requests.post(f"{BASE_URL}/resources/optimize/{project_id}")
    optimization = response.json()
    
    print_json(optimization, "Optimization Results")
    
    # Print top recommendations
    print("\n🏆 Top Recommendations:")
    for i, rec in enumerate(optimization["recommendations"][:5], 1):
        print(f"\n{i}. {rec['resource_name']} (Match Score: {rec['match_score']}%)")
        print(f"   Reasoning: {rec['reasoning']}")
        print(f"   Skills:")
        for skill, details in rec["skill_match"].items():
            match_emoji = "✅" if details["match"] == "excellent" else "⚠️" if details["match"] == "partial" else "❌"
            print(f"      {match_emoji} {skill}: {details['actual']}/{details['required']}")

def test_create_scenario(resource_ids, project_id):
    """Test 6: Create and compare scenarios."""
    print("\n🔮 TEST 6: Creating what-if scenarios...")
    
    # Scenario 1: Balanced approach
    scenario1 = {
        "name": "Balanced Approach",
        "description": "Distribute work evenly across team",
        "allocations": [
            {
                "resource_id": resource_ids[0],
                "project_id": project_id,
                "allocated_hours": 80,
                "start_date": "2026-02-01T00:00:00Z",
                "end_date": "2026-03-31T23:59:59Z"
            },
            {
                "resource_id": resource_ids[1],
                "project_id": project_id,
                "allocated_hours": 80,
                "start_date": "2026-02-01T00:00:00Z",
                "end_date": "2026-03-31T23:59:59Z"
            },
            {
                "resource_id": resource_ids[2],
                "project_id": project_id,
                "allocated_hours": 80,
                "start_date": "2026-02-01T00:00:00Z",
                "end_date": "2026-03-31T23:59:59Z"
            }
        ]
    }
    
    # Scenario 2: Focused approach
    scenario2 = {
        "name": "Focused Approach",
        "description": "Concentrate resources on key personnel",
        "allocations": [
            {
                "resource_id": resource_ids[0],
                "project_id": project_id,
                "allocated_hours": 120,
                "start_date": "2026-02-01T00:00:00Z",
                "end_date": "2026-03-31T23:59:59Z"
            },
            {
                "resource_id": resource_ids[1],
                "project_id": project_id,
                "allocated_hours": 120,
                "start_date": "2026-02-01T00:00:00Z",
                "end_date": "2026-03-31T23:59:59Z"
            }
        ]
    }
    
    # Create scenarios
    response1 = requests.post(f"{BASE_URL}/resources/scenarios", json=scenario1)
    s1 = response1.json()
    print(f"✅ Created scenario: {s1['name']} (ID: {s1['id']})")
    
    response2 = requests.post(f"{BASE_URL}/resources/scenarios", json=scenario2)
    s2 = response2.json()
    print(f"✅ Created scenario: {s2['name']} (ID: {s2['id']})")
    
    # Compare scenarios
    print("\n📊 Comparing scenarios...")
    response = requests.post(f"{BASE_URL}/resources/scenarios/compare", json=[s1['id'], s2['id']])
    comparison = response.json()
    
    print_json(comparison, "Scenario Comparison")

def run_all_tests():
    """Run all tests in sequence."""
    print("\n" + "="*60)
    print("🚀 MODULE 3: RESOURCE ALLOCATION OPTIMIZER - FULL TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Create project with requirements
        project_id = test_create_project_with_requirements()
        
        # Test 2: Create resources with skills
        resource_ids = test_create_resources_with_skills()
        
        # Test 3: Check utilization
        test_resource_utilization()
        
        # Test 4: Detect conflicts
        test_detect_conflicts()
        
        # Test 5: Get optimal allocation
        test_optimal_allocation(project_id)
        
        # Test 6: Scenario planning
        test_create_scenario(resource_ids, project_id)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
