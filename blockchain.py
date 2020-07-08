class blockChain:
    def __init__(self):
        self.chain = []
        self.allTxns = []
        self.Tcount = 0

    def append(self, BLOC):
        self.allTxns.extend(BLOC.transactions)
        self.chain.append(BLOC)
        self.Tcount += len(BLOC.transactions)
        return

    def __str__(self):
        print("Total no.of transactions:", self.Tcount)
        for D in self.chain:
            print("#"*144)
            print(D)
            print("#" * 144)
        return ""
