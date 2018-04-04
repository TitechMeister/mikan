from django.contrib import admin
from work.models import Activity, Workplace, Work, WorkPlan, PracticalWork


class PracticalWorkInline(admin.TabularInline):
    model = PracticalWork
    extra = 1


class WorkAdmin(admin.ModelAdmin):
    list_display = ("name", "assigned")
    list_filter = ("assigned_team", "assigned_section")


class WorkPlanAdmin(admin.ModelAdmin):
    list_filter = ("assigned_team", "assigned_section")
    inlines = (PracticalWorkInline,)


admin.site.register(Activity)
admin.site.register(Workplace)
admin.site.register(Work, WorkAdmin)
admin.site.register(WorkPlan, WorkPlanAdmin)
