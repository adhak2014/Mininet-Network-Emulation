from mininet.net import Mininet
from mininet.topolib import TreeTopo

tree = TreeTopo(depth = 2, fanout = 2)
net = Mininet(topo = tree)
net.start()
h1, h2, h3, h4 = net.hosts[0], net.hosts[1], net.hosts[2], net.hosts[3]
print(h1.cmd('ping -c2 %s'%h2.IP()))
print(h1.cmd('ping -c2 %s'%h3.IP()))
print(h1.cmd('ping -c2 %s'%h4.IP()))
net.stop()
