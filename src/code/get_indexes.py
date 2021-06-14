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