
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .form import ApplicantForm, LaboratoryForm, OcsafForm
from .models import Applicant
from django.http import HttpResponse
import csv
from django.db.models import Avg, Sum, Count, Q
from django.contrib import messages
#Import Pagination Stuff
from django.core.paginator import Paginator




# Create your views here.

def applicant_search(request):
    #determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #Query the Applicant DB Model
        searched = Applicant.objects.filter(lastName__icontains=searched)
        #Test for null
        if not searched:
            messages.success(request, "Applicant does not exist")
            return render(request, 'pmeApp/applicant-search.html',{})
        else:
            return render(request, 'pmeApp/applicant-search.html',{'searched': searched})
    else:
        return render(request, 'pmeApp/applicant-search.html',{})   

    


#CSV File

def report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=report.csv'

    #Create a cvs writer
    writer = csv.writer(response)

    #Designate the Model
    applicant = Applicant.objects.all()

    #Add column headings to the csv file
    writer.writerow(['LAST NAME','FIRST NAME','MI','SUFFIX','SEX','BIRTH DATE','CONTACT NR','AUTHORITY DATE','MTF','PURPOSE', 'LAB DATE STARTED', 'LAB DATE COMPLETED','LAB STATUS','LAB REMARKS', 'ECG DATE STARTED', 'ECG DATE COMPLETED','ECG STATUS','ECG REMARKS', 'XRAY DATE STARTED', 'XRAY DATE COMPLETED','XRAY STATUS','XRAY REMARKS', 'NP DATE STARTED', 'NP WRITTEN EXAM','NP INITIAL INTERVIEW','NP FINAL INTERVIEW', 'NP DATE COMPLETED', 'NP STATUS', 'NP REMARKS', 'DENTAL DATE STARTED', 'DENTAL DATE COMPLETED','DENTAL STATUS','DENTAL REMARKS', 'IMMUNIZATION DATE STARTED', 'IMMUNIZATION DATE COMPLETED','IMMUNIZATION STATUS','IMMUNIZATION REMARKS', 'LAB DATE STARTED', 'LAB DATE COMPLETED','LAB STATUS','LAB REMARKS', 'DRUG TEST DATE STARTED', 'DRUG TEST DATE COMPLETED','DRUG TEST STATUS','DRUG TEST REMARKS', 'EENT DATE STARTED', 'EENT DATE COMPLETED','EENT STATUS','EENT REMARKS', 'GENPHY DATE STARTED', 'GENPHY DATE COMPLETED','GENPHY STATUS','GENPHY REMARKS', 'OCSAF STATUS', 'OCSAF FINDINGS','OCSAF DATE OF CERT','OCSAF REMARKS', ])

    #Loop thru and output
    for applicant in applicant:
        writer.writerow([applicant.lastName, applicant.firstName, applicant.middleInitial, applicant.suffix, applicant.sex, applicant.birthDate, applicant.contactNumber, applicant.authorityDate, applicant.mtf, applicant.purpose, applicant.labDateStarted, applicant.npDateCompleted, applicant.labStatus, applicant.labRemarks, applicant.ecgDateStarted, applicant.ecgDateCompleted, applicant.ecgStatus, applicant.ecgRemarks, applicant.xrayDateStarted, applicant.xrayDateCompleted, applicant.xrayStatus, applicant.xrayRemarks, applicant.npDateStarted, applicant.npWrittenExam, applicant.npInitialInterview, applicant.npFinalInterview, applicant.npDateCompleted, applicant.npStatus, applicant.npRemarks, applicant.dentalDateStarted, applicant.dentalDateCompleted, applicant.dentalStatus, applicant.dentalRemarks, applicant.immunizationDateStarted, applicant.immunizationDateCompleted, applicant.immunizationStatus, applicant.immunizationRemarks, applicant.eentDateStarted, applicant.eentDateCompleted, applicant.eentStatus, applicant.eentRemarks, applicant.genPhyDateStarted, applicant.genPhyDateCompleted, applicant.genPhyStatus, applicant.genPhyRemarks, applicant.ocsafStatus, applicant.ocsafFindings, applicant.ocsafDateOfCert, applicant.ocsafRemarks,])
    return response

