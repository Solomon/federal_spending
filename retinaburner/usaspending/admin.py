from django.contrib import admin
from retinaburner.usaspending.models import Contract
#from dcdata.grants.models import Grant

class ContractAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contract, ContractAdmin)


#class GrantAdmin(admin.ModelAdmin):
 #   pass

#admin.site.register(Grant, GrantAdmin)