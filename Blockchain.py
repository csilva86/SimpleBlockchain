import time
import datetime
import hashlib

import pymysql

class Transaction:
    #   CLASS TRANSACTION'S ATTRIBUTES:
    #       blockHash    : The hash of the block which the transaction was processed
    #       fromAddress  : The user that started the stransaction
    #       toAddress    : The user that recieved the transaction
    #       amount       : The value for the transaction
    #       transactHash : The hash for the transaction
    #       status       : Indicates if the transaction was processed or not. Possible values:
    #                         (C): Completed
    #                         (P): Processing
    #                         (R): Rejected
    #
    blockHash = ''
    fromAddress = ''
    toAddress = ''
    amount = 0.0
    transactHash = ''
    status = ''

    def __init__(self):
        self.blockHash = ''
        self.fromAddress = ''
        self.toAddress = ''
        self.amount = 0.0
        self.transactHash = ''
        self.status = ''

    #   METHOD ==> calculateTransactionHash(self):
    #       Calculates the hashe value for each transaction
    def calculateTransactionHash(self):
        return hashlib.sha256((str(self.fromAddress) + str(self.toAddress) + str(self.amount) + str(self.transactHash)).encode('utf-8')).hexdigest()

    #   METHOD ==> newTransaction(self,fromAddress,toAddress,amount):
    #       Creates new Transactions
    def newTransaction(self,fromAddress,toAddress,amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.transactHash = self.calculateTransactionHash()
        self.status = 'P'

    #   METHOD ==> printTransactions(self):
    #       Prints transactions Infos
    def printTransactions(self):
        return '\t\tBlockHash    : '+str(self.blockHash)+'\n\t\tFromAddress  : '+str(self.fromAddress)+'\n\t\tToAddress    : '+str(self.toAddress)+'\n\t\tAmount       : '+str(self.amount)+'\n\t\tTransactHash : '+str(self.transactHash)+'\n\t\tStatus       : '+str(self.status)+'\n\n'

class Block:
    #   CLASS BLOCK'S ATTRIBUTES:
    #       timwatamp    : Indicates when the block was created
    #       data         : The list of transactions inside each block
    #       previousHash : The hash of previous block
    #       hash         : The hash of current block
    #       nonce        : The value that will be used to compose a valid hash

    timestamp = 0
    #data = 0
    transactions = []
    previousHash = '0'
    hash = '0'
    nonce = 0

    #   CONSTRUCTOR
    #       Defines the initial values for each block created
    def __init__(self, timestamp, transactions, previousHash = '0'):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.hash = self.calculateHash()
        self.nonce = 0

    #   METHOD ==> calculateHash(self)
    #       Calculates the hash of a block considering its timestamp, data and previous hashe values
    def calculateHash(self):
        return hashlib.sha256((str(self.timestamp) + str(self.nonce) + str(self.transactions) + str(self.previousHash)).encode('utf-8')).hexdigest()

    #   METHOD ==> mineBlock(self, difficulty)
    #       Created new blocks to be added to the blockchain
    def mineBlock(self, difficulty):
        while self.hash[:difficulty] != '0'*(difficulty):
            self.nonce += 1
            self.hash = self.calculateHash()

    #   METHOD ==> printBlockInfo(self):
    #       Prints the block's informations
    def printBlockInfo(self):
        transactInfo = ''
        if self.nonce != 0:
            for tr in self.transactions:
                transactInfo = transactInfo + tr.printTransactions()
        return "\tDate          : " + (str(time.ctime(self.timestamp))) + "\n\tPrevious Hash : "+ (str(self.previousHash)) + "\n\tCurrent Hash  : "+ (str(self.hash)) + "\n\tNonce         : "+ (str(self.nonce)) + "\n\tTransactions  : \n"+ (str(transactInfo))

class BlockChain:
    chain = []
    difficulty = 0
    pendingTransactions = []
    reward = 0.0

    #   CONSTRUCTOR
    #       Initializes each Blockchain Object
    def __init__(self):
        self.chain = []
        self.difficulty = 4

    #   METHOD ==> genesis(self)
    #       Creates the Genesis Block for the Blockchain
    def genesis(self):
        self.chain.append(Block(time.time(),'Genesis','0000000000000000000000000000000000000000000000000000000000000000'))
        self.addBlockToDB(self.chain[0])
    #   METHOD ==> getLastHash
    #       Returns the hash of the last block
    def getLastHash(self):
        index = len(self.chain)
        return self.chain[index - 1].hash

    #   METHOD ==> appendBlocks(self)
    #       Appends new blocks to the current blockchain
    def appendBlocks(self):
        block = Block(time.time(),self.pendingTransactions,self.getLastHash())
        block.mineBlock(self.difficulty)
        for transact in block.transactions:
            transact.blockHash = block.hash

        self.chain.append(block)
        self.addBlockToDB(block)
        for tr in block.transactions:
            self.addTransactionToDB(tr)

    #   METHOD ==> createTransactions(self,transaction)
    #       Creates a new transaction and appends it to the transaction List
    def createTransactions(self,transaction):
        self.pendingTransactions.append(transaction)

    def printPendingTransactions(self):
        for transact in self.pendingTransactions:
            print(transact.printTransactions())

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

    #   METHOD ==> addTransactionToDB(self,tr)
    #       Adds all transactions apended in blocks to the DB
    def addTransactionToDB(self,tr):
        # Open database connection
        db = pymysql.connect("localhost","blockuser","BlockChain#321","blockdb" )
        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        blhash = tr.blockHash
        fromAd = tr.fromAddress
        toAddr = tr.toAddress
        tramou = tr.amount
        trHash = tr.transactHash
        trstat = tr.status

        sql = "INSERT INTO TRANSACTIONS(BLOCK_HASH,FROMADDRESS,TOADDRESS,AMOUNT,TRANSACTION_HASH,STATUS) VALUES ('%s', '%s', '%s', '%f', '%s', '%s')" % (blhash, fromAd, toAddr, tramou, trHash, trstat)
        print(sql)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        #disconnect from server
        db.close()

    #   METHOD ==> addBlockToDB(self,bl):
    #       Adds all new blocks generated on the chain to DB
    def addBlockToDB(self,bl):
        # Open database connection
        db = pymysql.connect("localhost","blockuser","BlockChain#321","blockdb" )
        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        tstamp = bl.timestamp
        prHash = bl.previousHash
        crHash = bl.hash
        cNonce = bl.nonce

        sql = "INSERT INTO BLOCK(TIMESTAMP,PREVIOUS_HASH, HASH, NONCE) VALUES ('%d', '%s', '%s', '%d')" % (tstamp, prHash, crHash, cNonce)

        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        #disconnect from server
        db.close()
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
bl = BlockChain()
bl.genesis()
tr = Transaction()
tr1 = Transaction()
tr2 = Transaction()
tr3 = Transaction()
tr.newTransaction('add3','add4',280)
bl.createTransactions(tr)
tr1.newTransaction('add1','add2',80)
bl.createTransactions(tr1)
tr2.newTransaction('add5','add8',241)
bl.createTransactions(tr2)
tr3.newTransaction('add6','add3',512)
bl.createTransactions(tr3)
bl.appendBlocks()

for block in bl.chain:
    print(block.printBlockInfo(),"\n")
