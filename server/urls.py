"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from irctapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('gettest', views.get_test),
    path('getvalue', views.get_value),
    path('getinvoices', views.get_invoices),
    path('getinvoicesproblems', views.get_invoices_problems),
    path('getsumrevenue', views.get_sum_revenue),
    path('gettableproblems', views.get_table_problems),
    path('getdashboardtab', views.get_dashboard_table),
    path('getinvoicesacc', views.get_account_invoices),
    path('getmedia', views.get_amount_average_invoices),
    path('getlistproblems', views.get_list_problems),
    path('submitinvoice', views.submit_invoice),
    path('submitothers', views.submit_others),
    path('getqtdsimilar', views.get_qtd_similar),
    path('hasrecommendation', views.has_recommendation_invoices),
    path('submitotherscomplete', views.submit_others_complete),
    path('getqtdsimilarcomplete', views.get_qtd_similar_complete),
    path('getservicesdetails', views.get_services_details_invoice),
    path('getinvoiceschart', views.get_invoices_chart),
    path('getserviceschart', views.get_services_chart),
    path('getservicesstackedchart', views.get_services_stacked_chart),
    path('gettotalinvoicesmonth', views.get_total_invoices_in_month),
    path('getpercentinvoicesrisk', views.get_percent_invoices_in_risk),
    path('gettotalrevenueatrisk', views.get_total_revenue_at_risk),
    path('getcustomerproblemschart', views.get_customer_data_chart),
    path('getvalueproblemschart', views.get_value_problems_chart),
    path('getinfocard', views.get_info_card),
    path('getsummary', views.get_summary),
    path('gettypesofrisk', views.get_types_risk),
    path('resetdatabase', views.reset_database),
    path('getnotanalyzedlist', views.get_not_analyzed_list),
    path('getbackofficelist', views.get_backoffice_list),
    path('getcustomerlist', views.get_customer_list),
    path('getreviewlist', views.get_review_list),

    path('login', views.login_auth),
    path('logout', views.logout_auth),
    path('qalistnamerisks', views.qa_get_all_risks_names),
    path('qagetcardbyrisk', views.qa_get_card_by_risk),
    path('qafilterlistrisk', views.filter_risks_by_string),
    path('qasetstatusmethod', views.set_status_method_item),
    path('qafavoritemethod', views.favorite_status_method),

    path('getreasonsbyinvoice', views.get_reasons_by_inv)
]
