from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('create/', views.applicant_create_view, name="applicant-create"),
    path('list/', views.applicant_list_view, name="applicant-list"),
    path('applicant_update/<applicant_id>', views.applicant_update_view, name="applicant-update"),
    path('applicant_delete/<applicant_id>', views.applicant_delete_view, name="applicant-delete"),
    path('laboratory_view/', views.laboratory_view, name="laboratory-view"),
    path('laboratory_update/<laboratory_id>', views.laboratory_update, name="laboratory-update"),
    path('report_csv', views.report_csv, name="report-csv"),
    path('ocsaf_view/', views.ocsaf_view, name="ocsaf-view"),
    path('ocsaf_update/<ocsaf_id>', views.ocsaf_update, name="ocsaf-update"),
    path('applicant_search/', views.applicant_search, name="applicant-search"),
    
]