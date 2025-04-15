# portfolio_app/serializers.py
from rest_framework import serializers
from wagtail.images.models import Image
from .models import Profile, Education, SkillCategory, Skill, Project, Experience, ContactMessage

class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Image
        fields = ['id', 'title', 'url']
    
    def get_url(self, obj):
        return obj.file.url if obj and obj.file else None

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = ImageSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'title', 'profile_image', 'about_text',
            'email', 'phone', 'location', 'resume',
            'github', 'linkedin', 'twitter'
        ]

class EducationSerializer(serializers.ModelSerializer):
    logo = ImageSerializer(read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Education
        fields = [
            'id', 'institution', 'logo', 'degree', 'field_of_study',
            'start_date', 'end_date', 'is_current', 'description', 'duration'
        ]
    
    def get_duration(self, obj):
        if obj.is_current:
            return f"{obj.start_date.strftime('%b %Y')} - Present"
        elif obj.end_date:
            return f"{obj.start_date.strftime('%b %Y')} - {obj.end_date.strftime('%b %Y')}"
        else:
            return obj.start_date.strftime('%b %Y')

class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ['id', 'name']

class SkillSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'category_name', 'proficiency', 'icon']

class ProjectSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)
    technologies = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'short_description', 'image',
            'technologies', 'github_link', 'demo_link', 'featured', 'date_created'
        ]
    
    def get_technologies(self, obj):
        return [tag.name for tag in obj.technologies.all()]

class ExperienceSerializer(serializers.ModelSerializer):
    logo = ImageSerializer(read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = [
            'id', 'company', 'position', 'logo',
            'start_date', 'end_date', 'is_current', 'description', 'duration'
        ]
    
    def get_duration(self, obj):
        if obj.is_current:
            return f"{obj.start_date.strftime('%b %Y')} - Present"
        elif obj.end_date:
            return f"{obj.start_date.strftime('%b %Y')} - {obj.end_date.strftime('%b %Y')}"
        else:
            return obj.start_date.strftime('%b %Y')

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message']