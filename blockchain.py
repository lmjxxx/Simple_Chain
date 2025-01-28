'''
create block, add block to chian, define block architecture
'''
import time
from utils import sha256

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp, validator):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.validator = validator
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_data = (
            str(self.index) +
            str(self.transactions) +
            str(self.timestamp) +
            self.previous_hash + 
            self.validator
        )
        return sha256(block_data)
    
    def show_block(self):
        return (
            f"Block Index: {self.index}\n"
            f"Transactions: {self.transactions}\n"
            f"Previous Hash: {self.previous_hash}\n"
            f"Timestamp: {self.timestamp}\n"
            f"Validator: {self.validator}\n"
            f"Block Hash: {self.hash}\n"
        )

class Blockchain:
        def __init__(self):
            self.chain = []
            
        def get_latest_block(self):
            return self.chain[-1]
        
        def genesis_block(self, genesis_block):
            self.chain.append(genesis_block)
            
            
        def add_block(self, block):
            if block.previous_hash != self.get_latest_block().hash:
                raise ValueError("Invalid Previous Block Hash")
            
            if block.hash != block.calculate_hash():
                raise ValueError("Invalid Block Hash Mismatch")
            
            self.chain.append(block)
    
        def create_block(self, transactions, previous_hash, validator):
        
            new_block = Block(
                index = len(self.chain),
                transactions = transactions,
                timestamp = time.time(),
                previous_hash = previous_hash,
                validator = validator
            )
            self.add_block(new_block)
            return new_block 
        
        def show_chain(self):
            for block in self.chain:
                print(block.show_block())
        


if __name__ == "__main__":
    blockchain = Blockchain()
    
    genesis_block = Block(
        index = 0,
        transactions = "Genesis",
        timestamp = time.time(), 
        previous_hash = "0x0000000000000000000000000000000000000000",
        validator = "0x0000000000000000000000000000000000000000"
    )
    
    blockchain.genesis_block(genesis_block)
    blockchain.create_block("Transaction 1", blockchain.get_latest_block().hash, "Validator 1")
    # print(blockchain.get_latest_block().show_block())
    
    blockchain.create_block("Transaction 2", blockchain.get_latest_block().hash, "Validator 2")
    blockchain.create_block("Transaction 2", blockchain.get_latest_block().hash, "Validator 2")
    
    blockchain.show_chain()
    