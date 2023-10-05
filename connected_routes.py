from mininet.node import OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.net import Mininet

def topology():
    
    net = Mininet(topo = None, switch=OVSSwitch, waitConnected=True)

    info("*** Creating a router\n")
    r1 = net.addHost('r1', ip='10.10.10.1/24')
    r1.cmd('ifconfig r1-eth2 10.20.20.1 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth3 10.30.30.1 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth4 10.40.40.1 netmask 255.255.255.0')
    r1.cmd('sysctl net.ipv4.ip_forward=1')
    
    info("*** Creating switches\n")
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')
    s3 = net.addSwitch('s3', failMode='standalone')
    s4 = net.addSwitch('s4', failMode='standalone')
 
    info("*** Creating switches to router links\n")
    net.addLink(s1, r1, intfName1='s1-eth1', intfName2='r1-eth1', params2={'ip':'10.10.10.1/24'})
    net.addLink(s2, r1, intfName1='s2-eth1', intfName2='r1-eth2', params2={'ip':'10.20.20.1/24'})
    net.addLink(s3, r1, intfName1='s3-eth1', intfName2='r1-eth3', params2={'ip':'10.30.30.1/24'})
    net.addLink(s4, r1, intfName1='s4-eth1', intfName2='r1-eth4', params2={'ip':'10.40.40.1/24'})
    
    info("*** Creating nodes\n")
    h1 = net.addHost('h1', ip='10.10.10.100/24', defaultRoute='via 10.10.10.1')
    h2 = net.addHost('h2', ip='10.20.20.100/24', defaultRoute='via 10.20.20.1')
    h3 = net.addHost('h3', ip='10.30.30.100/24', defaultRoute='via 10.30.30.1')
    h4 = net.addHost('h4', ip='10.40.40.100/24', defaultRoute='via 10.40.40.1')

    info("*** Creating hosts to switches links\n")
    net.addLink(h1, s1, intfName1='h1-eth0', intfName2='s1-eth2')
    net.addLink(h2, s2, intfName1='h2-eth0', intfName2='s2-eth2')
    net.addLink(h3, s3, intfName1='h3-eth0', intfName2='s3-eth2')
    net.addLink(h4, s4, intfName1='h4-eth0', intfName2='s4-eth2')

    info("*** Starting network\n")
    net.build()
    net.start()
 
    for link in net.links:
        print(link)
    print()
    
    net.pingFull()
    
    info( '*** Routing Table on Router:\n' )
    info(r1.cmd('route'))
    info(r1.cmd('ifconfig'))
    
    info("*** Enter Mininet CLI. To exit, type “exit”\n")
    CLI(net)

    info("*** Stop the network emulation\n")
    net.stop()
    
if __name__ == '__main__':
    setLogLevel('info')
    topology()