#Home view
def index(request):
    #CARD MTFs
    cardAFGH = Applicant.objects.filter(mtf ="AFGH",).count()
    cardFABH = Applicant.objects.filter(mtf ="FABH",).count()
    cardAFCH = Applicant.objects.filter(mtf ="AFCH",).count()
    cardCGARSH = Applicant.objects.filter(mtf ="CGARSH",).count()
    cardBGBNEABH = Applicant.objects.filter(mtf ="BGBNEABH",).count()
    cardEAABH = Applicant.objects.filter(mtf ="EAABH",).count()

    #OVERALL RECAP TABLE
    countMale =  Applicant.objects.filter(sex ="MALE").count()
    countFemale =  Applicant.objects.filter(sex ="FEMALE").count()
    countTotal =  countMale + countFemale
    countMaleOngoing = Applicant.objects.filter(sex ="MALE", ocsafStatus ="ONGOING",).count()
    countFemaleOngoing = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="ONGOING",).count()
    countTotalOngoing = countMaleOngoing + countFemaleOngoing
    countMaleP1 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P1",).count()
    countFemaleP1 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P1",).count()
    countTotalP1 = countMaleP1 + countFemaleP1
    countMaleP2 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P2",).count()
    countFemaleP2 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P2",).count()
    countTotalP2 = countMaleP2 + countFemaleP2
    countMaleDQ = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DQ",).count()
    countFemaleDQ = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DQ",).count()
    countTotalDQ = countMaleDQ + countFemaleDQ
    countMaleDNC = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNC",).count()
    countFemaleDNC = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNC",).count()
    countTotalDNC = countMaleDNC + countFemaleDNC
    countMaleDNR = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNR",).count()
    countFemaleDNR = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNR",).count()
    countTotalDNR = countMaleDNR + countFemaleDNR
    countGrandTotal = countTotalOngoing + countTotalP1 + countTotalP2 + countTotalDQ + countTotalDNC + countTotalDNR

    #AFGH TABLE
    AFGHcountMale =  Applicant.objects.filter(sex ="MALE", mtf = "AFGH").count()
    AFGHcountFemale =  Applicant.objects.filter(sex ="FEMALE", mtf = "AFGH").count()
    AFGHcountTotal =  AFGHcountMale + AFGHcountFemale
    AFGHcountMaleOngoing = Applicant.objects.filter(sex ="MALE", ocsafStatus ="ONGOING", mtf = "AFGH").count()
    AFGHcountFemaleOngoing = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="ONGOING", mtf = "AFGH").count()
    AFGHcountTotalOngoing = AFGHcountMaleOngoing + AFGHcountFemaleOngoing
    AFGHcountMaleP1 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P1", mtf = "AFGH").count()
    AFGHcountFemaleP1 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P1", mtf = "AFGH").count()
    AFGHcountTotalP1 = AFGHcountMaleP1 + AFGHcountFemaleP1
    AFGHcountMaleP2 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P2", mtf = "AFGH").count()
    AFGHcountFemaleP2 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P2", mtf = "AFGH").count()
    AFGHcountTotalP2 = AFGHcountMaleP2 + AFGHcountFemaleP2
    AFGHcountMaleDQ = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DQ", mtf = "AFGH").count()
    AFGHcountFemaleDQ = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DQ", mtf = "AFGH").count()
    AFGHcountTotalDQ = AFGHcountMaleDQ + AFGHcountFemaleDQ
    AFGHcountMaleDNC = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNC", mtf = "AFGH").count()
    AFGHcountFemaleDNC = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNC", mtf = "AFGH").count()
    AFGHcountTotalDNC = AFGHcountMaleDNC + AFGHcountFemaleDNC
    AFGHcountMaleDNR = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNR", mtf = "AFGH").count()
    AFGHcountFemaleDNR = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNR", mtf = "AFGH").count()
    AFGHcountTotalDNR = AFGHcountMaleDNR + AFGHcountFemaleDNR
    AFGHcountGrandTotal = AFGHcountTotalOngoing + AFGHcountTotalP1 + AFGHcountTotalP2 + AFGHcountTotalDQ + AFGHcountTotalDNC + AFGHcountTotalDNR

    #FABH TABLE
    FABHcountMale =  Applicant.objects.filter(sex ="MALE", mtf = "FABH").count()
    FABHcountFemale =  Applicant.objects.filter(sex ="FEMALE", mtf = "FABH").count()
    FABHcountTotal =  FABHcountMale + FABHcountFemale
    FABHcountMaleOngoing = Applicant.objects.filter(sex ="MALE", ocsafStatus ="ONGOING", mtf = "FABH",).count()
    FABHcountFemaleOngoing = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="ONGOING", mtf = "FABH",).count()
    FABHcountTotalOngoing = FABHcountMaleOngoing + FABHcountFemaleOngoing
    FABHcountMaleP1 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P1", mtf = "FABH",).count()
    FABHcountFemaleP1 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P1", mtf = "FABH",).count()
    FABHcountTotalP1 = FABHcountMaleP1 + FABHcountFemaleP1
    FABHcountMaleP2 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P2", mtf = "FABH",).count()
    FABHcountFemaleP2 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P2", mtf = "FABH",).count()
    FABHcountTotalP2 = FABHcountMaleP2 + FABHcountFemaleP2
    FABHcountMaleDQ = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DQ", mtf = "FABH",).count()
    FABHcountFemaleDQ = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DQ", mtf = "FABH",).count()
    FABHcountTotalDQ = FABHcountMaleDQ + FABHcountFemaleDQ
    FABHcountMaleDNC = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNC", mtf = "FABH",).count()
    FABHcountFemaleDNC = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNC", mtf = "FABH",).count()
    FABHcountTotalDNC = FABHcountMaleDNC + FABHcountFemaleDNC
    FABHcountMaleDNR = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNR", mtf = "FABH",).count()
    FABHcountFemaleDNR = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNR", mtf = "FABH",).count()
    FABHcountTotalDNR = FABHcountMaleDNR + FABHcountFemaleDNR
    FABHcountGrandTotal = FABHcountTotalOngoing + FABHcountTotalP1 + FABHcountTotalP2 + FABHcountTotalDQ + FABHcountTotalDNC + FABHcountTotalDNR

    #AFCH
    AFCHcountMale =  Applicant.objects.filter(sex ="MALE", mtf = "AFCH").count()
    AFCHcountFemale =  Applicant.objects.filter(sex ="FEMALE", mtf = "AFCH").count()
    AFCHcountTotal =  AFCHcountMale + AFCHcountFemale
    AFCHcountMaleOngoing = Applicant.objects.filter(sex ="MALE", ocsafStatus ="ONGOING", mtf = "AFCH",).count()
    AFCHcountFemaleOngoing = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="ONGOING", mtf = "AFCH",).count()
    AFCHcountTotalOngoing = AFCHcountMaleOngoing + AFCHcountFemaleOngoing
    AFCHcountMaleP1 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P1", mtf = "AFCH",).count()
    AFCHcountFemaleP1 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P1", mtf = "AFCH",).count()
    AFCHcountTotalP1 = AFCHcountMaleP1 + AFCHcountFemaleP1
    AFCHcountMaleP2 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P2", mtf = "AFCH",).count()
    AFCHcountFemaleP2 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P2", mtf = "AFCH",).count()
    AFCHcountTotalP2 = AFCHcountMaleP2 + AFCHcountFemaleP2
    AFCHcountMaleDQ = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DQ", mtf = "AFCH",).count()
    AFCHcountFemaleDQ = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DQ", mtf = "AFCH",).count()
    AFCHcountTotalDQ = AFCHcountMaleDQ + AFCHcountFemaleDQ
    AFCHcountMaleDNC = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNC", mtf = "AFCH",).count()
    AFCHcountFemaleDNC = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNC", mtf = "AFCH",).count()
    AFCHcountTotalDNC = AFCHcountMaleDNC + AFCHcountFemaleDNC
    AFCHcountMaleDNR = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNR", mtf = "AFCH",).count()
    AFCHcountFemaleDNR = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNR", mtf = "AFCH",).count()
    AFCHcountTotalDNR = AFCHcountMaleDNR + AFCHcountFemaleDNR
    AFCHcountGrandTotal = AFCHcountTotalOngoing + AFCHcountTotalP1 + AFCHcountTotalP2 + AFCHcountTotalDQ + AFCHcountTotalDNC + AFCHcountTotalDNR

    #CGARSH
    CGARSHcountMale =  Applicant.objects.filter(sex ="MALE", mtf = "CGARSH").count()
    CGARSHcountFemale =  Applicant.objects.filter(sex ="FEMALE", mtf = "CGARSH").count()
    CGARSHcountTotal =  CGARSHcountMale + CGARSHcountFemale
    CGARSHcountMaleOngoing = Applicant.objects.filter(sex ="MALE", ocsafStatus ="ONGOING", mtf = "CGARSH",).count()
    CGARSHcountFemaleOngoing = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="ONGOING", mtf = "CGARSH",).count()
    CGARSHcountTotalOngoing = CGARSHcountMaleOngoing + CGARSHcountFemaleOngoing
    CGARSHcountMaleP1 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P1", mtf = "CGARSH",).count()
    CGARSHcountFemaleP1 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P1", mtf = "CGARSH",).count()
    CGARSHcountTotalP1 = CGARSHcountMaleP1 + CGARSHcountFemaleP1
    CGARSHcountMaleP2 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P2", mtf = "CGARSH",).count()
    CGARSHcountFemaleP2 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P2", mtf = "CGARSH",).count()
    CGARSHcountTotalP2 = CGARSHcountMaleP2 + CGARSHcountFemaleP2
    CGARSHcountMaleDQ = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DQ", mtf = "CGARSH",).count()
    CGARSHcountFemaleDQ = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DQ", mtf = "CGARSH",).count()
    CGARSHcountTotalDQ = CGARSHcountMaleDQ + CGARSHcountFemaleDQ
    CGARSHcountMaleDNC = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNC", mtf = "CGARSH",).count()
    CGARSHcountFemaleDNC = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNC", mtf = "CGARSH",).count()
    CGARSHcountTotalDNC = CGARSHcountMaleDNC + CGARSHcountFemaleDNC
    CGARSHcountMaleDNR = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNR", mtf = "CGARSH",).count()
    CGARSHcountFemaleDNR = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNR", mtf = "CGARSH",).count()
    CGARSHcountTotalDNR = CGARSHcountMaleDNR + CGARSHcountFemaleDNR
    CGARSHcountGrandTotal = CGARSHcountTotalOngoing + CGARSHcountTotalP1 + CGARSHcountTotalP2 + CGARSHcountTotalDQ + CGARSHcountTotalDNC + CGARSHcountTotalDNR

    #BGBNEAB
    BGBNEABHcountMale =  Applicant.objects.filter(sex ="MALE", mtf = "BGBNEABH").count()
    BGBNEABHcountFemale =  Applicant.objects.filter(sex ="FEMALE", mtf = "BGBNEABH").count()
    BGBNEABHcountTotal =  BGBNEABHcountMale + BGBNEABHcountFemale
    BGBNEABHcountMaleOngoing = Applicant.objects.filter(sex ="MALE", ocsafStatus ="ONGOING", mtf = "BGBNEABH",).count()
    BGBNEABHcountFemaleOngoing = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="ONGOING", mtf = "BGBNEABH",).count()
    BGBNEABHcountTotalOngoing = BGBNEABHcountMaleOngoing + BGBNEABHcountFemaleOngoing
    BGBNEABHcountMaleP1 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P1", mtf = "BGBNEABH",).count()
    BGBNEABHcountFemaleP1 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P1", mtf = "BGBNEABH",).count()
    BGBNEABHcountTotalP1 = BGBNEABHcountMaleP1 + BGBNEABHcountFemaleP1
    BGBNEABHcountMaleP2 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P2", mtf = "BGBNEABH",).count()
    BGBNEABHcountFemaleP2 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P2", mtf = "BGBNEABH",).count()
    BGBNEABHcountTotalP2 = BGBNEABHcountMaleP2 + BGBNEABHcountFemaleP2
    BGBNEABHcountMaleDQ = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DQ", mtf = "BGBNEABH",).count()
    BGBNEABHcountFemaleDQ = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DQ", mtf = "BGBNEABH",).count()
    BGBNEABHcountTotalDQ = BGBNEABHcountMaleDQ + BGBNEABHcountFemaleDQ
    BGBNEABHcountMaleDNC = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNC", mtf = "BGBNEABH",).count()
    BGBNEABHcountFemaleDNC = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNC", mtf = "BGBNEABH",).count()
    BGBNEABHcountTotalDNC = BGBNEABHcountMaleDNC + BGBNEABHcountFemaleDNC
    BGBNEABHcountMaleDNR = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNR", mtf = "BGBNEABH",).count()
    BGBNEABHcountFemaleDNR = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNR", mtf = "BGBNEABH",).count()
    BGBNEABHcountTotalDNR = BGBNEABHcountMaleDNR + BGBNEABHcountFemaleDNR
    BGBNEABHcountGrandTotal = BGBNEABHcountTotalOngoing + BGBNEABHcountTotalP1 + BGBNEABHcountTotalP2 + BGBNEABHcountTotalDQ + BGBNEABHcountTotalDNC + BGBNEABHcountTotalDNR
    
    #EAAB
    EAABHcountMale =  Applicant.objects.filter(sex ="MALE", mtf = "EAABH").count()
    EAABHcountFemale =  Applicant.objects.filter(sex ="FEMALE", mtf = "EAABH").count()
    EAABHcountTotal =  EAABHcountMale + EAABHcountFemale
    EAABHcountMaleOngoing = Applicant.objects.filter(sex ="MALE", ocsafStatus ="ONGOING", mtf = "EAABH",).count()
    EAABHcountFemaleOngoing = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="ONGOING", mtf = "EAABH",).count()
    EAABHcountTotalOngoing = EAABHcountMaleOngoing + EAABHcountFemaleOngoing
    EAABHcountMaleP1 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P1", mtf = "EAABH",).count()
    EAABHcountFemaleP1 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P1", mtf = "EAABH",).count()
    EAABHcountTotalP1 = EAABHcountMaleP1 + EAABHcountFemaleP1
    EAABHcountMaleP2 = Applicant.objects.filter(sex ="MALE", ocsafStatus ="P2", mtf = "EAABH",).count()
    EAABHcountFemaleP2 = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="P2", mtf = "EAABH",).count()
    EAABHcountTotalP2 = EAABHcountMaleP2 + EAABHcountFemaleP2
    EAABHcountMaleDQ = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DQ", mtf = "EAABH",).count()
    EAABHcountFemaleDQ = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DQ", mtf = "EAABH",).count()
    EAABHcountTotalDQ = EAABHcountMaleDQ + EAABHcountFemaleDQ
    EAABHcountMaleDNC = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNC", mtf = "EAABH",).count()
    EAABHcountFemaleDNC = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNC", mtf = "EAABH",).count()
    EAABHcountTotalDNC = EAABHcountMaleDNC + EAABHcountFemaleDNC
    EAABHcountMaleDNR = Applicant.objects.filter(sex ="MALE", ocsafStatus ="DNR", mtf = "EAABH",).count()
    EAABHcountFemaleDNR = Applicant.objects.filter(sex ="FEMALE", ocsafStatus ="DNR", mtf = "EAABH",).count()
    EAABHcountTotalDNR = EAABHcountMaleDNR + EAABHcountFemaleDNR
    EAABHcountGrandTotal = EAABHcountTotalOngoing + EAABHcountTotalP1 + EAABHcountTotalP2 + EAABHcountTotalDQ + EAABHcountTotalDNC + EAABHcountTotalDNR

    return render(request, 'pmeApp/index.html',{
        
        #CARD MTFs
        'cardAFGH': cardAFGH, 'cardFABH': cardFABH, 
        'cardAFCH': cardAFCH, 'cardCGARSH': cardCGARSH, 
        'cardBGBNEABH': cardBGBNEABH, 'cardEAABH': cardEAABH,
        #OVERALL RECAP TABLE
        'countMale': countMale, 'countFemale': countFemale, 
        'countTotal': countTotal, 'countMaleOngoing': countMaleOngoing, 
        'countFemaleOngoing': countFemaleOngoing, 'countTotalOngoing': countTotalOngoing, 
        'countMaleP1': countMaleP1, 'countFemaleP1': countFemaleP1, 
        'countTotalP1': countTotalP1, 'countMaleP2': countMaleP2, 
        'countFemaleP2': countFemaleP2, 'countTotalP2': countTotalP2, 
        'countMaleDQ': countMaleDQ, 'countFemaleDQ': countFemaleDQ, 
        'countTotalDQ': countTotalDQ, 'countMaleDNC': countMaleDNC, 
        'countFemaleDNC': countFemaleDNC, 'countTotalDNC': countTotalDNC, 
        'countMaleDNR': countMaleDNR, 'countFemaleDNR': countFemaleDNR, 
        'countTotalDNR': countTotalDNR, 'countGrandTotal': countGrandTotal,
        #AFGH TABLE
        'AFGHcountMale': AFGHcountMale, 'AFGHcountFemale': AFGHcountFemale, 
        'AFGHcountTotal': AFGHcountTotal, 'AFGHcountMaleOngoing': AFGHcountMaleOngoing, 
        'AFGHcountFemaleOngoing': AFGHcountFemaleOngoing, 'AFGHcountTotalOngoing': AFGHcountTotalOngoing, 
        'AFGHcountMaleP1': AFGHcountMaleP1, 'AFGHcountFemaleP1': AFGHcountFemaleP1, 
        'AFGHcountTotalP1': AFGHcountTotalP1, 'AFGHcountMaleP2': AFGHcountMaleP2, 
        'AFGHcountFemaleP2': AFGHcountFemaleP2, 'AFGHcountTotalP2': AFGHcountTotalP2, 
        'AFGHcountMaleDQ': AFGHcountMaleDQ, 'AFGHcountFemaleDQ': AFGHcountFemaleDQ, 
        'AFGHcountTotalDQ': AFGHcountTotalDQ, 'AFGHcountMaleDNC': AFGHcountMaleDNC, 
        'AFGHcountFemaleDNC': AFGHcountFemaleDNC, 'AFGHcountTotalDNC': AFGHcountTotalDNC, 
        'AFGHcountMaleDNR': AFGHcountMaleDNR, 'AFGHcountFemaleDNR': AFGHcountFemaleDNR, 
        'AFGHcountTotalDNR': AFGHcountTotalDNR, 'AFGHcountGrandTotal': AFGHcountGrandTotal,
        #FABH TABLE
        'FABHcountMale': FABHcountMale, 'FABHcountFemale': FABHcountFemale, 
        'FABHcountTotal': FABHcountTotal, 'FABHcountMaleOngoing': FABHcountMaleOngoing, 
        'FABHcountFemaleOngoing': FABHcountFemaleOngoing, 'FABHcountTotalOngoing': FABHcountTotalOngoing, 
        'FABHcountMaleP1': FABHcountMaleP1, 'FABHcountFemaleP1': FABHcountFemaleP1, 
        'FABHcountTotalP1': FABHcountTotalP1, 'FABHcountMaleP2': FABHcountMaleP2, 
        'FABHcountFemaleP2': FABHcountFemaleP2, 'FABHcountTotalP2': FABHcountTotalP2, 
        'FABHcountMaleDQ': FABHcountMaleDQ, 'FABHcountFemaleDQ': FABHcountFemaleDQ, 
        'FABHcountTotalDQ': FABHcountTotalDQ, 'FABHcountMaleDNC': FABHcountMaleDNC, 
        'FABHcountFemaleDNC': FABHcountFemaleDNC, 'FABHcountTotalDNC': FABHcountTotalDNC, 
        'FABHcountMaleDNR': FABHcountMaleDNR, 'FABHcountFemaleDNR': FABHcountFemaleDNR, 
        'FABHcountTotalDNR': FABHcountTotalDNR, 'FABHcountGrandTotal': FABHcountGrandTotal,
        #AFCH
        'AFCHcountMale': AFCHcountMale, 'AFCHcountFemale': AFCHcountFemale, 
        'AFCHcountTotal': AFCHcountTotal, 'AFCHcountMaleOngoing': AFCHcountMaleOngoing, 
        'AFCHcountFemaleOngoing': AFCHcountFemaleOngoing, 'AFCHcountTotalOngoing': AFCHcountTotalOngoing, 
        'AFCHcountMaleP1': AFCHcountMaleP1, 'AFCHcountFemaleP1': AFCHcountFemaleP1, 
        'AFCHcountTotalP1': AFCHcountTotalP1, 'AFCHcountMaleP2': AFCHcountMaleP2, 
        'AFCHcountFemaleP2': AFCHcountFemaleP2, 'AFCHcountTotalP2': AFCHcountTotalP2, 
        'AFCHcountMaleDQ': AFCHcountMaleDQ, 'AFCHcountFemaleDQ': AFCHcountFemaleDQ, 
        'AFCHcountTotalDQ': AFCHcountTotalDQ, 'AFCHcountMaleDNC': AFCHcountMaleDNC, 
        'AFCHcountFemaleDNC': AFCHcountFemaleDNC, 'AFCHcountTotalDNC': AFCHcountTotalDNC, 
        'AFCHcountMaleDNR': AFCHcountMaleDNR, 'AFCHcountFemaleDNR': AFCHcountFemaleDNR, 
        'AFCHcountTotalDNR': AFCHcountTotalDNR, 'AFCHcountGrandTotal': AFCHcountGrandTotal,
        #CGARSH
        'CGARSHcountMale': CGARSHcountMale, 'CGARSHcountFemale': CGARSHcountFemale, 
        'CGARSHcountTotal': CGARSHcountTotal, 'CGARSHcountMaleOngoing': CGARSHcountMaleOngoing, 
        'CGARSHcountFemaleOngoing': CGARSHcountFemaleOngoing, 'CGARSHcountTotalOngoing': CGARSHcountTotalOngoing, 
        'CGARSHcountMaleP1': CGARSHcountMaleP1, 'CGARSHcountFemaleP1': CGARSHcountFemaleP1, 
        'CGARSHcountTotalP1': CGARSHcountTotalP1, 'CGARSHcountMaleP2': CGARSHcountMaleP2, 
        'CGARSHcountFemaleP2': CGARSHcountFemaleP2, 'CGARSHcountTotalP2': CGARSHcountTotalP2, 
        'CGARSHcountMaleDQ': CGARSHcountMaleDQ, 'CGARSHcountFemaleDQ': CGARSHcountFemaleDQ, 
        'CGARSHcountTotalDQ': CGARSHcountTotalDQ, 'CGARSHcountMaleDNC': CGARSHcountMaleDNC, 
        'CGARSHcountFemaleDNC': CGARSHcountFemaleDNC, 'CGARSHcountTotalDNC': CGARSHcountTotalDNC, 
        'CGARSHcountMaleDNR': CGARSHcountMaleDNR, 'CGARSHcountFemaleDNR': CGARSHcountFemaleDNR, 
        'CGARSHcountTotalDNR': CGARSHcountTotalDNR, 'CGARSHcountGrandTotal': CGARSHcountGrandTotal,
        #BGBNEAB
        'BGBNEABHcountMale': BGBNEABHcountMale, 'BGBNEABHcountFemale': BGBNEABHcountFemale, 
        'BGBNEABHcountTotal': BGBNEABHcountTotal, 'BGBNEABHcountMaleOngoing': BGBNEABHcountMaleOngoing, 
        'BGBNEABHcountFemaleOngoing': BGBNEABHcountFemaleOngoing, 'BGBNEABHcountTotalOngoing': BGBNEABHcountTotalOngoing, 
        'BGBNEABHcountMaleP1': BGBNEABHcountMaleP1, 'BGBNEABHcountFemaleP1': BGBNEABHcountFemaleP1, 
        'BGBNEABHcountTotalP1': BGBNEABHcountTotalP1, 'BGBNEABHcountMaleP2': BGBNEABHcountMaleP2, 
        'BGBNEABHcountFemaleP2': BGBNEABHcountFemaleP2, 'BGBNEABHcountTotalP2': BGBNEABHcountTotalP2, 
        'BGBNEABHcountMaleDQ': BGBNEABHcountMaleDQ, 'BGBNEABHcountFemaleDQ': BGBNEABHcountFemaleDQ, 
        'BGBNEABHcountTotalDQ': BGBNEABHcountTotalDQ, 'BGBNEABHcountMaleDNC': BGBNEABHcountMaleDNC, 
        'BGBNEABHcountFemaleDNC': BGBNEABHcountFemaleDNC, 'BGBNEABHcountTotalDNC': BGBNEABHcountTotalDNC, 
        'BGBNEABHcountMaleDNR': BGBNEABHcountMaleDNR, 'BGBNEABHcountFemaleDNR': BGBNEABHcountFemaleDNR, 
        'BGBNEABHcountTotalDNR': BGBNEABHcountTotalDNR, 'BGBNEABHcountGrandTotal': BGBNEABHcountGrandTotal,
        #EAAB
        'EAABHcountMale': EAABHcountMale, 'EAABHcountFemale': EAABHcountFemale, 
        'EAABHcountTotal': EAABHcountTotal, 'EAABHcountMaleOngoing': EAABHcountMaleOngoing, 
        'EAABHcountFemaleOngoing': EAABHcountFemaleOngoing, 'EAABHcountTotalOngoing': EAABHcountTotalOngoing, 
        'EAABHcountMaleP1': EAABHcountMaleP1, 'EAABHcountFemaleP1': EAABHcountFemaleP1, 
        'EAABHcountTotalP1': EAABHcountTotalP1, 'EAABHcountMaleP2': EAABHcountMaleP2, 
        'EAABHcountFemaleP2': EAABHcountFemaleP2, 'EAABHcountTotalP2': EAABHcountTotalP2, 
        'EAABHcountMaleDQ': EAABHcountMaleDQ, 'EAABHcountFemaleDQ': EAABHcountFemaleDQ, 
        'EAABHcountTotalDQ': EAABHcountTotalDQ, 'EAABHcountMaleDNC': EAABHcountMaleDNC, 
        'EAABHcountFemaleDNC': EAABHcountFemaleDNC, 'EAABHcountTotalDNC': EAABHcountTotalDNC, 
        'EAABHcountMaleDNR': EAABHcountMaleDNR, 'EAABHcountFemaleDNR': EAABHcountFemaleDNR, 
        'EAABHcountTotalDNR': EAABHcountTotalDNR, 'EAABHcountGrandTotal': EAABHcountGrandTotal,
        })


