from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Bio, Post, Video, Project
from .serializers import (
    BioSerializer, PostSerializer, PostListSerializer,
    VideoSerializer, ProjectSerializer, ProjectListSerializer
)


# Bio Views
class BioDetailView(generics.RetrieveAPIView):
    """Get the author's bio"""
    serializer_class = BioSerializer
    
    def get_object(self):
        return Bio.objects.first()  # Get the single bio instance


# Post Views
class PostListView(generics.ListAPIView):
    """List all published posts"""
    serializer_class = PostListSerializer
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags=tag)
        return queryset


class PostDetailView(generics.RetrieveAPIView):
    """Get a specific post by slug"""
    serializer_class = PostSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True)


# Video Views
class VideoListView(generics.ListAPIView):
    """List all published videos"""
    serializer_class = VideoSerializer
    
    def get_queryset(self):
        return Video.objects.filter(is_published=True)


class VideoDetailView(generics.RetrieveAPIView):
    """Get a specific video by slug"""
    serializer_class = VideoSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Video.objects.filter(is_published=True)


# Project Views
class ProjectListView(generics.ListAPIView):
    """List all published projects"""
    serializer_class = ProjectListSerializer
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True)


class ProjectDetailView(generics.RetrieveAPIView):
    """Get a specific project by slug"""
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True)


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
