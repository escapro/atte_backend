from django.db import models
from django.contrib.auth.models import User
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    shift_start_time = models.TimeField(null=True)
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.schema_name

class Domain(DomainMixin):
    pass

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client = models.ManyToManyField(Client)

    def __str__(self):
        
        return "user: {}".format(self.user)
        # return "{}".format(self.user)

    # def getTags(self):
    #     return self.client.values_list()

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client = models.ManyToManyField(Client,)
    
    def __str__(self):
        return "user: {}, client: {}".format(self.user, self.client)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.user, self.client)
