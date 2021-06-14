---
sidebar: auto
sidebarDepth: 0
---

# Code
You can download the whole [code folder here](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/tree/main/src/code).
## Indexing
### [add_addresses.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/add_addresses.py)
```py
#add_addresses.py

import json
import sys
import gc

block_id = None
txid_index = 0
vout_index = 0
item_number = 0

for line in sys.stdin:
    block = json.loads(line)
    # Check block order
    assert(block_id==None or block["height"]==block_id+1)
    block_id = block["height"]
    
    for tx in block["tx"]:
        for vout in tx["vout"]:
            assert("scriptPubKey" in vout)
            assert("asm" in vout["scriptPubKey"])
            # If pubkey: create "addresses" field and put the pubkey inside
            if vout["scriptPubKey"]["type"] == "pubkey":
                assert("addresses" not in vout["scriptPubKey"])
                asm = vout["scriptPubKey"]["asm"].split(" ")
                pubKey = asm[0]
                vout["scriptPubKey"]["addresses"] = [pubKey]
            # addresses in non nulldata or nonstandard vout assertion
            if vout["scriptPubKey"]["type"] != "nulldata":
                if vout["scriptPubKey"]["type"] != "nonstandard":
                    assert("addresses" in vout["scriptPubKey"])
    sys.stdout.write(json.dumps(block) + "\n")
```

### [make_list.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/make_list.py)
```py
#make_list.py

import json
import sys
import gc

txid_index = 0
vout_index = 0
item_number = 0
for line in sys.stdin:
    block = json.loads(line)
    for tx in block["tx"]:
        # Count tx
        sys.stdout.write(str(item_number) + " " + tx["txid"] + " " + str(txid_index) + "\n")
        txid_index += 1
        item_number += 1
        # Count non coinbase vins        
        for vin in tx["vin"]:
            if "txid" in vin:
                sys.stdout.write(str(item_number) + " " + vin["txid"] + "\n")
                item_number += 1
                vin_id = vin["txid"] + "," + str(vin["vout"])
                sys.stdout.write(str(item_number) + " " + vin_id + "\n")
                item_number += 1
        # Count vouts
        for vout in tx["vout"]:
            vout_id = tx["txid"] + "," + str(vout["n"])
            sys.stdout.write(str(item_number) + " " + vout_id + " " + str(vout_index) + "\n")
            vout_index += 1
            item_number += 1
            # Count addresses
            if "addresses" in vout["scriptPubKey"]:
                for address in vout["scriptPubKey"]["addresses"]:
                    sys.stdout.write(str(item_number) + " " + address + "\n")
                    item_number += 1
    #StdErr monitoring                
    sys.stderr.write("block " + str(block["height"]) + ": " + str(item_number) + " items\n")
    sys.stderr.flush()

```

### [get_addresses.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/get_addresses.py)
```py
#get_addresses.py

import sys
import json

item_number = 0
# Blocks
for line in sys.stdin:
    block = json.loads(line)
    # Transactions
    for tx in block["tx"]:
        # Vouts
        for vout in tx["vout"]:
            if "scriptPubKey" in vout:
                if "addresses" in vout["scriptPubKey"]:
                    for address in vout["scriptPubKey"]["addresses"]:
                        sys.stdout.write(str(address) + " " + str(item_number) + "\n")
                        item_number += 1
    #StdErr monitoring
    sys.stderr.write("block " + str(block["height"]) + ", " + str(item_number) + " items\n")
    sys.stderr.flush()
```

### [list_translate.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/list_translate.py)
```py
#list_translate.py

import sys

nb_done = 0
for line in sys.stdin:
    l = line.strip().split()
    assert(len(l) in [2,3])
    if len(l)==3:
        index = l[2]
    if l[0] != '-1':
        sys.stdout.write(l[0] + " " + index + "\n")
    nb_done += 1
    if nb_done % 1000000 == 0:
        sys.stderr.write(str(nb_done / 100000) + " million(s) lines processed.\n")
sys.stderr.write(str(nb_done) + " lines processed.\nFinished.\n")
```

