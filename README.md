Final Project:
*server is decomissioned, disabling message functionality

-fp.py: The main file to be run from, handling the gui and some interpretation of messages. The framework was lifted from A5 with various modifications
        -Users can be created through the file drop down
        -users can be communicated with by add user and their username

-ds_messenger.py: handles the majority of server communication

-ds_protocol.py: interprets and organizes the majority of server recieved communication

-Profile.py: holds profile and conversation objects which store the messages and other data

-exceptions.py: contains a couple simple exceptions for troublsome areas of the program
