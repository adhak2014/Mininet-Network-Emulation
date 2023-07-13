from mininet.node import Controller, OVSSwitch
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.link import TCLink

def topology():
    'Create a network and controller'
    net = Mininet(autoStaticArp=True, switch=OVSSwitch)
    c0 = net.addController('c0', ip='127.0.0.1', port=6653)

    info("*** Creating nodes\n")
    
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')

    s1 = net.addSwitch('s1')

    info("*** Adding Link\n")
    link1 = net.addLink(h1, s1, cls=TCLink); print(link1.intf1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    info("*** Starting network\n")
    net.build()
    net.start()

    
    info("*** h1 ifconfig\n")
    print(h1.cmd('ifconfig'))

    info("*** Configuring one intf with bandwidth of 5 Mbps\n")
    link1.intf1.config(bw=1)
    info("*** Running iperf to test\n")
    net.iperf((h1, h2), l4Type='TCP')
    print(h1.cmd('ping -c4 10.0.0.2'))

    info("*** Configuring one intf with loss of 50%\n")
    link1.intf1.config(loss=50)
    info("*** Running iperf to test\n")
    net.iperf((h1, h3), l4Type='UDP')
    print(h1.cmd('ping -c4 10.0.0.2'))

    info("*** Configuring one intf with delay of 100ms\n")
    link1.intf1.config(delay='100ms')
    info("*** Running iperf to test\n")
    net.iperf((h1, h4), l4Type='TCP')
    print(h1.cmd('ping -c4 10.0.0.2'))

    s1.cmdPrint('ovs-vsctl show')
    net.pingFull()

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
