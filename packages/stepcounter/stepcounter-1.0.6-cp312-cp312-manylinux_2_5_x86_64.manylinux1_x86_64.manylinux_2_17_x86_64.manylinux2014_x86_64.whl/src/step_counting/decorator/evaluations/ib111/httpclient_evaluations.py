from ..complexities import ComplexitiesDict, constant


httclient_complexities: ComplexitiesDict = dict()

httclient_HTTPConnection_complexities: ComplexitiesDict = {
    'auto_open': constant,
    'close': constant,
    'connect': constant,
    'debuglevel': constant,
    'default_port': constant,
    'endheaders': constant,
    'getresponse': constant,
    'putheader': constant,
    'putrequest': constant,
    'request': constant,
    'response_class': constant,
    'send': constant,
    'set_debuglevel': constant,
    'set_tunnel': constant,
}

httclient_HTTPSConnection_complexities: ComplexitiesDict = {
    'auto_open': constant,
    'close': constant,
    'connect': constant,
    'debuglevel': constant,
    'default_port': constant,
    'endheaders': constant,
    'getresponse': constant,
    'putheader': constant,
    'putrequest': constant,
    'request': constant,
    'response_class': constant,
    'send': constant,
    'set_debuglevel': constant,
    'set_tunnel': constant,
}
