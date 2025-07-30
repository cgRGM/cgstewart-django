# AWS CodePipeline CI/CD Setup

## Overview
This document describes the automated CI/CD pipeline for the CG Stewart Django API backend using AWS CodePipeline, CodeBuild, and ECS.

## Infrastructure Components

### 1. ECR Repository
- **Name**: `cgstewart-portfolio-api`
- **Purpose**: Stores Docker images for the Django application
- **Lifecycle Policy**: Keeps only the 10 most recent images

### 2. CodeBuild Project
- **Name**: `cgstewart-portfolio-build`
- **Purpose**: Builds Docker images, runs migrations, creates admin user, and pushes to ECR
- **Build Environment**: Amazon Linux 2, Docker runtime
- **Build Spec**: `apps/api/buildspec.yml`

### 3. CodePipeline
- **Name**: `cgstewart-portfolio-pipeline`
- **Stages**:
  1. **Source**: GitHub repository (`cgRGM/cgstewart-django`, branch `main`)
  2. **Build**: CodeBuild project for Docker build and Django setup
  3. **Deploy**: ECS service update with new Docker image

### 4. S3 Artifact Bucket
- **Name**: `cgstewart-portfolio-pipeline-artifacts-production`
- **Purpose**: Stores pipeline artifacts between stages

## Environment Variables (CodeBuild)

The CodeBuild project is configured with the following environment variables:

### AWS Resources
- `AWS_DEFAULT_REGION`: us-east-1
- `AWS_ACCOUNT_ID`: 992382618631
- `ECR_REPOSITORY_URI`: [ECR repository URL]

### Django Configuration
- `DJANGO_ADMIN_USERNAME`: [From Pulumi secrets]
- `DJANGO_ADMIN_EMAIL`: [From Pulumi secrets]
- `DJANGO_ADMIN_PASSWORD`: [From Pulumi secrets]

### DynamoDB Tables
- `BIO_TABLE_NAME`: cgstewart-portfolio-bio-production
- `POSTS_TABLE_NAME`: cgstewart-portfolio-posts-production
- `VIDEOS_TABLE_NAME`: cgstewart-portfolio-videos-production
- `PROJECTS_TABLE_NAME`: cgstewart-portfolio-projects-production

### S3 Configuration
- `STATIC_BUCKET_NAME`: cgstewart-portfolio

## GitHub Connection Setup

### Step 1: Authorize GitHub Connection
1. Go to AWS Console → Developer Tools → CodeStar Connections
2. Find connection: `cgstewart-portfolio-gh-conn`
3. Click "Update pending connection"
4. Authorize access to your GitHub repository `cgRGM/cgstewart-django`

**Connection ARN**: `arn:aws:codestar-connections:us-east-1:992382618631:connection/b0bc6bca-9987-432d-8628-cce51bf7e596`

## Pipeline Workflow

### Trigger
- Pipeline automatically triggers on pushes to the `main` branch of `cgRGM/cgstewart-django`

### Build Process (buildspec.yml)
1. **Pre-build**:
   - Login to ECR
   - Set up environment variables

2. **Build**:
   - Build Docker image with tag `latest`
   - Run Django migrations in temporary container
   - Create Django admin user in temporary container
   - Collect static files to S3

3. **Post-build**:
   - Push Docker image to ECR
   - Create `imagedefinitions.json` for ECS deployment

### Deploy Process
- ECS service automatically updates with new Docker image
- Zero-downtime deployment with rolling updates
- Health checks ensure successful deployment

## Manual Testing

### Test the Pipeline
1. Make a code change and push to `main` branch
2. Monitor pipeline execution in AWS Console → CodePipeline
3. Check CodeBuild logs for build details
4. Verify ECS service update and container health

### Check Deployment
```bash
# Check ECS service status
aws ecs describe-services --cluster cgstewart-portfolio-cluster --services cgstewart-portfolio-service

# Check container logs
aws logs tail /ecs/cgstewart-portfolio --follow
```

## Security Features

### IAM Roles and Policies
- **CodePipeline Role**: Minimal permissions for pipeline orchestration
- **CodeBuild Role**: Permissions for ECR, ECS, DynamoDB, and S3 access
- **ECS Task Role**: Runtime permissions for Django application

### Secrets Management
- Django admin credentials stored as Pulumi secrets
- Environment variables injected securely into build and runtime environments

## Monitoring and Troubleshooting

### Pipeline Monitoring
- AWS Console → CodePipeline → `cgstewart-portfolio-pipeline`
- CloudWatch logs for CodeBuild: `/aws/codebuild/cgstewart-portfolio-build`
- ECS logs: `/ecs/cgstewart-portfolio`

### Common Issues
1. **Build Failures**: Check CodeBuild logs for dependency or Docker issues
2. **Deploy Failures**: Verify ECS service health and container startup
3. **GitHub Connection**: Ensure connection is authorized and repository access is granted

## Production Endpoints

- **API**: https://api.byoui.com/api/v1/
- **Admin**: https://api.byoui.com/admin/
- **Health Check**: https://api.byoui.com/health/

## Next Steps

1. ✅ Authorize GitHub connection in AWS Console
2. ✅ Test pipeline by pushing code changes
3. ✅ Monitor first deployment
4. ✅ Verify Django admin access with Pulumi-managed credentials
5. ✅ Document any additional configuration needed

---

**Last Updated**: July 30, 2025
**Pulumi Stack**: `cgstewart-portfolio-backend-production`
