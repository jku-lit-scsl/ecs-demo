import logging

from statemachine import StateMachine, State
from statemachine.exceptions import TransitionNotAllowed


class DefconHandler(StateMachine):
    "Defcon modes handler"

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

    def before_cycle(self, event: str, source: State, target: State, message: str = ""):
        message = ". " + message if message else ""

        return f"Running {event} from {source.id} to {target.id}{message}"

    def increase(self):
        try:
            self.do_increase()
        except TransitionNotAllowed as e:
            logging.warning(f'Escalate mode not possible: {str(e)}')

    def decrease(self):
        try:
            self.do_decrease()
        except TransitionNotAllowed as e:
            logging.warning(f'Decrease mode not possible: {str(e)}')

    def on_enter_defcon_4_monitoring(self):
        # TODO: increase monitoring of cpu
        pass

    def on_enter_defcon_3_adv_sec(self):
        # TODO: enable advanced detection model
        pass

    def on_enter_defcon_2_restrict(self):
        # TODO: only allow priority messages
        pass

    def on_enter_defcon_1_localize(self):
        # TODO: localize entirely
        pass
