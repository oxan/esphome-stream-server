# Copyright (C) 2023 Oxan van Leeuwen
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
from esphome.components import sensor
from esphome.const import (
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
			entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
		)
	}
)

async def to_code(config):
	server = await cg.get_variable(config[CONF_STREAM_SERVER])

	sens = await sensor.new_sensor(config[CONF_CONNECTION_COUNT])
	cg.add(server.set_connection_count_sensor(sens))
