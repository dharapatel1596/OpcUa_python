#!/usr/bin/env python3
# coding: utf-8
from opcua import Server, ua, uamethod
import time

# Initiate Server and namespace  
s = Server()
s.set_server_name("OpcUa Test Server")
s.set_endpoint("opc.tcp://127.0.0.1:4841")
s.set_security_policy([ua.SecurityPolicyType.NoSecurity,ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign])  
# Register the OPC-UA namespace
idx = s.register_namespace("Robot Cell")   
idx1 = s.register_namespace("Method2") 

objects = s.get_objects_node()
# Define a Robot Station object with some tags
myobject = objects.add_object(idx, "Sensor Station")
   
# Add a sensor tag with a value and range
myvar1 = myobject.add_variable(idx, "Light curtain Sensor", False)
myvar1.set_writable(writable=True)
   
# Add a Cell Status tag with a value and range
myvar2 = myobject.add_variable(idx, "Recipe Complete Light", "Yellow")
myvar2.set_writable(writable=True)

# Add a recipe number tag with a value and range
myvar3 = myobject.add_variable(idx, "Recipe Number", 1)
myvar3.set_writable(writable=True)

# Set up method 1 to stop the robot when Light Curtain sensor activates
@uamethod
def stop_robot(parent, stop):
    """Stop Robot"""
    print("stop_robot was called with the arguments: [" + str(stop) + "]")
    print("Robot Stopped")
    return 1

# Declare the input and output arguments
inarg_stop = ua.Argument()
inarg_stop.Name = "Stop"
inarg_stop.DataType = ua.NodeId(ua.ObjectIds.Boolean)
inarg_stop.ValueRank = -1
inarg_stop.ArrayDimensions = []
inarg_stop.Description = ua.LocalizedText("State ot the robot")

outarg = ua.Argument()
outarg.Name = "Success"
outarg.DataType = ua.NodeId(ua.ObjectIds.Int64)
outarg.ValueRank = -1
outarg.ArrayDimensions = []
outarg.Description = ua.LocalizedText("Setting of robot successfull?")

# Set up method 2 to send the recipe number
@uamethod
def set_recipe(parent, number):
    """Sending recipe number to robot"""
    print("set_recipe was called with the arguments: [" + str(number) + "]")
    print("Recipe number:",number)
    myvar3.set_value(number)
    return 1

# Declare the input and output arguments
num = ua.Argument()
num.Name = "SetRecipe"
num.DataType = ua.NodeId(ua.ObjectIds.Int64)
num.ValueRank = -1
num.ArrayDimensions = []
num.Description = ua.LocalizedText("Recipe number to execute")

outarg_s = ua.Argument()
outarg_s.Name = "Success."
outarg_s.DataType = ua.NodeId(ua.ObjectIds.Int64)
outarg_s.ValueRank = -1
outarg_s.ArrayDimensions = []
outarg_s.Description = ua.LocalizedText("Setting of recipe successfull?")

# Add methods to server
myobject.add_method(idx, "Stop Robot", stop_robot, [inarg_stop], [outarg])
myobject.add_method(idx1, "Set Recipe", set_recipe, [num], [outarg_s])
  
try:
    # Start the server
    s.start() 
    while True:
        sensor = myvar1.get_value()
        print("Light curtain status:",sensor)
        light = myvar2.get_value()
        print("Recipe Complete Light Status:",light)
        recipe = myvar3.get_value()
        print("Recipe number status:",recipe)
        time.sleep(2)
finally:
    s.stop()