#!/usr/bin/env python3
"""
S3 Upload Diagnostic Script
Run this after uploading files through Django admin to verify they're in S3
"""

import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Bio, Post, Project
import boto3
from django.conf import settings

def check_s3_files():
    """Check if uploaded files actually exist in S3"""
    print("🔍 Checking S3 uploads...")
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    def check_file_in_s3(file_field, model_name, field_name):
        if file_field and file_field.name:
            try:
                s3_client.head_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=file_field.name
                )
                print(f"✅ {model_name} {field_name}: {file_field.name} - EXISTS in S3")
                print(f"   URL: {file_field.url}")
                return True
            except Exception as e:
                print(f"❌ {model_name} {field_name}: {file_field.name} - NOT FOUND in S3")
                print(f"   Error: {e}")
                return False
        else:
            print(f"ℹ️  {model_name} {field_name}: No file uploaded")
            return None
    
    # Check Bio files
    print("\n📋 Bio Files:")
    try:
        bio = Bio.objects.first()
        if bio:
            check_file_in_s3(bio.image, "Bio", "image")
            check_file_in_s3(bio.resume, "Bio", "resume")
        else:
            print("ℹ️  No Bio instance found")
    except Exception as e:
        print(f"❌ Error checking Bio: {e}")
    
    # Check Post files
    print("\n📝 Post Files:")
    try:
        posts = Post.objects.all()[:5]  # Check first 5 posts
        if posts:
            for post in posts:
                check_file_in_s3(post.image, f"Post '{post.title}'", "image")
        else:
            print("ℹ️  No Posts found")
    except Exception as e:
        print(f"❌ Error checking Posts: {e}")
    
    # Check Project files
    print("\n🚀 Project Files:")
    try:
        projects = Project.objects.all()[:5]  # Check first 5 projects
        if projects:
            for project in projects:
                check_file_in_s3(project.image, f"Project '{project.title}'", "image")
        else:
            print("ℹ️  No Projects found")
    except Exception as e:
        print(f"❌ Error checking Projects: {e}")

def list_s3_bucket_contents():
    """List all files in the S3 bucket"""
    print("\n📁 S3 Bucket Contents:")
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            MaxKeys=50
        )
        
        if 'Contents' in response:
            print(f"Found {len(response['Contents'])} files in bucket:")
            for obj in response['Contents']:
                size_kb = obj['Size'] / 1024
                print(f"  📄 {obj['Key']} ({size_kb:.1f} KB) - {obj['LastModified']}")
        else:
            print("🗂️  Bucket is empty")
            
    except Exception as e:
        print(f"❌ Error listing bucket contents: {e}")

if __name__ == "__main__":
    print("🔧 S3 Upload Diagnostic Tool")
    print("=" * 50)
    
    check_s3_files()
    list_s3_bucket_contents()
    
    print("\n" + "=" * 50)
    print("💡 How to use:")
    print("1. Upload files through Django admin")
    print("2. Run this script to verify they're in S3")
    print("3. Check the URLs to make sure they're accessible")
