from django.contrib import admin

from . models import HitCounter


class HitCounterAdmin(admin.ModelAdmin):
    pass


admin.site.register(HitCounter, HitCounterAdmin)
