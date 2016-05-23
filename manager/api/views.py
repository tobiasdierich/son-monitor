from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *
from api.serializers import *
from api.prometheus import *
#from api.serializers import UserSerializer
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from itertools import *
from django.forms.models import model_to_dict
import json
from drf_multiple_model.views import MultipleModelAPIView
from httpClient import Http


# Create your views here.


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'user': reverse('UserDetail', request=request, format=format),
        'tests': reverse('TestList', request=request, format=format),
        'test': reverse('TestDetail', request=request, format=format),
        'tests': reverse('UserList', request=request, format=format),
    })
########################################################################################

class SntUsersList(generics.ListCreateAPIView):
    queryset = monitoring_users.objects.all()
    serializer_class = SntUserSerializer

class SntUsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = monitoring_users.objects.all()
    serializer_class = SntUserSerializer

class SntServicesPerUserList(generics.ListAPIView):
    #queryset = monitoring_services.objects.all().filter(self.kwargs['usrID'])
    serializer_class = SntServicesFullSerializer

    def get_queryset(self):
        queryset = monitoring_services.objects.all()
        userid  = self.kwargs['usrID']
        return queryset.filter(user=userid)

class SntServicesList(generics.ListCreateAPIView):
    queryset = monitoring_services.objects.all()
    serializer_class = SntServicesSerializer

class SntFunctionsPerServiceList(generics.ListAPIView):
    #queryset = monitoring_functions.objects.all()
    serializer_class = SntFunctionsFullSerializer

    def get_queryset(self):
        queryset = monitoring_functions.objects.all()
        srvid  = self.kwargs['srvID']
        return queryset.filter(service__sonata_srv_id=srvid)

class SntServicesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = monitoring_services.objects.all()
    serializer_class = SntServicesSerializer

class SntFunctionsList(generics.ListCreateAPIView):
    queryset = monitoring_functions.objects.all()
    serializer_class = SntFunctionsSerializer

class SntFunctionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = monitoring_functions.objects.all()
    serializer_class = SntFunctionsSerializer

class SntNotifTypesList(generics.ListCreateAPIView):
    queryset = monitoring_notif_types.objects.all()
    serializer_class = SntNotifTypeSerializer

class SntNotifTypesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = monitoring_notif_types.objects.all()
    serializer_class = SntNotifTypeSerializer

class SntMetricsList(generics.ListCreateAPIView):
    queryset = monitoring_metrics.objects.all()
    serializer_class = SntMetricsSerializer

class SntMetricsPerFunctionList(generics.ListAPIView):
    #queryset = monitoring_metrics.objects.all()
    serializer_class = SntMetricsFullSerializer

    def get_queryset(self):
        queryset = monitoring_metrics.objects.all()
        functionid  = self.kwargs['funcID']
        result_list = list(chain(monitoring_services.objects.all(), monitoring_functions.objects.all(), monitoring_metrics.objects.all()))
        return queryset.filter(function__sonata_func_id=functionid)

class SntMetricsPerFunctionList1(generics.ListAPIView):
    #queryset = monitoring_metrics.objects.all()
    def list(self, request, *args, **kwargs):
        functionid  = kwargs['funcID']
        queryset = monitoring_metrics.objects.all().filter(function_id=functionid)
        dictionaries = [ obj.as_dict() for obj in queryset ]
        response = {}
        response['data_server_url']='http://sp.int2.sonata-nfv.eu:9091'
        response['metrics'] = dictionaries
        return Response(response)

