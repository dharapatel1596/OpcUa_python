# opcUa_python
This files demonstrate the OPCUA Server-Client implementation. The Client can access all the variables from server as well as multiple methods.

The Server has 3 variables defined for OPCUA Communication: Light Curtain Sensor, Recipe Complete Light and Recipe Number. Also, two methods were implemented. First method "stop_robot" is called when the Light curtain Sensor activates, it will send a Robot Stop signal. Second Method "set_recipe" is called when Recipe Complete Light turned 'Green', the next recipe number will be send to the robot.
