/* Copyright (C) 2020-2022 Oxan van Leeuwen
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#pragma once

#include "esphome/core/component.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "stream_server.h"

class StreamServerBinarySensor : public esphome::binary_sensor::BinarySensor, public esphome::Component {
 public:
  void set_stream_server(StreamServerComponent *stream_server) { stream_server_ = stream_server; }

  void loop() override;

  float get_setup_priority() const override { return esphome::setup_priority::DATA; }

 protected:
  StreamServerComponent *stream_server_;
};
