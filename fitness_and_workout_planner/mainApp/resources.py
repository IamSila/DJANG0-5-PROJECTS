#import_export modules
from import_export import resources
# models
from .models import Member

class MemberResource(resources.ModelResource):
    
    class Meta:
        model = Member
        fields = ('member_id', 'name', 'email', 'phone', 'membership', 'join_date', 'status')
        # exclude = ('create_at', 'updated_at')  # field will take precedence and exclude will be ignored.

        # we define ordering for the fields.
        import_order = ('member_id', 'name', 'email', 'phone', 'membership', 'join_date', 'status')
        export_order = ('member_id', 'name', 'email', 'phone', 'membership', 'join_date', 'status')
