"""
Pulumi infrastructure for CG Stewart's Django Portfolio Backend
Creates DynamoDB tables, IAM roles, and ECS deployment resources
"""

import pulumi
import pulumi_aws as aws
from pulumi import Config, Output, export
import json
import time

# Configuration
config = Config()
project_name = "cgstewart-portfolio"
environment = config.get("environment") or "production"

# Django admin credentials from Pulumi config
django_admin_name = config.require("django-admin-name")
django_admin_password = config.require_secret("django-admin-password")
django_admin_email = config.require("django-admin-email")

# DynamoDB Tables
def create_dynamodb_tables():
    """Create DynamoDB tables for the portfolio"""
    
    # Bio table (single record)
    bio_table = aws.dynamodb.Table(
        f"{project_name}-bio",
        name=f"{project_name}-bio-{environment}",
        billing_mode="PAY_PER_REQUEST",  # Serverless billing
        attributes=[
            aws.dynamodb.TableAttributeArgs(
                name="id",
                type="S"
            )
        ],
        hash_key="id",
        tags={
            "Environment": environment,
            "Project": project_name,
            "Component": "bio"
        }
    )
    
    # Posts table
    posts_table = aws.dynamodb.Table(
        f"{project_name}-posts",
        name=f"{project_name}-posts-{environment}",
        billing_mode="PAY_PER_REQUEST",
        attributes=[
            aws.dynamodb.TableAttributeArgs(
                name="id",
                type="S"
            ),
            aws.dynamodb.TableAttributeArgs(
                name="slug",
                type="S"
            )
        ],
        hash_key="id",
        global_secondary_indexes=[
            aws.dynamodb.TableGlobalSecondaryIndexArgs(
                name="slug-index",
                hash_key="slug",
                projection_type="ALL"
            )
        ],
        tags={
            "Environment": environment,
            "Project": project_name,
            "Component": "posts"
        }
    )
    
    # Videos table
    videos_table = aws.dynamodb.Table(
        f"{project_name}-videos",
        name=f"{project_name}-videos-{environment}",
        billing_mode="PAY_PER_REQUEST",
        attributes=[
            aws.dynamodb.TableAttributeArgs(
                name="id",
                type="S"
            ),
            aws.dynamodb.TableAttributeArgs(
                name="slug",
                type="S"
            )
        ],
        hash_key="id",
        global_secondary_indexes=[
            aws.dynamodb.TableGlobalSecondaryIndexArgs(
                name="slug-index",
                hash_key="slug",
                projection_type="ALL"
            )
        ],
        tags={
            "Environment": environment,
            "Project": project_name,
            "Component": "videos"
        }
    )
    
    # Projects table
    projects_table = aws.dynamodb.Table(
        f"{project_name}-projects",
        name=f"{project_name}-projects-{environment}",
        billing_mode="PAY_PER_REQUEST",
        attributes=[
            aws.dynamodb.TableAttributeArgs(
                name="id",
                type="S"
            ),
            aws.dynamodb.TableAttributeArgs(
                name="slug",
                type="S"
            )
        ],
        hash_key="id",
        global_secondary_indexes=[
            aws.dynamodb.TableGlobalSecondaryIndexArgs(
                name="slug-index",
                hash_key="slug",
                projection_type="ALL"
            )
        ],
        tags={
            "Environment": environment,
            "Project": project_name,
            "Component": "projects"
        }
    )
    
    return {
        "bio": bio_table,
        "posts": posts_table,
        "videos": videos_table,
        "projects": projects_table
    }

