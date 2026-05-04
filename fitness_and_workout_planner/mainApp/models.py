from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Member(models.Model):
    class Membership(models.TextChoices):
        BASIC: str = "BASIC", "Basic"
        PREMIUM: str = "PREMIUM", "Premium"
        STUDENT: str = "STUDENT", "Student"
    class Status(models.TextChoices):
        ACTIVE: str = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
    
    member_id = models.CharField(
        max_length= 255,
        db_index = True,
        unique = True,
        help_text= 'Unique identifier for the member'
    )

    name = models.CharField(
        max_length= 255,
        db_index = True
    )
    email = models.EmailField()
    phone = models.CharField(
        max_length=10
    )
    membership = models.CharField(
        max_length = 255,
        choices = Membership.choices,
        default = Membership.BASIC
    )

    join_date = models.DateField()

    status = models.CharField(
        max_length = 10,
        choices = Status.choices,
        default = Status.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    class Meta:
        ordering = ["-join_date"] # ordering members on the list
        indexes = [
            models.Index(fields=["member_id"]),
            models.Index(fields = ["status", "membership"])
        ]
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self) -> str:
        return f"{self.member_id} - {self.name}"


# gym class model
class GymClass(models.Model):
    class DayChoices(models.TextChoices):
        MONDAY = "MON", "Monday"
        TUESDAY = "TUE", "Tuesday"
        WEDNESDAY = "WED", "Wednesday"
        THURSDAY = "THU", "Thursday"
        FRIDAY = "FRI", "Friday"
        SATURDAY = "SAT", "Saturday"
        SUNDAY = "SUN", "Sunday"
    
    name = models.CharField(max_length=150)

    trainer = models.CharField(
        max_length=100,
        help_text="Trainer name (can be replaced with FK later)"
    )

    start_time = models.DateTimeField(
        help_text="Date and time of the class"
    )

    duration = models.PositiveIntegerField(
        help_text = "Duration in minutes"
    )

    day = models.CharField(
        choices = DayChoices.choices,
        max_length = 10
    )

    capacity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]
        indexes = [
            models.Index(fields=["start_time"]),
            models.Index(fields=["trainer"]),
            models.Index(fields=["name"])
        ]
        # constraints = [
        #     models.CheckConstraint(
        #         check=models.Q(duration__gt=0),
        #         name="duration_positive"
        #     ),
        #     models.CheckConstraint(
        #         check=models.Q(capacity__gt=0),
        #         name="capacity_positive"
        #     ),
        # ]

    def clean(self):
        # Prevent scheduling in the past
        if self.start_time < timezone.now():
            raise ValidationError("Class cannot be scheduled in the past.")

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def __str__(self):
        return f"{self.name} | {self.trainer} | {self.start_time}"
    

