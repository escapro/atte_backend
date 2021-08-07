# from crm.models import Client, Domain

# # create your public tenant
# tenant = Client(schema_name='ert',
#                 name='ert.',
#                 paid_until='2016-12-05',
#                 on_trial=False)
# tenant.save()

# # # Add one or more domains for the tenant
# domain = Domain()
# domain.domain = '127.0.0.1' # don't add your port or www here! on a local server you'll want to use localhost here
# domain.tenant = tenant
# domain.is_primary = True
# # domain.save()

# print("=====")
# print(domain)
# print("======")