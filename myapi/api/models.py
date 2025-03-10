from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Example: "Data and AI", "AI Lab", "Salesforce"

    def __str__(self):
        return self.name
    
# Custom Manager
class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Handles password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class Employee(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    employee_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")


    # Built-in fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Manager
    objects = EmployeeManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["employee_name", "designation","employee_id"]
    
    # Get Primary Skills
    def get_primary_skills(self):
        return self.skills.filter(is_primary=True)

    # Get Secondary Skills
    def get_secondary_skills(self):
        return self.skills.filter(is_primary=False)
    
    def __str__(self):
        return f"{self.employee_name} ({self.team.name if self.team else 'No Team'})"


# Clients Model
class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255, unique=True)
 
    def __str__(self):
        return self.client_name
 
# Projects Model
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project_progress = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
 
    def __str__(self):
        return self.project_name
 
# Technology Model
class Technology(models.Model):
    name = models.CharField(max_length=255, unique=True)
 
    def __str__(self):
        return self.name
 
# Project Employees Table
class ProjectEmployee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="project_assignments"
    )
    assigned_date = models.DateField(auto_now_add=True)
    role_in_project = models.CharField(max_length=255)  # Updated from is_team_lead
 
    class Meta:
        unique_together = ("project", "employee")  # Ensuring unique project-employee pair
 
    def __str__(self):
        return f"{self.employee.employee_name} - {self.role_in_project} in {self.project.project_name}"
 
 
# Project Technology Table 
class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
 
    class Meta:
        unique_together = ("project", "technology")  # Ensuring unique project-technology pair
 
    def __str__(self):
        return f"{self.project.project_name} uses {self.technology.name}"

class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="skills")
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)  # True = Primary, False = Secondary

    class Meta:
        unique_together = ("employee", "technology")  # Prevent duplicate skills

    def __str__(self):
        skill_type = "Primary" if self.is_primary else "Secondary"
        return f"{self.employee.employee_name} - {self.technology.name} ({skill_type})"
   
class Certification(models.Model):
    name = models.CharField(max_length=255)
    issued_by = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class EmployeeCertificate(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    certificate_file = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"{self.employee.employee_name} - {self.certification.name}"

