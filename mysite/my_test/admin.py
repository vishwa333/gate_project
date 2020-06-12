from django.contrib import admin

from .models import *
# Register your models here.
#admin.site.register(user)
from .models import testtype


@admin.register(testtype)
class TesttypeAdmin(admin.ModelAdmin):
    list_display = ('ttype',)
    pass

admin.site.register(test)
admin.site.register(test_result)
admin.site.register(test_responses)
