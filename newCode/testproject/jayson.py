import collections
import datetime
# json = [
# 		{  	"reloading": "false", 
# 			"last_updated": 1510954225.828333, 
# 			"newest runahead cycle point string": "20150901T0000Z", 
# 			"status_string": "the marathon continues", 
# 			"newest cycle point string": "20150901T1200Z", 
# 			"states": ["runahead", "running", "succeeded", "succeeded"], 
# 			"daemon time zone info": {"hours": 0, "string_basic": "Z", "string_extended": "Z", "minutes": 0}, 
# 			"state totals": {"running": 1, "runahead": 1, "succeeded": 2}, 
# 			"namespace definition order": ["root", "foo", "bar"], 
# 			"oldest cycle point string": "20150831T1200Z", 
# 			"run_mode": "live"
# 		}, 

# 		{	"foo.20150901T1200Z": 
# 				{"started_time_string": "2017-11-17T21:30:25Z", 
# 				"execution_time_limit": "null", 
# 				"mean_elapsed_time": 0.3, 
# 				"description": "", 
# 				"submit_num": 1, 
# 				"host": "localhost", 
# 				"finished_time_string": "null", 
# 				"logfiles": [], 
# 				"job_hosts": {"1": "localhost"}, 
# 				"spawned": "False", 
# 				"finished_time": "null", 
# 				"name": "foo", 
# 				"title": "", 
# 				"started_time": 1510954225.0, 
# 				"latest_message": "started", 
# 				"batch_sys_name": "background", 
# 				"label": "20150901T1200Z", 
# 				"state": "running", 
# 				"submitted_time": "null", 
# 				"submitted_time_string": "null"}, 

# 			"foo.20150901T0000Z": 
# 				{"started_time_string": "2017-11-17T21:30:22Z", 
# 				"execution_time_limit": "null", 
# 				"mean_elapsed_time": 0.3, 
# 				"description": "", 
# 				"submit_num": 1, 
# 				"host": "localhost", 
# 				"submit_method_id": "73703", 
# 				"finished_time_string": "2017-11-17T21:30:22Z",
# 				 "logfiles": [], 
# 				"job_hosts": {"1": "localhost"}, 
# 				"spawned": "True", 
# 				"finished_time": 1510954222.0, 
# 				"name": "foo", 
# 				"title": "", 
# 				"started_time": 1510954222.0, 
# 				"latest_message": "submitted", 
# 				"batch_sys_name": "background", 
# 				"label": "20150901T0000Z", 
# 				"state": "succeeded", 
# 				"submitted_time": "null", 
# 				"submitted_time_string": "null"}, 

# 			"bar.20150831T1200Z": 
# 				{"started_time_string": "2017-11-17T21:30:24Z", 
# 				"execution_time_limit": "null", 
# 				"mean_elapsed_time": 0.2, 
# 				"description": "", 
# 				"submit_num": 1, 
# 				"host": "localhost", 
# 				"submit_method_id": "73769", 
# 				"finished_time_string": "2017-11-17T21:30:24Z", 
# 				"logfiles": [], 
# 				"job_hosts": {"1": "localhost"}, 
# 				"spawned": "True", 
# 				"finished_time": 1510954224.0, 
# 				"name": "bar", 
# 				"title": "", 
# 				"started_time": 1510954224.0, 
# 				"latest_message": "succeeded", 
# 				"batch_sys_name": "background", 
# 				"label": "20150831T1200Z", 
# 				"state": "succeeded", 
# 				"submitted_time": 1510954224.0, 
# 				"submitted_time_string": "2017-11-17T13:30:24-08"}, 

# 			"bar.20150901T0000Z": 
# 				{"started_time_string": "null", 
# 				"execution_time_limit": "null", 
# 				"mean_elapsed_time": 0.2, 
# 				"description": "", 
# 				"submit_num": 0, 
# 				"finished_time_string": "null", 
# 				"logfiles": [], 
# 				"job_hosts": {}, 
# 				"spawned": "False", 
# 				"finished_time": "null", 
# 				"name": "bar", 
# 				"title": "", 
# 				"started_time": "null", 
# 				"latest_message": "", 
# 				"label": "20150901T0000Z", 
# 				"state": "runahead", 
# 				"submitted_time": "null", 
# 				"submitted_time_string":"null"}
# 		},

# 		{
# 			"root.20150901T1200Z": 
# 				{"state": "running", 
# 				"label": "20150901T1200Z", 
# 				"title": "null", 
# 				"name": "root", 
# 				"description": "null"}, 

# 			"root.20150901T0000Z": 
# 				{"state": "succeeded", 
# 				"label": "20150901T0000Z",
# 			 	"title": "null", 
# 			 	"name": "root", 
# 				"description": "null"}, 

# 			"root.20150831T1200Z": 
# 				{"state": "succeeded", 
# 				"label": "20150831T1200Z", 
# 				"title": "null", 
# 				"name": "root", 
# 				"description": "null"}
# 		}]

# 

