from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, Message, Indicators, Report


class MyUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'organization', 'role')
    search_fields = ('email', 'name', 'lastname', 'role')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {'fields': ('email', 'organization', 'role', 'password1', 'password2', 'name', 'lastname', 'age')}),
    )

    ordering = ('email',)


admin.site.register(User, MyUserAdmin)
admin.site.register(Organization)
admin.site.register(Message)
admin.site.register(Indicators)
admin.site.register(Report)
