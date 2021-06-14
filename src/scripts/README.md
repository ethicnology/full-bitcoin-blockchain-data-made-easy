---
sidebar: auto
sidebarDepth: 0
---

# Scripts

## Collection
### prerequisites
[Setup a bitcoin node.](https://bitcoin.org/en/full-node#setup-a-full-node)  

For **Linux** you can follow these steps
#### Download
```sh
wget https://bitcoincore.org/bin/bitcoin-core-0.21.1/bitcoin-0.21.1-x86_64-linux-gnu.tar.gz
```

#### Untar
```sh
tar xzf bitcoin-0.21.1-x86_64-linux-gnu.tar.gz
```

#### Install
```sh
sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-0.21.1/bin/*
```

#### Configure
In your **/home/** folder create a **.bitcoin** folder and a **bitcoin.conf**
```sh
mkdir ~/.bitcoin && touch ~/.bitcoin/bitcoin.conf
```

Use your favorite editor to configure your node
```ini
# Enable Remote Procedure Call
server=1
# Default RPC port
rpcport=8332
# Needed for RPC Auth
rpcuser=<Username>
# Needed for RPC Auth
rpcpassword=<Strong>
```

#### Usage
Run your node using **bitcoind**
```sh
bitcoind --daemon
```
> **_NOTE:_** If you run this command for the first time, you need to wait full synchronization with the bitcoin network, **it take hours and ~300 Go**.  



### extract
Please install [blockchain-ekstrakto](https://github.com/ethicnology/blockchain-ekstrakto) tool to extract blockchain dataset.  
Follow **README.md** instructions.

```sh
nohup python3 blockchain-ekstrakto.py --source 674000 2> blockchain.err | > blockchain.DSC &
```
> **_NOTE:_** time ~58 hours, output ~2.1 To.  

### reverse
```sh
nohup tac blockchain.DSC | python3 add_addresses.py | gzip -c > blockchain.ASC.gz &
```
> **_NOTE:_** time ~28 hours, output ~548 Go.

## Indexing
### prerequisites
```sh
export LC_ALL=C
```

### step 1
```sh
nohup zcat blockchain.ASC.gz | python3 make_list.py 2> step1.err | gzip -c > step1.gz &
```
> **_NOTE:_** time ~22 hours, output ~150 Go.  

### step 2
```sh
nohup zcat blockchain.ASC.gz | python3 get_addresses.py 2> step2.err | sort -T. -S10g --parallel=24 -k1,1 -k2,2n | awk 'BEGIN{old="none";}{if ($1!=old) print $0; old=$1;}' | sort -T. -S 10g --parallel=24 -nk2,2 | awk '{print "-1",$1,NR-1;}' | gzip -c > step2.gz &
```
> **_NOTE:_** time ~19 hours, output ~22 Go.  

### step 3
```sh
nohup zcat -c step1.gz step2.gz | sort -S 10g -T . -r -k2,3 --parallel=24 | gzip -c > step3.gz &
```
> **_NOTE:_** time ~6 hours, output ~99 Go.  

### step 4
```sh
nohup zcat step3.gz | python3 list_translate.py 2> step4.err | gzip -c > step4.gz &
```
> **_NOTE:_** time ~2 hours, output ~12 Go.  

### step 5
```sh
nohup zcat step4.gz | sort -S 10g -T . -nk1,1 --parallel=24 | gzip -c > step5.gz &
```
> **_NOTE:_** time ~3 hours, output ~37 Go.  

### step 6
```sh
nohup zcat blockchain.ASC.gz | python3 json_translate.py --file step5.gz 2> step6.err | gzip -c > blockchain.indexed.gz &
```
> **_NOTE:_** time ~? hours, output ~581 Go.  

### usage
```sh
nohup zcat blockchain.indexed.gz | python3 get_indexes.py 2> get_indexes.err &
```
```sh
gzip index_txids & gzip index_tios & gzip index_addresses &
```
> **_NOTE:_** time ~6 hours, output ~75 Go.


## Distillation
### prerequisites
```sh
tail -n 1 step6.err | gzip -c > blockchain.header.gz
# {"blocks": 674001, "vouts": 1673052718, "addresses": 797002334, "txids": 623483734}
```

### addresses
```sh
nohup gunzip -c blockchain.header.gz blockchain.indexed.gz | python3 distillation_addresses.py 2> distillation_addresses.err | gzip -c > blockchain.addresses.distilled.gz &
```
> **_NOTE:_** time ~25 hours, output ~12 Go.

### amounts
```sh
nohup gunzip -c blockchain.header.gz blockchain.indexed.gz | python3 distillation_amounts.py 2> distillation_amounts.err | gzip -c > blockchain.amounts.distilled.gz &
```
> **_NOTE:_** time ~400 hours.

### tios
```sh
nohup gunzip -c blockchain.header.gz blockchain.indexed.gz | python3 distillation_tios.py 2> distillation_tios.err | gzip -c > blockchain.tios.distilled.gz &
```

## Application : address clustering
### Heuristic
```sh
nohup zcat blockchain.distilled.gz | python3 heuristic.py 2> heuristic.err | gzip -c > heuristic.gz &
```
> **_NOTE:_** time ~22 minutes, output ~4 Go.    

### Union-Find
```sh
nohup zcat heuristic.gz | python3 union-find-clusters.py -n 797002334 -i 0 -o 0 2> union-find-clusters.err | gzip -c > clusters.gz &
```
> **_NOTE:_** time ~15 minutes, output ~3.8 Go.    