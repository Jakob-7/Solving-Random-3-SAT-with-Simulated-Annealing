import numpy as np
from copy import deepcopy

class KSAT:
    def __init__(self, N, M, K, seed = None):
        if not (isinstance(K, int) and K >= 2):
            raise Exception("k must be an int greater or equal than 2")
        self.K = K
        self.M = M
        self.N = N

        ## Optionally set up the random number generator state
        if seed is not None:
            np.random.seed(seed)
    
        # s is the sign matrix
        s = np.random.choice([-1,1], size=(M,K))
        
        # index is the matrix reporting the index of the K variables of the m-th clause 
        index = np.zeros((M,K), dtype = int)        
        for m in range(M):
            index[m] = np.random.choice(N, size=(K), replace=False)
            
        # Dictionary for keeping track of literals in clauses
        clauses = []   
        for n in range(N):
            clauses.append([i for i, row in enumerate(index) if n in row])
        
        self.s, self.index, self.clauses = s, index, clauses        
        
        ## Initialize the configuration
        x = np.ones(N, dtype=int)
        self.x = x
        self.init_config()

    ## Initialize (or reset) the current configuration
    def init_config(self):
        N = self.N 
        self.x[:] = np.random.choice([-1,1], size=(N))
        
        
    ## Definition of the cost function
    # Here you need to complete the function computing the cost using eq.(4) of pdf file
    # My code
    def cost(self):
        # Extract variables for each clause
        variables = self.x[self.index]  

        # Compute the literal evaluations
        literals = self.s * variables  
    
        # Evaluate unsatisfied clauses using Eq.(4)
        clause_cost = np.prod((1 - literals) / 2, axis=1)
    
        # Total cost is the sum of unsatisfied clauses
        total_cost = np.sum(clause_cost)
        return int(total_cost)


    ## Propose a valid random move. 
    def propose_move(self):
        N = self.N
        move = np.random.choice(N)
        return move
    
    ## Modify the current configuration, accepting the proposed move
    def accept_move(self, move):
        self.x[move] *= -1

    ## Compute the extra cost of the move (new-old, negative means convenient)
    # Here you need complete the compute_delta_cost function as explained in the pdf file
    # My code
    def compute_delta_cost(self, move):
    
        # Get the indices of clauses affected by flipping x[move]
        affected_clauses = np.array(self.clauses[move], dtype=int)
    
        # Extract the current literals for the affected clauses
        current_literals = self.s[affected_clauses] * self.x[self.index[affected_clauses]]
    
        # Evaluate clause satisfaction before flipping
        clause_satisfied_before = np.any(current_literals > 0, axis=1)
    
        # Simulate flipping x[move]
        flipped_literals = current_literals.copy()
    
        # Locate all positions where `move` appears in the affected clauses
        flip_positions = np.where(self.index[affected_clauses] == move)
        flipped_literals[flip_positions] *= -1  # Flip the affected literal
    
        # Evaluate clause satisfaction after flipping
        clause_satisfied_after = np.any(flipped_literals > 0, axis=1)
    
        # Calculate delta cost
        delta_cost = np.sum(clause_satisfied_before & ~clause_satisfied_after) -\
            np.sum(~clause_satisfied_before & clause_satisfied_after) 
        
        return delta_cost


    ## Make an entirely independent duplicate of the current object.
    def copy(self):
        return deepcopy(self)
    
    ## The display function should not be implemented
    def display(self):
        pass
        
