#! /usr/bin/env python
"""Sample use of the ncclient library for NETCONF

This script will retrieve information from a device.


"""

# Import libraries
from ncclient import manager
from xml.dom import minidom
import xmltodict
import sys

# Add parent directory to path to allow importing common varsss
# check if conflict happened
sys.path.append("..") # noqa
# from device_info import ios_xe1 as device # noqa
#from device_info import ios_xe1 as device # noqa
from mydevice_info import MakatiSW as device


# Create filter template for an interface
interface_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>{int_name}</name>
    </interface>
  </interfaces>
</filter>
"""

#Create filter template for BGP 
bgp_filter = """
 <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <router>
          <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
            <id>{int_id}</id>
          </bgp>
        </router>
      </native>
    </filter>
"""



# Open NETCONF connection to device
with manager.connect(host = device["address"],
                     port = device["netconf_port"],
                     username = device["username"],
                     password = device["password"],
                     hostkey_verify = False) as m:

    # Create desired NETCONF filter and <get-config>
    filter = bgp_filter.format(int_id = "100")
    r = m.get_config("running", filter)

    # Pretty print raw xml to screen
    xml_doc = minidom.parseString(r.xml)

    
    print(xml_doc.toprettyxml(indent = "  "))

    # Process the XML data into Python Dictionary and use
    bgp = xmltodict.parse(r.xml)
    
    ##json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式
    #jsonstr = json.dumps(interface,indent=1)

    #print json data
    #print(jsonstr)



    # Only if RPC returned datas
    if not bgp["rpc-reply"]["data"] is None:
        bgp = bgp["rpc-reply"]["data"]["native"]["router"]["bgp"]

        print("The bgp's local id is {id} remote id is {remote_id} remote as is {remote_as}".format(
                id = bgp["bgp"]["router-id"]["ip-id"],
                remote_as = bgp["neighbor"]["id"],
                remote_id = bgp["neighbor"]["remote-as"]
                )
            )
    else:
        print("No bgp {} config  found".format("As 100"))

