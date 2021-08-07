from django.contrib import admin

from .models import *

from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from main.models import Client

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('name', 'paid_until')

@admin.register(Domain)
class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('domain', 'id')

admin.site.register(Admin)
admin.site.register(Manager)
admin.site.register(Employee)

# # create your first real tenant
# tenant = Client(schema_name='qwewer',
#                 name='Fonzy Tenant',
#                 paid_until='2014-12-05',
#                 on_trial=True)
# tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!

# # Add one or more domains for the tenant
# domain = Domain()
# domain.domain = 'tenant.127.0.0.1' # don't add your port or www here!
# domain.tenant = tenant
# domain.is_primary = True
# domain.save()