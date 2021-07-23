#! /usr/bin/env python
"""Sample use of the ncclient library for NETCONF

This script will retrieve information from a device.


"""

# Import libraries
from ncclient import manager
from xml.dom import minidom
import xmltodict
import sys
import json

# Add parent directory to path to allow importing common varsss
# check if conflict happened
sys.path.append("..") # noqa
# from device_info import ios_xe1 as device # noqa
#from device_info import ios_xe1 as device # noqa
from mydevice_info import ios_xe1 as device


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

# Open NETCONF connection to device
with manager.connect(host = device["address"],
                     port = device["netconf_port"],
                     username = device["username"],
                     password = device["password"],
                     hostkey_verify = False) as m:

    # Create desired NETCONF filter and <get-config>
    filter = interface_filter.format(int_name = "TwoGigabitEthernet1/0/10")
    r = m.get_config("running", filter)

    # Pretty print raw xml to screen
    xml_doc = minidom.parseString(r.xml)

    
    print(xml_doc.toprettyxml(indent = "  "))

    # Process the XML data into Python Dictionary and use
    interface = xmltodict.parse(r.xml)
    
    ##json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式
    #jsonstr = json.dumps(interface,indent=1)

    #print json data
    #print(jsonstr)



    # Only if RPC returned data
    if not interface["rpc-reply"]["data"] is None:
        interface = interface["rpc-reply"]["data"]["interfaces"]["interface"]

        print("The interface {name} has ip address {ip}/{mask}".format(
                name = interface["name"]["#text"],
                ip = interface["ipv4"]["address"]["ip"],
                mask = interface["ipv4"]["address"]["netmask"],
                )
            )
    else:
        print("No interface {} found".format("GigabitEthernet1"))

