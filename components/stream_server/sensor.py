import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    STATE_CLASS_MEASUREMENT,
    ENTITY_CATEGORY_DIAGNOSTIC,
)
from . import ns, StreamServerComponent

CONF_CONNECTION_COUNT = "connection_count"
CONF_STREAM_SERVER = "stream_server"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_STREAM_SERVER): cv.use_id(StreamServerComponent),
        cv.Required(CONF_CONNECTION_COUNT): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
    }
)


async def to_code(config):
    server = await cg.get_variable(config[CONF_STREAM_SERVER])

    sens = await sensor.new_sensor(config[CONF_CONNECTION_COUNT])
    cg.add(server.set_connection_count_sensor(sens))
