import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.StandardHost;
import inet.linklayer.ethernet.EtherSwitch;

network UdpNetwork
{
    types:
        channel EthLink extends ned.DatarateChannel {
            delay = 1ms;
            datarate = 100Mbps;
        }
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=200,50");
        }
        client: StandardHost {
            @display("p=100,200");
        }
        server: StandardHost {
            @display("p=300,200");
        }
    connections allowunconnected:
        client.ethg++ <--> EthLink <--> server.ethg++;
}