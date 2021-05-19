import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID, CONF_PORT

# ESPHome doesn't know the Stream abstraction yet, so hardcode to use a UART for now.

DEPENDENCIES = ["uart"]

MULTI_CONF = True

StreamServerComponent = cg.global_ns.class_("StreamServerComponent", cg.Component)

CONFIG_SCHEMA = (
	cv.Schema(
		{
			cv.GenerateID(): cv.declare_id(StreamServerComponent),
			cv.Optional(CONF_PORT): cv.port,
		}
	)
		.extend(cv.COMPONENT_SCHEMA)
		.extend(uart.UART_DEVICE_SCHEMA)
)

def to_code(config):
	var = cg.new_Pvariable(config[CONF_ID])
	if CONF_PORT in config:
		cg.add(var.set_port(config[CONF_PORT]))

	yield cg.register_component(var, config)
	yield uart.register_uart_device(var, config)
