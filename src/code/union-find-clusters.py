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