### [json_translate.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/json_translate.py)
```py
#json_translate.py

import sys
import json
import gzip
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, help="Specify index file", required=True)
args = parser.parse_args()

index_file = gzip.open(args.file,"r")
previous_occurrence = None

def next_index():
    global previous_occurrence
    l = index_file.readline().strip().split()
    assert(len(l)==2)
    occurrence,index = int(l[0]),int(l[1])
    if previous_occurrence != None:
        assert(occurrence==previous_occurrence+1)
    previous_occurrence = occurrence
    return(index)

nb_blocks,nb_vouts,nb_addresses,nb_txids = 0,0,0,0
item_number = 0
for line in sys.stdin:
    block = json.loads(line)
    nb_blocks = block["height"]+1
    for tx in block["tx"]:
        tx["index"] = next_index()
        item_number += 1
        nb_txids = max(nb_txids,tx["index"]+1)
        for vin in tx["vin"]:
            if "txid" in vin:
                vin["txid_index"] = next_index()
                item_number += 1
                nb_txids = max(nb_txids,vin["txid_index"]+1)
                vin["index"] = next_index()
                item_number += 1
                nb_vouts = max(nb_vouts,vin["index"]+1)
        for vout in tx["vout"]:
            vout["index"] = next_index()
            item_number += 1
            nb_vouts = max(nb_vouts,vout["index"]+1)
            if "addresses" in vout["scriptPubKey"]:
                addresses_index = []
                for address in vout["scriptPubKey"]["addresses"]:
                    addresses_index.append(next_index())
                    item_number += 1
                    nb_addresses = max(nb_addresses,addresses_index[-1]+1)
                vout["scriptPubKey"]["addresses_index"] = addresses_index

    sys.stdout.write(json.dumps(block) + "\n")
    sys.stderr.write("{\"blocks\": %d, \"vouts\": %d, \"addresses\": %d, \"txids\": %d}\n"%(nb_blocks,nb_vouts,nb_addresses,nb_txids))
    sys.stderr.flush()


```

### [get_indexes.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/get_indexes.py)
```py
#get_indexes.py

import sys
import json

f_txids,f_tios,f_addresses=open("index_txids","w"),open("index_tios","w"),open("index_addresses","w")
i_txids,i_tios,i_addresses=0,0,0

for line in sys.stdin:
        block = json.loads(line)
        block_id = str(block["height"])
        for tx in block["tx"]:
                if tx["index"]==i_txids:
                        f_txids.write("%d %s\n"%(i_txids,tx["txid"]))
                        i_txids+=1
                for vout in tx["vout"]:
                        if "index" in vout and "n" in vout and vout["index"]==i_tios:
                                f_tios.write("%d %s\n"%(i_tios,tx["txid"]+','+str(vout["n"])))
                                i_tios+=1
                        if "index" in vout and "scriptPubKey" in vout and "addresses_index" in vout["scriptPubKey"]:
                                for i in range(len(vout["scriptPubKey"]["addresses_index"])):
                                        if vout["scriptPubKey"]["addresses_index"][i]==i_addresses:
                                                f_addresses.write("%d %s\n"%(i_addresses,vout["scriptPubKey"]["addresses"][i]))
                                                i_addresses += 1
        sys.stderr.write("block "+block_id+"\n")
        sys.stderr.flush()

for f in f_txids,f_tios,f_addresses:
        f.close()
```

