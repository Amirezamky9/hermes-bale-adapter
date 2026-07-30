# hermes-bale-adapter

<p align="center">
  <strong>📱 Bale platform adapter for <a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a></strong>
</p>

<p align="center">
  <a href="https://github.com/NousResearch/hermes-agent">
    <img src="https://img.shields.io/badge/Hermes-Agent-1.0+-blue" alt="Hermes Agent">
  </a>
  <a href="https://docs.bale.ai/">
    <img src="https://img.shields.io/badge/Bale-Bot%20API-green" alt="Bale Bot API">
  </a>
  <a href="https://github.com/Amirezamky9/hermes-bale-adapter/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT">
  </a>
</p>

---

## 📖 Overview

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) platform adapter for [Bale messenger](https://ble.ir/) (بله).

This plugin enables Hermes to communicate through Bale — an Iranian messaging platform with a Bot API nearly identical to Telegram's. The adapter leverages the `python-telegram-bot` library with a custom base URL, providing full feature parity with the built-in Telegram adapter.

> **Architecture:** Instead of reimplementing the entire adapter, this plugin clones the Telegram adapter's architecture and only overrides the base URL and platform identifier. This ensures all advanced features (streaming, inline keyboards, media handling, reconnection) work out of the box.

## ✨ Features

| Feature | Status |
|---------|--------|
| Long-polling (`getUpdates`) | ✅ |
| Text messages | ✅ |
| Streaming / edit messages | ✅ |
| Photo / video / voice / document send | ✅ |
| File upload & download | ✅ |
| Inline keyboard buttons | ✅ |
| Typing indicator | ✅ |
| Slash commands | ✅ |
| Reconnection & heartbeat | ✅ |
| Markdown formatting | ✅ |
| Cron job delivery | ✅ |
| Multi-user authorization | ✅ |
| Approval / clarify buttons | ✅ |
| Model picker | ✅ |

## 🚀 Installation

### Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com/docs/) installed and running
- A Bale bot token from [@botfather](https://ble.ir/botfather)

### 1. Clone this repo

```bash
cd ~/.hermes/plugins/platforms/
git clone https://github.com/Amirezamky9/hermes-bale-adapter.git bale
```

### 2. Set environment variables

Add to `~/.hermes/.env`:

```env
BALE_BOT_TOKEN=123456789:ABC123...
BALE_ALLOWED_USERS=66881162        # Your Bale user ID
BALE_HOME_CHANNEL=66881162         # Default chat ID for cron delivery
```

### 3. Enable in config

Add to `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - platforms/bale

gateway:
  platforms:
    bale:
      enabled: true
      extra:
        allow_from:
          - '66881162'
      home_channel:
        chat_id: '66881162'
        name: YourName
        platform: bale
      typing_indicator: true
```

### 4. Restart gateway

```bash
hermes gateway restart
```

## 🔧 Configuration Reference

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BALE_BOT_TOKEN` | ✅ | Bot token from @botfather |
| `BALE_ALLOWED_USERS` | ❌ | Comma-separated Bale user IDs |
| `BALE_ALLOW_ALL_USERS` | ❌ | Set to `true` to allow all users (dev only) |
| `BALE_HOME_CHANNEL` | ❌ | Default chat ID for cron / notifications |

### config.yaml Options

```yaml
gateway:
  platforms:
    bale:
      enabled: true
      token: "123456789:ABC..."    # Alternative to env var
      extra:
        allow_from: ['123456']     # Restrict to specific users
        base_url: "https://tapi.bale.ai"  # Override if needed
      home_channel:
        chat_id: '123456'
        name: YourName
        platform: bale
      typing_indicator: true
```

## 🐛 Troubleshooting

### Bot not connecting

```bash
# Test token with getMe
curl "https://tapi.bale.ai/bot$(grep BALE_BOT_TOKEN ~/.hermes/.env | cut -d= -f2)/getMe"
```

### Messages not received

1. Ensure the user has sent `/start` to the bot
2. Check `BALE_ALLOWED_USERS` includes the user's ID
3. Verify token is correct

### Gateway not loading plugin

```bash
# Debug plugin discovery
HERMES_PLUGINS_DEBUG=1 python3 -c "
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/hermes-agent'))
from hermes_cli.plugins import discover_plugins
discover_plugins()
" 2>&1 | grep bale
```

## 📁 Project Structure

```
hermes-bale-adapter/
├── README.md              # This file
├── LICENSE                # MIT License
├── plugin.yaml           # Plugin metadata
├── __init__.py           # Package init (exports register)
└── adapter.py            # BaleAdapter class (core logic)
```

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## 📚 References

- [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs/)
- [Bale Bot API Documentation](https://docs.bale.ai/)
- [Hermes Platform Adapter Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/platforms)
- [python-telegram-bot](https://docs.python-telegram-bot.org/)

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ for the Iranian developer community
</p>
