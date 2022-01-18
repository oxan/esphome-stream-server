# Copyright (C) 2022 Oxan van Leeuwen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_ID,
    CONF_DEVICE_CLASS,
    DEVICE_CLASS_CONNECTIVITY,
    CONF_ENTITY_CATEGORY,
    ENTITY_CATEGORY_DIAGNOSTIC,
)
from . import StreamServerComponent

CONF_STREAM_SERVER = "stream_server"

ns = binary_sensor.binary_sensor_ns
class_ = ns.class_("BinarySensor", binary_sensor.BinarySensor, cg.Component)

CONFIG_SCHEMA = binary_sensor.BINARY_SENSOR_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(class_),
        cv.Required(CONF_STREAM_SERVER): cv.use_id(StreamServerComponent),
        cv.Optional(CONF_DEVICE_CLASS, default=DEVICE_CLASS_CONNECTIVITY): binary_sensor.device_class,
        cv.Optional(CONF_ENTITY_CATEGORY, default=ENTITY_CATEGORY_DIAGNOSTIC): cv.entity_category,
    }
).extend(cv.COMPONENT_SCHEMA)

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield binary_sensor.register_binary_sensor(var, config)
    
    ss = yield cg.get_variable(config[CONF_STREAM_SERVER])
    cg.add(ss.register_connection_sensor(var))