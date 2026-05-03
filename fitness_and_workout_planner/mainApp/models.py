from django.db import models

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

    member_ship = models.CharField(
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
