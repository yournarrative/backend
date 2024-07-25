## Narrative Backend

### How to Run

2. Run `docker compose up --build` or use Pycharm run configs to launch services.
3. Hit endpoints using Postman or any other tool. Test script available in `tests/manual_test_script.py`

### Local Development

1. Run `poetry install` to install all dependencies (for local dev, optional if using Docker)
2. Test pre-commit hooks `pre-commit run --all-files`

### Resources Used

AWS ECS Setup: https://www.youtube.com/watch?v=esISkPlnxL0
SimpleAIChat for Structured LLM Outputs: https://minimaxir.com/2023/12/chatgpt-structured-data/
Instructor for Structured LLM Outputs: https://learnbybuilding.ai/tutorials/structured-data-extraction-with-instructor-and-llms

### Notes:

AWS Setup for subdomain (backend.prod.narrative.ai)

1. Go to Route 53 Hosted Zone
2. Create a new record set
3. Create CNAME record of the subdomain and point it to the load balancer DNS name (gotten from EC2 ALB service)

### TODO:

1. Read the FastAPI docs gg
   1. Check CORS accuracy
   2. Figure out right pattern for tests and write them
   3. Update security to check if updated activities belong to a user
   4. Session cookie handling?
2. Update data schema to store company data field for each activity
3. Create a VPN and hide a staging env behind it, so we can test the API without exposing it to the world
4. Update security group outbound rules to not be everything
