from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'mobile', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        ('User Credentials', {
         'fields': ('email', 'mobile', 'password')}),
        ('Personal info', {
         'fields': ("user_level", "first_name", "last_name", "address", "check_in_time", "check_out_time", "last_login", "is_delete", "created_datetime", "datetime_timestamp")}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

# in this case the password displayed unencrypted and also  unencrypted in database.
# admin.site.register(User)
