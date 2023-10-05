from mininet.node import OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.net import Mininet

def topology():
    'Create a network'
    net = Mininet(topo = None, switch=OVSSwitch, waitConnected=True)

    info("*** Creating switches\n")
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')
 
    info("*** Creating two routers\n")
    r1 = net.addHost('r1')
    r1.cmd('ifconfig r1-eth1 192.168.10.250/24')
    r1.cmd('ifconfig r1-eth2 10.0.0.1 netmask 255.255.255.252')
    r1.cmd('sysctl net.ipv4.ip_forward=1')
    
    r2 = net.addHost('r2')
    r2.cmd('ifconfig r2-eth1 192.168.20.250/24')
    r2.cmd('ifconfig r2-eth2 10.0.0.2 netmask 255.255.255.252')
    r2.cmd('sysctl net.ipv4.ip_forward=1')
    
    info("*** Creating router to router link\n")
    net.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2', params1={'ip':'10.0.0.1/30'}, params2={'ip':'10.0.0.2/30'})
    info("*** Creating switches to router links\n")
    net.addLink(s1, r1, intfName1='s1-eth3', intfName2='r1-eth1', params2={'ip':'192.168.10.250/24'})
    net.addLink(s2, r2, intfName1='s2-eth3', intfName2='r2-eth1', params2={'ip':'192.168.20.250/24'})
    
    info("*** Creating nodes\n")
    h1 = net.addHost('h1', ip='192.168.10.100/24', defaultRoute='via 192.168.10.250')
    h2 = net.addHost('h2', ip='192.168.10.101/24', defaultRoute='via 192.168.10.250')
    h3 = net.addHost('h3', ip='192.168.20.100/24', defaultRoute='via 192.168.20.250')
    h4 = net.addHost('h4', ip='192.168.20.101/24', defaultRoute='via 192.168.20.250')

    info("*** Creating hosts to switches links\n")
    net.addLink(h1, s1, intfName1='h1-eth0', intfName2='s1-eth1')
    net.addLink(h2, s1, intfName1='h2-eth0', intfName2='s1-eth2')
    net.addLink(h3, s2, intfName1='h3-eth0', intfName2='s2-eth1')
    net.addLink(h4, s2, intfName1='h4-eth0', intfName2='s2-eth2')

    info("*** Starting network\n")
    
    net.build()
    net.start()
    
    r1.cmd('ip route add to 192.168.20.0/24 via 10.0.0.2')
    r2.cmd('ip route add to 192.168.10.0/24 via 10.0.0.1')
    
    for link in net.links:
        print(link)
    print()
    
    net.pingFull()
    
    info( '*** Routing Table on Router:\n' )
    info(r1.cmd('route'))
    info(r1.cmd('ifconfig'))
    print()
    info(r2.cmd('route'))
    info(r2.cmd('ifconfig'))
     
    info("*** Enter Mininet CLI. To exit, type “exit”\n")
    CLI(net)

    info("*** Stop the network emulation\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
