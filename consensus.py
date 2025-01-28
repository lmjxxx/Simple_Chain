'''
Consensus Mechanism : Proof of Stake 
'''

import random
import time

class PoSConsensus:
    def __init__(self, staking_pool):
        self.staking_pool = staking_pool
                
    def sel_validator(self):
        '''
        staking 비율에 따라 validator 선정
        '''
        total_stake = self.staking_pool.get_total_stake() # total staked amount
        validators = list(self.staking_pool.stake.keys()) # validator list
        
        if total_stake == 0:
            return ValueError("No validators found")
        
        weight = self.staking_pool.calc_weight(validators) # list of weight for each validator
        
        selected_validator = random.choices(validators, weights=weight, k=1)
    
        self.staking_pool.decrease_weight(selected_validator[0], self.staking_pool.stake.get(selected_validator[0])[2])
        self.staking_pool.stake[selected_validator[0]] = (self.staking_pool.stake.get(selected_validator[0])[0], self.staking_pool.stake.get(selected_validator[0])[1], self.staking_pool.stake.get(selected_validator[0])[2], True)
        
        return selected_validator[0]
    
    def validate_block(self, block):
        
        

class StakingPool:
    def __init__(self):
        self.stake = {} # {staker_address : {staked_amount, time_stamp, weight, selected=False}} 
        
        
    def add_stake(self, staker_address, amount):
        current_time = time.time()
        if staker_address in self.stake: # is statker
            current_amount, _, weight, is_selected = self.stake[staker_address]
            self.stake[staker_address] = (current_amount + amount, current_time, weight, is_selected)
        else: # not staker, just node, staker add
            self.stake[staker_address] = (amount, current_time, self.calc_weight(staker_address), False)
    
    def remove_stake(self, staker_address, amount):
        if staker_address in self.stake:
            current_amount, timestamp, weight, is_selected = self.stake[staker_address]
            if current_amount > amount:
                self.stake[staker_address] = (current_amount - amount, timestamp, weight, self.stake[staker_address][3])
            else:
                del self.stake[staker_address]
    
    def get_total_stake(self):
        return sum(amount for amount, _, _, _ in self.stake.values())
    
    def get_timestamp(self,staker_address):
        if staker_address in self.stake:
            _, timestamp, _ = self.stake[staker_address]
            return timestamp
        return 0
    
    def get_weight(self, staker_address):
        if staker_address in self.stake:
            _, _, weight = self.stake[staker_address]
            return weight
        return 0
        
    def get_validator_stake(self, staker_address):
        return self.stake.get(staker_address, (0,0,0,0))[0]
    
    def calc_staking_period(self, staker_address):
        if staker_address in self.stake:
            _, timestamp, _, _ = self.stake[staker_address]
            return time.time() - timestamp
        return 0
    
    def calc_weight(self, staker_address): # staker_address is a list
        #  Todo: modify weight calculation algorithm to recover weight slowly 
        #  + Weight restoration at each block generation cycle
        weights = []
        for staker_address in staker_address:
            if staker_address in self.stake:
                amount, timestamp, _ , is_selected= self.stake[staker_address]
                
                if is_selected == True:
                    weight = 0
                else:
                    total_stake = self.get_total_stake()
                    amount_weight = amount / total_stake if total_stake > 0 else 0
                    period_weight = self.calc_staking_period(staker_address)
                        
                    weight = amount_weight * period_weight 
                    
                weights.append(weight)
                
                self.stake[staker_address] = (amount, timestamp, weight, False)
            else:
                weights.append(0)
        
        return weights 
        
    def decrease_weight(self, validator_address, weight): # 선정된 validator weight 감소, is_selected = True
        if validator_address in self.stake:
            amount, timestamp, weight, is_selected = self.stake[validator_address]
            self.stake[validator_address] = (amount, timestamp, weight - weight, is_selected)
            
            
            
    
class Reward:
    def __init__(self, staking_pool):
        self.staking_pool = staking_pool
        
    def rewardto(self, staker_address, reward):
        self.staking_pool.add_stake(staker_address, reward)