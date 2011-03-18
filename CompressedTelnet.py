COMPRESS = chr(85)
COMPRESS2 = chr(86)

import zlib
from telnetlib import Telnet
compressor = None

class CompressedTelnet(Telnet):
    @staticmethod
    def handle_stuff(session, command, option):
        print "WE GOT SOMETHIN"
        print "Command: ", ord(command)
        print "Option: ", ord(option)
        if command == telnetlib.WILL:
            if option == COMPRESS2:
                print "We got a COMPRESS2 request from the server"
                # respond to the server that we accept
                # TODO: Is this ok? Server doesn't respond to it by
                # sending IAC SB COMPRESS2 IAC SE
                session.write(telnetlib.IAC)
                session.write(telnetlib.DO)
                session.write(COMPRESS2)

        # the server may begin compression at any time by sending a 
        # IAC SB COMPRESS2 IAC SE sequence, immediately followed by the start # of the compressed stream. 
        if command == telnetlib.SB:
           if option == COMPRESS2:
                # All right, we're compressing! So:
                # the next thing we receive will be compressed.
                # set the global compression object
                print "Server says: Next thing be compressed."
                compressor = zlib.compressobj()
                # Actually the next thing will be IAC SE, but 
                # that is caught by the callback, not the displaying func.
                pass
        if command == telnetlib.SE:
                print "IAC SE"
                print ord(session.read_sb_data()) 
                # Nothing for now.
                pass

        def __init__(self):
            Telnet.__init__(self)
            self.set_option_negotiation_callback(CompressedTelnet.handle_stuff)




