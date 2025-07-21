from django.contrib import admin
from .models import Bio, Post, Video, Project


@admin.register(Bio)
class BioAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    
    fieldsets = (
        ('Profile Information', {
            'fields': ('image', 'about', 'resume')
        }),
        ('Social Media Links', {
            'fields': ('x_url', 'linkedin_url', 'github_url', 'youtube_url', 'twitch_url'),
            'classes': ('collapse',),  # Makes this section collapsible
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one bio instance
        return not Bio.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of bio
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tags', 'is_published', 'date_published')
    list_filter = ('tags', 'is_published', 'date_published', 'author')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_published'
    ordering = ('-date_published',)
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'image')
        }),
        ('Metadata', {
            'fields': ('author', 'tags', 'is_published')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'video_url', 'description')
        }),
        ('Settings', {
            'fields': ('is_published',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'stack', 'website_url', 'github_url', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description', 'stack')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'description', 'content', 'image')
        }),
        ('Technical Details', {
            'fields': ('stack', 'website_url', 'github_url')
        }),
        ('Settings', {
            'fields': ('is_published',)
        }),
    )
