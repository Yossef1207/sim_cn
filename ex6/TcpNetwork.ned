import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.StandardHost;

network SimpleTcpNetwork
{
    submodules:
        configurator: Ipv4NetworkConfigurator;
        client: StandardHost;
        server: StandardHost;
    connections allowunconnected:
        client.pppg++ <--> ned.DatarateChannel { delay = 400ms; datarate = 1Mbps; } <--> server.pppg++;
}
