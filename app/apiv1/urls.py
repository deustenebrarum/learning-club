from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import (
    UserViewSet, CourseViewSet, CourseMaterialViewSet,
    HomeworkViewSet, HomeworkSubmissionViewSet, AttendanceRecordViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'materials', CourseMaterialViewSet)
router.register(r'homeworks', HomeworkViewSet)
router.register(r'submissions', HomeworkSubmissionViewSet)
router.register(r'attendance', AttendanceRecordViewSet)


urlpatterns = router.urls + [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
