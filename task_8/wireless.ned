
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.StandardHost;
import inet.node.inet.Router;
import inet.node.wireless.AccessPoint;
import inet.physicallayer.wireless.ieee80211.packetlevel.Ieee80211ScalarRadioMedium;
import inet.visualizer.canvas.integrated.IntegratedCanvasVisualizer;

network SimpleWlanFtp
{
    @display("bgb=400,200;bgi=background/terrain,s");
    
    submodules:
        // Visualizer
        visualizer: IntegratedCanvasVisualizer {
            @display("p=50,50;is=s");
        }
        
        // Network configurator
        configurator: Ipv4NetworkConfigurator {
            @display("p=50,100;is=s");
        }
        
        // Radio medium
        radioMedium: Ieee80211ScalarRadioMedium {
            @display("p=50,150;is=s");
        }
        
        // Wireless client (FTP client)
        ftp_cli: StandardHost {
            @display("p=50,150;i=device/laptop");
        }
        
        // Access Point
        ap: AccessPoint {
            @display("p=125,150;i=device/accesspoint");
        }
        
        dsl_router: Router {
            @display("p=200,150;i=device/router");
        }
        
        // ISP Router
        isp_router: Router {
            @display("p=275,150;i=device/router");
        }
        
        // FTP Server
        ftp_srv: StandardHost {
            @display("p=350,150;i=device/server");
        }
	connections:
        // Ethernet connection: AP to DSL Router (100 Mbps)
        ap.ethg++ <--> {  datarate = 100Mbps; delay = 1ms; } <--> dsl_router.ethg++;
        
        // DSL connection: DSL Router to ISP Router (simulated with PPP)
        dsl_router.pppg++ <--> {  datarate = 40Mbps; delay = 10ms; } <--> isp_router.pppg++;
        
        // Internet connection: ISP Router to Server (100 Mbps)
        isp_router.ethg++ <--> {  datarate = 100Mbps; delay = 20ms; } <--> ftp_srv.ethg++;
}