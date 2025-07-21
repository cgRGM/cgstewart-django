from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Bio(models.Model):
    """Single bio instance for the author"""
    image = models.ImageField(upload_to='bio/', blank=True, null=True)
    about = models.TextField()
    
    # Social Media Links
    x_url = models.URLField(blank=True, null=True, help_text='X.com (Twitter) profile URL')
    linkedin_url = models.URLField(blank=True, null=True, help_text='LinkedIn profile URL')
    github_url = models.URLField(blank=True, null=True, help_text='GitHub profile URL')
    youtube_url = models.URLField(blank=True, null=True, help_text='YouTube channel URL')
    twitch_url = models.URLField(blank=True, null=True, help_text='Twitch channel URL')
    
    resume = models.FileField(upload_to='bio/resume/', blank=True, null=True, help_text='Upload your resume (PDF recommended)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Bio'
        verbose_name_plural = 'Bio'
    
    def __str__(self):
        return 'Author Bio'
    
    def save(self, *args, **kwargs):
        # Ensure only one bio instance exists
        if not self.pk and Bio.objects.exists():
            raise ValueError('Only one Bio instance is allowed')
        return super().save(*args, **kwargs)


class Post(models.Model):
    """Blog posts"""
    TAG_CHOICES = [
        ('general', 'General'),
        ('tech', 'Tech'),
        ('book_reviews', 'Book Reviews'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    excerpt = models.TextField(max_length=300, help_text='Short description of the post')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_published = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tags = models.CharField(max_length=20, choices=TAG_CHOICES, default='general')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_published']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})


class Video(models.Model):
    """Video content"""
    title = models.CharField(max_length=200)
    video_url = models.URLField(help_text='YouTube, Vimeo, or other video platform URL')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Project(models.Model):
    """Portfolio projects"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    stack = models.CharField(max_length=300, help_text='Technologies used (comma-separated)')
    website_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(blank=True, null=True, help_text='Markdown content for project details')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'slug': self.slug})
