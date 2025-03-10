from rest_framework import serializers
from .models import (
    Client, 
    Project, 
    Employee, 
    Technology, 
    ProjectEmployee, 
    ProjectTechnology, 
    Team
    )
from rest_framework import serializers
from .models import (
    Project,
    ProjectEmployee, 
    ProjectTechnology, 
    Employee, 
    Client, 
    Technology, 
    Certification, 
    EmployeeCertificate, 
    EmployeeSkill,
    Team
    )
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

Employee = get_user_model()

class RegisterEmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ["email", "password", "employee_name", "designation","employee_id"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # Hash password
        return Employee.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": EmployeeSerializer(user).data,
        }

# create project and assign team leader with this ID (not use this now)

# class ProjectCreationSerializer(serializers.ModelSerializer):
#     client_id = serializers.IntegerField(write_only=True)
#     team_lead_id = serializers.CharField(write_only=True)  # Assign team lead via ProjectEmployee
#     employee_ids = serializers.ListField(child=serializers.CharField(), write_only=True)
#     technologies = serializers.ListField(child=serializers.IntegerField(), write_only=True)

#     class Meta:
#         model = Project
#         fields = ["name", "description", "client_id", "team_lead_id", "employee_ids", "technologies"]

#     def create(self, validated_data):
#         client_id = validated_data.pop("client_id")
#         team_lead_id = validated_data.pop("team_lead_id")
#         employee_ids = validated_data.pop("employee_ids")
#         technology_ids = validated_data.pop("technologies")

#         # Fetch Client
#         try:
#             client = Client.objects.get(pk=client_id)
#         except Client.DoesNotExist:
#             raise serializers.ValidationError({"client_id": "Invalid client ID."})

#         # Fetch Team Lead
#         try:
#             team_lead = Employee.objects.get(employee_id=team_lead_id)
#         except Employee.DoesNotExist:
#             raise serializers.ValidationError({"team_lead_id": "Invalid team lead ID."})

#         # Create Project
#         project = Project.objects.create(client=client, **validated_data)

#         # Assign Team Leader
#         ProjectEmployee.objects.create(project=project, employee=team_lead, role_in_project="Team Leader")

#         # Assign Employees
#         for emp_id in employee_ids:
#             try:
#                 employee = Employee.objects.get(employee_id=emp_id)
#                 role = "Employee"
#                 if emp_id == team_lead_id:  # If team lead is in employee list, ensure correct role
#                     role = "Team Leader"
#                 ProjectEmployee.objects.create(project=project, employee=employee, role_in_project=role)
#             except Employee.DoesNotExist:
#                 raise serializers.ValidationError({"employee_ids": f"Employee with ID {emp_id} does not exist."})

#         # Assign Technologies
#         for tech_id in technology_ids:
#             try:
#                 technology = Technology.objects.get(id=tech_id)
#                 ProjectTechnology.objects.create(project=project, technology=technology)
#             except Technology.DoesNotExist:
#                 raise serializers.ValidationError({"technologies": f"Technology with ID {tech_id} does not exist."})

#         return project



class ProjectDetailSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(source="client.client_id", read_only=True)
    client_name = serializers.CharField(source="client.client_name", read_only=True)
    project_id = serializers.IntegerField(read_only=True)
    employee_count = serializers.SerializerMethodField()
    tech_stack = serializers.SerializerMethodField()
    employee_list = serializers.SerializerMethodField()

    managers = serializers.SerializerMethodField()
    team_leaders = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "client_id",
            "client_name",
            "project_id",
            "project_name",
            "description",
            "managers",
            "team_leaders",
            "start_date",
            "end_date",
            "project_progress",
            "employee_count",
            "tech_stack",
            "employee_list",
        ]


    def get_employee_count(self, obj):
        return ProjectEmployee.objects.filter(project=obj).count()

    def get_tech_stack(self, obj):
        technologies = ProjectTechnology.objects.filter(project=obj).select_related("technology")
        return [{"id": tech.technology.id, "name": tech.technology.name} for tech in technologies]
    
    def get_managers(self, obj):
        manager = Employee.objects.filter(
            project_assignments__project=obj, project_assignments__role_in_project="manager"
        )
        return EmployeeInProjectSerializer(manager, many=True, context={"project": obj}).data

    def get_team_leaders(self, obj):
        team_leaders = Employee.objects.filter(
            project_assignments__project=obj, project_assignments__role_in_project="team lead"
        )
        return EmployeeInProjectSerializer(team_leaders, many=True, context={"project": obj}).data


    def get_employee_list(self, obj):
        employees = Employee.objects.filter(project_assignments__project=obj).exclude(
            project_assignments__role_in_project__in=["manager", "team leader"]
        )
        return EmployeeInProjectSerializer(employees, many=True, context={"project": obj}).data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
    def get_employee_count(self, obj):
        return ProjectEmployee.objects.filter(project=obj).count()

