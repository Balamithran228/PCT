from rest_framework import viewsets,status
from .models import Client, Project, Employee, Technology, ProjectEmployee, ProjectTechnology
from .serializers import ClientSerializer, ProjectSerializer, EmployeeSerializer, TechnologySerializer, ProjectEmployeeSerializer, ProjectTechnologySerializer, ProjectCreationSerializer, ProjectDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@api_view(["POST"])
def create_project(request):
    serializer = ProjectCreationSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save()
        return Response({"message": "Project created successfully!", "project_id": project.project_id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_projects_by_client(request, client_id):
    # Fetch projects related to the client
    projects = Project.objects.filter(client_id=client_id)

    if not projects.exists():
        return Response({"message": "No projects found for this client."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_project_details(request, client_id, project_id):
    project = get_object_or_404(Project, client_id=client_id, project_id=project_id)
    serializer = ProjectDetailSerializer(project)
    return Response(serializer.data)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

class ProjectEmployeeViewSet(viewsets.ModelViewSet):
    queryset = ProjectEmployee.objects.all()
    serializer_class = ProjectEmployeeSerializer

class ProjectTechnologyViewSet(viewsets.ModelViewSet):
    queryset = ProjectTechnology.objects.all()
    serializer_class = ProjectTechnologySerializer

