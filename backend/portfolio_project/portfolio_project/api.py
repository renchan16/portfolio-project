# portfolio_app/api.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Profile, Education, SkillCategory, Skill, Project, Experience, ContactMessage
from .serializers import (
    ProfileSerializer, EducationSerializer, SkillCategorySerializer,
    SkillSerializer, ProjectSerializer, ExperienceSerializer, ContactMessageSerializer
)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def list(self, request):
        # Return only the first profile (assuming there's only one)
        try:
            profile = self.get_queryset().first()
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except:
            return Response({})

class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all().order_by('-start_date')
    serializer_class = EducationSerializer

class SkillCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    
    def list(self, request):
        categories = SkillCategory.objects.all()
        result = {}
        
        for category in categories:
            skills = Skill.objects.filter(category=category)
            result[category.name] = SkillSerializer(skills, many=True).data
            
        return Response(result)

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by('-featured', '-date_created')
    serializer_class = ProjectSerializer

class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all().order_by('-start_date')
    serializer_class = ExperienceSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]