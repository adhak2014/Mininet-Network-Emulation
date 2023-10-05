from mininet.net import Mininet
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Intf

def myNetwork():
    net = Mininet(topo = None)

    info('*** Add Switch\n')
    s1 = net.addSwitch('s1', cls = OVSKernelSwitch, failMode = 'standalone')
    
    info('*** Add Routers\n')
    r1 = net.addHost('r1', cls = Node, intf = 'r1-eth1', ip = '10.0.0.1/24')

    info('*** Enable Routing\n')
    r1.cmd('sysctl net.ipv4.ip_forward=1')

    info('*** Add Hosts\n')
    h1 = net.addHost('h1', cls = Host, ip = '10.0.0.100/24', defaultRoute = 'via 10.0.0.1')
    h2 = net.addHost('h2', cls = Host, ip = '10.0.0.101/24', defaultRoute = 'via 10.0.0.1')
    h3 = net.addHost('h3', cls = Host, ip = '10.0.0.102/24', defaultRoute = 'via 10.0.0.1')
    h4 = net.addHost('h4', cls = Host, ip = '172.16.0.100/24', defaultRoute = 'via 172.16.0.1')

    info('*** Add Links\n')
    net.addLink(s1, r1, intName2 = 'r1-eth1', params2 = {'ip': '10.0.0.1/24'})
    net.addLink(h4, r1, intName2 = 'r1-eth2', params2 = {'ip': '172.16.0.1/24'})
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    info('*** Starting network\n')
    net.build()
    net.start()

    info("*** Enter Mininet CLI. To exit, type “exit”\n")
    CLI(net)

    info('*** Disable Routing\n')
    r1.cmd('sysctl net.ipv4.ip_forward=0')

    info("*** Stop the network emulation\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
