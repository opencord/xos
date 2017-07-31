XOS_GLOBAL_DEFAULT_POLICY = True

class XOSSecurityContext(object):
    def __init__(self):
        self.grant_access = True
        self.write_access = True
        self.read_access = True
