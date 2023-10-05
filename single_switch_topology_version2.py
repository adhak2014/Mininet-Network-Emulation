from mininet.node import OVSKernelSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.net import Mininet

def topology():

    info("*** Create a network with OpenvSwitch switching capability\n")
    net = Mininet(topo = None, switch=OVSKernelSwitch)

    info("*** Create 6 hosts with base IP address 10.0.0.0/24\n")
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    h5 = net.addHost('h5', ip='10.0.0.5/24')
    h6 = net.addHost('h6', ip='10.0.0.6/24')
    
    info("*** Create 1 single openvswitch switch\n")
    s1 = net.addSwitch('s1', failMode='standalone')

    info("*** Add links between each host and the switch\n")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)
    net.addLink(h5, s1)
    net.addLink(h6, s1)

    info("*** Starting the network emulation \n")
    net.build()           # Build the emulated network 
    net.start()           # Start all nodes; controler, switches, and hosts
    
    info("*** Show all links\n")
    for link in net.links:
        print(link)
    print()
    
    info("*** Verify connectivity between all hosts\n")
    net.pingFull()

    info("*** Enter Mininet CLI. To exit, type “exit”\n")
    CLI(net)

    info("*** Stop the network emulation\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
