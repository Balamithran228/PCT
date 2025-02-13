from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet, EmployeeViewSet, TechnologyViewSet, ProjectEmployeeViewSet, ProjectTechnologyViewSet, create_project, get_projects_by_client, get_project_details

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'project-employees', ProjectEmployeeViewSet)
router.register(r'project-technologies', ProjectTechnologyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("create_project/", create_project, name="create_project"),
    path("projects/client/<int:client_id>/", get_projects_by_client, name="get_projects_by_client"),
    path("client/<int:client_id>/<int:project_id>/", get_project_details, name="project-details"),
]
