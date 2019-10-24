class Motob:
    def __init__(self):
        self.motors = []
        self.value = []

    def update(self, value):
        self.value = value
        self.operationalize()

    def operationalize(self):
