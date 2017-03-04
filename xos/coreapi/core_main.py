import time

from reaper import ReaperThread
from grpc_server import XOSGrpcServer, restart_chameleon

def show_banner():
    print " __   __   ____     _____      _____"
    print " \ \ / /  / __ \   / ____|    / ____|"
    print "  \ V /  | |  | | | (___     | |        ___    _ __    ___:"
    print "   > <   | |  | |  \___ \    | |       / _ \  | '__|  / _ \\"
    print "  / . \  | |__| |  ____) |   | |____  | (_) | | |    |  __/"
    print " /_/ \_\  \____/  |_____/     \_____|  \___/  |_|     \___|"
    print ""

if __name__ == '__main__':
    django.setup()

    reaper = ReaperThread().start()

    server = XOSGrpcServer().start()

    restart_chameleon()

    show_banner()

    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    try:
        while 1:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop()
        reaper.stop()

