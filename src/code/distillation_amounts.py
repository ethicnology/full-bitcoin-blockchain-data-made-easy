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
