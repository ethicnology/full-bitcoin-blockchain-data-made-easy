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
