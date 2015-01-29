 #! /usr/bin/env python
import subprocess, os, sys, string
from lxml import etree

def publish_to_ganglia(name, value, type, units):
    gmetric_path = '/usr/bin/gmetric'
#    gmetric_path = 'gmetric'

    gmetric_sys_call = gmetric_path

    if (name != '' and type != ''):

        name = string.replace(name, '/', '_')
        print '------------------------------------------'
        print 'name: ' + name
        print  'value: ' +  value
        print 'type: ' + type
        print 'units: ' + units
        output = subprocess.Popen([gmetric_path, '-n', name, '-v', value, '-t', type, '-u', units], stdout=subprocess.PIPE).communicate()[0]
#        print 'output from gmetric :' +  output


def roxie_handler_from_file(name):
  try:
    metrics_file = open('/tmp/.roxie_metrics', 'r')
    output = metrics_file.read()  
    metrics_file.close()

#    print output
    xp = etree.fromstring(output)
    metrics = []

    for child in xp[0][0]:
#      print "name: " + child.attrib.get('name')
#      print "value: " + child.attrib.get('value')
      metrics.append((string.replace(child.attrib.get('name'),'\/', '_'), child.attrib.get('value')))
      if string.replace(child.attrib.get('name'), '/', '_') == string.replace(name, '/', '_'):
        print "name: " + child.attrib.get('name')
        print "value: " + child.attrib.get('value')
        return child.attrib.get('value')
  except IOError:
    print "IOError"
    metrics_file.close()

def roxie_handler(name):
  conf_file = '/etc/HPCCSystems/environment.conf'

  for line in open(conf_file, 'r').readlines():
    if ('path=' in line):
      bin_path = line[5:]
      break
  test_socket_path = bin_path.strip() + '/bin/testsocket'

  output = subprocess.Popen([test_socket_path, '.', '<control:metrics/>'], stdout=subprocess.PIPE).communicate()[0]
#  print output
  xp = etree.fromstring(output)
  metrics = []

  for child in xp[0][0]:
    metrics.append((string.replace(child.attrib.get('name'),'\/', '_'), child.attrib.get('value')))
    if string.replace(child.attrib.get('name'), '/', '_') == string.replace(name, '/', '_'):
      return child.attrib.get('value')




def roxie_handler2(name, index):
  conf_file = '/etc/HPCCSystems/environment.conf'

  for line in open(conf_file, 'r').readlines():
    if ('path=' in line):
      bin_path = line[5:]
      break
  test_socket_path = bin_path.strip() + '/bin/testsocket'

  output = subprocess.Popen([test_socket_path, '.', '<control:metrics/>'], stdout=subprocess.PIPE).communicate()[0]
#  print output
  xp = etree.fromstring(output)
  metrics = []

  for child in xp[0][0]:
    metrics.append((string.replace(child.attrib.get('name'),'\/', '_'), child.attrib.get('value')))
    if string.replace(child.attrib.get('name'), '/', '_') == string.replace(name, '/', '_'):
#      return child.attrib.get('value')
       name_param = string.replace(child.attrib.get('name'), '\/', '_')
#       print name_param
       value_param = child.attrib.get('value')
#       print value_param
#      type_param = child.attrib.get('value_type')
       type_param = descriptors[index]['value_type']
       units_param = descriptors[index]['units']
       if (type_param is None):
           print '*OVERRIDING*'
           type_param = 'string'
#       print 'type_param = ' + type_param
#       print 'units_param = ' + units_param
       publish_to_ganglia(name_param, value_param, type_param, units_param)
 #   index += 1

def metric_cleanup():
  '''cleaned up'''
  pass

