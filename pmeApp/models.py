from django.db import models

# Create your models here.
class Applicant(models.Model):

    genderChoices = [
         ("MALE","MALE"),
         ("FEMALE","FEMALE"),
     ]
    
    mtfChoices = [
         ("AFGH","AFGH"),
         ("FABH","FABH"),
         ("AFCH","AFCH"),
         ("CGARSH","CGARSH"),
         ("BGBNEABH","BGBNEABH"),
         ("EAABH","EAABH"),
     ]
    
    purposeChoices = [
        ("SE","SE"),
        ("CS","CS"),
    ]

    medicalStatusChoices = [
        ("ONGOING","ONGOING"),
        ("COMPLETED","COMPLETED"),
        ("w/ COMPLIANCE","w/ COMPLIANCE"),
        ("DNR","DNR"),
        ("DNC","DNC"),
        ("DQ","DQ"),
    ]

    npStatusChoices = [
        ("ONGOING","ONGOING"),
        ("COMPLETED","COMPLETED"),
        ("DNR","DNR"),
        ("DNC","DNC"),
        ("DQ","DQ"),
    ]

    ocsafStatusChoices = [
        ("P1","P1"),
        ("P2","P2"),
        ("ONGOING","ONGOING"),
        ("DNR","DNR"),
        ("DNC","DNC"),
        ("DQ","DQ"),
    ]

    lastName = models.CharField('Last Name', max_length=100)
    firstName = models.CharField('First Name',max_length=100)
    middleInitial = models.CharField('MI', max_length=10, blank=True)
    suffix = models.CharField('Suffix', max_length=10, blank=True)
    sex = models.CharField('Sex', max_length=10, choices=genderChoices, blank=True)
    birthDate = models.DateField('Birth Date', blank=True, null=True)
    contactNumber = models.CharField('Contact Number',max_length=20, blank=True)
    authorityDate = models.DateField('Authority Date', blank=True, null=True)
    mtf = models.CharField('MTF', max_length=10, choices=mtfChoices, blank=True)
    purpose = models.CharField('Purpose',max_length=10, choices=purposeChoices, blank=True)

    #Laboratory
    labDateStarted = models.DateField('Date Started', blank=True, null=True)
    labDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    labStatus = models.CharField('LAB Status', max_length=50, choices=medicalStatusChoices, blank=True)
    labRemarks = models.TextField('LAB Remarks',max_length=250, blank=True)

    #ECG
    ecgDateStarted = models.DateField('Date Started', blank=True, null=True)
    ecgDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    ecgStatus = models.CharField('ECG Status', max_length=50, choices=medicalStatusChoices, blank=True)
    ecgRemarks = models.TextField('ECG Remarks',max_length=250, blank=True)
    
    #X-ray
    xrayDateStarted = models.DateField('Date Started', blank=True, null=True)
    xrayDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    xrayStatus = models.CharField('X-ray Status', max_length=50, choices=medicalStatusChoices, blank=True)
    xrayRemarks = models.TextField('X-ray Remarks',max_length=250, blank=True)

    #NP
    npDateStarted = models.DateField('Date Started', blank=True, null=True)
    npWrittenExam = models.CharField('NP Written Exam', max_length=50, choices=npStatusChoices, blank=True)
    npInitialInterview = models.CharField('NP Written Exam', max_length=50, choices=npStatusChoices, blank=True)
    npFinalInterview = models.CharField('NP Written Exam', max_length=50, choices=npStatusChoices, blank=True)
    npDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    npStatus = models.CharField('NP Status', max_length=50, choices=medicalStatusChoices, blank=True)
    npRemarks = models.TextField('NP Remarks',max_length=250, blank=True)

    #Dental
    dentalDateStarted = models.DateField('Date Started', blank=True, null=True)
    dentalDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    dentalStatus = models.CharField('Dental Status', max_length=50, choices=medicalStatusChoices, blank=True)
    dentalRemarks = models.TextField('Dental Remarks',max_length=250, blank=True)

    #Immunization
    immunizationDateStarted = models.DateField('Date Started', blank=True, null=True)
    immunizationDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    immunizationStatus = models.CharField('Immunization Status', max_length=50, choices=medicalStatusChoices, blank=True)
    immunizationRemarks = models.TextField('Immunization Remarks',max_length=250, blank=True)

    #Drug Test
    drugTestDateStarted = models.DateField('Date Started', blank=True, null=True)
    drugTestDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    drugTestStatus = models.CharField('Drug Test Status', max_length=50, choices=medicalStatusChoices, blank=True)
    drugTestRemarks = models.TextField('Drug Test Remarks',max_length=250, blank=True)

    #EENT
    eentDateStarted = models.DateField('Date Started', blank=True, null=True)
    eentDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    eentStatus = models.CharField('EENT Test Status', max_length=50, choices=medicalStatusChoices, blank=True)
    eentRemarks = models.TextField('EENT Test Remarks',max_length=250, blank=True)

    #GenPhy
    genPhyDateStarted = models.DateField('Date Started', blank=True, null=True)
    genPhyDateCompleted = models.DateField('Date Completed', blank=True, null=True)
    genPhyStatus = models.CharField('GenPhy Test Status', max_length=50, choices=medicalStatusChoices, blank=True)
    genPhyRemarks = models.TextField('GenPhy  Test Remarks',max_length=250, blank=True)

    #OCSAF
    ocsafStatus = models.CharField('OCSAF Status', max_length=50, choices=ocsafStatusChoices, blank=True)
    ocsafFindings = models.TextField('OCSAF Findings',max_length=250, blank=True)
    ocsafDateOfCert = models.DateField('OCSAF Date of Certification', blank=True, null=True)
    ocsafRemarks = models.TextField('OCSAF Remarks',max_length=250, blank=True)
    

    def __str__ (self):
        return self.lastName +" "+ self.firstName +" "+ self.middleInitial