## Distillation
### [distillation_addresses.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/distillation_addresses.py)
```py
#distillation_addresses.py

import sys
import json

sizes = json.loads(sys.stdin.readline())
sys.stderr.write(str(sizes)+"\n")
v_addresses = [[]]*sizes["vouts"]

for line in sys.stdin:
        block = json.loads(line)
        block_id = str(block["height"])
        timestamp = str(block["time"])

        for tx in block["tx"]:
                sys.stdout.write(block_id+" "+timestamp)
                sys.stdout.write(" "+str(tx["index"]))
                in_addresses = set()
                for vin in tx["vin"]:
                        if "index" in vin:
                                in_addresses.update(v_addresses[vin["index"]])
                                v_addresses[vin["index"]] = None
                out_addresses = set()
                for vout in tx["vout"]:
                        if "index" in vout and "scriptPubKey" in vout and "addresses_index" in vout["scriptPubKey"]:
                                assert(v_addresses[vout["index"]]==[])
                                v_addresses[vout["index"]] = vout["scriptPubKey"]["addresses_index"]
                                out_addresses.update(v_addresses[vout["index"]])
                sys.stdout.write(" "+str(len(in_addresses)))
                sys.stdout.write(" "+str(len(out_addresses)))
                for a in in_addresses:
                        sys.stdout.write(" "+str(a))
                for a in out_addresses:
                        sys.stdout.write(" "+str(a))
                sys.stdout.write("\n")

        sys.stderr.write("block "+block_id+"\n")
        sys.stderr.flush()
```
### [distillation_amounts.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/distillation_amounts.py)
```py
#distillation_amounts.py

import sys
import json

sizes = json.loads(sys.stdin.readline())
sys.stderr.write(str(sizes)+"\n")
v_amount = [-1]*sizes["vouts"]

for line in sys.stdin:
	block = json.loads(line)
	block_id = str(block["height"])
	timestamp = str(block["time"])
	prefix=block_id+" "+timestamp+" "

	for tx in block["tx"]:
		sys.stdout.write(prefix)
		nb_in=0
		assert("vin" in tx and "vout" in tx and "index" in tx)
		for vin in tx["vin"]:
			if "index" in vin:
				nb_in += 1
		nb_out = len(tx["vout"])
		sys.stdout.write("%d %d %d"%(tx["index"],nb_in,nb_out))
		for vin in tx["vin"]:
			assert("index" in vin or "coinbase" in vin)
			if "index" in vin:
				sys.stdout.write(" %d"%v_amount[vin["index"]])
				v_amount[vin["index"]] = -1
		for vout in tx["vout"]:
			assert("index" in vout)
			assert("value" in vout)
			assert(v_amount[vout["index"]]==-1)
			v_amount[vout["index"]] = int(round(vout["value"]*10**8))
			sys.stdout.write(" %d"%v_amount[vout["index"]])
		sys.stdout.write("\n")

	sys.stderr.write("block "+block_id+"\n")
	sys.stderr.flush()

```
### [distillation_tios.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/distillation_tios.py)
```py
#distillation_tios.py

import sys
import json

sizes = json.loads(sys.stdin.readline())
sys.stderr.write(str(sizes)+"\n")

for line in sys.stdin:
        block = json.loads(line)
        block_id = str(block["height"])
        timestamp = str(block["time"])

        for tx in block["tx"]:
                sys.stdout.write(block_id+" "+timestamp)
                sys.stdout.write(" "+str(tx["index"]))
                in_tios = []
                for vin in tx["vin"]:
                        if "index" in vin:
                                in_tios.append(vin["index"])
                out_tios = []
                for vout in tx["vout"]:
                        if "index" in vout:
                                out_tios.append(vout["index"])
                sys.stdout.write(" "+str(len(in_tios)))
                sys.stdout.write(" "+str(len(out_tios)))
                for a in in_tios:
                        sys.stdout.write(" "+str(a))
                for a in out_tios:
                        sys.stdout.write(" "+str(a))
                sys.stdout.write("\n")

        sys.stderr.write("block "+block_id+"\n")
        sys.stderr.flush()

```

## Application : address clustering
### Heuristic
#### [heuristic.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/heuristic.py)
```py
#heuristic.py

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




```

### Union-Find
#### [union-find-clusters.py](https://github.com/ethicnology/full-bitcoin-blockchain-data-made-easy/blob/main/src/code/union-find-clusters.py)
```py
#union-find-clusters.py

import sys
import argparse

# reads lines of the form "u v i o" meaning that u and v are in the same clusters;
# discards lines with a given value for i and o above a given threshold

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nodes", type=int, help="maximal node index", required=True)
parser.add_argument("-i", "--max_in", type=int, help="maximal number of input nodes; 0 if no limit", required=True)
parser.add_argument("-o", "--max_out", type=int, help="maximal number of output nodes; 0 if no limit", required=True)
args = parser.parse_args()

n,max_in,max_out = args.nodes,args.max_in,args.max_out
sys.stderr.write("%d nodes, max_in %d, max_out %d\n"%(n,max_in,max_out))

def union(x,y):
        if x!=y:
                S[x] = y

def find(x):
        y = x
        while S[x] != x:
                x = S[x]
        while S[y] != x: # path compression                                                                                                 
                (S[y],y) = (x,S[y])
        return x

sys.stderr.write("initializing...")
sys.stderr.flush()
S = list(range(n))
sys.stderr.write(" done.\n")
sys.stderr.flush()

sys.stderr.write("build clusters...")
sys.stderr.flush()
for line in sys.stdin:
        l = line.strip().split()
        assert(len(l)==4)
        [u,v,nb_in,nb_out] = [int(x) for x in l]
        assert(u>=0 and v>=0 and u<n and v<n and nb_in>=0 and nb_out>=0 and nb_in<=n and nb_out<=n)
        if (max_in==0 or nb_in <= max_in) and (max_out==0 or nb_out <= max_out):
                union(find(u),find(v))
sys.stderr.write(" done.\n")
sys.stderr.flush()

sys.stderr.write("output results...")
sys.stderr.flush()
sys.stdout.write("# node_id cluster_number\n")
nb_clusters = 0
clusters = {}
for i in range(n):
        c = find(i)
        if c not in clusters:
                clusters[c] = nb_clusters
                nb_clusters += 1
        sys.stdout.write("%d %d\n"%(i,clusters[c]))
sys.stderr.write(" done.\n")
sys.stderr.flush()


```