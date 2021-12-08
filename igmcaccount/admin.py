from django.http import HttpResponse
from django.contrib import admin

from igmcaccount.models import User

class AccountsAdmin(admin.ModelAdmin):
    '''Define admin model for custom User model.'''
    fieldsets = (
        (None, {
            'fields': (
            'email',
            'username',
            'full_name',
            'currency',
            'phone_number',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_verified',
        )
        }),
        ('Advanced options', {
            'classes': ('collapse', 'extrapretty'),
            'fields': ('last_login',  'groups', 'user_permissions'),
        }),
    )
    list_per_page = 20
    list_display = ('email', 'username', 'is_active',)
    list_filter = ('created_at', 'is_active', )
    actions_on_bottom = True
    search_fields = ('email',)
    actions = ('deactivate_user', 'activate_user', )

    def deactivate_user(self, request, queryset):
        '''Deactivate selected user accounts.'''
        rows_updated = queryset.update(is_active=False)
        if rows_updated == 1:
            message_bit = '1 user was'
        else:
            message_bit = '{} users were' .format(rows_updated)
        self.message_user(request, '{} successfully deactivated.'.format(message_bit))

    def activate_user(self, request, queryset):
        '''Activate selected user accounts.'''
        rows_updated = queryset.update(is_active=True)
        if rows_updated == 1:
            message_bit = '1 user was'
        else:
            message_bit = '{} users were'.format(rows_updated)
        self.message_user(request, '{} successfully activated.'.format(message_bit))

    deactivate_user.short_description = 'Deactivate selected'
    activate_user.short_description = 'Activate selected'

# class ProfilesAdmin(admin.ModelAdmin):
#     fields =('full_name','currency','phone_number','user')

admin.site.register(User, AccountsAdmin,)


