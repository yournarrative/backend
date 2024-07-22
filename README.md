## Narrative Backend

### How to Run
1. Run `poetry install` to install all dependencies
2. Run `docker compose up --build` or use Pycharm run configs to launch services.
3. Hit endpoints using Postman or any other tool. Test script available in `tests/manual_test_script.py`

### Resources Used
AWS ECS Setup: https://www.youtube.com/watch?v=esISkPlnxL0
SimpleAIChat for Structured LLM Outputs: https://minimaxir.com/2023/12/chatgpt-structured-data/
Instructor for Structured LLM Outputs: https://learnbybuilding.ai/tutorials/structured-data-extraction-with-instructor-and-llms

### Notes:
AWS Setup for subdomain (backend.prod.narrative.ai)
1. Go to Route 53 Hosted Zone
2. Create a new record set
3. Create CNAME record of the subdomain and point it to the load balancer DNS name (gotten from EC2 ALB service)

