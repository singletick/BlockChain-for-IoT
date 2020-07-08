from datetime import datetime as DT
from merklelib import MerkleTree


class block:
    blockCount = 0

    def __init__(self, pH, txnList, PoW, minerID):
        self.blockHeight = block.blockCount
        block.blockCount += 1

        self.prevHash = pH
        self.transactions = txnList
        self.timestamp = DT.timestamp(DT.now())
        self.hash = PoW['Hash']
        self.nonce = PoW['nonce']
        self.difficulty = PoW['difficulty']
        self.mTree = MerkleTree(txnList)
        self.mRoot = self.mTree.merkle_root
        self.minerID = minerID

    def __str__(self):
        print("Block's Height:", self.blockHeight)
        print("No.of Transactions:", len(self.transactions),
              "     Time:", DT.fromtimestamp(self.timestamp))
        print("previous HASH:", self.prevHash)

        print("-" * 75, "Transaction  Details", "-" * 75, sep="")
        for T in self.transactions:
            # print(T)
            # {"Sender":S,"Message":msg,"Signature":signature}
            print("Sender: ", T['Sender'].address[:60], end=",  ")
            print("Message: ", T['Message'], end=",  ")
            print("Signature: ", T['Signature'].hex()[:60])
        print("-"*170)

        print("Merkley Root:", self.mRoot)
        print("\nNONCE     :", self.nonce)
        print("Difficulty  :", self.difficulty)
        print("current HASH:", self.hash)
        print("MinerID     :", self.minerID, end='\n\n')
        return ""
