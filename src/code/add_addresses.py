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