def metric_init(params):
  global descriptors
  descriptors = []

  descriptors.append(
     {'name' : 'resultsReceived',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'results recv',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Total Results Received',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'ibytiPacketsFromSelf_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'packets / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'IBYTI Packets From Self / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'restarts',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'restarts',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Total Restarts',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'nodeCacheHits_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'hits / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Node Cache Hits / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'ibytiPacketsSent_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'packets / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'IBYTI Packets Sent / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'maxScanLength',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'length',
     'value_type': 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Max Scan Length',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'ibytiPacketsWorked_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'worked / sec',
       'value_type': 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'IBYTI Packets Worked / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'hiMax_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'high max / sec',
       'value_type': 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'High Max / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'retriesIgnoredPrm',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'retries ignored',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Retries Ignored Prm',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'retriesReceivedSec',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'retries recv',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Retries Received Sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'loQueryActive_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'queries active',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Low Query Active / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
    { 'name' : 'retriesReceivedPrm_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'retries recv / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Retries Received Prm / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'nodeCacheHits',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'hits',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Node Cache Hits',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'queryCount_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'query count / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Query Count / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'loQueryActive',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'active queries',
       'value_type': 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Low Query Active',
      'groups' : 'roxie' }
  ) 
 
  descriptors.append(
     {'name' : 'cacheAdds_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'cache adds / sec',
       'value_type': 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Cache Adds / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'unknownMin_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'unknown / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Unknown Min / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'packetsAbandoned',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'packets abandoned',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Packets Abandoned',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'nodeCacheAdds',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'cache adds',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Node Cache Adds',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'loAverage',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'low average',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Low Average',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'slaQueryFailed_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'queries / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Slave Query Failed / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'preloadCacheHits',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'cache hits',
      'value_type' : 'uint',
      'slope:' : 'postive',
      'format' : '%u',
      'description' : 'Preload Cache Hits',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'loMin',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'low min',
      'value_type' : 'uint',
      'slope:' : 'postive',
      'format' : '%u',
      'description' : 'Low Min',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'activitiesStarted',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'activities started',
      'value_type' : 'uint',
      'slope:' : 'postive',
      'format' : '%u',
      'description' : 'Activties Started',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'diskReadStarted',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'starts',
      'value_type' : 'uint',
      'slope:' : 'postive',
      'format' : '%u',
      'description' : 'Disk Read Started',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'globalLocks',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'locks',
      'value_type' : 'uint',
      'slope:' : 'postive',
      'format' : '%u',
      'description' : 'Global Locks',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'retriesNeeded',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'retries',
      'value_type' : 'uint',
      'slope:' : 'postive',
      'format' : '%u',
      'description' : 'Retries Needed',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'ibytiPacketsSent',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'packets sent',
      'value_type' : 'uint',
      'slope:' : 'postive',
      'format' : '%u',
      'description' : 'IBYTI Packets Sent',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'loMax',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'low max',
      'value_type' : 'uint',
      'slope:' : 'postive',
      'format' : '%u',
      'description' : 'Low Max',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'hiQueryActive_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'hi queries / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'High Query Active / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'hiQueryActive',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'hi active queries',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'High Query Active',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'unknownQueryFailed',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'queries',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Unknown Query Failed',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'loQueryCount',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'low query count',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Low Query Count',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'ibytiNoDelaysSec',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'no delays / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'IBYTI No Delays Sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'loQueryCount_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'query count / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Low Query Count / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'unknownMin',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'min unknown',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Unknown Min',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'packetsReceived',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'packets recv',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Packets Received',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'unwantedDiscarded_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'discarded / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Unwanted Discarded / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'hiQueryFailed',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'hi failed queries',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'High Query Failed',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'rowsIn',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'rows in',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Rows In',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'unknownQueryActive',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'active queries',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Unknown Query Active',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'unknownMax_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'max unknown / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Unknown Max / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'retriesSent_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'retries sent / sec',
       'value_type': 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Retries Sent / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'ibytiNoDelaysPrm',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'no delays',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'IBYTI No Delays Prm',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'slaQueryActive_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'active queries / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Slave Queries Active / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'packetsAbandoned_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'pkts / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Packets Abandoned / sec ',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'slaMin_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'slaves min / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Slave Min / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'totScanLength',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'length',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Total Scan Length',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'ibytiPacketsHalfWorked_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'packets / sec',
       'value_type': 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'IBYTI Packs Half Worked / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'slaMax',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'slave max',
       'value_type': 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Slave Max',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'packetsReceived_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'packets / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Packets Received / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'cacheHits',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'cache hits',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Cache Hits',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'hiQueryFailed_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'queries / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'High Query Failed / sec',
      'groups' : 'roxie' }
  ) 

  descriptors.append(
     {'name' : 'rowsIn_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'rows in / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'Rows In / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'ibytiPacketsFromSelf',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'packets',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'IBYTI Packets From Self',
      'groups' : 'roxie' }
  )

  descriptors.append(
     {'name' : 'slaQueryCount_s',
      'call_back' : roxie_handler_from_file,
      'time_max' : 90,
      'units' : 'query count / sec',
      'value_type' : 'uint',
      'slope:' : 'both',
      'format' : '%u',
      'description' : 'slaQueryCount / sec',
      'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'leafCacheHits',
     'call_back' : roxie_handler_from_file,
     'time_max' : 90,
     'units' : 'cache hits',
      'value_type': 'uint',
     'slope:' : 'both',
     'format' : '%u',
     'description' : 'Leaf Cache Hits',
     'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'nodeCacheAdds_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'cache adds / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Node Cache Adds / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'leafCacheAdds_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'cache adds / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Leaf Cache Adds / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'unknownQueryCount_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'query count / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Unknown Query Count / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'cacheAdds',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'cache adds',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Cache Adds',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'packetsRetried_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets retried / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Packets Retried / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'hiMax',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'hi max',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'High Max',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'hiMin',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'hi min',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Hi Min',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'postFiltered_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'posts / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Post Filtered /  sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'unknownQueryFailed_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'queries / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Unknown Query Failed / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'ibytiNoDelaysSec_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'no delays sec / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'IBYTI No Delays Sec / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'maxQueueLength',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'queue length',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Max Queue Length',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'leafCacheAdds',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'adds',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Lead Cache Adds',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'packetsRetried',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'retries',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Packets Retried',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'slavesActive',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'slaves active',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Slaves Active',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'hiMin_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'hi min / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Hi Min / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'hiAverage',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'hi avg',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Hi Average',
    'groups' : 'roxie' }
  )

#  descriptors.append(
#    {'name' : 'lastQueryTime',
#    'call_back' : roxie_handler_from_file,
#    'time_max' : 90,
#    'units' : 'query time',
#       'value_type': 'uint',
#    'slope:' : 'both',
#    'format' : '%u',
#    'description' : 'Last Query Time',
#    'groups' : 'roxie' }
#  )

  descriptors.append(
    {'name' : 'packetsSent',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Packets Sent',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'dataBufferPages',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'pages',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Data Buffer Pages',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'loMin_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'min / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Low Min / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'slaQueryFailed',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'queries',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Slave Query Failed',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'unknownAverage',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'avg',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Unknown Average',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'resultsReceived_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'recv / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Results Received / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'unknownQueryCount',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'query count',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Unknown Query Count',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'nodesLoaded',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'nodes',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Nodes Loaded',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'preloadCacheAdds',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'adds',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Preload Cache Adds',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'meanScanLength',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'legnth',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Mean Scan Length',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'unknownQueryActive_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'queries / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Unknown Active Queries / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'retriesSent',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'retries sent',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Retries Sent',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'hiQueryCount_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'query count / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'High Query Count / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'activitiesCompleted',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'activities completed',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Activities Completed',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'diskReadCompleted',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'disk reads completed',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Disk Read Completed',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'dataBuffersActive',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'buffers active',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Data Buffers Active',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'ibytiNoDelaysPrm_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'no delays prm / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'IBYTI No Delays Prm / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'ibytiPacketsReceived',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets recv',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'IBYTI Packets Received',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'leafCacheHits_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'cache hits / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Leaf Cache Hits / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'slaAverage',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'slave avg',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Slave Average',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'retriesReceivedPrm',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'retries recv',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Retries Received Prm',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'unwantedDiscarded',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'discarded',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Unwanted Discarded',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'slaMin',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'slaves',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Slave Min',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'retriesIgnoredSec_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'retries',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Retries Ignored Sec / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'retriesReceivedSec_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'recv / s',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Retries Received Sec / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'loQueryFailed_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'queries / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Low Query Failed / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'maxSlavesActive',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'slaves active',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Max Slaves Active',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'numFilesToProcess',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'files',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Number of Files To Process',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'rowsOut_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'rows',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Rows Out / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'postFiltered',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'posts',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'POST filtered',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'retriesNeeded_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'needed / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Retries Need / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'slaMax_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'slaves',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Slave Max / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'ibytiPacketsTooLate',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'IBYTI Packets Too Late',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'cacheHits_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'hits / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Cache Hits / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'totScans',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'scans',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Total Scans',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'slaQueryActive',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'queries active',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Slave Queries Active',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'ibytiPacketsReceived_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets recv',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'IBYTI Packets Received / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'indexRecordsRead',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'reads',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Index Records Read',
    'groups' : 'roxie' }
  )
 
  descriptors.append(
    {'name' : 'rowsOut',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'rows',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Rows Out',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'ibytiPacketsWorked',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets worked',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'IBYTI Packets Worked',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'queryCount',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'query count',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Query Count',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'ibytiPacketsTooLate_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'IBYTI Packets Too Late / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'ibytiPacketsHalfWorked',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'IBYTI Packets Half Worked',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'retriesIgnoredPrm_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'retries',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Retries Ignored Prm / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'hiQueryCount',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'query count',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'High Query Count',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'packetsSent_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'packets / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Packets Sent / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'globalSignals',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'signals',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Global Signals',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'unknownMax',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'unknown',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Unknown Max',
    'groups' : 'roxie' }
  )

  descriptors.append(
    {'name' : 'slaQueryCount',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'query count',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Slave Query Count',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'indexRecordsRead_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'reads / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Index Records Read / sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'loMax_s',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'low max / sec',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Low Max / sec',
    'groups' : 'roxie' }
  )

#  descriptors.append(
#    {'name' : 'lastQueryDate',
#    'call_back' : roxie_handler_from_file,
#    'time_max' : 90,
#    'units' : 'date',
#     'value_type' : 'uint',
#    'slope:' : 'both',
#    'format' : '%u',
#    'description' : 'Last Query Date',
#    'groups' : 'roxie' }
#  )

  descriptors.append(
   {'name' : 'retriesIgnoredSec',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'retries',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Retries Ignored Sec',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'abortsSent',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'aborts',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Aborts Sent',
    'groups' : 'roxie' }
  )

  descriptors.append(
   {'name' : 'loQueryFailed',
    'call_back' : roxie_handler_from_file,
    'time_max' : 90,
    'units' : 'queries',
     'value_type' : 'uint',
    'slope:' : 'both',
    'format' : '%u',
    'description' : 'Low Query Failed',
    'groups' : 'roxie' }
  )

  return descriptors

if __name__ == '__main__':
    params = {
        "device": "eth0",
        "host"  : "localhost",
        "debug" : True,
        }
    metric_init(params)

    counter = 0
    for d in descriptors:
#        v = d['call_back'](d['name'], counter)
#        roxie_handler2(d['name'], counter)
        roxie_handler_from_file(d['name'])
        counter += 1




