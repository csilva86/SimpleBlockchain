import time
import datetime
import hashlib

class Block:
    #   CLASS BLOCK'S ATTRIBUTES:
    #       timwatamp    : Indicates when the block was created
    #       data         : The list of transactions inside each block
    #       previousHash : The hash of previous block
    #       hash         : The hash of current block
    #       nonce        : The value that will be used to compose a valid hash

    timestamp = 0
    data = 0
    previousHash = '0'
    hash = '0'
    nonce = 0

    #   CONSTRUCTOR
    #       Defines the initial values for each block created
    def __init__(self, timestamp, data, previousHash = '0'):
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.hash = self.calculateHash()
        self.nonce = 0

    #   METHOD ==> calculateHash(self)
    #       Calculates the hash of a block considering its timestamp, data and previous hashe values
    def calculateHash(self):
        return hashlib.sha256((str(self.timestamp) + str(self.nonce) + str(self.data) + str(self.previousHash)).encode('utf-8')).hexdigest()

    #   METHOD ==> mineBlock(self, difficulty)
    #       Created new blocks to be added to the blockchain
    def mineBlock(self, difficulty):
        while self.hash[:difficulty] != '0'*(difficulty):
            self.nonce += 1
            self.hash = self.calculateHash()

    def printBlockInfo(self):
        return "\tDate          : " + (str(time.ctime(self.timestamp))) +"\n\tAmount        : "+ (str(self.data)) +"\n\tPrevious Hash : "+ (str(self.previousHash)) +"\n\tCurrent Hash  : "+ (str(self.hash)) +"\n\tNonce         : "+ (str(self.nonce))

class BlockChain:
    chain = []
    difficulty = 0

    #   CONSTRUCTOR
    #       Initializes each Blockchain Object
    def __init__(self):
        self.chain = []
        self.difficulty = 4

    #   METHOD ==> genesis(self)
    #       Creates the Genesis Block for the Blockchain
    def genesis(self):
        self.chain.append(Block(time.time(),'Genesis','0000000000000000000000000000000000000000000000000000000000000000'))

    #   METHOD ==> getLastHash
    #       Returns the hash of the last block
    def getLastHash(self):
        index = len(self.chain)
        return self.chain[index - 1].hash

    #   METHOD ==> appendBlocks(self)
    #       Appends new blocks to the current blockchain
    def appendBlocks(self):
        bl = Block(time.time(),100,self.getLastHash())
        bl.mineBlock(self.difficulty)
        self.chain.append(bl)

    #   METHOD isChainValid(self)
    #       Validate if the chain is valid by checking the blocks one by one
    def isChainValid(self):
        currentBlock = self.chain[0]
        previousBlock = self.chain[0]
        index = 1
        if len(self.chain) > 1:
            while index < len(self.chain):
                currentBlock = self.chain[index]
                previousBlock = self.chain[index - 1]

                if currentBlock.previousHash != previousBlock.hash:
                    return False

                if currentBlock.hash != currentBlock.calculateHash():
                    print("\n\nHash Antigo : ",currentBlock.hash,"\nHash Novo   : ",currentBlock.calculateHash())
                    return False
                index += 1
            else:
                if currentBlock.hash != currentBlock.calculateHash():
                    print("\n\nHash Antigo : ",currentBlock.hash,"\nHash Novo   : ",currentBlock.calculateHash())
                    return False
        return True

####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
bl = BlockChain()
bl.genesis()
bl.appendBlocks()
bl.appendBlocks()
bl.appendBlocks()
bl.appendBlocks()
bl.appendBlocks()
bl.appendBlocks()
bl.chain[1].data = 200

for block in bl.chain:
    print(block.printBlockInfo(),"\n")

print(bl.isChainValid())
