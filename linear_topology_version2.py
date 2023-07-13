from mininet.node import Controller, OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.net import Mininet

def topology():
    
    info("*** Create a network with OpenvSwitch switching capability\n")
    net = Mininet(switch=OVSSwitch)

    info("*** Create a controller running locally and listening at port 6653\n")
    c0 = net.addController('c0', ip='127.0.0.1', port=6653, protocols="OpenFlow13")

    info("*** Create 4 hosts with base IP address 172.31.0.0/24 and predefined MAC addresses\n")
    h1 = net.addHost('h1', mac="00:00:00:00:11:11", ip='172.31.0.1/24')
    h2 = net.addHost('h2', mac="00:00:00:00:22:22", ip='172.31.0.2/24')
    h3 = net.addHost('h3', mac="00:00:00:00:33:33", ip='172.31.0.3/24')
    h4 = net.addHost('h4', mac="00:00:00:00:44:44", ip='172.31.0.4/24')

    net.startTerms()
    
    info("*** Create 4 single switches\n")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    info("*** Add links between each host and a switch\n")
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(h4, s4)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s4)

    info("*** Starting the network emulation \n")
    net.build()         # Build the emulated network
    c0.start()          # Start the controller
    s1.start([c0])      # Start switch s1 
    s2.start([c0])      # Start switch s2
    s3.start([c0])      # Start switch s3
    s4.start([c0])      # Start switch s4
    
    info("*** Show all links\n")
    for link in net.links:
        print(link)
    print()
    
    info("*** Verify connectivity between all hosts\n")
    net.pingFull()

    info("*** Enter Mininet CLI. To exit, type “exit”\n")
    CLI(net)

    info("*** Stop the terminal of all hosts\n")
    net.stopXterms()

    info("*** Stop the network emulation\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