# IAM Role for ECS Task
def create_ecs_task_role(dynamodb_tables, s3_bucket_name):
    """Create IAM role for ECS tasks with DynamoDB and S3 permissions"""
    
    # ECS Task Execution Role
    task_execution_role = aws.iam.Role(
        f"{project_name}-ecs-execution-role",
        assume_role_policy="""{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    }
                }
            ]
        }"""
    )
    
    # Attach basic ECS execution policy
    aws.iam.RolePolicyAttachment(
        f"{project_name}-ecs-execution-policy",
        role=task_execution_role.name,
        policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
    )
    
    # ECS Task Role (for application permissions)
    task_role = aws.iam.Role(
        f"{project_name}-ecs-task-role",
        assume_role_policy="""{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    }
                }
            ]
        }"""
    )
    
    # DynamoDB permissions
    dynamodb_policy = aws.iam.RolePolicy(
        f"{project_name}-dynamodb-policy",
        role=task_role.id,
        policy=pulumi.Output.all(
            bio_table=dynamodb_tables["bio"].arn,
            posts_table=dynamodb_tables["posts"].arn,
            videos_table=dynamodb_tables["videos"].arn,
            projects_table=dynamodb_tables["projects"].arn
        ).apply(lambda args: f"""{{
            "Version": "2012-10-17",
            "Statement": [
                {{
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                        "dynamodb:DeleteItem",
                        "dynamodb:Query",
                        "dynamodb:Scan",
                        "dynamodb:BatchGetItem",
                        "dynamodb:BatchWriteItem"
                    ],
                    "Resource": [
                        "{args['bio_table']}",
                        "{args['posts_table']}",
                        "{args['videos_table']}",
                        "{args['projects_table']}",
                        "{args['bio_table']}/index/*",
                        "{args['posts_table']}/index/*",
                        "{args['videos_table']}/index/*",
                        "{args['projects_table']}/index/*"
                    ]
                }}
            ]
        }}""")
    )
    
    # S3 permissions for existing bucket
    s3_policy = aws.iam.RolePolicy(
        f"{project_name}-s3-policy",
        role=task_role.id,
        policy=f"""{{
            "Version": "2012-10-17",
            "Statement": [
                {{
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        "arn:aws:s3:::{s3_bucket_name}",
                        "arn:aws:s3:::{s3_bucket_name}/*"
                    ]
                }}
            ]
        }}"""
    )
    
    return {
        "execution_role": task_execution_role,
        "task_role": task_role
    }

