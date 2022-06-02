from django.contrib import admin

from .models import *

from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_admin

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' %
                        (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# admin.site.register(Audittrail)
# admin.site.register(Subscriptions)
# admin.site.register(TblAdmin)
class TblAttendanceAdmin(admin.ModelAdmin):
    list_display = ["fld_ai_id", "fld_user_id", "fld_latitude",
                    "fld_longitude", "fld_date", "fld_time"]
    search_fields = ["fld_user_id__id",
                     "fld_user_id__email", "fld_date", "fld_time"]
    # list_filter = ['status', 'is_ordered']


class TblAttendanceLogAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "site_name",
                    "distance", "check_in_time", "check_out_time", "visit_id"]
    search_fields = ["user_id__id",
                     "user_id__email", "visit_id"]
    # list_filter = ['status', 'is_ordered']


admin.site.register(TblAttendanceLog, TblAttendanceLogAdmin)
admin.site.register(TblAttendance, TblAttendanceAdmin)
admin.site.register(TblRates)
admin.site.register(TblSites)
admin.site.register(TblUserDevices)
admin.site.register(TblUserLevel)
admin.site.register(TblUserSites)
admin.site.register(TblUserReimbursements)