class SntNewServiceConf(generics.CreateAPIView):
    serializer_class = NewServiceSerializer
    def post(self, request, *args, **kwargs):
        service = request.data['service']
        functions = request.data['functions']
        rules = request.data['rules']
        
        if not service['sonata_usr_id']:
            u = monitoring_users.objects.all().filter(sonata_userid='system')  
        else:
            u = monitoring_users.objects.all().filter(sonata_userid=service['sonata_usr_id'])             
        
        if u.count() == 0:
            #add new user
            usr = monitoring_users(sonata_userid=service['sonata_usr_id'])
            usr.save()
        else:
            usr = u[0]
        s = monitoring_services.objects.all().filter(sonata_srv_id=service['sonata_srv_id'])
        if s.count() > 0:
            s.delete()
    
    srv_pop_id = ''
        srv_host_id = ''
        if service['pop_id']: 
            srv_pop_id = service['pop_id']
        if service['host_id']: 
            srv_host_id = service['host_id']
        srv = monitoring_services(sonata_srv_id=service['sonata_srv_id'], name=service['name'], description=service['description'], host_id=srv_host_id, user=usr, pop_id=srv_pop_id)
        srv.save()
        for f in functions:
            print f['pop_id']
            func = monitoring_functions(service=srv ,host_id=f['host_id'] ,name=f['name'] , sonata_func_id=f['sonata_func_id'] , description=f['description'], pop_id=f['pop_id'])
            func.save()
            for m in f['metrics']:
                metric = monitoring_metrics(function=func ,name=m['name'] ,cmd=m['cmd'] ,threshold=m['threshold'] ,interval=m['interval'] ,description=m['description'])
                metric.save()
        
        rls = {}
        rls['service'] = service['sonata_srv_id']
        rls['vnf'] = "To be found..."
        rls['rules'] = []  
        for r in rules:
            #print json.dumps(r)
            nt = monitoring_notif_types.objects.all().filter(id=r['notification_type'])
            if nt.count() == 0:
                return Response({'error':'Alert notification type does not supported. Action Aborted'}, status=status.HTTP_400_BAD_REQUEST)
                srv.delete()
            else:
                rule = monitoring_rules(service=srv, summary=r['summary'] ,notification_type=nt[0], name=r['name'] ,condition=r['condition'] ,duration=r['duration'] ,description=r['description'] )
                rule.save()
                rl = {}
                rl['name'] = r['name']
        rl['description'] = r['description']
                rl['summary'] = r['summary']
                rl['duration'] = r['duration']
                rl['notification_type'] = r['notification_type']
                rl['condition'] = r['condition']
                rl['labels'] = ["serviceID=\""+rls['service']+"\""]
        rls['rules'].append(rl)

        if len(rules) > 0:
            cl = Http()
        rsp = cl.POST('http://prometheus:9089/prometheus/rules',[],json.dumps(rls))            
            if rsp == 200:
                return Response({'status':"success"})
            else:
                srv.delete()
                return Response({'error': 'Service update fail '+str(rsp)})

    def getVnfId(funct_,host_):
        for fn in funct_:
            if fn['host_id'] == host_:
                return fn['sonata_func_id']
            else:
                return 'Undefined'

class SntMetricsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = monitoring_metrics.objects.all()
    serializer_class = SntMetricsSerializer

class SntRulesList(generics.ListCreateAPIView):
    queryset = monitoring_rules.objects.all()
    serializer_class = SntRulesSerializer

class SntRulesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = monitoring_rules.objects.all()
    serializer_class = SntRulesSerializer

class SntPromMetricList(generics.RetrieveAPIView):
    serializer_class = promMetricsListSerializer
    def get(self, request, *args, **kwargs):
        mt = ProData('prometheus',9090)
        data = mt.getMetrics()
        response = {}
        response['metrics'] = data['data']
        print response
        return Response(response)

class SntPromMetricData(generics.CreateAPIView):
    serializer_class = SntPromMetricSerializer
    '''
    {
    "name": "up",
    "start": "2016-02-28T20:10:30.786Z",
    "end": "2016-03-03T20:11:00.781Z",
    "step": "1h",
    "labels": [{"labeltag":"instance", "labelid":"192.168.1.39:9090"},{"labeltag":"group", "labelid":"development"}]
    }
    '''
    def post(self, request, *args, **kwargs):
        mt = ProData('prometheus',9090)
        data = mt.getTimeRangeData(request.data)
        response = {}
        #print data
        try:
            response['metrics'] = data['data']
        except KeyError:
            response = data
        return Response(response)

 
