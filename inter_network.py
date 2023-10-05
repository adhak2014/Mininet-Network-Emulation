from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.node import Host, Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

def myNetwork():
    net = Mininet(topo = None)

    info('*** Add Switch\n')
    s1 = net.addSwitch('s1', cls = OVSKernelSwitch, failMode = 'standalone')
    s2 = net.addSwitch('s2', cls = OVSKernelSwitch, failMode = 'standalone')
    s3 = net.addSwitch('s3', cls = OVSKernelSwitch, failMode = 'standalone')
    s4 = net.addSwitch('s4', cls = OVSKernelSwitch, failMode = 'standalone')
    s5 = net.addSwitch('s5', cls = OVSKernelSwitch, failMode = 'standalone')
    s6 = net.addSwitch('s6', cls = OVSKernelSwitch, failMode = 'standalone')
    
    info('*** Add Routers\n')
    r1 = net.addHost('r1', cls = Node, intf = 'r1-eth1', ip = '192.168.1.1/24')
    r2 = net.addHost('r2', cls = Node, intf = 'r2-eth1', ip = '10.12.12.2/30')
    r3 = net.addHost('r3', cls = Node, intf = 'r3-eth1', ip = '192.168.3.1/24')
    r4 = net.addHost('r4', cls = Node, intf = 'r4-eth1', ip = '192.168.5.1/24')

    info('*** Add Hosts\n')
    h1 = net.addHost('h1', cls = Host, ip = '192.168.1.100/24', defaultRoute = 'via 192.168.1.1')
    h2 = net.addHost('h2', cls = Host, ip = '192.168.2.100/24', defaultRoute = 'via 192.168.2.1')
    h3 = net.addHost('h3', cls = Host, ip = '192.168.3.100/24', defaultRoute = 'via 192.168.3.1')
    h4 = net.addHost('h4', cls = Host, ip = '192.168.4.100/24', defaultRoute = 'via 192.168.4.1')
    h5 = net.addHost('h5', cls = Host, ip = '192.168.5.100/24', defaultRoute = 'via 192.168.5.1')
    h6 = net.addHost('h6', cls = Host, ip = '192.168.6.100/24', defaultRoute = 'via 192.168.6.1')
    
    info('*** Add Links\n')

    info('*** Switch to Router Links\n')
    net.addLink(s1, r1, intName2 = 'r1-eth1', params2 = {'ip': '192.168.1.1/24'})
    net.addLink(s2, r1, intName2 = 'r1-eth2', params2 = {'ip': '192.168.2.1/24'})
    net.addLink(s3, r3, intName2 = 'r3-eth1', params2 = {'ip': '192.168.3.1/24'})
    net.addLink(s4, r3, intName2 = 'r3-eth3', params2 = {'ip': '192.168.4.1/24'})
    net.addLink(s5, r4, intName2 = 'r4-eth1', params2 = {'ip': '192.168.5.1/24'})
    net.addLink(s6, r4, intName2 = 'r4-eth3', params2 = {'ip': '192.168.6.1/24'})

    info('*** Router to Router Links\n')
    net.addLink(r1, r2, intfName1='r1-eth3', intfName2='r2-eth1', params1={'ip': '10.12.12.1/30'}, params2={'ip': '10.12.12.2/30'})
    net.addLink(r2, r3, intfName1='r2-eth2', intfName2='r3-eth2', params1={'ip': '10.23.23.2/30'}, params2={'ip': '10.23.23.1/30'})
    net.addLink(r2, r4, intfName1='r2-eth3', intfName2='r4-eth2', params1={'ip': '10.24.24.2/30'}, params2={'ip': '10.24.24.1/30'})

    info('*** Host to Switch Links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(h4, s4)
    net.addLink(h5, s5)
    net.addLink(h6, s6)

    info('*** Starting network\n')
    net.build()
    net.start()

    info('*** Enable Routing\n')
    info(net['r1'].cmd("sysctl net.ipv4.ip_forward=1"))
    info(net['r2'].cmd("sysctl net.ipv4.ip_forward=1"))
    info(net['r3'].cmd("sysctl net.ipv4.ip_forward=1"))
    info(net['r4'].cmd("sysctl net.ipv4.ip_forward=1"))

    info('*** Add routes\n')

    info('*** Router r1\n')
    info(net['r1'].cmd("ip route add 10.23.23.0/30 via 10.12.12.2 dev r1-eth3"))
    info(net['r1'].cmd("ip route add 10.24.24.0/30 via 10.12.12.2 dev r1-eth3"))
    info(net['r1'].cmd("ip route add 192.168.3.0/24 via 10.12.12.2 dev r1-eth3"))
    info(net['r1'].cmd("ip route add 192.168.4.0/24 via 10.12.12.2 dev r1-eth3"))
    info(net['r1'].cmd("ip route add 192.168.5.0/24 via 10.12.12.2 dev r1-eth3"))
    info(net['r1'].cmd("ip route add 192.168.6.0/24 via 10.12.12.2 dev r1-eth3"))

    info('*** Router r2\n')
    info(net['r2'].cmd("ip route add 192.168.1.0/24 via 10.12.12.1 dev r2-eth1"))
    info(net['r2'].cmd("ip route add 192.168.2.0/24 via 10.12.12.1 dev r2-eth1"))
    info(net['r2'].cmd("ip route add 192.168.3.0/24 via 10.23.23.1 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 192.168.4.0/24 via 10.23.23.1 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 192.168.5.0/24 via 10.24.24.1 dev r2-eth3"))
    info(net['r2'].cmd("ip route add 192.168.6.0/24 via 10.24.24.1 dev r2-eth3"))

    info('*** Router r3\n')
    info(net['r3'].cmd("ip route add 192.168.1.0/24 via 10.23.23.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 192.168.2.0/24 via 10.23.23.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.12.12.0/30 via 10.23.23.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 192.168.5.0/24 via 10.23.23.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 192.168.6.0/24 via 10.23.23.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.24.24.0/30 via 10.23.23.2 dev r3-eth2"))

    info('*** Router r4\n')
    info(net['r4'].cmd("ip route add 192.168.1.0/24 via 10.24.24.2 dev r4-eth2"))
    info(net['r4'].cmd("ip route add 192.168.2.0/24 via 10.24.24.2 dev r4-eth2"))
    info(net['r4'].cmd("ip route add 10.12.12.0/30 via 10.24.24.2 dev r4-eth2"))
    info(net['r4'].cmd("ip route add 192.168.3.0/24 via 10.24.24.2 dev r4-eth2"))
    info(net['r4'].cmd("ip route add 192.168.4.0/24 via 10.24.24.2 dev r4-eth2"))
    info(net['r4'].cmd("ip route add 10.23.23.0/30 via 10.24.24.2 dev r4-eth2"))

    info("*** Enter Mininet CLI. To exit, type “exit”\n")
    CLI(net)

    info('*** Enable Routing\n')
    info(net['r1'].cmd("sysctl net.ipv4.ip_forward=0"))
    info(net['r2'].cmd("sysctl net.ipv4.ip_forward=0"))
    info(net['r3'].cmd("sysctl net.ipv4.ip_forward=0"))
    info(net['r4'].cmd("sysctl net.ipv4.ip_forward=0"))

    info("*** Stop the network emulation\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
