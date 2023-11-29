from secure_mod.defcon_handler import DefconHandler
from util.utils import setup

if __name__ == '__main__':
    setup()
    # mqtt_fw = MQTTForwarder()
    # mqtt_fw.publish("python/test", f"{get_current_time_in_millis()}")

    defcon_handler = DefconHandler()

    defcon_handler.increase()
    defcon_handler.decrease()

    # defcon_handler._graph().write_png("test_state_machine_internal.png")
