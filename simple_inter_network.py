from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():
    net = Mininet(topo = None, build = False, ipBase = '10.0.0.0/8')
    info('*** Adding controller\n')

    info('*** Add Switch\n')
    s1 = net.addSwitch('s1', cls = OVSKernelSwitch, failMode = 'standalone')
    
    info('*** Add Routers\n')
    r1 = net.addHost('r1', cls = Node, intf = 'r1-eth1', ip = '10.0.0.1/24')
    r1.cmd('sysctl -w net.ipv4.ip_forward = 1')

    info('*** Add Hosts\n')
    h1 = net.addHost('h1', cls = Host, ip = '10.0.0.11/24', defaultRoute = 'via 10.0.0.1')
    h2 = net.addHost('h2', cls = Host, ip = '10.0.0.12/24', defaultRoute = 'via 10.0.0.1')
    h3 = net.addHost('h3', cls = Host, ip = '10.0.0.13/24', defaultRoute = 'via 10.0.0.1')
    h4 = net.addHost('h4', cls = Host, ip = '172.16.0.40/24', defaultRoute = 'via 172.16.0.1')
    info('*** Add Links\n')
    net.addLink(s1, r1, intName2 = 'r1-eth1', params2 = {'ip': '10.0.0.1/24'})
    net.addLink(h4, r1, intName2 = 'r1-eth2', params2 = {'ip': '172.16.0.1/24'})
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    info('*** Starting network\n')
    net.build()

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([])

    info('*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
