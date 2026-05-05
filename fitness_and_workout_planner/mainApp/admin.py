from django.contrib import admin

# models
from .models import Member, GymClass, Trainer

#import_export modules
from import_export import resources


# Register your models here.
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["member_id", "name", "membership", "join_date", "status"]
    # list_filter = []
    search_fields = ["name", "member_id", "membership"]

@admin.register(GymClass)
class GymClassAdmin(admin.ModelAdmin):
    list_display = ["name", "trainer", "duration", "day", "capacity", "start_time", "end_time"]
    search_fields = ["name", "trainer"]



@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'email', 'phone', 'status', 'years_of_experience']
    list_filter = ['status', 'specialization', 'hire_date']
    search_fields = ['name', 'email', 'phone', 'specialization']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'profile_image', 'bio')
        }),
        ('Professional Information', {
            'fields': ('specialization', 'years_of_experience', 'certifications', 'status')
        }),
        ('Employment Details', {
            'fields': ('hire_date',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )



class MemberResource(resources.ModelResource):
    
    class Meta:
        model = Member
        fields = ('member_id', 'name', 'email', 'phone', 'membership', 'join_date', 'status')
        exclude = ('create_at', 'updated_at')  # field will take precedence and exclude will be ignored.

        # we define ordering for the fields.
        import_order = ('member_id', 'name', 'email', 'phone', 'membership', 'join_date', 'status')
        export_order = ('member_id', 'name', 'email', 'phone', 'membership', 'join_date', 'status')