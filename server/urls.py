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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from irctapp.views import IndexView, get_reasons_by_inv, favorite_status_method, set_status_method_item, filter_risks_by_string, qa_get_card_by_risk, qa_get_all_risks_names, logout_auth, login_auth, \
    get_review_list, get_customer_list, get_backoffice_list, get_not_analyzed_list, reset_database, get_types_risk, get_summary, get_info_card, get_value_problems_chart, get_customer_data_chart, \
    get_total_revenue_at_risk, get_percent_invoices_in_risk, get_total_invoices_in_month, get_services_stacked_chart, get_services_chart, get_invoices_chart, get_services_details_invoice, \
    get_qtd_similar_complete, submit_others_complete, has_recommendation_invoices, get_qtd_similar, submit_others, submit_invoice, get_list_problems, get_amount_average_invoices, get_account_invoices, \
    get_dashboard_table, get_table_problems, get_sum_revenue, get_invoices_problems, get_invoices, get_value, get_test

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('gettest', get_test),
    path('getvalue', get_value),
    path('getinvoices', get_invoices),
    path('getinvoicesproblems', get_invoices_problems),
    path('getsumrevenue', get_sum_revenue),
    path('gettableproblems', get_table_problems),
    path('getdashboardtab', get_dashboard_table),
    path('getinvoicesacc', get_account_invoices),
    path('getmedia', get_amount_average_invoices),
    path('getlistproblems', get_list_problems),
    path('submitinvoice', submit_invoice),
    path('submitothers', submit_others),
    path('getqtdsimilar', get_qtd_similar),
    path('hasrecommendation', has_recommendation_invoices),
    path('submitotherscomplete', submit_others_complete),
    path('getqtdsimilarcomplete', get_qtd_similar_complete),
    path('getservicesdetails', get_services_details_invoice),
    path('getinvoiceschart', get_invoices_chart),
    path('getserviceschart', get_services_chart),
    path('getservicesstackedchart', get_services_stacked_chart),
    path('gettotalinvoicesmonth', get_total_invoices_in_month),
    path('getpercentinvoicesrisk', get_percent_invoices_in_risk),
    path('gettotalrevenueatrisk', get_total_revenue_at_risk),
    path('getcustomerproblemschart', get_customer_data_chart),
    path('getvalueproblemschart', get_value_problems_chart),
    path('getinfocard', get_info_card),
    path('getsummary', get_summary),
    path('gettypesofrisk', get_types_risk),
    path('resetdatabase', reset_database),
    path('getnotanalyzedlist', get_not_analyzed_list),
    path('getbackofficelist', get_backoffice_list),
    path('getcustomerlist', get_customer_list),
    path('getreviewlist', get_review_list),

    path('login', login_auth),
    path('logout', logout_auth),
    path('qalistnamerisks', qa_get_all_risks_names),
    path('qagetcardbyrisk', qa_get_card_by_risk),
    path('qafilterlistrisk', filter_risks_by_string),
    path('qasetstatusmethod', set_status_method_item),
    path('qafavoritemethod', favorite_status_method),

    path('getreasonsbyinvoice', get_reasons_by_inv)
]
