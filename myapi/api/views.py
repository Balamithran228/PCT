from rest_framework import viewsets, status, generics
from .models import (
    Client, 
    Project, 
    Employee, 
    Technology, 
    ProjectEmployee, 
    ProjectTechnology, 
    Certification, 
    EmployeeCertificate, 
    EmployeeSkill,
    Team 
    )
from .serializers import (
    ClientSerializer,
    ProjectSerializer, 
    EmployeeSerializer, 
    TechnologySerializer, 
    ProjectEmployeeSerializer, 
    ProjectTechnologySerializer, 
    # ProjectCreationSerializer, 
    ProjectDetailSerializer, 
    CertificationSerializer, 
    EmployeeCertificateSerializer, 
    TeamSerializer,
    EmployeeSkillSerializer
    )
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# For Employee Register
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
# For Employee Login 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# For Employee Logout
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
# For Authentication and permission decorator
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView



class RegisterEmployee(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        employee_name = request.data.get("employee_name")
        designation = request.data.get("designation")
        employee_id = request.data.get("employee_id")

        if not email or not password or not employee_name or not designation or not employee_id:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email, password=password, employee_name=employee_name, designation=designation,employee_id=employee_id
        )

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class LoginEmployee(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutEmployee(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated, IsAdminOrReadOnly])
# def create_project(request):
#     serializer = ProjectCreationSerializer(data=request.data)
#     if serializer.is_valid():
#         project = serializer.save()
#         return Response({"message": "Project created successfully!", "project_id": project.project_id}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
def get_projects_by_client(request, client_id):
    # Fetch projects related to the client
    projects = Project.objects.filter(client_id=client_id)

    if not projects.exists():
        return Response({"message": "No projects found for this client."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
def get_project_details(request, client_id, project_id):
    project = get_object_or_404(Project, client_id=client_id, project_id=project_id)
    serializer = ProjectDetailSerializer(project)
    return Response(serializer.data)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

# Partial update implemented to skills and certificates also
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def partial_update(self, request, *args, **kwargs):
        employee = self.get_object()

        # Fields allowed to update (excluding email & password)
        allowed_fields = ["employee_name", "designation", "employee_id"]

        # Update only allowed fields
        for field in allowed_fields:
            if field in request.data:
                setattr(employee, field, request.data[field])

        # Update Primary Skills (Add only if not existing)
        primary_skills = request.data.get("primary_skills", [])
        for skill_id in primary_skills:
            skill, created = Skill.objects.get_or_create(id=skill_id)
            if not employee.skills.filter(id=skill_id, is_primary=True).exists():
                employee.skills.add(skill)

        # Update Secondary Skills (Add only if not existing)
        secondary_skills = request.data.get("secondary_skills", [])
        for skill_id in secondary_skills:
            skill, created = Skill.objects.get_or_create(id=skill_id)
            if not employee.skills.filter(id=skill_id, is_primary=False).exists():
                employee.skills.add(skill)

        # Save updates
        employee.save()
        serializer = self.get_serializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ProjectEmployeeViewSet(viewsets.ModelViewSet):
    queryset = ProjectEmployee.objects.all()
    serializer_class = ProjectEmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ProjectTechnologyViewSet(viewsets.ModelViewSet):
    queryset = ProjectTechnology.objects.all()
    serializer_class = ProjectTechnologySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

class EmployeeCertificateViewSet(viewsets.ModelViewSet):
    queryset = EmployeeCertificate.objects.all()
    serializer_class = EmployeeCertificateSerializer
    permission_classes = [IsAuthenticated]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    # Create & List Employee Skills
class EmployeeSkillListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeSkill.objects.all()
    serializer_class = EmployeeSkillSerializer

# Retrieve, Update & Delete Employee Skills
class EmployeeSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeSkill.objects.all()
    serializer_class = EmployeeSkillSerializer