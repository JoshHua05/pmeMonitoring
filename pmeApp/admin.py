from django.contrib import admin
from .models import Applicant

# Register your models here.
@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('lastName', 'firstName', 'middleInitial','suffix', 'sex', 'birthDate', 'contactNumber', 'authorityDate', 'mtf', 'purpose',)
    ordering = ('lastName',)
    search_fields = ('lastName','firstName', 'middleInitial','suffix', 'sex', 'birthDate', 'contactNumber', 'authorityDate', 'mtf', 'purpose',)
    list_filter = ('lastName','purpose',)
