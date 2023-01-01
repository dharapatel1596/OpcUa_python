#!/usr/bin/env python3
# coding: utf-8
from opcua import Client

client = Client("opc.tcp://127.0.0.1:4841/freeopcua/server/") # Initiate

try :
    # Connect to Server
    client.connect()
    
    # Get the Server defined variables
    object_node = client.get_objects_node()
    child_node = object_node.get_children()[1]
    total = child_node.get_children()
    chvars = child_node.get_children()[0]
    
    # Read the status of a sensor
    light_curtain = chvars.get_value()
    # Change the value of a sensor
    new_val = chvars.set_value(True)
    light_curtain = chvars.get_value()
    
    # When light curtain sensor activates call Method 
    if light_curtain == True:
        stop_robot = child_node.get_children()[3]
        s1 = object_node.call_method(stop_robot,True)
        
    # Get the Recipe complete Sensor status
    chvars1 = child_node.get_children()[1]
    # Change the value of a sensor
    change = chvars1.set_value("Green")
    r_comp = chvars1.get_value()
    
    # When Recipe Complete Sensor "Green" call Method
    chvars1 = child_node.get_children()[2]
    if r_comp == "Green":
        set_recipe = child_node.get_children()[4]
        s2 = object_node.call_method(set_recipe,5)
       
finally :
    # Disconnect when finish
    client.disconnect()
