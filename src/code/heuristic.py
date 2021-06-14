# Builds the graph of addresses connected if they appear together as input of a same transaction.        

# Input format: each line represents a transaction as follows:                                           
# num_block block_timestamp num_transaction nb_addresses_in nb_addresses_out addresses_in addresses_out  
# where addresses_in is a sequence of nb_addresses_in distinct addresses, and addresses_out a sequence of nb_addresses_out distinct addresses                                                                    

# Output: a sequence of lines, each representing a link of the form "a b i o" meaning that addresses a and b are input addresses of a transaction with i input addresses and o output addresses.                 
# Not all possible such links are written as output, but enough to ensure that all input addresses are connected through a path (sequence of links).                                                             
# Redundant links may appear.                                                                            

# Note: several strategies are possible for linking addresses together, that have an impact on graph structure and so on computations on this graph.                                                             

# Example: if input is:                                                                                  
# x x 1 2 1 a b c                                                                                        
# y y 2 3 2 d e b f g                                                                                    
# then a valid output is:                                                                                
# a b 2 1                                                                                                
# d e 3 2                                                                                                
# d b 3 2                                                                                                
# and another valid output is:                                                                           
# a b 2 1                                                                                                
# d e 3 2                                                                                                
# e b 3 2                                                                                                

import sys

for line in sys.stdin:
        tr = line.split()
        assert(len(tr)>4)
        [nb_in,nb_out] = [int(tr[i]) for i in (3,4)]
        in_addresses = tr[5:5+nb_in]
        # variant: sort addresses to increase redundancy?                                                
        # in_addresses.sort()                                                                            

        # first approach: link the first address to all others                                           
        for a in in_addresses[1:]:
                sys.stdout.write("%s %s %d %d\n"%(in_addresses[0],a,nb_in,nb_out))

        # second approach: builds a linear path between addresses                                        
#       for i in range(nb_in-1):                                                                         
#               sys.stdout.write("%s %s %d %d\n"%(in_addresses[i],in_addresses[i+1],nb_in,nb_out))       



