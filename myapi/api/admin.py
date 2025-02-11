from django.contrib import admin
from .models import Employee, Client, Project, Technology, ProjectEmployee, ProjectTechnology
 
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Technology)
admin.site.register(ProjectEmployee)
admin.site.register(ProjectTechnology)