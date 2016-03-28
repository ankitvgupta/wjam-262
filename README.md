WJAM 262
========

## New User? Try this.
1. Go to the `client` directory
2. Run `./client.py` and you will get a usage hint. As per the usage hint, use `rest` to try our Restful API Server and `wire` to try our Custom Wire Protocol. (Note: if this is your first connection, you must use the `register` keyword to register a new user).
3. Once you've run the `client.py` interpreter, you can press enter to get a list of useful commands. Message away!


# High Level Overview

## Client
The client folder contains the code that will run in the clients for this software. 
### Description of Files
- [client.py](client/client.py): This is the main driver program for the client. The command line arguments to this program determine which api (Rest/WireProtocol) to use, and it registers the appropriate handler and waits for an instruction.
- [basehandler.py](client/basehandler.py): This is the abstract client handler class, and it implements some shared functions between the Rest and WireProtocol handler. RestHandler and WireHandler inherit this class, and implement the parsing system for the various commands (getting users, making groups, getting/sending messages, etc.)
- [resthandler.py](client/resthandler.py): The REST-specific implementation of BaseHandler.
- [wirehandler.py](client/wirehandler.py): The WireProtocol-specific implementation of BaseHandler.

## Server
The files in the top-level directory contain the server code
- [server.py](server.py)
- [requestprocessor.py](requestprocessor.py)
- [RestAPIStub.py](RestAPIStub.py)
- [WireProtocolStub.py](WireProtocolStub.py)
- [requirements.txt](requirements.txt)