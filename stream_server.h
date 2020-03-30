#pragma once

#include "esphome/core/component.h"

#include <memory>
#include <string>
#include <vector>
#include <Stream.h>
#include <ESPAsyncTCP.h>

class StreamServerComponent : public esphome::Component {
public:
    explicit StreamServerComponent(Stream *stream) : stream_{stream} {}

    void setup() override;
    void loop() override;
    void dump_config() override;
    void on_shutdown() override;

    void set_port(uint16_t port) { this->port_ = port; }

protected:
    void cleanup();
    void read();
    void write();

    struct Client {
        Client(AsyncClient *client, std::vector<uint8_t> &recv_buf);
        ~Client();

        AsyncClient *tcp_client{nullptr};
        std::string identifier{};
        bool disconnected{false};
    };

    Stream *stream_{nullptr};
    AsyncServer server_{0};
    uint16_t port_{6638};
    std::vector<uint8_t> recv_buf_{};
    std::vector<std::unique_ptr<Client>> clients_{};
};
