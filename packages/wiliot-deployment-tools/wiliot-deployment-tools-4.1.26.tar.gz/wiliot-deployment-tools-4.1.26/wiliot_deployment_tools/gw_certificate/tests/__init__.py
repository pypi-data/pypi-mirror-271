from wiliot_deployment_tools.gw_certificate.tests.coupling import CouplingTest
from wiliot_deployment_tools.gw_certificate.tests.downlink import DownlinkTest 
from wiliot_deployment_tools.gw_certificate.tests.connection import ConnectionTest
from wiliot_deployment_tools.gw_certificate.tests.uplink import UplinkTest
TESTS = [ConnectionTest, UplinkTest, DownlinkTest]
