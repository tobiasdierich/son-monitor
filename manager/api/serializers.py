from rest_framework import serializers
from api.models import *
from api.serializers import *
from django.contrib.auth.models import User
from django.core import serializers as core_serializers

#######################################################################################################

class SntUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = monitoring_users
        fields = ('id', 'first_name', 'last_name', 'email', 'sonata_userid', 'created')


class SntServicesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_users.objects.all())
    #user = SntUserSerializer()
    class Meta:
        model = monitoring_services
        fields = ('id', 'sonata_srv_id', 'name', 'description', 'created', 'user', 'host_id','pop_id')

class SntServicesFullSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_users.objects.all())
    user = SntUserSerializer()
    class Meta:
        model = monitoring_services
        fields = ('id', 'sonata_srv_id', 'name', 'description', 'created', 'user', 'host_id','pop_id')

class SntFunctionsSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_services.objects.all())
    #service = SntServicesSerializer()
    class Meta:
        model = monitoring_functions
        fields = ('id', 'sonata_func_id', 'name', 'description', 'created', 'service', 'host_id','pop_id')

class SntFunctionsFullSerializer(serializers.ModelSerializer):
    #service = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_services.objects.all())
    service = SntServicesSerializer()
    class Meta:
        model = monitoring_functions
        fields = ('id', 'sonata_func_id', 'name', 'description', 'created', 'service', 'host_id', 'pop_id')

class SntMetricsSerializer(serializers.ModelSerializer):
    #function = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_functions.objects.all())
    #function = SntFunctionsSerializer()
    class Meta:
        model = monitoring_metrics
        fields = ('id', 'name', 'description', 'threshold', 'interval','cmd', 'function', 'created',)

class SntNewMetricsSerializer(serializers.ModelSerializer):
    #function = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_functions.objects.all())
    #function = SntFunctionsSerializer()
    class Meta:
        model = monitoring_metrics
        fields = ('name', 'description', 'threshold', 'interval','cmd', 'function', 'created')

class SntMetricsFullSerializer(serializers.ModelSerializer):
    #function = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_functions.objects.all())
    function = SntFunctionsSerializer()
    class Meta:
        model = monitoring_metrics
        fields = ('id', 'name', 'description', 'threshold', 'interval','cmd', 'function', 'created',)

class SntMetricsSerializer1(serializers.ModelSerializer):
    sonata_func_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_functions.objects.all())

    class Meta:
        model = monitoring_metrics
        fields = ('id', 'name', 'description', 'threshold', 'interval','cmd', 'sonata_func_id', 'created',)

class SntNotifTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = monitoring_notif_types
        fields = ('id', 'type',)

class SntRulesSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_services.objects.all())
    #function = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_functions.objects.all())
    notification_type = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_notif_types.objects.all())
    class Meta:
        model = monitoring_rules
        fields = ('id', 'name', 'duration', 'summary', 'description', 'condition', 'notification_type','service', 'created',)

class SntNewFunctionsSerializer(serializers.ModelSerializer):
    #service = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_services.objects.all())
    #service = SntServicesSerializer()
    metrics = SntNewMetricsSerializer(many=True)
    class Meta:
        model = monitoring_functions
        fields = ('sonata_func_id', 'name', 'description', 'created', 'host_id', 'pop_id', 'metrics')

class SntNewRulesSerializer(serializers.ModelSerializer):
    #service = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_services.objects.all())
    #function = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_functions.objects.all())
    #notification_type = serializers.PrimaryKeyRelatedField(read_only=False, queryset=monitoring_notif_types.objects.all())
    class Meta:
        model = monitoring_rules
        fields = ('name', 'duration', 'summary', 'description', 'condition', 'notification_type', 'created',)

class NewServiceSerializer(serializers.Serializer):
    service = SntServicesSerializer()
    functions = SntNewFunctionsSerializer(many=True)
    rules = SntNewRulesSerializer(many=True)

class promMetricLabelSerializer(serializers.Serializer):
    metric_name = ''

class promMetricsListSerializer(serializers.Serializer):
    metrics = promMetricLabelSerializer(many=True)

class promLabelsSerializer(serializers.Serializer):
    labels = {'label':'id'}

class SntPromMetricSerializer(serializers.Serializer):
    name = serializers.CharField()
    labels = promLabelsSerializer(many=True)


class wsLabelSerializer(serializers.Serializer):
    label = ''

class SntWSreqSerializer(serializers.Serializer):
    metric = serializers.CharField()
    filters = wsLabelSerializer(many=True)


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = SntRulesSerializer(many=True)
    created = serializers.DateTimeField()

######################################################################################
'''
class TestTBSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        
        #Create and return a new `Snippet` instance, given the validated data.
        

        return test_tb.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        #Update and return an existing `Snippet` instance, given the validated data.
        
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=test_tb.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'api', 'owner', 'snippets')
'''

'''
{
    "service": {
        "sonata_srv_id": "NS777777",
        "name": "service test1",
        "description": "service test description",
        "host_id": "",
        "pop_id": "",
        "sonata_usr_id": "123456"
    },
    "functions": [{
        "sonata_func_id": "NF112233",
        "name": "function test 1",
        "description": "function description",
        "pop_id": "111111",
        "host_id": "555555",
        "metrics": [{
            "name": "metric_1",
            "description": "metric test description",
            "threshold": 50,
            "interval": 10,
            "units": "kB",
            "cmd": "cmd1"
        }, {
            "name": "metric_2",
            "description": "metric test description",
            "threshold": 45,
            "interval": 35,
            "units": "kB",
            "cmd": "cmd2"
        }]
    }, {
        "sonata_func_id": "NF445566",
        "name": "function test 21",
        "description": "function description",
        "pop_id": "111111",
        "host_id": "88888",
        "metrics": [{
            "name": "metric3",
            "description": "metric test description",
            "threshold": 46,
            "interval": 23,
            "units": "kB",
            "cmd": "cmd3"
        }, {
            "name": "metric_4",
            "description": "metric test description",
            "threshold": 89,
            "interval": 34,
            "units": "kB",
            "cmd": "cmd4"
        }]
    }],
    "rules": [{
        "name": "Rule 4",
        "duration": "4m",
        "summary": "Rule",
        "description": "Rule ",
        "condition": "metric1-metric2> 0.25",
        "notification_type": 2
    }, {
        "name": "Rule 45",
        "duration": "4m",
        "summary": "Rule sweet rule... ",
        "description": "Rule sweet rule ....",
        "condition": "metric3-metric4> 0.25",
        "notification_type": 2
    }]
}
'''