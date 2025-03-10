from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet,
    ProjectViewSet, 
    EmployeeViewSet, 
    TechnologyViewSet, 
    ProjectEmployeeViewSet, 
    ProjectTechnologyViewSet, 
    # create_project, 
    get_projects_by_client, 
    get_project_details, 
    RegisterEmployee, 
    LoginEmployee, 
    LogoutEmployee, 
    CertificationViewSet, 
    EmployeeCertificateViewSet, 
    TeamViewSet
    )
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'project-employees', ProjectEmployeeViewSet)
router.register(r'project-technologies', ProjectTechnologyViewSet)
router.register(r'certifications', CertificationViewSet)  # /api/certifications/
router.register(r'employee-certificates', EmployeeCertificateViewSet)  # /api/employee-certificates/
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('register/', RegisterEmployee.as_view(), name='register'),
    path('login/', LoginEmployee.as_view(), name='login'),
    path('logout/', LogoutEmployee.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),
    # path("create_project/", create_project, name="create_project"),
    path("projects/client/<int:client_id>/", get_projects_by_client, name="get_projects_by_client"),
    path("client/<int:client_id>/<int:project_id>/", get_project_details, name="project-details"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