# VPC and Networking
def create_networking():
    """Create VPC, subnets, and security groups for ECS"""
    
    # Create VPC
    vpc = aws.ec2.Vpc(
        f"{project_name}-vpc",
        cidr_block="10.0.0.0/16",
        enable_dns_hostnames=True,
        enable_dns_support=True,
        tags={
            "Name": f"{project_name}-vpc",
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # Create Internet Gateway
    igw = aws.ec2.InternetGateway(
        f"{project_name}-igw",
        vpc_id=vpc.id,
        tags={
            "Name": f"{project_name}-igw",
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # Get available AZs
    azs = aws.get_availability_zones(state="available")
    
    # Create public subnets in first two AZs
    public_subnets = []
    for i in range(min(2, len(azs.names))):
        subnet = aws.ec2.Subnet(
            f"{project_name}-public-subnet-{i+1}",
            vpc_id=vpc.id,
            cidr_block=f"10.0.{i+1}.0/24",
            availability_zone=azs.names[i],
            map_public_ip_on_launch=True,
            tags={
                "Name": f"{project_name}-public-subnet-{i+1}",
                "Environment": environment,
                "Project": project_name
            }
        )
        public_subnets.append(subnet)
    
    # Create route table for public subnets
    public_rt = aws.ec2.RouteTable(
        f"{project_name}-public-rt",
        vpc_id=vpc.id,
        tags={
            "Name": f"{project_name}-public-rt",
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # Create route to Internet Gateway
    aws.ec2.Route(
        f"{project_name}-public-route",
        route_table_id=public_rt.id,
        destination_cidr_block="0.0.0.0/0",
        gateway_id=igw.id
    )
    
    # Associate public subnets with route table
    for i, subnet in enumerate(public_subnets):
        aws.ec2.RouteTableAssociation(
            f"{project_name}-public-rta-{i+1}",
            subnet_id=subnet.id,
            route_table_id=public_rt.id
        )
    
    # Security Group for ALB
    alb_security_group = aws.ec2.SecurityGroup(
        f"{project_name}-alb-sg",
        description="Security group for CG Stewart portfolio ALB",
        vpc_id=vpc.id,
        ingress=[
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=80,
                to_port=80,
                cidr_blocks=["0.0.0.0/0"]
            ),
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=443,
                to_port=443,
                cidr_blocks=["0.0.0.0/0"]
            )
        ],
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                protocol="-1",
                from_port=0,
                to_port=0,
                cidr_blocks=["0.0.0.0/0"]
            )
        ],
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # Security Group for ECS tasks
    ecs_security_group = aws.ec2.SecurityGroup(
        f"{project_name}-ecs-sg",
        description="Security group for CG Stewart portfolio ECS tasks",
        vpc_id=vpc.id,
        ingress=[
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=8000,
                to_port=8000,
                security_groups=[alb_security_group.id]
            )
        ],
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                protocol="-1",
                from_port=0,
                to_port=0,
                cidr_blocks=["0.0.0.0/0"]
            )
        ],
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    return {
        "vpc_id": vpc.id,
        "subnet_ids": [subnet.id for subnet in public_subnets],
        "alb_security_group": alb_security_group,
        "ecs_security_group": ecs_security_group
    }

# ECS Cluster and Service
def create_ecs_infrastructure(roles, networking, dynamodb_tables, django_admin_name, django_admin_password, django_admin_email, hosted_zone, s3_bucket_name, ecr_repository):
    """Create ECS cluster, task definition, and service"""
    
    # Domain configuration
    domain_name = config.require("domain_name")
    api_domain = f"api.{domain_name}"
    
    # ECS Cluster
    cluster = aws.ecs.Cluster(
        f"{project_name}-cluster",
        name=f"{project_name}-{environment}",
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # CloudWatch Log Group
    log_group = aws.cloudwatch.LogGroup(
        f"{project_name}-logs",
        name=f"/ecs/{project_name}-{environment}",
        retention_in_days=7,  # Keep logs for 7 days
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # ECS Task Definition
    task_definition = aws.ecs.TaskDefinition(
        f"{project_name}-task",
        family=f"{project_name}-{environment}",
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        cpu="256",  # 0.25 vCPU
        memory="512",  # 512 MB
        execution_role_arn=roles["execution_role"].arn,
        task_role_arn=roles["task_role"].arn,
        container_definitions=pulumi.Output.all(
            log_group_name=log_group.name,
            bio_table=dynamodb_tables["bio"].name,
            posts_table=dynamodb_tables["posts"].name,
            videos_table=dynamodb_tables["videos"].name,
            projects_table=dynamodb_tables["projects"].name,
            django_admin_name=django_admin_name,
            django_admin_password=django_admin_password,
            django_admin_email=django_admin_email,
            s3_bucket_name=s3_bucket_name,
            ecr_repository_url=ecr_repository.repository_url
        ).apply(lambda args: f"""[
            {{
                "name": "{project_name}-container",
                "image": "{args['ecr_repository_url']}:latest",
                "portMappings": [
                    {{
                        "containerPort": 8000,
                        "protocol": "tcp"
                    }}
                ],
                "essential": true,
                "logConfiguration": {{
                    "logDriver": "awslogs",
                    "options": {{
                        "awslogs-group": "{args['log_group_name']}",
                        "awslogs-region": "us-east-1",
                        "awslogs-stream-prefix": "ecs"
                    }}
                }},
                "environment": [
                    {{
                        "name": "DJANGO_SETTINGS_MODULE",
                        "value": "config.settings"
                    }},
                    {{
                        "name": "AWS_DEFAULT_REGION",
                        "value": "us-east-1"
                    }},
                    {{
                        "name": "DYNAMODB_BIO_TABLE",
                        "value": "{args['bio_table']}"
                    }},
                    {{
                        "name": "DYNAMODB_POSTS_TABLE",
                        "value": "{args['posts_table']}"
                    }},
                    {{
                        "name": "DYNAMODB_VIDEOS_TABLE",
                        "value": "{args['videos_table']}"
                    }},
                    {{
                        "name": "DYNAMODB_PROJECTS_TABLE",
                        "value": "{args['projects_table']}"
                    }},
                    {{
                        "name": "DJANGO_ADMIN_NAME",
                        "value": "{args['django_admin_name']}"
                    }},
                    {{
                        "name": "DJANGO_ADMIN_PASSWORD",
                        "value": "{args['django_admin_password']}"
                    }},
                    {{
                        "name": "DJANGO_ADMIN_EMAIL",
                        "value": "{args['django_admin_email']}"
                    }},
                    {{
                        "name": "STATIC_BUCKET_NAME",
                        "value": "{args['s3_bucket_name']}"
                    }}
                ]
            }}
        ]"""),
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # Application Load Balancer
    alb = aws.lb.LoadBalancer(
        f"{project_name}-alb",
        name=f"{project_name}-{environment}",
        load_balancer_type="application",
        subnets=networking["subnet_ids"],
        security_groups=[networking["alb_security_group"].id],
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # Target Group
    target_group = aws.lb.TargetGroup(
        f"{project_name}-tg",
        name=f"{project_name}-{environment}",
        port=8000,
        protocol="HTTP",
        vpc_id=networking["vpc_id"],
        target_type="ip",
        health_check=aws.lb.TargetGroupHealthCheckArgs(
            enabled=True,
            healthy_threshold=2,
            interval=30,
            matcher="200",
            path="/admin/",  # Django admin as health check
            port="traffic-port",
            protocol="HTTP",
            timeout=5,
            unhealthy_threshold=2
        ),
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # ACM SSL Certificate for HTTPS
    ssl_cert = aws.acm.Certificate(
        f"{project_name}-ssl-cert",
        domain_name="api.byoui.com",
        subject_alternative_names=["*.byoui.com"],
        validation_method="DNS",
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # Create DNS validation records in Route 53
    def create_validation_records(domain_validation_options):
        validation_records = []
        for i, dvo in enumerate(domain_validation_options):
            validation_record = aws.route53.Record(
                f"{project_name}-ssl-validation-{i}",
                zone_id=hosted_zone.zone_id,
                name=dvo["resource_record_name"],
                type=dvo["resource_record_type"],
                records=[dvo["resource_record_value"]],
                ttl=300,
                opts=pulumi.ResourceOptions(parent=ssl_cert)
            )
            validation_records.append(validation_record)
        return validation_records
    
    validation_records = ssl_cert.domain_validation_options.apply(create_validation_records)
    
    # Wait for certificate validation to complete
    ssl_cert_validation = aws.acm.CertificateValidation(
        f"{project_name}-ssl-cert-validation",
        certificate_arn=ssl_cert.arn,
        validation_record_fqdns=validation_records.apply(lambda records: [record.fqdn for record in records]),
        opts=pulumi.ResourceOptions(parent=ssl_cert)
    )
    
    # Create A record to point api.byoui.com to the load balancer
    api_dns_record = aws.route53.Record(
        f"{project_name}-api-dns",
        zone_id=hosted_zone.zone_id,
        name=api_domain,
        type="A",
        aliases=[
            aws.route53.RecordAliasArgs(
                name=alb.dns_name,
                zone_id=alb.zone_id,
                evaluate_target_health=True
            )
        ],
        opts=pulumi.ResourceOptions(parent=alb)
    )
    
    # Update existing HTTP Listener to redirect to HTTPS
    http_listener = aws.lb.Listener(
        f"{project_name}-listener",  # Use same name as existing listener
        load_balancer_arn=alb.arn,
        port="80",
        protocol="HTTP",
        default_actions=[
            aws.lb.ListenerDefaultActionArgs(
                type="redirect",
                redirect=aws.lb.ListenerDefaultActionRedirectArgs(
                    port="443",
                    protocol="HTTPS",
                    status_code="HTTP_301"
                )
            )
        ],
        tags={
            "Environment": environment,
            "Project": project_name
        }
    )
    
    # HTTPS Listener (using validated certificate)
    https_listener = aws.lb.Listener(
        f"{project_name}-https-listener",
        load_balancer_arn=alb.arn,
        port="443",
        protocol="HTTPS",
        ssl_policy="ELBSecurityPolicy-TLS-1-2-2017-01",
        certificate_arn=ssl_cert_validation.certificate_arn,
        default_actions=[
            aws.lb.ListenerDefaultActionArgs(
                type="forward",
                target_group_arn=target_group.arn
            )
        ],
        tags={
            "Environment": environment,
            "Project": project_name
        },
        opts=pulumi.ResourceOptions(depends_on=[ssl_cert_validation])
    )
    
    # ECS Service
    service = aws.ecs.Service(
        f"{project_name}-service",
        name=f"{project_name}-{environment}",
        cluster=cluster.id,
        task_definition=task_definition.arn,
        desired_count=1,  # Single instance for personal portfolio
        launch_type="FARGATE",
        network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
            assign_public_ip=True,
            subnets=networking["subnet_ids"],
            security_groups=[networking["ecs_security_group"].id]
        ),
        load_balancers=[
            aws.ecs.ServiceLoadBalancerArgs(
                target_group_arn=target_group.arn,
                container_name=f"{project_name}-container",
                container_port=8000
            )
        ],
        tags={
            "Environment": environment,
            "Project": project_name
        },
        opts=pulumi.ResourceOptions(depends_on=[https_listener])
    )
    
    return {
        "cluster": cluster,
        "service": service,
        "alb": alb,
        "task_definition": task_definition,
        "ssl_cert": ssl_cert,
        "ssl_cert_validation": ssl_cert_validation,
        "https_listener": https_listener,
        "http_listener": http_listener
    }

# Main infrastructure setup
def main():
    # Get S3 bucket name from config
    s3_bucket_name = config.require("s3_bucket_name")
    
    # Get Route 53 hosted zone for the domain
    hosted_zone = aws.route53.get_zone(name="byoui.com")
    
    # Create resources
    dynamodb_tables = create_dynamodb_tables()
    networking = create_networking()
    roles = create_ecs_task_role(dynamodb_tables, s3_bucket_name)
    # =============================================================================
    # ECR Repository for Container Images
    # =============================================================================
    
    # ECR repository for storing Docker images
    ecr_repository = aws.ecr.Repository(
        f"{project_name}-ecr-repo",
        name=f"{project_name}-api",
        image_tag_mutability="MUTABLE",
        image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
            scan_on_push=True
        ),
        force_delete=True
    )
    
    # ECR lifecycle policy to manage old images
    aws.ecr.LifecyclePolicy(
        f"{project_name}-ecr-lifecycle",
        repository=ecr_repository.name,
        policy="""{
            "rules": [
                {
                    "rulePriority": 1,
                    "description": "Keep last 10 images",
                    "selection": {
                        "tagStatus": "any",
                        "countType": "imageCountMoreThan",
                        "countNumber": 10
                    },
                    "action": {
                        "type": "expire"
                    }
                }
            ]
        }"""
    )
    
    # Create ECS infrastructure with ECR repository
    ecs_infrastructure = create_ecs_infrastructure(roles, networking, dynamodb_tables, django_admin_name, django_admin_password, django_admin_email, hosted_zone, s3_bucket_name, ecr_repository)
    
    # =============================================================================
    # CI/CD Pipeline with CodePipeline
    # =============================================================================
    
    # S3 bucket for CodePipeline artifacts
    pipeline_bucket = aws.s3.Bucket(
        f"{project_name}-pipeline-artifacts",
        bucket=f"{project_name}-pipeline-artifacts-{pulumi.get_stack()}",
        force_destroy=True
    )
    
    # Block public access to pipeline bucket
    aws.s3.BucketPublicAccessBlock(
        f"{project_name}-pipeline-bucket-pab",
        bucket=pipeline_bucket.id,
        block_public_acls=True,
        block_public_policy=True,
        ignore_public_acls=True,
        restrict_public_buckets=True
    )
    
    # CodePipeline service role
    codepipeline_role = aws.iam.Role(
        f"{project_name}-codepipeline-role",
        assume_role_policy="""{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "codepipeline.amazonaws.com"
                    }
                }
            ]
        }"""
    )
    
    # CodePipeline policy
    codepipeline_policy = aws.iam.RolePolicy(
        f"{project_name}-codepipeline-policy",
        role=codepipeline_role.id,
        policy=pulumi.Output.all(
            pipeline_bucket_arn=pipeline_bucket.arn,
            ecr_repo_arn=ecr_repository.arn
        ).apply(lambda args: json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:GetBucketVersioning",
                        "s3:PutObjectAcl",
                        "s3:PutObject"
                    ],
                    "Resource": [
                        args['pipeline_bucket_arn'],
                        f"{args['pipeline_bucket_arn']}/*"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "codestar-connections:UseConnection"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "codebuild:BatchGetBuilds",
                        "codebuild:StartBuild"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "ecs:UpdateService",
                        "ecs:DescribeServices",
                        "ecs:DescribeTaskDefinition",
                        "ecs:RegisterTaskDefinition"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "iam:PassRole"
                    ],
                    "Resource": "*"
                }
            ]
        }))
    )
    
    # CodeBuild service role
    codebuild_role = aws.iam.Role(
        f"{project_name}-codebuild-role",
        assume_role_policy="""{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "codebuild.amazonaws.com"
                    }
                }
            ]
        }"""
    )
    
    # CodeBuild policy
    codebuild_policy = aws.iam.RolePolicy(
        f"{project_name}-codebuild-policy",
        role=codebuild_role.id,
        policy=pulumi.Output.all(
            pipeline_bucket_arn=pipeline_bucket.arn,
            ecr_repo_arn=ecr_repository.arn,
            s3_bucket_arn=f"arn:aws:s3:::{s3_bucket_name}",
            bio_table_arn=dynamodb_tables["bio"].arn,
            posts_table_arn=dynamodb_tables["posts"].arn,
            videos_table_arn=dynamodb_tables["videos"].arn,
            projects_table_arn=dynamodb_tables["projects"].arn
        ).apply(lambda args: json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "arn:aws:logs:*:*:*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:PutObject"
                    ],
                    "Resource": [
                        args['pipeline_bucket_arn'],
                        f"{args['pipeline_bucket_arn']}/*",
                        args['s3_bucket_arn'],
                        f"{args['s3_bucket_arn']}/*"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:BatchGetImage",
                        "ecr:GetAuthorizationToken",
                        "ecr:PutImage",
                        "ecr:InitiateLayerUpload",
                        "ecr:UploadLayerPart",
                        "ecr:CompleteLayerUpload"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                        "dynamodb:DeleteItem",
                        "dynamodb:Query",
                        "dynamodb:Scan",
                        "dynamodb:BatchGetItem",
                        "dynamodb:BatchWriteItem"
                    ],
                    "Resource": [
                        args['bio_table_arn'],
                        args['posts_table_arn'],
                        args['videos_table_arn'],
                        args['projects_table_arn']
                    ]
                }
            ]
        }))
    )
    
    # CodeBuild project
    codebuild_project = aws.codebuild.Project(
        f"{project_name}-build",
        name=f"{project_name}-build",
        service_role=codebuild_role.arn,
        artifacts=aws.codebuild.ProjectArtifactsArgs(
            type="CODEPIPELINE"
        ),
        environment=aws.codebuild.ProjectEnvironmentArgs(
            compute_type="BUILD_GENERAL1_MEDIUM",
            image="aws/codebuild/amazonlinux2-x86_64-standard:5.0",
            type="LINUX_CONTAINER",
            privileged_mode=True,  # Required for Docker builds
            environment_variables=[
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="AWS_DEFAULT_REGION",
                    value="us-east-1"
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="AWS_ACCOUNT_ID",
                    value=aws.get_caller_identity().account_id
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="IMAGE_REPO_NAME",
                    value=ecr_repository.name
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="IMAGE_TAG",
                    value="latest"
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="STATIC_BUCKET_NAME",
                    value=s3_bucket_name
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="DJANGO_ADMIN_USERNAME",
                    value=django_admin_name
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="DJANGO_ADMIN_EMAIL",
                    value=django_admin_email
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="DJANGO_ADMIN_PASSWORD",
                    value=django_admin_password
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="BIO_TABLE_NAME",
                    value=dynamodb_tables["bio"].name
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="POSTS_TABLE_NAME",
                    value=dynamodb_tables["posts"].name
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="VIDEOS_TABLE_NAME",
                    value=dynamodb_tables["videos"].name
                ),
                aws.codebuild.ProjectEnvironmentEnvironmentVariableArgs(
                    name="PROJECTS_TABLE_NAME",
                    value=dynamodb_tables["projects"].name
                )
            ]
        ),
        source=aws.codebuild.ProjectSourceArgs(
            type="CODEPIPELINE",
            buildspec="apps/api/buildspec.yml"
        )
    )
    
    # GitHub connection (this needs to be manually authorized in AWS Console)
    github_connection = aws.codestarconnections.Connection(
        f"{project_name}-gh-conn",
        name=f"{project_name}-gh-conn",
        provider_type="GitHub"
    )
    
    # CodePipeline
    pipeline = aws.codepipeline.Pipeline(
        f"{project_name}-pipeline",
        name=f"{project_name}-pipeline",
        role_arn=codepipeline_role.arn,
        artifact_stores=[
            aws.codepipeline.PipelineArtifactStoreArgs(
                location=pipeline_bucket.bucket,
                type="S3"
            )
        ],
        stages=[
            # Source stage
            aws.codepipeline.PipelineStageArgs(
                name="Source",
                actions=[
                    aws.codepipeline.PipelineStageActionArgs(
                        name="Source",
                        category="Source",
                        owner="AWS",
                        provider="CodeStarSourceConnection",
                        version="1",
                        output_artifacts=["source_output"],
                        configuration={
                            "ConnectionArn": github_connection.arn,
                            "FullRepositoryId": "cgRGM/cgstewart-django",
                            "BranchName": "main"
                        }
                    )
                ]
            ),
            # Build stage
            aws.codepipeline.PipelineStageArgs(
                name="Build",
                actions=[
                    aws.codepipeline.PipelineStageActionArgs(
                        name="Build",
                        category="Build",
                        owner="AWS",
                        provider="CodeBuild",
                        version="1",
                        input_artifacts=["source_output"],
                        output_artifacts=["build_output"],
                        configuration={
                            "ProjectName": codebuild_project.name
                        }
                    )
                ]
            ),
            # Deploy stage
            aws.codepipeline.PipelineStageArgs(
                name="Deploy",
                actions=[
                    aws.codepipeline.PipelineStageActionArgs(
                        name="Deploy",
                        category="Deploy",
                        owner="AWS",
                        provider="ECS",
                        version="1",
                        input_artifacts=["build_output"],
                        configuration={
                            "ClusterName": ecs_infrastructure["cluster"].name,
                            "ServiceName": ecs_infrastructure["service"].name,
                            "FileName": "imagedefinitions.json"
                        }
                    )
                ]
            )
        ]
    )
    
    # Export important values
    export("dynamodb_tables", {
        "bio": dynamodb_tables["bio"].name,
        "posts": dynamodb_tables["posts"].name,
        "videos": dynamodb_tables["videos"].name,
        "projects": dynamodb_tables["projects"].name
    })
    # Get domain configuration
    domain_name = config.require("domain_name")
    api_domain = f"api.{domain_name}"
    
    pulumi.export("api_domain", api_domain)
    pulumi.export("ssl_certificate_arn", ecs_infrastructure["ssl_cert_validation"].certificate_arn)
    pulumi.export("https_endpoint", pulumi.Output.concat("https://", api_domain))
    pulumi.export("route53_zone_id", hosted_zone.zone_id)
    
    # CI/CD Pipeline exports
    pulumi.export("pipeline_name", pipeline.name)
    pulumi.export("github_connection_arn", github_connection.arn)
    pulumi.export("codebuild_project_name", codebuild_project.name)
    pulumi.export("pipeline_bucket", pipeline_bucket.bucket)

if __name__ == "__main__":
    main()
