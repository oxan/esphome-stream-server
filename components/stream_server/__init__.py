import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID, CONF_PORT, CONF_BUFFER_SIZE

# ESPHome doesn't know the Stream abstraction yet, so hardcode to use a UART for now.

AUTO_LOAD = ["socket"]

DEPENDENCIES = ["uart", "network"]

MULTI_CONF = True

ns = cg.global_ns
StreamServerComponent = ns.class_("StreamServerComponent", cg.Component)


def validate_buffer_size(buffer_size):
    if buffer_size & (buffer_size - 1) != 0:
        raise cv.Invalid("Buffer size must be a power of two.")
    return buffer_size


CONFIG_SCHEMA = cv.All(
    cv.require_esphome_version(2022, 3, 0),
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(StreamServerComponent),
            cv.Optional(CONF_PORT, default=6638): cv.port,
            cv.Optional(CONF_BUFFER_SIZE, default=128): cv.All(
                cv.positive_int, validate_buffer_size
            ),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    cg.add(var.set_port(config[CONF_PORT]))
    cg.add(var.set_buffer_size(config[CONF_BUFFER_SIZE]))

    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
