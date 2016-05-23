from __future__ import unicode_literals

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from datetime import datetime
from django.utils import timezone

# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())



class monitoring_users(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    sonata_userid = models.CharField(max_length=60)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "monitoring_users"
        ordering = ('created',)
        managed = True

    def __unicode__(self):
        return u'%s %s %s' % (self.first_name, self.last_name, self.sonata_userid)

class monitoring_services(models.Model):
    user = models.ForeignKey(monitoring_users)
    pop_id = models.CharField(max_length=60, blank=True)
    host_id = models.CharField(max_length=60, blank=True)
    name = models.CharField(max_length=30, blank=True)
    sonata_srv_id = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=1024)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "monitoring_services"
        ordering = ('created',)
        managed = True

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.description, self.sonata_srv_id)


class monitoring_functions(models.Model):
    service = models.ForeignKey(monitoring_services)
    pop_id = models.CharField(max_length=60, blank=True)
    host_id = models.CharField(max_length=60, blank=True)
    name = models.CharField(max_length=30, blank=True)
    sonata_func_id = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=1024)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "monitoring_functions"
        ordering = ('created',)
        managed = True

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.description, self.sonata_func_id)

class monitoring_metrics(models.Model):
    function = models.ForeignKey(monitoring_functions)
    name = models.CharField(max_length=30, blank=True)
    cmd = models.CharField(max_length=1024, null=True)
    threshold = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    interval = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    description = models.CharField(max_length=1024, null=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "monitoring_metrics"
        ordering = ('created',)
        managed = True

    def as_dict(self):
        return {
            #'function': self.function['id'],
            'name': self.name,
            'cmd': self.cmd,
            'threshold':self.threshold,
            'interval':self.interval,
            'description':self.description,
            'created':self.created
            # other stuff
        }  

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.description, self.cmd)

class monitoring_notif_types(models.Model):
    type = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = "monitoring_notif_types"
        managed = True

    def __unicode__(self):
        return u'%s %s' % (self.id, self.type)

class monitoring_rules(models.Model):
    service = models.ForeignKey(monitoring_services)
    #function = models.ForeignKey(monitoring_functions, blank=True)
    summary = models.CharField(max_length=1024, blank=True)
    notification_type = models.ForeignKey(monitoring_notif_types)
    name = models.CharField(max_length=60, blank=True)
    condition = models.CharField(max_length=2048, blank=False)
    duration = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=2048)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "monitoring_rules"
        ordering = ('created',)
        managed = True

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.description, self.cmd)

class prom_metric(object):
    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return u'%s' % (self.name)

#rq = {'metric':'prometheus_data_size','labels':[{'instanseID':'jdhfksdhfk'}],'start':'2016-02-01T20:10:30.786Z', 'end':'2016-02-28T20:11:00.781Z', 'step':'1h'}


class ServiceConf(object):
    def __init__(self, service, functions, metrics, rules, created=None):
        self.service = service
        self.functions = functions
        self.metrics = metrics
        self.rules = rules
