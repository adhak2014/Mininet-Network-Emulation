from mininet.net import Mininet
from mininet.topo import MinimalTopo
from mininet.node import OVSKernelSwitch

myTopo = MinimalTopo()
net = Mininet(topo = myTopo, switch = OVSKernelSwitch)
net.start()
for link in net.links:
        print(link)
h1, h2 = net.hosts[0], net.hosts[1]
print(h1.cmd('ping -c2 %s'%h2.IP()))
net.stop()
