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