def tables(request):
    return render(request, 'pmeApp/tables.html')

#Applicant create view
def applicant_create_view(request):
    submitted = False
    if request.method == "POST":
         form = ApplicantForm(request.POST)
         if form.is_valid():
              form.save()
              return HttpResponseRedirect('/create?submitted=True')
    else:
         form = ApplicantForm
         if 'submitted' in request.GET:
              submitted = True
    return render(request,'pmeApp/applicant.html', {'form':form, 'submitted':submitted})

#Applicant list view
def applicant_list_view(request):

    if 'q' in request.GET:
        q= request.GET['q']
        #applicant = Applicant.objects.filter(lastName__icontains=q)
        multiple_q = Q(Q(lastName__icontains=q) | Q(firstName__icontains=q) | Q(contactNumber__icontains=q))
        applicant = Applicant.objects.filter(multiple_q)

    else:
        applicant = Applicant.objects.all()

        #Set up Pagination
        p = Paginator(Applicant.objects.all(), 10)
        page = request.GET.get('page')
        applicant = p.get_page(page)
    
    return render(request, 'pmeApp/applicant-list.html',{'applicant': applicant,})

#Applicant update view
def applicant_update_view(request, applicant_id):
    applicant = Applicant.objects.get(pk = applicant_id)
    form = ApplicantForm(request.POST or None, instance=applicant)
    if form.is_valid():
        form.save()
        return redirect('applicant-list')
    return render(request, 'pmeApp/applicant-update.html', {'applicant': applicant, 'form': form})

