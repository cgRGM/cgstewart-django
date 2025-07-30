#!/usr/bin/env python3
"""
DynamoDB management script for CG Stewart's portfolio
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our models and config
from blog.dynamo_config import configure_pynamodb
from blog.pynamo_models import Bio, Post, Video, Project, create_all_tables, delete_all_tables

def test_connection():
    """Test DynamoDB connection"""
    try:
        configure_pynamodb()
        print("✅ DynamoDB configuration loaded successfully")
        
        # Try to check if Bio table exists
        exists = Bio.exists()
        print(f"✅ Connection test successful. Bio table exists: {exists}")
        return True
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def create_tables():
    """Create all DynamoDB tables"""
    try:
        configure_pynamodb()
        print("Creating DynamoDB tables...")
        create_all_tables(wait=True)
        print("✅ All tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def delete_tables():
    """Delete all DynamoDB tables"""
    try:
        configure_pynamodb()
        print("⚠️  Deleting all DynamoDB tables...")
        delete_all_tables()
        print("✅ All tables deleted!")
        return True
    except Exception as e:
        print(f"❌ Failed to delete tables: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    try:
        configure_pynamodb()
        print("Creating sample data...")
        
        # Create Bio
        bio = Bio()
        bio.about = "I'm CG Stewart, a software developer passionate about creating innovative solutions."
        bio.x_url = "https://x.com/cgstewart"
        bio.linkedin_url = "https://linkedin.com/in/cgstewart"
        bio.github_url = "https://github.com/cgstewart"
        bio.save()
        print("✅ Bio created")
        
        # Create a sample post
        post = Post()
        post.title = "Welcome to My Blog"
        post.excerpt = "This is my first blog post using PynamoDB and DynamoDB!"
        post.content = "# Welcome\n\nThis is the full content of my first blog post."
        post.author = "cgstewart"
        post.tags = ["general", "tech"]
        post.save()
        print("✅ Sample post created")
        
        # Create a sample video
        video = Video()
        video.title = "Introduction to DynamoDB"
        video.video_url = "https://youtube.com/watch?v=example"
        video.description = "Learn the basics of DynamoDB in this tutorial."
        video.save()
        print("✅ Sample video created")
        
        # Create a sample project
        project = Project()
        project.title = "Portfolio Website"
        project.description = "A modern portfolio website built with Django and Next.js"
        project.content = "## Overview\n\nThis project showcases my work and skills."
        project.stack = ["Django", "Next.js", "DynamoDB", "AWS"]
        project.github_url = "https://github.com/cgstewart/portfolio"
        project.website_url = "https://cgstewart.dev"
        project.save()
        print("✅ Sample project created")
        
        print("✅ All sample data created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return False

def list_data():
    """List all data in tables"""
    try:
        configure_pynamodb()
        print("\n📊 Current data in tables:")
        
        # List Bio
        print("\n🔹 Bio:")
        try:
            bio = Bio.get('author_bio')
            print(f"  About: {bio.about[:50]}...")
            print(f"  Created: {bio.created_at}")
        except Bio.DoesNotExist:
            print("  No bio found")
        
        # List Posts
        print("\n🔹 Posts:")
        posts = list(Post.scan())
        if posts:
            for post in posts:
                print(f"  - {post.title} (Published: {post.date_published})")
        else:
            print("  No posts found")
        
        # List Videos
        print("\n🔹 Videos:")
        videos = list(Video.scan())
        if videos:
            for video in videos:
                print(f"  - {video.title} ({video.video_url})")
        else:
            print("  No videos found")
        
        # List Projects
        print("\n🔹 Projects:")
        projects = list(Project.scan())
        if projects:
            for project in projects:
                print(f"  - {project.title} (Stack: {', '.join(project.stack)})")
        else:
            print("  No projects found")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to list data: {e}")
        return False

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("""
🚀 DynamoDB Management Script for CG Stewart's Portfolio

Usage: python manage_dynamo.py <command>

Commands:
  test        - Test DynamoDB connection
  create      - Create all tables
  delete      - Delete all tables (⚠️  destructive!)
  sample      - Create sample data
  list        - List all data in tables
  setup       - Full setup (create tables + sample data)
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'test':
        test_connection()
    elif command == 'create':
        create_tables()
    elif command == 'delete':
        confirm = input("⚠️  Are you sure you want to delete all tables? (yes/no): ")
        if confirm.lower() == 'yes':
            delete_tables()
        else:
            print("Cancelled.")
    elif command == 'sample':
        create_sample_data()
    elif command == 'list':
        list_data()
    elif command == 'setup':
        print("🚀 Setting up DynamoDB for CG Stewart's Portfolio...")
        if create_tables():
            print("Waiting for tables to be ready...")
            import time
            time.sleep(5)  # Wait for tables to be ready
            create_sample_data()
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == '__main__':
    main()
