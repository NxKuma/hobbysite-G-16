from django.contrib import admin

from .models import Commission, Job


class JobInline(admin.StackedInline):
    model = Job


class JobAdmin(admin.ModelAdmin):
    model = Job


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [JobInline]


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)