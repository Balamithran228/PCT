from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    employee_id = models.CharField(max_length=50, primary_key=True)
    employee_name = models.CharField(max_length=255)
    employee_role = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    # Built-in fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Manager
    objects = EmployeeManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["employee_name", "employee_role"]

    def __str__(self):
        return self.employee_name


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
    team_lead = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="leading_projects")
 
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
    is_team_lead = models.BooleanField(default=False) 
 
    class Meta:
        unique_together = ("project", "employee")  # Ensuring unique project-employee pair
 
    def __str__(self):
        return f"{self.employee.employee_name} in {self.project.project_name}"
 
 
# Project Technology Table 
class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
 
    class Meta:
        unique_together = ("project", "technology")  # Ensuring unique project-technology pair
 
    def __str__(self):
        return f"{self.project.project_name} uses {self.technology.name}"