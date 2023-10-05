from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI

myTopo = LinearTopo(k = 4)
net = Mininet(topo = myTopo, switch = OVSKernelSwitch)
net.start()
for link in net.links:
        print(link)
h1, h2, h3, h4 = net.hosts[0], net.hosts[1], net.hosts[2], net.hosts[3]
print(h1.cmd('ping -c2 %s'%h2.IP()))
print(h1.cmd('ping -c2 %s'%h3.IP()))
print(h1.cmd('ping -c2 %s'%h4.IP()))

info("*** Enter Mininet CLI. To exit, type “exit”\n")
CLI(net)

info("*** Stop the network emulation\n")
net.stop()
