import logging

from statemachine import StateMachine, State
from statemachine.exceptions import TransitionNotAllowed

from secure_mod.monitoring_controller import MonitoringController
from util.mqtt_forwarder import MQTTForwarder


class DefconHandler(StateMachine):
    """Defcon modes handler"""

    def __init__(self, mqtt_fw: MQTTForwarder):
        # init base monitoring
        self.monController = MonitoringController(mqtt_fw)
        self.monController.start_monitoring()
        super().__init__()

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

    def increase(self):
        try:
            self.do_increase()
            logging.info(f"Increased defcon mode to: {self.current_state.id}")
        except TransitionNotAllowed as e:
            logging.warning(f'Increase defcon mode not possible: {str(e)}')

    def decrease(self):
        try:
            self.do_decrease()
            logging.info(f"Decreased defcon mode to: {self.current_state.id}")
        except TransitionNotAllowed as e:
            logging.warning(f'Decrease defcon mode not possible: {str(e)}')

    def on_enter_defcon_5_normal(self):
        self.monController.reset_frequency()
        pass


    def on_enter_defcon_4_monitoring(self):
        new_fq = 0.5
        logging.info(f"Set new monioting frequency to: {new_fq}")
        self.monController.set_new_frequency(new_fq)

    def on_enter_defcon_3_adv_sec(self):
        # TODO: count mqtt messages
        pass

    def on_enter_defcon_2_restrict(self):
        # TODO: disable mqtt
        pass

    def on_enter_defcon_1_localize(self):
        # TODO: shutdown device
        pass
