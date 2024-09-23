Stream server for ESPHome
=========================

Custom component for ESPHome to expose a UART stream over WiFi or Ethernet. Provides a serial-to-wifi bridge as known
from ESPLink or ser2net, using ESPHome.

This component creates a TCP server listening on port 6638 (by default), and relays all data between the connected
clients and the serial port. It doesn't support any control sequences, telnet options or RFC 2217, just raw data.

Usage
-----

Requires ESPHome v2022.3.0 or newer.

```yaml
external_components:
  - source: github://wolffshots/esphome-stream-server

stream_server:
```

You can set the UART ID and port to be used under the `stream_server` component.

```yaml
uart:
   id: uart_bus
   # add further configuration for the UART here

stream_server:
   uart_id: uart_bus
   port: 1234
```

Sensors
-------
The server provides a binary sensor that signals whether there currently is a client connected:

```yaml
binary_sensor:
  - platform: stream_server
    connected:
      name: Connected
```

It also provides a numeric sensor that indicates the number of connected clients:

```yaml
sensor:
  - platform: stream_server
    connection_count:
      name: Number of connections
```

Advanced
--------
It is possible to define multiple stream servers for multiple UARTs simultaneously:

```yaml
uart:
  - id: uart1
    # ...
  - id: uart2
    # ...

stream_server:
  - uart_id: uart1
    port: 1234
  - uart_id: uart2
    port: 1235
```

The stream server has an internal buffer into which UART data is read before it is transmitted over TCP. The size of
this buffer can be changed using the `buffer_size` option, and must be a power of two. Increasing the buffer size above
the default of 128 bytes can help to achieve optimal throughput, and is especially helpful when using high baudrates. It
can also be necessary to increase the [`rx_buffer_size`][uart-config] option of the UART itself.

```yaml
stream_server:
    buffer_size: 2048
```

[uart-config]: https://esphome.io/components/uart.html#configuration-variables

The original project from [oxan](https://github.com/oxan) has been extended to include a whitelist of IPs that the 
server will connect to. This is not an ironclad protection against ne'er-do-wells but increases the barrier to entry for
messing with your serial devices.

One similar thing you could do is a similar change to add a "signing" field to the config so IPs need to do something extra to connect but that is out of scope for my changes.

To include a whitelist you would do the following:
```yaml
uart:
   id: uart_bus

stream_server:
   uart_id: uart_bus
   port: 1234
  whitelist:
    - 192.168.1.100
    - 192.168.1.102
```

If you want to debug why it wouldn't be connecting then you can enable debug logs with

```yaml
logger:
  baud_rate: 0
  level: debug
```

And then when a device attempts to connect and is denied you should see a log like this from the component:
```
[W][stream_server:090]: Client 192.168.1.105 is not whitelisted and will be disconnected.
[D][stream_server:072]: Current whitelist is:
[D][stream_server:074]: 	'192.168.1.101'
[D][stream_server:074]: 	'192.168.1.102'
```
