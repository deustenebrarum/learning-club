from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class UserRole(models.TextChoices):
    STUDENT = "student", "Студент"
    TEACHER = "teacher", "Преподаватель"
    ADMIN = "admin", "Администратор"


class User(AbstractUser):
    group = models.ForeignKey(
        "StudentsGroup", on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def has_role(self, role):
        return self.groups.filter(name=role).exists()

    @property
    def is_student(self):
        return self.has_role(UserRole.STUDENT)

    @property
    def is_teacher(self):
        return self.has_role(UserRole.TEACHER)

    @property
    def is_admin(self):
        return self.has_role(UserRole.ADMIN)


class StudentsGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'groups__name': UserRole.TEACHER}
    )

    def __str__(self):
        return self.title


class CourseMaterial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(
        upload_to='materials/', blank=True, null=True
    )
    link = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'groups__name': UserRole.TEACHER}
    )

    def __str__(self):
        return self.title


class Homework(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'groups__name': UserRole.TEACHER}
    )

    def __str__(self):
        return self.title


class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'groups__name': UserRole.STUDENT}
    )
    submission_link = models.URLField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"


class AttendanceRecord(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'groups__name': UserRole.STUDENT}
    )
    date = models.DateField()
    was_present = models.BooleanField()
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return (
            f"{self.student.username} " +
            "- {'Присутствовал' if self.was_present else 'Отсутствовал'}"
        )
