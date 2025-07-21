from django.urls import path
from . import views

urlpatterns = [
    # API Overview
    path('', views.api_overview, name='api-overview'),
    
    # Bio
    path('bio/', views.BioDetailView.as_view(), name='bio-detail'),
    
    # Posts
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    
    # Videos
    path('videos/', views.VideoListView.as_view(), name='video-list'),
    path('videos/<slug:slug>/', views.VideoDetailView.as_view(), name='video-detail'),
    
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),
]
