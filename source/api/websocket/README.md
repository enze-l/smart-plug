# Websocket Api

This api should demonstrate how a controlling instance could steer
consumers. In order to do this, the plug contacts a server and listens to commands from it.

For testing purposes there is an example for the implementation of such a server [provided](../../../tools/websocket_server.py). It can be run via ```make websocket-server```

To configure it utilize the [config](../../../tools/websocket_config.py). The commands that the server will issue are retrieved from the "WEBSOCKET_MESSAGE_STRING". Each command is seperated by a \n which symbolizes a new line. The commands are sent n seconds apart, defined by "WEBSOCKET_COMMAND_INTERVALL_SECONDS". 
