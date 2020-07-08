from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
# import hmac
# from Crypto.Cipher import AES
from imageai.Detection.Custom import CustomObjectDetection

from blockchain import blockChain
from block import block

import random


class drone():
    droneCount = 0

    def __init__(self, zone):
        # Serial.no
        self.num = drone.droneCount

        # keys
        self.__sk = RSA.generate(1024)
        self.pk = self.__sk.publickey()
        self.boss = self.pk

        # droneID
        self.idProof = {}
        self.idProof['public_KEY'] = self.pk.exportKey('DER').hex()
        # self.idProof['Node_ID']=None
        # self.idProof['block_no']=None
        self.idProof['okToSend'] = True
        self.idProof['okToRecieve'] = True
        self.idProof['block_no'] = None
        self.address = "00"
        self.zone = zone
        # self.address = sign.hex()

        self.blocksmined = 0
        self.rE = 100
        self.head = False
        # drone's chain
        self.chain = blockChain()

        # Static
        drone.droneCount += 1

    def __str__(self):
        print("drone.no:", str(self.num))
        print("droneID:", self.address)
        print("publicKEY:", self.pk)
        print("Blocks mined:", self.blocksmined)
        print("----"*16)
        return ""

    def getSignature(self, txn):
        encoded = str(txn).encode()
        hashedMsg = SHA.new(encoded)
        author = PKCS1_v1_5.new(self.__sk)
        signature = author.sign(hashedMsg)
        self.rE -= random.random()
        return signature

    def genesisBlock(self, oneTxnList):
        try:
            pH = self.chain.chain[-1].hash
        except:
            pH = "0"
        # pk=self.pk.exportKey('DER').hex().encode()
        # key=hmac.HMAC(pk)
        S = oneTxnList[0]["Sender"]
        pk = S.pk.exportKey()
        hshpk = SHA.new(pk)
        auth = PKCS1_v1_5.new(self.__sk)
        sign = auth.sign(hshpk)
        S.address = sign.hex()
        S.boss = self.pk
        S.idProof['block_no'] = self.blocksmined+1

        PoW = {'difficulty': 4}  # Consider getting blockChain as parameter
        PoW['Hash'], PoW['nonce'] = self.__PoW(pH, oneTxnList)
        miner = self.address
        self.blocksmined += 1
        return block(pH, oneTxnList, PoW, miner)

    def createBlock(self, txnList):
        pH = self.chain.chain[-1].hash
        if(txnList == []):
            return
        verifiedList = []
        unverifiedList = []

        # Verifying transactions      {"Sender":S,"Message":msg,"Signature":signature}
        for T in txnList:
            idchecked = self.checkID(T['Sender'])

            encoded = str(T["Message"]).encode()
            hashedMsg = SHA.new(encoded)
            auth = PKCS1_v1_5.new(T['Sender'].pk)
            verified = auth.verify(hashedMsg, T['Signature'])

            if(idchecked and verified):
                verifiedList.append(T)
            else:
                unverifiedList.append(T)

        PoW = {'difficulty': 4}  # Consider getting difficulty as parameter
        PoW['Hash'], PoW['nonce'] = self.__PoW(pH, verified)
        miner = self.address
        self.blocksmined += 1
        self.rE -= (4+random.random())
        return block(pH, verifiedList, PoW, miner), unverifiedList

    def __PoW(self, pH, verifiedList):
        diff = 4
        # diff=blockChain.difficulty
        nonce = random.randint(0, 100)
        data = pH+str(verifiedList)+str(nonce)
        newHash = SHA.new(data.encode()).hexdigest()
        while newHash[:diff] != '0'*diff:
            nonce += 1
            data = pH+str(verifiedList)+str(nonce)
            newHash = SHA.new(data.encode()).hexdigest()
        return newHash, nonce

    def insert(self, BLOC):
        try:
            pH = self.chain.chain[-1].hash
        except:
            pH = "0"
        if(pH == BLOC.prevHash):
            self.chain.append(BLOC)
        return

    def checkID(self, U):
        UID = U.idProof
        identified = None not in UID.values()

        msg = U.pk.exportKey()
        hshmsg = SHA.new(msg)

        sign = bytes.fromhex(U.address)
        verifier = PKCS1_v1_5.new(self.boss)
        verified = verifier.verify(hshmsg, sign)

        return identified and verified

    def detectImage(self, test_image):
        # try:
        detector = CustomObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(
            detection_model_path="detection_model-ex-33--loss-4.97.h5")
        detector.setJsonPath(configuration_json="detection_config.json")
        detector.loadModel()

        results = detector.detectObjectsFromImage(input_image=test_image,
                                                  output_image_path="resulted-"+test_image,
                                                  minimum_percentage_probability=40)
        # except:
        #     result = [{'percentage_probability': random.random()}]

        return results
