from drone import drone
from cloud import cloud
from block import block

# from time import time
import random
import winsound

initE = 100
threshold = 1/3


def broadcast(obj, network, CLOUD, I):
    if(isinstance(obj, block)):
        for D in network['drones']:
            D.insert(obj)
        network['lastBlock'] = obj

    elif(isinstance(obj, dict)):
        network['txns'].append(obj)
        CLOUD.send(obj)  # Each transaction is shared with cloud
        if(len(network['txns']) == 2):
            miner = random.choice(network['heads'])
            BLOC, unverified = miner.createBlock(network['txns'])
            network['txns'].clear()
            broadcast(BLOC, network, CLOUD, I)
            I.extend(unverified)


def updateCHeads():
    for d in cHeads:
        d.head = False
    cHeads.clear()
    for z in zones:

        p = 1 / len(zones[z])
        r = random.randint(1 / p)
        k = len(zones)

        nH = None
        pre = 0
        # I'm still not sure why we are doing,
        # for d in zones[z]:
        #     rE = d.rE
        #     T = p * rE * k / initE
        #     den = 1 - p * (r % (1 / p))
        #     PRE = T / den
        # PRE = rE-Econsumed-pathLoss
        # if (PRE > pre):
        #     pre = T
        #     nH = d
        ####-inner for-#####
        # nH.head = True
        cHeads.append(nH)
    ###-outer for-###
    print("New cluster Heads appointed.")


CLOUD = cloud()
# N=int(input("Enter no.of IoT drones:"))
N = 12
invalidTxns = []
dList = [drone(i % 4) for i in range(N)]
zones = {
    0: [],
    1: [],
    2: [],
    3: []
}
cHeads = []
for d in dList:
    zones[d.zone].append(d)
for eachZone in zones:
    node = random.choice(zones[eachZone])
    node.head = True
    cHeads.append(node)


network = {
    'drones': dList,
    'heads': cHeads,
    'lastBlock': None,
    'txns': []
}

# winsound.Beep(600, 400)
# start=time()
for S in dList:
    msg = 'X'
    signature = S.getSignature(msg)
    oneTxnList = [{"Sender": S, "Message": msg, "Signature": signature}]
    miner = dList[0]
    BLOC = miner.genesisBlock(oneTxnList)
    broadcast(BLOC, network, CLOUD, invalidTxns)

# winsound.Beep(600, 800)


images = [
    ["test-00.jpg", "test-01.jpg"],
    ["test-10.jpg", "test-11.jpg"]
]
Intrude = True
newList = network['drones'].copy()
if(Intrude):
    newList.append(drone(-1))


# start=time()
for x in range(2):
    for y in range(2):
        S = random.choice(newList)
        result = S.detectImage(images[x][y])
        if(result):
            # winsound.Beep(600, 10)
            dir = random.random() * 360
            dir = "{:.2f}".format(dir)
            msg = str(x)+"|"+str(y)+"|"+dir+"|"
            msg += str(result[0]['percentage_probability'])
            signature = S.getSignature(msg)
            txn = {"Sender": S, "Message": msg, "Signature": signature}
            broadcast(txn, network, CLOUD, invalidTxns)
        winsound.Beep(600, 700)

# print("TOTAL TIME:",time()-start)
# winsound.Beep(600, 700)

temp = input("-" * 90 + "IDENTITY" + "-" * 90)
for D in newList:
    print("Drone.no:", D.num)
    print("Drone-ID:", D.address)
    for k, v in D.idProof.items():
        print(k+":", v)
    print()

temp = input("-"*90 + "DRONE DETAILS" + "-"*90)
for i in newList:
    print(i)

temp = input("-"*90 + "BLOCKCHAIN" + "-"*90)
print(dList[0].chain)

temp = input("-"*90 + "IN CLOUD" + "-"*90)
CLOUD.getTransactions()

print("\n\nVerifying transactions in cloud.....")
CLOUD.verify(network['lastBlock'].mTree)
print("Verification done!\n\n")

temp = input("-"*90 + "IN CLOUD" + "-"*90)
CLOUD.getTransactions()
print("\n\n")

temp = input("-"*90 + "NETWORK" + "-"*90)
for T in network['txns']:
    print("Sender: ", T['Sender'].address[:60], end=",  ")
    print("Message: ", T['Message'], end=",  ")
    print("Signature: ", T['Signature'].hex()[:60])
print("\n\n")

temp = input("-"*90 + "ALL TXNS" + "-"*90)
for T in dList[0].chain.allTxns:
    print("Sender: ", T['Sender'].address[:60], end=",  ")
    print("Message: ", T['Message'], end=",  ")
    print("Signature: ", T['Signature'].hex()[:60])
