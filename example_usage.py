#!/usr/bin/env python3
"""
Example usage of the Multi-Agent System Generator
"""

from multi_agent_generator import MultiAgentGenerator
import os

# Make sure you have your API key set
if not os.getenv('ANTHROPIC_API_KEY'):
    print("⚠️  Warning: ANTHROPIC_API_KEY not set!")
    print("Set it with: export ANTHROPIC_API_KEY='your-key'")
    exit(1)

# Create generator instance
generator = MultiAgentGenerator()

print("="*80)
print("Example 1: Simple Redis + Worker System")
print("="*80)

spec1 = """
Create a simple job queue system:

Agent 1: Redis server on default port
Agent 2: Python producer script that adds jobs (JSON format) to Redis list 'jobs' every 3 seconds
Agent 3: Python worker script that pops jobs from the list and processes them

Job format: {"job_id": "uuid", "task": "process_data", "priority": 1-10}
"""

files1 = generator.generate_system(
    spec=spec1,
    output_dir="./example-redis-system"
)

print(f"\n✅ Generated {len(files1)} files in ./example-redis-system/")
print("To run: cd example-redis-system && docker-compose up\n")

print("="*80)
print("Example 2: Database Analytics Pipeline")
print("="*80)

spec2 = """
Create an analytics data pipeline:

Agent 1: PostgreSQL database
- Database: analytics_db
- Table: page_views (id, user_id, page_url, timestamp)

Agent 2: Python event generator
- Generates random page view events every 2 seconds
- Inserts into page_views table

Agent 3: Python aggregator  
- Runs every 30 seconds
- Counts page views per user
- Prints top 10 users to console

Agent 4: Python REST API (FastAPI)
- GET /stats - returns page view statistics
- GET /users/{user_id}/views - returns views for specific user
- Port 8000
"""

files2 = generator.generate_system(
    spec=spec2,
    output_dir="./example-analytics-pipeline"
)

print(f"\n✅ Generated {len(files2)} files in ./example-analytics-pipeline/")
print("To run: cd example-analytics-pipeline && docker-compose up\n")

print("="*80)
print("Example 3: Iterative Development")
print("="*80)

# Start with basic system
basic_spec = """
Agent 1: MongoDB on default port
Agent 2: Python script that inserts documents every 5 seconds
"""

files3 = generator.generate_system(
    spec=basic_spec,
    output_dir="./example-mongodb-system"
)

print(f"✅ Initial system: {len(files3)} files")

# Now add a query agent
files3 = generator.iterate_on_system(
    spec=basic_spec,
    modification="Add a third agent that queries MongoDB and prints document count every 10 seconds",
    existing_files=files3,
    output_dir="./example-mongodb-system"
)

print(f"✅ After iteration 1: Added query agent")

# Add monitoring
files3 = generator.iterate_on_system(
    spec=basic_spec,
    modification="Add logging to file for all agents, log to /app/logs directory",
    existing_files=files3,
    output_dir="./example-mongodb-system"
)

print(f"✅ After iteration 2: Added logging")
print(f"Final system in ./example-mongodb-system/\n")

print("="*80)
print("All examples generated! Review the directories and run with docker-compose.")
print("="*80)
