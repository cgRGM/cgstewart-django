"""
PynamoDB models for CG Stewart's portfolio
Converting Django models to DynamoDB using PynamoDB
"""

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, 
    UTCDateTimeAttribute, 
    BooleanAttribute,
    ListAttribute,
    MapAttribute,
    NumberAttribute
)
from datetime import datetime
import uuid
import os
from django.utils.text import slugify
from decouple import config


class Bio(Model):
    """Single bio instance for the author"""
    
    class Meta:
        table_name = config('DYNAMODB_BIO_TABLE', default='cgstewart-bio-production')
        region = config('AWS_REGION', default='us-east-1')
        
    # Use a fixed ID since there's only one bio
    id = UnicodeAttribute(hash_key=True, default='author_bio')
    
    # Bio content
    about = UnicodeAttribute()
    image_url = UnicodeAttribute(null=True)
    
    # Social Media Links
    x_url = UnicodeAttribute(null=True)
    linkedin_url = UnicodeAttribute(null=True)
    github_url = UnicodeAttribute(null=True)
    youtube_url = UnicodeAttribute(null=True)
    twitch_url = UnicodeAttribute(null=True)
    
    # Resume
    resume_url = UnicodeAttribute(null=True)
    
    # Timestamps
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)
    
    def save(self, **kwargs):
        self.updated_at = datetime.now()
        return super().save(**kwargs)


class Post(Model):
    """Blog posts"""
    
    class Meta:
        table_name = config('DYNAMODB_POSTS_TABLE', default='cgstewart-posts-production')
        region = config('AWS_REGION', default='us-east-1')
        
    # Primary key
    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    
    # Post content
    title = UnicodeAttribute()
    slug = UnicodeAttribute()
    image_url = UnicodeAttribute(null=True)
    excerpt = UnicodeAttribute()
    content = UnicodeAttribute()
    
    # Author (simplified - just store username/id)
    author = UnicodeAttribute()
    
    # Tags as a list
    tags = ListAttribute(of=UnicodeAttribute, default=list)
    
    # Status
    is_published = BooleanAttribute(default=True)
    
    # Timestamps
    date_published = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)
    
    def save(self, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        self.updated_at = datetime.now()
        return super().save(**kwargs)


class Video(Model):
    """Video content"""
    
    class Meta:
        table_name = config('DYNAMODB_VIDEOS_TABLE', default='cgstewart-videos-production')
        region = config('AWS_REGION', default='us-east-1')
        
    # Primary key
    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    
    # Video content
    title = UnicodeAttribute()
    slug = UnicodeAttribute()
    video_url = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    
    # Status
    is_published = BooleanAttribute(default=True)
    
    # Timestamps
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)
    
    def save(self, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        self.updated_at = datetime.now()
        return super().save(**kwargs)


class Project(Model):
    """Portfolio projects"""
    
    class Meta:
        table_name = config('DYNAMODB_PROJECTS_TABLE', default='cgstewart-projects-production')
        region = config('AWS_REGION', default='us-east-1')
        
    # Primary key
    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    
    # Project content
    title = UnicodeAttribute()
    slug = UnicodeAttribute()
    description = UnicodeAttribute()
    content = UnicodeAttribute(null=True)
    
    # Stack as a list of technologies
    stack = ListAttribute(of=UnicodeAttribute, default=list)
    
    # URLs
    website_url = UnicodeAttribute(null=True)
    github_url = UnicodeAttribute(null=True)
    image_url = UnicodeAttribute(null=True)
    
    # Status
    is_published = BooleanAttribute(default=True)
    
    # Timestamps
    created_at = UTCDateTimeAttribute(default=datetime.now)
    updated_at = UTCDateTimeAttribute(default=datetime.now)
    
    def save(self, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        self.updated_at = datetime.now()
        return super().save(**kwargs)


# Utility functions for table management
def create_all_tables(wait=True):
    """Create all DynamoDB tables"""
    models = [Bio, Post, Video, Project]
    
    for model in models:
        if not model.exists():
            print(f"Creating table: {model.Meta.table_name}")
            model.create_table(read_capacity_units=1, write_capacity_units=1, wait=wait)
        else:
            print(f"Table already exists: {model.Meta.table_name}")


def delete_all_tables():
    """Delete all DynamoDB tables (use with caution!)"""
    models = [Bio, Post, Video, Project]
    
    for model in models:
        if model.exists():
            print(f"Deleting table: {model.Meta.table_name}")
            model.delete_table()
        else:
            print(f"Table doesn't exist: {model.Meta.table_name}")
