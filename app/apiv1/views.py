# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        user = self.request.user
        if isinstance(user, User) and user.is_admin:
            return AdminUserSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User) and user.is_admin:
            return User.objects.all()
        if isinstance(user, User) and user.is_teacher:
            return User.objects.filter(groups__name=UserRole.STUDENT)
        return User.objects.none()

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User) and user.is_admin:
            return Course.objects.all()
        if isinstance(user, User) and user.is_teacher:
            return Course.objects.filter(instructor=user)
        if isinstance(user, User) and user.is_student:
            return Course.objects.filter(studentsgroup__user=user)
        return Course.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if isinstance(user, User) and user.is_teacher:
            serializer.save(instructor=user)
        else:
            super().perform_create(serializer)

class CourseMaterialViewSet(viewsets.ModelViewSet):
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_serializer_class(self):
        user = self.request.user
        if isinstance(user, User) and user.is_teacher:
            return TeacherCourseMaterialSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User) and user.is_admin:
            return CourseMaterial.objects.all()
        if isinstance(user, User) and user.is_teacher:
            return CourseMaterial.objects.filter(uploaded_by=user)
        if isinstance(user, User) and user.is_student:
            return CourseMaterial.objects.filter(course__studentsgroup__user=user)
        return CourseMaterial.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if isinstance(user, User):
            serializer.save(uploaded_by=user)

class HomeworkViewSet(viewsets.ModelViewSet):
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User) and user.is_admin:
            return Homework.objects.all()
        if isinstance(user, User) and user.is_teacher:
            return Homework.objects.filter(assigned_by=user)
        if isinstance(user, User) and user.is_student:
            return Homework.objects.filter(course__studentsgroup__user=user)
        return Homework.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if isinstance(user, User):
            serializer.save(assigned_by=user)

class HomeworkSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if isinstance(user, User) and user.is_student:
            return StudentHomeworkSubmissionSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User) and user.is_admin:
            return HomeworkSubmission.objects.all()
        if isinstance(user, User) and user.is_teacher:
            return HomeworkSubmission.objects.filter(
                homework__course__instructor=user
            )
        if isinstance(user, User) and user.is_student:
            return HomeworkSubmission.objects.filter(student=user)
        return HomeworkSubmission.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def set_grade(self, request, pk=None):
        submission = self.get_object()
        grade = request.data.get('grade')
        
        if grade is None or not (0 <= int(grade) <= 100):
            return Response(
                {'error': 'Invalid grade value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submission.grade = grade
        submission.save()
        return Response({'status': 'grade set'})

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User) and user.is_admin:
            return AttendanceRecord.objects.all()
        if isinstance(user, User) and user.is_teacher:
            return AttendanceRecord.objects.filter(
                student__group__course__instructor=user
            )
        if isinstance(user, User) and user.is_student:
            return AttendanceRecord.objects.filter(student=user)
        return AttendanceRecord.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if isinstance(user, User) and user.is_teacher:
            serializer.save()
        else:
            raise permissions.exceptions.PermissionDenied()