json = [  
   {  
      "reloading":"false",
      "last_updated":1511307521.907317,
      "newest runahead cycle point string":"null",
      "status_string":"running",
      "newest cycle point string":"20521020T1200Z",
      "states":[  
         "ready",
         "ready"
      ],
      "daemon time zone info":{  
         "hours":0,
         "string_basic":"Z",
         "string_extended":"Z",
         "minutes":0
      },
      "state totals":{  
         "ready":2
      },
      "namespace definition order":[  
         "root",
         "foo",
         "bar"
      ],
      "oldest cycle point string":"20521020T0000Z",
      "run_mode":"live"
   },
   {  
      "foo.20521020T1200Z":{  
         "started_time_string":"null",
         "execution_time_limit":"null",
         "mean_elapsed_time":0.3,
         "description":"",
         "submit_num":1,
         "host":"localhost",
         "finished_time_string":"null",
         "logfiles":[  

         ],
         "job_hosts":{  
            "1":"localhost"
         },
         "spawned":"False",
         "finished_time":"null",
         "name":"foo",
         "title":"",
         "started_time":"null",
         "latest_message":"",
         "batch_sys_name":"background",
         "label":"20521020T1200Z",
         "state":"ready",
         "submitted_time":"null",
         "submitted_time_string":"null"
      },
      "bar.20521020T0000Z":{  
         "started_time_string":"null",
         "execution_time_limit":"null",
         "mean_elapsed_time":0.3,
         "description":"",
         "submit_num":1,
         "host":"localhost",
         "finished_time_string":"null",
         "logfiles":[  

         ],
         "job_hosts":{  
            "1":"localhost"
         },
         "spawned":"False",
         "finished_time":"null",
         "name":"bar",
         "title":"",
         "started_time":"null",
         "latest_message":"",
         "batch_sys_name":"background",
         "label":"20521020T0000Z",
         "state":"ready",
         "submitted_time":"null",
         "submitted_time_string":"null"
      }
   },
   {  
      "root.20521020T0000Z":{  
         "state":"ready",
         "label":"20521020T0000Z",
         "title":"null",
         "name":"root",
         "description":"null"
      },
      "root.20521020T1200Z":{  
         "state":"ready",
         "label":"20521020T1200Z",
         "title":"null",
         "name":"root",
         "description":"null"
      }
   }
]

# data = json[2]
#foo = 'foo.20150901T1200Z'
state_list = json[0]['state totals']
other_list = json[1]

# print other_list.keys()
# name = other_list['name']

# print data

# for list in data:
#     for x in list:
#         print x

# for state, val in state_list.items():
	# print "%s: %d" % (state, val)

# for bliss in other_list.items():
#     # for x in list:
#     	# name = bliss
#         print bliss
# for bliss in other_list.items():
#     # for x in list:
#     	# name = bliss
#     	name = other_list['name']
#         print name


# global name_list
# # name_list = set()
# name_list = {}
# for x in  other_list:
	
# 	name_list = other_list[x]
# 	# print x
# 	info = "%s %s %s" % (name_list['label'], name_list['name'], name_list['state'])
# 	# print name_list['name']
# 	print info
# 	# for n in _name:
# 	# 	print n

summary = "state summary: "
update = "updated: "
update_totals = json[0]['last_updated']
value = datetime.datetime.fromtimestamp(update_totals)
updated_at = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
update += "\033[1;38m%s\033[0m" % updated_at
ns_defn_order = json[0]['namespace definition order']
count = 0
state_totals = json[0]['state totals']


for state, tot in state_totals.items():
	#print tot
	# print state
	subst = " %d " % tot
	# print subst
	# summary += get_status_prop(state, 'ascii_ctrl', subst)
	summary += subst



status1 = json[0]['status_string']
# len_header = sum(len(status1))
status2 = ''
suffix = '_'.join(list(status1.replace(' ', '_'))) + status2
divider_str = '_' * 104
divider_str = "\033[1;31m%s%s\033[0m" % (
divider_str[:-len(suffix)], suffix)

# print divider_str


print "---------------------------------------------------------"

task_info = {}
name_list = set()
task_ids = other_list.keys()
for task_id in task_ids:
	# print ("ID: " , task_id)
    name = other_list[task_id]['name']
    # print "NAME: " + name
    point_string = other_list[task_id]['label']
    # print "POINT: " + point_string
    count += 1
    state = other_list[task_id]['state']
    # print "STATE: " + state
    name_list.add(name)
    # print ("LIST: ", name_list)
    # print name
    # print point_string
    # print state
    if point_string not in task_info:
       	task_info[point_string] = {}
    task_info[point_string][name] = (state, "color" , name)
    # print task_info
# print count

# print "---------------------------------------------------------"

sorted_name_list = sorted(name_list)
# print sorted_name_list
# print 
# print point_string
sorted_task_info = {}
for point_str, info in task_info.items():
    sorted_task_info[point_str] = collections.OrderedDict()
    # print ("POINT: " , point_str)
    # print ("INFO: " , info)
    for name in sorted_name_list:
        if name in name_list:
            # (Defn order includes family names.).
            # print ("Name: " ,name)
            # print info.get(name)
            sorted_task_info[point_str][name] = info.get(name)
            # print sorted_task_info

print "---------------------------------------------------------"


print update
print summary
print divider_str
tracker = 0
blitlines = {}
for point_str, val in sorted_task_info.items():
	# print ("POINT: ", point_str)
	# print ("VAL: " , val) 
	indx = point_str
	# print ("INDEX: " ,val)
	line = "\033[1;34m%s\033[0m" % point_str
	# print line
	sline = ""
	for name, info in val.items():
		# print info
		# print ("NAME: " , name)
		# print("I_NFO: ", info)
		if info is not None:
			tracker += 1
			sline =  " %s" % info[2]
			# print sline
			# print "we out here"
	# print tracker
	# blitlines[indx] = line
	lineout = "%s: %s" %(line, sline )
	print lineout

print ""
print ""
print ""

	# indxs = blitlines.keys()
	# try:
	# 	int(indxs[1])
	# except:
	# 	indxs.sort()
	# else:
	# 	indxs.sort(key=int)
	# for ix in indxs:
	# 	print blitlines[ix]


# print name
# print name_list
	
# print state_list
