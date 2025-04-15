# portfolio_app/models.py
from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Profile model
@register_snippet
class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    profile_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    about_text = RichTextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    resume = models.FileField(upload_to='documents/', blank=True, null=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('title'),
            ImageChooserPanel('profile_image'),
        ], heading="Basic Information"),
        FieldPanel('about_text'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone'),
            FieldPanel('location'),
            FieldPanel('resume'),
        ], heading="Contact Information"),
        MultiFieldPanel([
            FieldPanel('github'),
            FieldPanel('linkedin'),
            FieldPanel('twitter'),
        ], heading="Social Links"),
    ]
    
    def __str__(self):
        return self.name

# Education model
@register_snippet
class Education(Orderable):
    institution = models.CharField(max_length=100)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = RichTextField(blank=True)
    
    panels = [
        FieldPanel('institution'),
        ImageChooserPanel('logo'),
        FieldPanel('degree'),
        FieldPanel('field_of_study'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('is_current'),
        FieldPanel('description'),
    ]
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"

# Skill categories
@register_snippet
class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    
    panels = [
        FieldPanel('name'),
    ]
    
    def __str__(self):
        return self.name

# Skills model
@register_snippet
class Skill(Orderable):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    proficiency = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        default=5
    )
    icon = models.CharField(max_length=100, blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('category'),
        FieldPanel('proficiency'),
        FieldPanel('icon'),
    ]
    
    def __str__(self):
        return self.name

# Project technology tag
class ProjectTechnologyTag(TaggedItemBase):
    content_object = ParentalKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='tagged_technologies'
    )

# Project model
@register_snippet
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    short_description = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    technologies = ClusterTaggableManager(
        through=ProjectTechnologyTag,
        blank=True
    )
    github_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    date_created = models.DateField()
    
    panels = [
        FieldPanel('title'),
        FieldPanel('short_description'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
        FieldPanel('technologies'),
        FieldPanel('github_link'),
        FieldPanel('demo_link'),
        FieldPanel('featured'),
        FieldPanel('date_created'),
    ]
    
    def __str__(self):
        return self.title

# Experience model
@register_snippet
class Experience(Orderable):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = RichTextField()
    
    panels = [
        FieldPanel('company'),
        FieldPanel('position'),
        ImageChooserPanel('logo'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('is_current'),
        FieldPanel('description'),
    ]
    
    def __str__(self):
        return f"{self.position} at {self.company}"

# Contact message model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.name}: {self.subject}"