#Applicant delete view
def applicant_delete_view(request, applicant_id):
    applicant = Applicant.objects.get(pk = applicant_id)
    if request.method == 'POST':
        applicant.delete()
        return redirect('applicant-list')
    return render(request, 'pmeApp/applicant-delete.html')


#LABORATORY VIEWS

#Laboratory List view
def laboratory_view(request):

    if 'q' in request.GET:
        q= request.GET['q']
        #applicant = Applicant.objects.filter(lastName__icontains=q)
        multiple_q = Q(Q(lastName__icontains=q) | Q(firstName__icontains=q) | Q(contactNumber__icontains=q))
        laboratory = Applicant.objects.filter(multiple_q)
    else:
        laboratory = Applicant.objects.all()

        #Set up Pagination
        p = Paginator(Applicant.objects.all(), 10)
        page = request.GET.get('page')
        laboratory = p.get_page(page)

    return render(request, 'pmeApp/lab/laboratory.html',{'laboratory': laboratory,})

#Laboratory Update view
def laboratory_update(request, laboratory_id):
    laboratory = Applicant.objects.get(pk = laboratory_id)
    form = LaboratoryForm(request.POST or None, instance=laboratory)
    if form.is_valid():
        form.save()
        return redirect('laboratory-view')
    return render(request, 'pmeApp/lab/laboratory-update.html', {'laboratory': laboratory, 'form': form})


#OCSAF VIEWS
def ocsaf_view(request):
    if 'q' in request.GET:
        q= request.GET['q']
        #applicant = Applicant.objects.filter(lastName__icontains=q)
        multiple_q = Q(Q(lastName__icontains=q) | Q(firstName__icontains=q) | Q(contactNumber__icontains=q))
        ocsaf = Applicant.objects.filter(multiple_q)

    else:
        ocsaf = Applicant.objects.all()

        #Set up Pagination
        p = Paginator(Applicant.objects.all(), 10)
        page = request.GET.get('page')
        ocsaf = p.get_page(page)

    return render(request, 'pmeApp/ocsaf/ocsaf.html',{'ocsaf': ocsaf,})

#Laboratory Update view
def ocsaf_update(request, ocsaf_id):
    ocsaf = Applicant.objects.get(pk = ocsaf_id)
    form = OcsafForm(request.POST or None, instance=ocsaf)
    if form.is_valid():
        form.save()
        return redirect('ocsaf-view')
    return render(request, 'pmeApp/ocsaf/ocsaf-update.html', {'ocsaf': ocsaf, 'form': form})