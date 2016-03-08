import json, httplib, time





def getMetrics(srv_addr_, srv_port_):
	# curl 'http://83.235.169.221:8080/api/v1/label/__name__/values?_=1456903913'
    # curl 'http://83.235.169.221:8080/api/v1/query_rprometheus_data_size&start=2016-02-01T20:10:30.786Z&end=2016-02-28T20:11:00.781Z&step=1h'
	print 'getMetrics'
	now = int(time.time())
	path = "".join(("/api/v1/label/__name__/values?_=", str(now)))
	d = HttpGet(srv_addr_,srv_port_,path)
	return d


def getTimeRangeData(srv_addr, srv_port,req):
	path = "".join(("/api/v1/query_range?query=",req['metric'],"&start=",req['start'],"&end=",req['end'],"&step=",req['step'] ))
	print path
	d = HttpGet(srv_addr,srv_port,path)
	print d

def HttpGet(srv_addr,srv_port,path):
	print "lalakis"
	httpServ = httplib.HTTPConnection(srv_addr, srv_port)
   	httpServ.connect()
   	httpServ.request("GET", path)
   	response = httpServ.getresponse()
   	data = json.loads(response.read())
   	httpServ.close()
   	return data


if __name__ == "__main__":
    print getMetrics("192.168.1.70", 9090)
    rq = {'metric':'prometheus_data_size','labels':[{'instanseID':'jdhfksdhfk'}],'start':'2016-02-01T20:10:30.786Z', 'end':'2016-02-28T20:11:00.781Z', 'step':'1h'}
    print getTimeRangeData("192.168.1.70", 9090, rq)
