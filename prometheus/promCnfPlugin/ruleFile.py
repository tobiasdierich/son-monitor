import json, yaml, httplib, subprocess, time

class fileBuilder(object):

    def __init__(self, serviceID, rules, path):
        self.serviceID = serviceID
        self.rules = rules
        self.prometheusPth = path

    def relaodConf(self):
        print 'reload....'

     def buildRule(self, rule):
        labels =''
        rule['name'] = rule['name'].replace(':','_')
        for lb in rule['labels']:
            labels += lb +', '        
        rule = 'ALERT ' + rule['name'].replace (" ", "_") +'\n'+'  IF ' + self.conditionRule(rule['condition']) + '\n'+'  FOR ' + rule['duration'] + '\n'+' LABELS {'+labels[:-2]+'}'+'\n'+'  ANNOTATIONS { '+'\n'+'    summary = "'+rule['summary']+' {{$labels.instance}}",'+'\n'+'    description = "'+rule['description']+' {{ $labels.instance }} of job {{ $labels.job }}",'+'\n'+'}'+'\n'
        return rule

    def conditionRule(self, rule):
        els = rule.split(" ")
        index = 0
        for el in els:
            if ':' in el:
                ep = el.split(':')
                els[index] = " "+ep[1]+'{id=\"'+ep[0]+'\"} '
            index +=1
        return ''.join(str(x) for x in els)

    def writeFile(self):
        body = ''
        for r in self.rules:
            body += self.buildRule(r)
        filename = "".join((self.prometheusPth,'rules/',self.serviceID, '.rules'))

        with open(filename, 'w') as outfile:
            outfile.write(body)
        #    json.dump(body, outfile)

        if self.validate(filename) == 0:
            #print "RuleFile created SUCCESSFULY"
            #add file to conf file
            with open(self.prometheusPth+'prometheus.yml', 'r') as conf_file:
                conf = yaml.load(conf_file)
                for rf in conf['rule_files']:
                    if filename in rf:
                        self.reloadServer()
                        return "RuleFile updated SUCCESSFULY - SERVER Reloaded"
                conf['rule_files'].append(filename)
                print conf['rule_files']
                with open(self.prometheusPth+'prometheus.yml', 'w') as yml:
                    yaml.safe_dump(conf, yml)
                self.reloadServer()
            return "RuleFile created SUCCESSFULY - SERVER Reloaded"
        else:
            return "RuleFile creation FAILED"
        
    def validate(self,file):
        checktool = '.'+self.prometheusPth+'promtool'
        p = subprocess.Popen([checktool, 'check-rules', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, status = p.communicate()
        print status
        rc = p.returncode
        if rc == 0:
            if 'SUCCESS' in status:
                return 0
            else:
                return 10
        else:
            return rc


    def reloadServer(self):
        httpServ = httplib.HTTPConnection("localhost", 9090)
        httpServ.connect()
        httpServ.request("POST", "/-/reload")
        response = httpServ.getresponse()
        #print response.status
        httpServ.close()

