import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import ned.DatarateChannel;



network OperatorNetwork
{
    @display("bgb=905,479");
    types:
        channel GatewayToBackbone extends DatarateChannel
        {
            delay = 10ms;
            datarate = 10Mbps;
        }
        channel BackboneToAccess extends DatarateChannel
        {
            delay = 15ms; //
            datarate = 2Mbps;
        }
        channel ISDNLink extends DatarateChannel
        {
            delay = 40ms;
            datarate = 64kbps;
        }


    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=60,115");
        }
        gateway: Router {
            @display("p=160,115");
        }

        // Backbone Routers
        backbone[5]: Router {
            @display("p=291,128");
        }

        // Access Routers
        access[25]: Router {
            @display("p=419,134");
        }

        // Users
        user[625]: StandardHost {
            @display("p=587,134");
        }

    connections allowunconnected:
        // Gateway to Backbone
        for i=0..4 {
            gateway.pppg++ <--> GatewayToBackbone <--> backbone[i].pppg++;
        }

        // Backbone to Access
        for k=0..24 {
            backbone[int(floor(k / 5))].pppg++ <--> BackboneToAccess <--> access[k].pppg++;
        }

        // Access to Users
        for k=0..624 {
            access[int(floor(k / 25))].pppg++ <--> ISDNLink <--> user[k].pppg++;
        }
}
