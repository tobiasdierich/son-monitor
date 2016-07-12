'''
Copyright (c) 2015 SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote 
products derived from this software without specific prior written 
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through 
the Horizon 2020 and 5G-PPP programmes. The authors would like to 
acknowledge the contributions of their colleagues of the SONATA 
partner consortium (www.sonata-nfv.eu).
'''

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
	