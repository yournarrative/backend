## INFRASTRUCTURE

### Code Management
1. Github project: https://github.com/SilverMVP
2. Github actions under `.github/workflows/main.yaml` to build and deploy backend image to AWS ECR upon successful merge with main branch.

### AWS Process
1. Use ECR Repo to host Docker images
2. Use ECS cluster to deploy using task definition and task deployment on Fargate
3. Default VPC and security group used
   1. Security group allows all inbound traffic on port 5001
4. Manually revise & deploy task definition to update image version
5. Lambda will be created on the AWS UI to read from S3 and invoke backend service