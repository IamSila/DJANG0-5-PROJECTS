from django.contrib import admin
from .models import Member
# Register your models here.
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["member_id", "name", "membership", "join_date", "status"]
    # list_filter = []
    search_fields = ["name", "member_id", "membership"]