class EmployeeCertificateSerializer(serializers.ModelSerializer):
    certification_name = serializers.ReadOnlyField(source="certification.name")
    issued_by = serializers.ReadOnlyField(source="certification.issued_by")
    issue_date = serializers.DateField(format="%Y-%m-%d")  # Formatting date for readability
    expiry_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)
    certificate_file_url = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeCertificate
        fields = ["certification_name", "issued_by", "issue_date", "expiry_date", "certificate_file_url"]

    def get_certificate_file_url(self, obj):
        request = self.context.get("request")
        if obj.certificate_file:
            return request.build_absolute_uri(obj.certificate_file.url) if request else obj.certificate_file.url
        return None
    
class EmployeeInProjectSerializer(serializers.ModelSerializer):
    role_in_project = serializers.SerializerMethodField()
    primary_skills = serializers.SerializerMethodField()
    secondary_skills = serializers.SerializerMethodField()
    certifications = EmployeeCertificateSerializer(source="employeecertificate_set", many=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_name', 'designation', 'email', "role_in_project", "primary_skills", "secondary_skills", "certifications"]

    def get_role_in_project(self, obj):
        project = self.context.get("project")  # Get project from context
        if not project:
            return None  # If no project context, return None

        project_employee = obj.project_assignments.filter(project=project).first()  # Use correct related name
        return project_employee.role_in_project if project_employee else None

    def get_primary_skills(self, obj):
        return [skill.technology.name for skill in obj.skills.filter(is_primary=True).select_related("technology")]

    def get_secondary_skills(self, obj):
        return [skill.technology.name for skill in obj.skills.filter(is_primary=False).select_related("technology")]
    
class EmployeeSerializer(serializers.ModelSerializer):
    primary_skills = serializers.SerializerMethodField()
    secondary_skills = serializers.SerializerMethodField()
    certifications = EmployeeCertificateSerializer(source="employeecertificate_set", many=True)
    assigned_projects = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_name', 'designation', 'team', 'email', 'password', "primary_skills", "secondary_skills", "certifications", "assigned_projects"]
        extra_kwargs = {'password': {'write_only': True}}

    def get_primary_skills(self, obj):
        return [skill.technology.name for skill in obj.skills.filter(is_primary=True).select_related("technology")]

    def get_secondary_skills(self, obj):
        return [skill.technology.name for skill in obj.skills.filter(is_primary=False).select_related("technology")]
    
    def get_assigned_projects(self, obj):
        """Fetch projects where the employee is assigned"""
        return [
            {
                "project_id": assignment.project.project_id,
                "project_name": assignment.project.project_name,
                "role_in_project": assignment.role_in_project,
                "assigned_date": assignment.assigned_date
            }
            for assignment in obj.project_assignments.select_related("project")
        ]
    
class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'

class ProjectEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEmployee
        fields = '__all__'

class ProjectTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTechnology
        fields = '__all__'

class EmployeeSkillSerializer(serializers.ModelSerializer):
    technology_name = serializers.ReadOnlyField(source="technology.name")
    employee_name = serializers.ReadOnlyField(source="employee.employee_name")

    class Meta:
        model = EmployeeSkill
        fields = ["id", "employee", "employee_name", "technology", "technology_name", "is_primary"]



class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class EmployeeCertificateSerializer(serializers.ModelSerializer):
    certification_name = serializers.CharField(source='certification.name', read_only=True)
    issued_by = serializers.CharField(source='certification.issued_by', read_only=True)

    class Meta:
        model = EmployeeCertificate
        fields = ['id', 'employee', 'certification', 'certification_name', 'issued_by', 'issue_date', 'expiry_date', 'certificate_file']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"