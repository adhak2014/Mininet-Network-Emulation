from mininet.node import Controller, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections

def topology():
    
    info("*** Create a network with OpenvSwitchKernel switching capability and Traffic Control     link\n")
    net = Mininet(switch=OVSKernelSwitch, link=TCLink)

    info("*** Create 2 hosts\n")
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    info("*** Create 1 single switch\n")
    s1 = net.addSwitch('s1')

    info("*** Create a controller running locally and listening at port 6653\n")
    c0 = net.addController('c0')

    info("*** Add links between each host and the switch\n")
    info("*** Each link is set to a specific bandwidth, delay, max_queue_size, and a loss rate")

    net.addLink(h1, s1, bw=10, delay='50ms', max_queue_size=1000, loss=10)
    net.addLink(h2, s1, bw=10, delay='100ms', max_queue_size=1000, loss=10)

    info("*** Starting the network emulation \n")
    net.start()

    info("*** Verify connectivity between h1 and h2\n")
    print(h1.cmd('ping -c10 %s'%h2.IP()))
    
    info("*** Dumping hosts connections\n")
    dumpNodeConnections(net.hosts)
    
    info("*** Stop the network emulation\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
