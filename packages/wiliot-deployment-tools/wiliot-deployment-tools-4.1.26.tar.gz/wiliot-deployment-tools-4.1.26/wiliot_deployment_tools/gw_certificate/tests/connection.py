import datetime
import time
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.gw_certificate.api_if.gw_capabilities import GWCapabilities
from wiliot_deployment_tools.gw_certificate.tests.generic import PASS_STATUS, GenericStage, GenericTest
from wiliot_deployment_tools.gw_certificate.api_if.api_validation import validate_message, MESSAGE_TYPES
from wiliot_deployment_tools.interface.mqtt import MqttClient

class ConnectionStage(GenericStage):
    def __init__(self, mqttc:MqttClient, **kwargs):
        self.mqttc = mqttc
        self.__dict__.update(kwargs)
        super().__init__(stage_name=type(self).__name__, **self.__dict__)
        
    def run(self):
        self.stage_pass = False
        input('Please unplug GW from power. Press enter when unplugged')
        self.mqttc.flush_messages()
        input('Please plug GW back to power. Press enter when plugged')
        debug_print('Waiting for GW to connect... (Timeout 3 minutes)')
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        status_message = None
        while datetime.datetime.now() < timeout and status_message is None:
            status_message = self.mqttc.get_status_message()
        if status_message is not None:
            self.add_to_stage_report('GW Status packet received:')
            debug_print(status_message)
            validation = validate_message(MESSAGE_TYPES.STATUS, status_message)
            self.stage_pass = validation[0]
            # set GW Capabilities:
            for key, value in status_message.items():
                if key in GWCapabilities.get_capabilities() and type(value) is bool:
                    self.gw_capabilities.set_capability(key, value)
                    self.add_to_stage_report(f'Set Capability: {key} - {value}')
            # Add reason test failed to report if neccessary
            self.add_to_stage_report(validation[1]) if not self.stage_pass else None
            # Add status packet to test report
            self.add_to_stage_report(str(status_message))
        else:
            self.add_to_stage_report("No message recieved from GW in status topic after 3 mins")
    
    def generate_stage_report(self):
        self.report_html = self.template_engine.render_template('stage.html', stage_name = self.stage_name, stage_pass=self.stage_pass, stage_report=self.report.split('\n'))
        debug_print(self.report)
        return super().generate_stage_report()
    

class ConnectionTest(GenericTest):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        self.stages = [ConnectionStage(**self.__dict__)]
        
    def run(self):
        super().run()
        self.test_pass = False
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.test_pass = stage.stage_pass
            self.add_to_test_report(stage.generate_stage_report())
