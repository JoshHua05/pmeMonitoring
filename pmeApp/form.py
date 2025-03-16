from django import forms
from django.forms import ModelForm
from .models import Applicant

class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ('lastName','firstName','middleInitial','suffix','sex','birthDate','contactNumber','authorityDate','mtf','purpose',)

class LaboratoryForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ('lastName','firstName','middleInitial','labDateStarted','labDateCompleted','labStatus','labRemarks',)

class OcsafForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ('lastName','firstName','middleInitial','ocsafStatus','ocsafFindings','ocsafDateOfCert','ocsafRemarks',)