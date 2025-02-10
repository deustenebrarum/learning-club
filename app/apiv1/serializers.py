from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import (
    User, UserRole, Course, CourseMaterial,
    Homework, HomeworkSubmission, AttendanceRecord,
)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    group = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'role', 'group', 'is_active'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_role(self, obj):
        if obj.is_admin:
            return UserRole.ADMIN
        if obj.is_teacher:
            return UserRole.TEACHER
        return UserRole.STUDENT

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(
        source='instructor.get_full_name', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'instructor', 'instructor_name']
        extra_kwargs = {
            'instructor': {'write_only': True}
        }

    def validate_instructor(self, value):
        if not value.is_teacher:
            raise serializers.ValidationError("Instructor must be a teacher")
        return value


class CourseMaterialSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = CourseMaterial
        fields = '__all__'
        read_only_fields = ['uploaded_by']

    def validate(self, data):
        user = self.context['request'].user
        if not user.is_teacher:
            raise serializers.ValidationError(
                "Only teachers can upload materials")
        return data


class HomeworkSerializer(serializers.ModelSerializer):
    assigned_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ['assigned_by']

    def validate_assigned_by(self, value):
        if not value.is_teacher:
            raise serializers.ValidationError(
                "Only teachers can assign homework")
        return value


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = HomeworkSubmission
        fields = '__all__'
        read_only_fields = ['submitted_at', 'grade']

    def validate_student(self, value):
        if not value.is_student:
            raise serializers.ValidationError(
                "Only students can submit homework")
        return value


class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)

        if request and request.user.is_student:
            fields['grade'].read_only = True
        return fields


class AdminUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['date_joined', 'last_login']


class TeacherCourseMaterialSerializer(CourseMaterialSerializer):
    class Meta(CourseMaterialSerializer.Meta):
        fields = '__all__'
        read_only_fields = ['course', 'uploaded_by']


class StudentHomeworkSubmissionSerializer(HomeworkSubmissionSerializer):
    class Meta(HomeworkSubmissionSerializer.Meta):
        exclude = ['grade']
