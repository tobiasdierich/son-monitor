from __future__ import unicode_literals

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from datetime import datetime

# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())



class monitoring_users(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    sonata_userid = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
		db_table = "monitoring_users"
		ordering = ('created',)
		managed = True

    def __unicode__(self):
        return u'%s %s %s' % (self.first_name, self.last_name, self.sonata_userid)

class monitoring_services(models.Model):
    user = models.ForeignKey(monitoring_users)
    host_id = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    sonata_srv_id = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
		db_table = "monitoring_services"
		ordering = ('created',)
		managed = True

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.description, self.sonata_srv_id)


class monitoring_functions(models.Model):
    service = models.ForeignKey(monitoring_services)
    host_id = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    sonata_func_id = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "monitoring_functions"
        ordering = ('created',)
        managed = True

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.description, self.sonata_func_id)

class monitoring_metrics(models.Model):
    function = models.ForeignKey(monitoring_functions)
    name = models.CharField(max_length=30, blank=True)
    cmd = models.CharField(max_length=1024, blank=False)
    threshold = models.DecimalField(max_digits=6, decimal_places=2)
    interval = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)

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
    name = models.CharField(max_length=30, blank=True)
    condition = models.CharField(max_length=1024, blank=False)
    duration = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)

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
#####################################################################################
'''
class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='leila@example.com', content='foo bar')

class test_tb(models.Model):
    owner = models.ForeignKey('auth.User', related_name='api')
    highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    def save(self, *args, **kwargs):
    	"""
    	Use the `pygments` library to create a highlighted HTML
    	representation of the code snippet.
    	"""
    	lexer = get_lexer_by_name(self.language)
    	linenos = self.linenos and 'table' or False
    	options = self.title and {'title': self.title} or {}
    	formatter = HtmlFormatter(style=self.style, linenos=linenos,full=True, **options)
    	self.highlighted = highlight(self.code, lexer, formatter)
    	super(test_tb, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)
'''