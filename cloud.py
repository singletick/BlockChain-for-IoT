class cloud:
    def __init__(self, limit=5):
        self.limit = limit
        self.data = []
        self.unverified = []

    def send(self, msg):
        if(isinstance(msg, dict)):
            if(len(self.data) == self.limit):
                self.data.pop(0)
            self.data.append(msg)
        return

    def verify(self, tree):
        for msg in self.data:
            if(tree.get_proof(str(msg))):
                print("TRIGGERS FIRE DEPARTMENT!")
            else:
                self.unverified.append(msg)
        self.data.clear()
        self.data.extend(self.unverified)
        return

    def getTransactions(self):
        i = 1
        print("No.of txns:", len(self.data))
        for T in self.data:
            print(i)
            i += 1
            # print(T)
            print("Sender: ", T['Sender'].address[:60], end=",  ")
            print("Message: ", T['Message'], end=",  ")
            print("Signature: ", T['Signature'].hex()[:60])
            print()
