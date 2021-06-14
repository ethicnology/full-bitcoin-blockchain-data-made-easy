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