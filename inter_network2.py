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

    info('*** Add Switches\n')
    s1 = net.addSwitch('s1', cls = OVSKernelSwitch, failMode = 'standalone')
    s2 = net.addSwitch('s2', cls = OVSKernelSwitch, failMode = 'standalone')
    s3 = net.addSwitch('s3', cls = OVSKernelSwitch, failMode = 'standalone')

    info('*** Add Routers\n')
    r1 = net.addHost('r1', cls = Node, intf = 'r1-eth0', ip = '209.165.201.11/27')
    r2 = net.addHost('r2', cls = Node, intf = 'r2-eth0', ip = '209.165.201.1/27')
    r1.cmd('sysctl -w net.ipv4.ip_forward = 1')
    r2.cmd('sysctl -w net.ipv4.ip_forward = 1')

    info('*** Add Hosts\n')
    h1 = net.addHost('h1', cls = Host, ip = '192.168.0.11/24', defaultRoute = 'via 192.168.0.1')
    h2 = net.addHost('h2', cls = Host, ip = '192.168.0.12/24', defaultRoute = 'via 192.168.0.1')
    h3 = net.addHost('h3', cls = Host, ip = '192.168.0.13/24', defaultRoute = 'via 192.168.0.1')
    h4 = net.addHost('h4', cls = Host, ip = '192.168.0.14/24', defaultRoute = 'via 192.168.0.1')
    h5 = net.addHost('h5', cls = Host, ip = '209.165.200.235/27', defaultRoute = 'via 209.165.200.225')
    h6 = net.addHost('h6', cls = Host, ip = '209.165.200.236/27', defaultRoute = 'via 209.165.200.225')
    h7 = net.addHost('h7', cls = Host, ip = '192.168.1.17/24', defaultRoute = 'via 192.168.1.1')
    h8 = net.addHost('h8', cls = Host, ip = '192.168.1.18/24', defaultRoute = 'via 192.168.1.1')
    h9 = net.addHost('h9', cls = Host, ip = '198.51.100.171/24', defaultRoute = 'via 198.51.100.1')
    h10 = net.addHost('h10', cls = Host, ip = '209.165.202.133/27', defaultRoute = 'via 209.165.202.129')
    h11 = net.addHost('h11', cls = Host, ip = '203.0.113.202/24', defaultRoute = 'via 203.0.113.1')
    
    info('*** Add Links\n')
    net.addLink(r1, r2, intName2 = 'r2-eth0', params2 = {'ip': '209.165.201.1/27'})

    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(h5, s2)
    net.addLink(h6, s2)
    net.addLink(h7, s3)
    net.addLink(h8, s3)
    net.addLink(s1, r1, intName2 = 'r1-eth1', params2 = {'ip': '209.165.200.225/27'})
    net.addLink(s2, r1, intName2 = 'r1-eth2', params2 = {'ip': '192.168.0.1/24'})
    net.addLink(s3, r1, intName2 = 'r1-eth3', params2 = {'ip': '192.168.1.1/24'})
    net.addLink(h9, r2, intName2 = 'r2-eth1', params2 = {'ip': '198.51.100.1/24'})
    net.addLink(h10, r2, intName2 = 'r2-eth2', params2 = {'ip': '209.165.202.129/27'})
    net.addLink(h11, r2, intName2 = 'r2-eth3', params2 = {'ip': '203.0.113.1/24'})   
    info('*** Starting network\n')
    net.build()

    
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s3').start([])

    info('*** Add routes\n')
    r1.cmd('ip route add default via 209.165.201.1')
    r2.cmd('ip route add to 209.165.200.224/27 via 209.165.201.11')
    r2.cmd('ip route add to 192.168.0.0/16 via 209.165.201.11')

    info('*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
