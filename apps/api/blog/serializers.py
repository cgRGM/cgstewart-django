from rest_framework import serializers
from .models import Bio, Post, Video, Project


class BioSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Bio
        fields = [
            'id', 'image', 'image_url', 'about', 'x_url', 'linkedin_url', 'github_url', 
            'youtube_url', 'twitch_url', 'resume', 'resume_url', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        """Get public URL for image"""
        return obj.image.url if obj.image else None
    
    def get_resume_url(self, obj):
        """Get public URL for resume"""
        return obj.resume.url if obj.resume else None


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'image', 'image_url', 'excerpt', 'content', 'author', 'author_name',
            'date_published', 'slug', 'tags', 'is_published', 'created_at', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        """Get public URL for image"""
        return obj.image.url if obj.image else None


class PostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for post listings"""
    author = serializers.StringRelatedField(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'image', 'image_url', 'excerpt', 'author', 
            'date_published', 'slug', 'tags'
        ]
    
    def get_image_url(self, obj):
        """Get public URL for image"""
        return obj.image.url if obj.image else None


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'video_url', 'slug', 'description', 
            'is_published', 'created_at', 'updated_at'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    stack_list = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'stack', 'stack_list', 'website_url', 
            'github_url', 'slug', 'content', 'image', 'image_url', 'is_published', 
            'created_at', 'updated_at'
        ]
    
    def get_stack_list(self, obj):
        """Convert comma-separated stack string to list"""
        if obj.stack:
            return [tech.strip() for tech in obj.stack.split(',')]
        return []
    
    def get_image_url(self, obj):
        """Get public URL for image"""
        return obj.image.url if obj.image else None


class ProjectListSerializer(serializers.ModelSerializer):
    """Simplified serializer for project listings"""
    stack_list = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'stack_list', 'website_url', 
            'github_url', 'slug', 'image', 'image_url'
        ]
    
    def get_stack_list(self, obj):
        """Convert comma-separated stack string to list"""
        if obj.stack:
            return [tech.strip() for tech in obj.stack.split(',')]
        return []
    
    def get_image_url(self, obj):
        """Get public URL for image"""
        return obj.image.url if obj.image else None
