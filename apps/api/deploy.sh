#!/bin/bash

# Deployment script for CG Stewart's Django Portfolio Backend
# This script handles the complete deployment process

set -e  # Exit on any error

echo "🚀 Starting deployment of CG Stewart's Portfolio Backend..."

# Configuration
PROJECT_NAME="cgstewart-portfolio"
AWS_REGION="us-east-1"
ECR_REPOSITORY="${PROJECT_NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if AWS CLI is installed and configured
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if Pulumi is installed
    if ! command -v pulumi &> /dev/null; then
        log_error "Pulumi is not installed. Please install it first."
        exit 1
    fi
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials not configured. Please run 'aws configure'."
        exit 1
    fi
    
    log_info "Prerequisites check passed ✅"
}

# Get or create ECR repository
setup_ecr() {
    log_info "Setting up ECR repository..."
    
    # Check if repository exists
    if aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $AWS_REGION &> /dev/null; then
        log_info "ECR repository '$ECR_REPOSITORY' already exists"
    else
        log_info "Creating ECR repository '$ECR_REPOSITORY'..."
        aws ecr create-repository \
            --repository-name $ECR_REPOSITORY \
            --region $AWS_REGION \
            --image-scanning-configuration scanOnPush=true
    fi
    
    # Get repository URI
    ECR_URI=$(aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $AWS_REGION --query 'repositories[0].repositoryUri' --output text)
    log_info "ECR Repository URI: $ECR_URI"
}

# Build and push Docker image
build_and_push_image() {
    log_info "Building and pushing Docker image..."
    
    # Get ECR login token
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI
    
    # Build image
    log_info "Building Docker image..."
    docker build -t $PROJECT_NAME .
    
    # Tag image
    docker tag $PROJECT_NAME:latest $ECR_URI:latest
    
    # Push image
    log_info "Pushing image to ECR..."
    docker push $ECR_URI:latest
    
    log_info "Docker image pushed successfully ✅"
}

# Deploy infrastructure with Pulumi
deploy_infrastructure() {
    log_info "Deploying infrastructure with Pulumi..."
    
    cd infrastructure
    
    # Initialize Pulumi stack if it doesn't exist
    if ! pulumi stack ls | grep -q "production"; then
        log_info "Creating Pulumi stack 'production'..."
        pulumi stack init production
    else
        log_info "Using existing Pulumi stack 'production'"
        pulumi stack select production
    fi
    
    # Set configuration
    if [ -z "$S3_BUCKET_NAME" ]; then
        log_warn "S3_BUCKET_NAME environment variable not set. Please set it:"
        read -p "Enter your existing S3 bucket name: " S3_BUCKET_NAME
    fi
    
    pulumi config set s3_bucket_name $S3_BUCKET_NAME
    pulumi config set environment production
    
    # Update the task definition with the actual ECR URI
    log_info "Updating task definition with ECR URI..."
    
    # Deploy infrastructure
    log_info "Running Pulumi deployment..."
    pulumi up --yes
    
    # Get outputs
    DYNAMODB_BIO_TABLE=$(pulumi stack output dynamodb_tables --json | jq -r '.bio')
    DYNAMODB_POSTS_TABLE=$(pulumi stack output dynamodb_tables --json | jq -r '.posts')
    DYNAMODB_VIDEOS_TABLE=$(pulumi stack output dynamodb_tables --json | jq -r '.videos')
    DYNAMODB_PROJECTS_TABLE=$(pulumi stack output dynamodb_tables --json | jq -r '.projects')
    LOAD_BALANCER_DNS=$(pulumi stack output load_balancer_dns)
    
    log_info "Infrastructure deployed successfully ✅"
    log_info "Load Balancer DNS: $LOAD_BALANCER_DNS"
    
    cd ..
}

# Update ECS service with new image
update_ecs_service() {
    log_info "Updating ECS service..."
    
    # Get cluster and service names from Pulumi
    cd infrastructure
    CLUSTER_NAME=$(pulumi stack output ecs_cluster_name)
    cd ..
    
    # Force new deployment
    aws ecs update-service \
        --cluster $CLUSTER_NAME \
        --service "${PROJECT_NAME}-production" \
        --force-new-deployment \
        --region $AWS_REGION
    
    log_info "ECS service update initiated ✅"
}

# Create sample data
create_sample_data() {
    log_info "Creating sample data..."
    
    # Set environment variables for the script
    export DYNAMODB_BIO_TABLE=$DYNAMODB_BIO_TABLE
    export DYNAMODB_POSTS_TABLE=$DYNAMODB_POSTS_TABLE
    export DYNAMODB_VIDEOS_TABLE=$DYNAMODB_VIDEOS_TABLE
    export DYNAMODB_PROJECTS_TABLE=$DYNAMODB_PROJECTS_TABLE
    export AWS_REGION=$AWS_REGION
    
    # Run the sample data creation script
    uv run python manage_dynamo.py sample
    
    log_info "Sample data created ✅"
}

# Main deployment function
main() {
    case "${1:-all}" in
        "prereq")
            check_prerequisites
            ;;
        "ecr")
            setup_ecr
            ;;
        "build")
            build_and_push_image
            ;;
        "infra")
            deploy_infrastructure
            ;;
        "update")
            update_ecs_service
            ;;
        "sample")
            create_sample_data
            ;;
        "all")
            check_prerequisites
            setup_ecr
            build_and_push_image
            deploy_infrastructure
            update_ecs_service
            
            log_info "🎉 Deployment completed successfully!"
            log_info "Your application is available at: http://$LOAD_BALANCER_DNS"
            log_info ""
            log_info "Next steps:"
            log_info "1. Wait a few minutes for the service to start"
            log_info "2. Create sample data: ./deploy.sh sample"
            log_info "3. Access your Django admin at: http://$LOAD_BALANCER_DNS/admin/"
            ;;
        *)
            echo "Usage: $0 {prereq|ecr|build|infra|update|sample|all}"
            echo ""
            echo "Commands:"
            echo "  prereq  - Check prerequisites"
            echo "  ecr     - Setup ECR repository"
            echo "  build   - Build and push Docker image"
            echo "  infra   - Deploy infrastructure with Pulumi"
            echo "  update  - Update ECS service"
            echo "  sample  - Create sample data"
            echo "  all     - Run complete deployment (default)"
            exit 1
            ;;
    esac
}

main "$@"
