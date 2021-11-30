/* Copyright (C) 2020-2021 Oxan van Leeuwen
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

#include "stream_server.h"

#include "esphome/core/log.h"
#include "esphome/core/util.h"

#if ESPHOME_VERSION_CODE >= VERSION_CODE(2021, 10, 0)
#include "esphome/components/network/util.h"
#endif

static const char *TAG = "streamserver";

using namespace esphome;

void StreamServerComponent::setup() {
  ESP_LOGCONFIG(TAG, "Setting up stream server...");
  this->recv_buf_.reserve(128);

  this->server_ = AsyncServer(this->port_);
  this->server_.begin();
  this->server_.onClient(
      [this](void *h, AsyncClient *tcpClient) {
        if (tcpClient == nullptr)
          return;

        this->clients_.push_back(std::unique_ptr<Client>(new Client(tcpClient, this->recv_buf_)));
      },
      this);
}

void StreamServerComponent::loop() {
  this->cleanup();
  this->read();
  this->write();
}

void StreamServerComponent::cleanup() {
  auto discriminator = [](std::unique_ptr<Client> &client) { return !client->disconnected; };
  auto last_client = std::partition(this->clients_.begin(), this->clients_.end(), discriminator);
  for (auto it = last_client; it != this->clients_.end(); it++)
    ESP_LOGD(TAG, "Client %s disconnected", (*it)->identifier.c_str());

  this->clients_.erase(last_client, this->clients_.end());
}

void StreamServerComponent::read() {
  int len;
  while ((len = this->stream_->available()) > 0) {
    char buf[128];
    len = std::min(len, 128);
#if ESPHOME_VERSION_CODE >= VERSION_CODE(2021, 10, 0)
    this->stream_->read_array(reinterpret_cast<uint8_t *>(buf), len);
#else
    this->stream_->readBytes(buf, len);
#endif
    for (auto const &client : this->clients_)
      client->tcp_client->write(buf, len);
  }
}

void StreamServerComponent::write() {
#if ESPHOME_VERSION_CODE >= VERSION_CODE(2021, 10, 0)
  this->stream_->write_array(this->recv_buf_);
  this->recv_buf_.clear();
#else
  size_t len;
  while ((len = this->recv_buf_.size()) > 0) {
    this->stream_->write(this->recv_buf_.data(), len);
    this->recv_buf_.erase(this->recv_buf_.begin(), this->recv_buf_.begin() + len);
  }
#endif
}

void StreamServerComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "Stream Server:");
  ESP_LOGCONFIG(TAG, "  Address: %s:%u",
#if ESPHOME_VERSION_CODE >= VERSION_CODE(2021, 10, 0)
                esphome::network::get_ip_address().str().c_str(),
#else
                network_get_address().c_str(),
#endif
                this->port_);
}

void StreamServerComponent::on_shutdown() {
  for (auto &client : this->clients_)
    client->tcp_client->close(true);
}

StreamServerComponent::Client::Client(AsyncClient *client, std::vector<uint8_t> &recv_buf)
    : tcp_client{client}, identifier{client->remoteIP().toString().c_str()}, disconnected{false} {
  ESP_LOGD(TAG, "New client connected from %s", this->identifier.c_str());

  this->tcp_client->onError([this](void *h, AsyncClient *client, int8_t error) { this->disconnected = true; });
  this->tcp_client->onDisconnect([this](void *h, AsyncClient *client) { this->disconnected = true; });
  this->tcp_client->onTimeout([this](void *h, AsyncClient *client, uint32_t time) { this->disconnected = true; });

  this->tcp_client->onData(
      [&](void *h, AsyncClient *client, void *data, size_t len) {
        if (len == 0 || data == nullptr)
          return;

        auto buf = static_cast<uint8_t *>(data);
        recv_buf.insert(recv_buf.end(), buf, buf + len);
      },
      nullptr);
}

StreamServerComponent::Client::~Client() { delete this->tcp_client; }
