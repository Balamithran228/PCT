from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet, EmployeeViewSet, TechnologyViewSet, ProjectEmployeeViewSet, ProjectTechnologyViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'project-employees', ProjectEmployeeViewSet)
router.register(r'project-technologies', ProjectTechnologyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
