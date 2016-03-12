from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

# API endpoints



urlpatterns = [
	url(r'^api/v1/users$', views.SntUsersList.as_view()),
	url(r'^api/v1/user/(?P<pk>[0-9]+)/$', views.SntUsersDetail.as_view()),

	url(r'^api/v1/services$', views.SntServicesList.as_view()),
	url(r'^api/v1/services/user/(?P<usrID>[^/]+)/$', views.SntServicesPerUserList.as_view()),
    url(r'^api/v1/service/(?P<pk>[0-9]+)/$', views.SntServicesDetail.as_view()),
	url(r'^api/v1/service/new$', views.SntNewServiceConf.as_view()),
    #url(r'^api/v1/serviceconf$', views.SntServiceConfList.as_view()),

	url(r'^api/v1/functions$', views.SntFunctionsList.as_view()),
	url(r'^api/v1/function/(?P<pk>[0-9]+)/$', views.SntFunctionsDetail.as_view()),
	url(r'^api/v1/functions/service/(?P<srvID>[^/]+)/$', views.SntFunctionsPerServiceList.as_view()),

	url(r'^api/v1/metrics$', views.SntMetricsList.as_view()),
	url(r'^api/v1/metric/(?P<pk>[0-9]+)/$', views.SntMetricsDetail.as_view()),
	url(r'^api/v1/metrics/function/(?P<funcID>[^/]+)/$', views.SntMetricsPerFunctionList1.as_view()),

	url(r'^api/v1/alerts/rules$', views.SntRulesList.as_view()),
	url(r'^api/v1/alerts/rule/(?P<pk>[0-9]+)/$', views.SntRulesDetail.as_view()),

	url(r'^api/v1/notification/types$', views.SntNotifTypesList.as_view()),
	url(r'^api/v1/notification/type/(?P<pk>[0-9]+)/$', views.SntNotifTypesDetail.as_view()),

	url(r'^api/v1/prometheus/metrics/list$', views.SntPromMetricList.as_view()),
	url(r'^api/v1/prometheus/metrics/data$', views.SntPromMetricData.as_view()),

	url(r'^docs/', include('rest_framework_swagger.urls')),
	
]

urlpatterns = format_suffix_patterns(urlpatterns)



	
    #url(r'^api/test/$', views.TestList.as_view()),
    #url(r'^api/test/(?P<pk>[0-9]+)/$', views.TestDetail.as_view()),
    #url(r'^users/$', views.UserList.as_view()),
	#url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
	