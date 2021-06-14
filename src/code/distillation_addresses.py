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