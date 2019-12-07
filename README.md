# BlockChain-for-IoT

There are 3 stages to completely enable the mentioned IoT framework: 

#### 1.Device setup phase 
  First, we give the number of devices so that it creates a public/private key pair for the devices. Later each device is made to do a genesis transaction with the central HUB.
Thus, every valid device which is added to the network should do a genesis transaction so that later in the data transmission phase its identity gets verified. The Identity of a device is created only when it makes a genesis transaction with the hub.

#### 2.Dual identity validation
  As mentioned above, once the ID is created it can do further data transmissions within the network. The ID is created using the following attributes:
  **a.Block Number
  b.Block Hash
  c.Difficulty target
  d.Node ID
  e.Public key**

#### 3. Secure data transmission
This is the final stage where the network is ready to transmit data from one to another. A transaction (data which is being transferred) is considered to be valid only if the ID of the sender and the receiver is verified, and then a valid signature of the sender is authenticated.  
If the ID is not verified or the signature is not authentic, the transaction is said to be invalid and discarded immediately. 
Furthermore, a block has a limitation of number of transactions to be held. In our project, we have set the limit to 6 i.e. a block is created for every 6 valid transactions.
