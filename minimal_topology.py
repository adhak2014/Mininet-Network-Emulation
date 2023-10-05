from mininet.net import Mininet
from mininet.topo import MinimalTopo
from mininet.node import OVSKernelSwitch
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

myTopo = MinimalTopo()
net = Mininet(topo = myTopo, switch = OVSKernelSwitch)

net.start()
dumpNodeConnections(net.hosts)
print('*' * 50)
for link in net.links:
        print(link)
print('*' * 50)
net.pingAll()
print('*' * 50)
h1, h2 = net.hosts[0], net.hosts[1]
print(h1.cmd('ping -c2 %s'%h2.IP()))

info("*** Enter Mininet CLI. To exit, type “exit”\n")
CLI(net)

info("*** Stop the network emulation\n")
net.stop()
