from rest_framework import serializers
from .models import Client, Project, Employee, Technology, ProjectEmployee, ProjectTechnology
from rest_framework import serializers
from .models import Project, ProjectEmployee, ProjectTechnology, Employee, Client, Technology

class ProjectCreationSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)  # Expect client_id instead of full client object
    team_lead_id = serializers.CharField(write_only=True)  # Expect team lead ID
    employee_ids = serializers.ListField(child=serializers.CharField(), write_only=True)  # Employee IDs list
    technologies = serializers.ListField(child=serializers.IntegerField(), write_only=True)  # Technology IDs list

    class Meta:
        model = Project
        fields = ["project_name", "client_id", "project_progress", "start_date", "end_date", "team_lead_id", "employee_ids", "technologies"]

    def create(self, validated_data):
        # Extract client_id, team_lead_id, employee_ids, and technologies
        client_id = validated_data.pop("client_id")
        team_lead_id = validated_data.pop("team_lead_id")
        employee_ids = validated_data.pop("employee_ids")
        technology_ids = validated_data.pop("technologies")

        # Fetch the client object
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            raise serializers.ValidationError({"client_id": "Invalid client ID."})

        # Fetch the team lead object
        try:
            team_lead = Employee.objects.get(employee_id=team_lead_id)
        except Employee.DoesNotExist:
            raise serializers.ValidationError({"team_lead_id": "Invalid team lead ID."})

        # Create the project
        project = Project.objects.create(client=client, team_lead=team_lead, **validated_data)
        # Ensure team lead is assigned first with `is_team_lead=True`
        ProjectEmployee.objects.create(project=project, employee=team_lead, is_team_lead=True)
        # Assign employees to the project
        for emp_id in employee_ids:
            try:
                employee = Employee.objects.get(employee_id=emp_id)
                is_team_lead = (employee.employee_id == team_lead_id)
                ProjectEmployee.objects.create(project=project, employee=employee, is_team_lead=is_team_lead)
            except Employee.DoesNotExist:
                raise serializers.ValidationError({"employee_ids": f"Employee with ID {emp_id} does not exist."})

        # Assign technologies to the project
        for tech_id in technology_ids:
            try:
                technology = Technology.objects.get(id=tech_id)
                ProjectTechnology.objects.create(project=project, technology=technology)
            except Technology.DoesNotExist:
                raise serializers.ValidationError({"technologies": f"Technology with ID {tech_id} does not exist."})

        return project


class ProjectDetailSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(source="client.client_id", read_only=True)
    client_name = serializers.CharField(source="client.client_name", read_only=True)
    project_id = serializers.IntegerField(read_only=True)
    team_lead_id = serializers.SerializerMethodField()
    team_lead_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    tech_stack = serializers.SerializerMethodField()
    employee_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "client_id",
            "client_name",
            "project_id",
            "project_name",
            "description",
            "team_lead_id",
            "team_lead_name",
            "start_date",
            "end_date",
            "project_progress",
            "employee_count",
            "tech_stack",
            "employee_list",
        ]

    def get_team_lead_id(self, obj):
        team_lead = ProjectEmployee.objects.filter(project=obj, is_team_lead=True).first()
        return team_lead.employee.employee_id if team_lead else None

    def get_team_lead_name(self, obj):
        team_lead = ProjectEmployee.objects.filter(project=obj, is_team_lead=True).first()
        return team_lead.employee.employee_name if team_lead else None

    def get_employee_count(self, obj):
        return ProjectEmployee.objects.filter(project=obj).count()

    def get_tech_stack(self, obj):
        technologies = ProjectTechnology.objects.filter(project=obj).select_related("technology")
        return [{"id": tech.technology.id, "name": tech.technology.name} for tech in technologies]

    def get_employee_list(self, obj):
        employees = ProjectEmployee.objects.filter(project=obj).select_related("employee")
        return [{"id": emp.employee.employee_id, "name": emp.employee.employee_name, "role": emp.employee.employee_role} for emp in employees]


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

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_name', 'employee_role', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

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
