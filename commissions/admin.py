from django.contrib import admin

from .models import Commission, Job, JobApplication


class JobApplicationInline(admin.StackedInline):
    model = JobApplication


class JobInline(admin.StackedInline):
    model = Job


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication


class JobAdmin(admin.ModelAdmin):
    model = Job
    inlines = [JobApplicationInline]


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [JobInline]


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)