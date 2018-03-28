class Finding:

    def __init__(self, source, name, description=None, address=None, pc=None, severity=None):
        self.source = source
        self.name = name
        self.description = description
        self.address = address
        self.pc = pc
        self.severity = severity