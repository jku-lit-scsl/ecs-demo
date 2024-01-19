import logging

from statemachine import StateMachine, State
from statemachine.exceptions import TransitionNotAllowed

from Adafruit_Python_DHT.examples.AdafruitDHT import set_qos_temperature
from config.config import network_conf
from secure_mod.intrusion_detector import set_max_calls
from secure_mod.monitoring_controller import MonitoringController
from util.setup import get_operating_mode, CLOUD_SERVER
from util.utils import send_update_knowledge_base, singleton


@singleton
class DefconHandler(StateMachine):
    """Defcon modes handler"""

    defcon_5_normal = State(initial=True)
    defcon_4_monitoring = State()
    defcon_3_adv_sec = State()
    defcon_2_restrict = State()
    defcon_1_localize = State()

    do_increase = (
            defcon_5_normal.to(defcon_4_monitoring)
            | defcon_4_monitoring.to(defcon_3_adv_sec)
            | defcon_3_adv_sec.to(defcon_2_restrict)
            | defcon_2_restrict.to(defcon_1_localize)
    )

    do_decrease = (
            defcon_1_localize.to(defcon_2_restrict)
            | defcon_2_restrict.to(defcon_3_adv_sec)
            | defcon_3_adv_sec.to(defcon_4_monitoring)
            | defcon_4_monitoring.to(defcon_5_normal)
    )

    def __init__(self, mqtt_receiver):
        # init base monitoring
        self.monController = MonitoringController(self)
        self.monController.start_monitoring()
        self.mqtt_receiver = mqtt_receiver
        self.previous_state = None
        super().__init__()

    def increase(self):
        self.previous_state = self.current_state
        try:
            self.do_increase()
            logging.info(f"Increased defcon mode to: {self.current_state.id}")

            if get_operating_mode() != CLOUD_SERVER:
                send_update_knowledge_base(self.current_state.id, network_conf['my_ip'])
        except TransitionNotAllowed as e:
            logging.warning(f'Increase defcon mode not possible: {str(e)}')

    def decrease(self):
        self.previous_state = self.current_state
        try:
            self.do_decrease()
            logging.info(f"Decreased defcon mode to: {self.current_state.id}")
            if get_operating_mode() != CLOUD_SERVER:
                send_update_knowledge_base(self.current_state.id, network_conf['my_ip'])
        except TransitionNotAllowed as e:
            logging.warning(f'Decrease defcon mode not possible: {str(e)}')

    def on_enter_defcon_5_normal(self):

        self.mqtt_receiver.set_ids(True)
        set_max_calls(150)

        # reset defcon 4
        self.monController.reset_frequency()
        pass

    def on_enter_defcon_4_monitoring(self):
        # set defcon 4
        new_fq = 0.5
        logging.info(f"Set new monitoring frequency of CPU load to: {new_fq}")
        self.monController.set_new_frequency(new_fq)
        set_max_calls(500)

        # reset defcon 3
        if self.mqtt_receiver:
            self.mqtt_receiver.set_ids(False)

    def on_enter_defcon_3_adv_sec(self):
        set_max_calls(1000)
        set_qos_temperature(0)
        # set defcon 3

    def on_enter_defcon_2_restrict(self):
        set_max_calls(1500)
        if self.previous_state.id == 'defcon_1_localize':
            self.mqtt_receiver.start_broker_service()
        set_qos_temperature(2)

    def on_enter_defcon_1_localize(self):
        self.mqtt_receiver.stop_broker_service()
        # send critical data via websockets
        pass

    def get_current_state(self):
        return self.current_state.id
