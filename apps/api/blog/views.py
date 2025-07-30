from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404
from pynamodb.exceptions import DoesNotExist
from .pynamo_models import Bio, Post, Video, Project
from .serializers import (
    BioSerializer, PostSerializer, PostListSerializer,
    VideoSerializer, ProjectSerializer, ProjectListSerializer
)


# Bio Views
class BioDetailView(APIView):
    """Get the author's bio from DynamoDB"""
    
    def get(self, request):
        try:
            # Get the single bio instance using fixed ID
            bio = Bio.get('author_bio')
            serializer = BioSerializer(bio)
            return Response(serializer.data)
        except DoesNotExist:
            return Response(
                {'error': 'Bio not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


# Post Views
class PostListView(APIView):
    """List all published posts from DynamoDB"""
    
    def get(self, request):
        try:
            # Scan for all published posts
            posts = []
            for post in Post.scan(Post.is_published == True):
                posts.append(post)
            
            # Filter by tag if provided
            tag = request.query_params.get('tag', None)
            if tag:
                posts = [post for post in posts if tag in post.tags]
            
            # Sort by date_published (newest first)
            posts.sort(key=lambda x: x.date_published, reverse=True)
            
            serializer = PostListSerializer(posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error fetching posts: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostDetailView(APIView):
    """Get a specific post by slug from DynamoDB"""
    
    def get(self, request, slug):
        try:
            # Scan for post with matching slug and is_published=True
            for post in Post.scan((Post.slug == slug) & (Post.is_published == True)):
                serializer = PostSerializer(post)
                return Response(serializer.data)
            
            return Response(
                {'error': 'Post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error fetching post: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Video Views
class VideoListView(APIView):
    """List all published videos from DynamoDB"""
    
    def get(self, request):
        try:
            # Scan for all published videos
            videos = []
            for video in Video.scan(Video.is_published == True):
                videos.append(video)
            
            # Sort by created_at (newest first)
            videos.sort(key=lambda x: x.created_at, reverse=True)
            
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error fetching videos: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VideoDetailView(APIView):
    """Get a specific video by slug from DynamoDB"""
    
    def get(self, request, slug):
        try:
            # Scan for video with matching slug and is_published=True
            for video in Video.scan((Video.slug == slug) & (Video.is_published == True)):
                serializer = VideoSerializer(video)
                return Response(serializer.data)
            
            return Response(
                {'error': 'Video not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error fetching video: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Project Views
class ProjectListView(APIView):
    """List all published projects from DynamoDB"""
    
    def get(self, request):
        try:
            # Scan for all published projects
            projects = []
            for project in Project.scan(Project.is_published == True):
                projects.append(project)
            
            # Sort by created_at (newest first)
            projects.sort(key=lambda x: x.created_at, reverse=True)
            
            serializer = ProjectListSerializer(projects, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error fetching projects: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectDetailView(APIView):
    """Get a specific project by slug from DynamoDB"""
    
    def get(self, request, slug):
        try:
            # Scan for project with matching slug and is_published=True
            for project in Project.scan((Project.slug == slug) & (Project.is_published == True)):
                serializer = ProjectSerializer(project)
                return Response(serializer.data)
            
            return Response(
                {'error': 'Project not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error fetching project: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# API Overview
@api_view(['GET'])
def api_overview(request):
    """API endpoints overview"""
    api_urls = {
        'Bio': '/api/v1/bio/',
        'Posts': {
            'List': '/api/v1/posts/',
            'Detail': '/api/v1/posts/{slug}/',
            'Filter by tag': '/api/v1/posts/?tag={tag}'
        },
        'Videos': {
            'List': '/api/v1/videos/',
            'Detail': '/api/v1/videos/{slug}/'
        },
        'Projects': {
            'List': '/api/v1/projects/',
            'Detail': '/api/v1/projects/{slug}/'
        }
    }
    return Response(api_urls)
