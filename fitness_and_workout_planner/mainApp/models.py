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
        max_length = 10,
        choices = DayChoices.choices
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
        actual_day = self.start_time.strftime("%a").upper()[:3]
        if self.day != actual_day:
            raise ValidationError("Day must match start_time.")

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def __str__(self):
        return f"{self.name} | {self.trainer} | {self.start_time}"
    


from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.utils import timezone

class Trainer(models.Model):
    # Status Choices
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        ON_LEAVE = 'on_leave', 'On Leave'
        SUSPENDED = 'suspended', 'Suspended'
    
    # Name field
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        help_text="Full name of the trainer"
    )
    
    # Specialization field
    specialization = models.CharField(
        max_length=200,
        help_text="Trainer's area of expertise (e.g., Yoga, Cardio, Strength Training)"
    )
    
    # Email field
    email = models.EmailField(
        unique=True,
        max_length=254,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            message="Enter a valid email address"
        )],
        help_text="Trainer's email address"
    )
    
    # Phone field
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
        )],
        help_text="Trainer's contact number"
    )
    
    # Status field
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text="Current employment status"
    )
    
    # Additional useful fields (optional but recommended)
    profile_image = models.ImageField(
        upload_to='trainers/profiles/',
        null=True,
        blank=True,
        help_text="Trainer's profile picture"
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Short biography or description"
    )
    
    years_of_experience = models.PositiveIntegerField(
        default=0,
        help_text="Number of years of experience"
    )
    
    certifications = models.TextField(
        blank=True,
        null=True,
        help_text="List of certifications (comma-separated)"
    )
    
    hire_date = models.DateField(
        default=timezone.now,
        help_text="Date when trainer was hired"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trainers'
        verbose_name = 'Trainer'
        verbose_name_plural = 'Trainers'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['specialization']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_status_display_color(self):
        """Return CSS class for status badge"""
        status_colors = {
            'active': 'status active',
            'inactive': 'status inactive',
            'on_leave': 'status warning',
            'suspended': 'status danger'
        }
        return status_colors.get(self.status, 'status')
    
    def is_active(self):
        """Check if trainer is active"""
        return self.status == self.Status.ACTIVE
    
    def get_specializations_list(self):
        """Return specializations as a list"""
        return [s.strip() for s in self.specialization.split(',')]
    
    def save(self, *args, **kwargs):
        # Auto-capitalize name
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)