import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    DEVICE_CLASS_CONNECTIVITY,
    ENTITY_CATEGORY_DIAGNOSTIC,
)
from . import ns, StreamServerComponent

CONF_CONNECTED = "connected"
CONF_STREAM_SERVER = "stream_server"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_STREAM_SERVER): cv.use_id(StreamServerComponent),
        cv.Required(CONF_CONNECTED): binary_sensor.binary_sensor_schema(
            device_class=DEVICE_CLASS_CONNECTIVITY,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
    }
)


async def to_code(config):
    server = await cg.get_variable(config[CONF_STREAM_SERVER])

    sens = await binary_sensor.new_binary_sensor(config[CONF_CONNECTED])
    cg.add(server.set_connected_sensor(sens))
