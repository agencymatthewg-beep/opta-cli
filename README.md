# Opta CLI

> **Enhanced Claude Code** — All the best AI CLI features, combined.

**Opta CLI** is an enhanced version of Claude Code that brings together the best features from across the AI coding tool ecosystem. It maintains full compatibility with Claude Code while adding production-grade middleware, enhanced provider support, terminal theming, and advanced multi-agent capabilities.

> **Note:** This repository will be transferred to the [`optamize`](https://github.com/optamize) organization.  
> Current base: Fork of [Aider v0.86.2](https://github.com/Aider-AI/aider)

---

## 🚀 Installation

```bash
pip install opta-cli
```

### Requirements
- Python 3.9 or later
- API key for your preferred LLM provider (Claude, GPT-4, etc.)

---

## ⚡ Quick Start

### Interactive Mode
```bash
opta
```

Start an interactive coding session. Opta will help you build, refactor, and debug code.

### Print Mode
```bash
opta -p "explain how this function works"
```

Get instant answers without entering interactive mode.

### Continue Conversation
```bash
opta -c
```

Resume your last conversation.

### With Specific Model
```bash
opta --model opus
opta --model sonnet
```

### Pipe Input
```bash
cat app.py | opta -p "add error handling"
```

---

## ✨ Features

### Claude Code Compatibility
- **Interactive REPL** — Natural conversation with your codebase
- **MCP Integration** — Full Model Context Protocol server support
- **Subagents** — Delegate tasks to specialized AI agents
- **Session Management** — Auto-save and resume conversations
- **Permission System** — Fine-grained control over allowed tools
- **Memory & Context** — OPTA.md files for persistent instructions
- **Git Integration** — Auto-commits with AI-generated messages

### Enhanced Beyond Claude Code

#### Production Middleware
- **Retry logic** with exponential backoff
- **Circuit breaker** for failing services
- **Rate limiting** to prevent quota exhaustion
- **Token tracking** — Real-time usage display

#### Enhanced Providers
- **15+ LLM Providers** — Claude, GPT-4, Gemini, Perplexity, Groq, Mistral, watsonx, and more
- **Local models** — Ollama, LMStudio, LocalAI support
- **Smart model selection** — Cost optimization

#### Terminal Experience
- **8 Terminal Themes** — Monokai, Dracula, Solarized, Nord, Gruvbox, Tomorrow, GitHub, Default
- **Shell mode toggle** — Ctrl-X to switch between AI and shell
- **Streaming improvements** — Better real-time feedback

#### IDE Integration
- **VS Code extension** — Full IDE experience (planned)
- **ACP support** — Agent Client Protocol for Zed, JetBrains (planned)
- **File watching** — Auto-trigger on save

#### Multi-Agent Orchestration
- **Agent swarms** — Sequential, hierarchical, and graph patterns
- **Parallel execution** — Multiple agents working simultaneously
- **Agent marketplace** — Pre-built agent templates (planned)

---

## 📖 Usage Examples

### Start with Files
```bash
opta app.py utils.py
```

### Add MCP Server
```bash
opta mcp add @modelcontextprotocol/server-filesystem
```

### Use Subagents
```bash
opta --agents agents.json
```

### Set Spending Limit
```bash
opta --max-budget-usd 5.00
```

### Auto-commit Changes
```bash
opta --auto-commits
```

---

## 🎨 Terminal Themes

Switch themes with:
```bash
opta --theme dracula
```

Available themes: `monokai`, `dracula`, `solarized-dark`, `solarized-light`, `nord`, `gruvbox-dark`, `gruvbox-light`, `tomorrow-night`, `github`, `default`

---

## 🔧 Configuration

### Global Config
```bash
opta config set model sonnet
opta config set auto-commits true
```

### OPTA.md Files
Create an `OPTA.md` file in your project root for persistent instructions:

```markdown
# Project Context
This is a Flask API that handles user authentication.

## Code Style
- Use type hints
- Prefer dataclasses over dicts
- Maximum line length: 100 characters

## Testing
Run tests with: pytest tests/
```

Opta will automatically load these instructions in every session.

---

## 🤖 Subagents

Define specialized agents in `agents.json`:

```json
{
  "agents": [
    {
      "name": "test-writer",
      "description": "Writes unit tests",
      "model": "sonnet",
      "tools": ["write_file", "read_file"]
    },
    {
      "name": "code-reviewer",
      "description": "Reviews code for bugs",
      "model": "opus",
      "tools": ["read_file"]
    }
  ]
}
```

Opta will automatically invoke the right agent based on your request.

---

## 🔌 MCP Integration

Connect to Model Context Protocol servers:

```bash
# Add a server
opta mcp add @modelcontextprotocol/server-filesystem

# List connected servers
opta mcp list

# Configure with file
opta --mcp-config mcp-config.json
```

---

## 🛠️ Advanced Features

### Shell Mode Toggle
Press **Ctrl-X** to toggle between AI mode and shell mode. Execute shell commands without leaving Opta.

### Permission Modes
```bash
# Plan mode - ask before executing
opta --permission-mode plan

# Restrict tools
opta --disallowedTools delete_file,exec

# Skip permissions (use with caution!)
opta --dangerously-skip-permissions
```

### Session Management
```bash
# Resume by ID
opta -r abc123

# Fork a session
opta --fork-session abc123

# Link to GitHub PR
opta --from-pr https://github.com/user/repo/pull/123
```

---

## 📊 Supported Models

| Provider | Models | Notes |
|----------|--------|-------|
| Anthropic | Claude Opus, Sonnet, Haiku | Recommended |
| OpenAI | GPT-4, GPT-4 Turbo | Excellent |
| Google | Gemini 2.0 Flash | Fast & affordable |
| Groq | Llama 3.3 70B | Extremely fast |
| Perplexity | Sonar models | Web-enhanced |
| Local | Ollama, LMStudio | Privacy-focused |

Full list: [Supported Models](https://aider.chat/docs/llms.html)

---

## 🎯 Roadmap

### v1.0 (MVP) — Current
- [x] Claude Code parity
- [x] Production middleware
- [x] Enhanced providers
- [x] Terminal theming
- [ ] Documentation complete

### v1.5 (Enhanced)
- [ ] VS Code extension
- [ ] ACP support for Zed/JetBrains
- [ ] Enhanced agent marketplace
- [ ] K2.5 local swarm optimization

### v2.0 (Full Vision)
- [ ] Multi-agent orchestration UI
- [ ] Full OpenClaw ecosystem integration
- [ ] Agent collaboration patterns
- [ ] Performance dashboard

---

## 📚 Documentation

- **Getting Started** — [Quick Start Guide](https://opta-cli.optamize.biz/docs/quick-start)
- **Configuration** — [Config Reference](https://opta-cli.optamize.biz/docs/config)
- **MCP Servers** — [MCP Guide](https://opta-cli.optamize.biz/docs/mcp)
- **Subagents** — [Agent Guide](https://opta-cli.optamize.biz/docs/agents)
- **API Reference** — [API Docs](https://opta-cli.optamize.biz/docs/api)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📜 License

Apache 2.0 — See [LICENSE.txt](LICENSE.txt)

This project is a fork of [Aider](https://github.com/Aider-AI/aider) by Paul Gauthier.

---

## 💬 Community

- **GitHub Issues** — [Report bugs or request features](https://github.com/optamize/opta-cli/issues)
- **Discord** — Coming soon
- **Twitter** — [@optamize](https://twitter.com/optamize)

---

## 🙏 Acknowledgments

Built on the excellent foundation of [Aider](https://github.com/Aider-AI/aider) by Paul Gauthier and contributors.

Incorporates ideas and features from:
- [MCP-CLI](https://github.com/modelcontextprotocol/cli) — Production middleware
- [Kimi-CLI](https://github.com/kimi-ai/kimi-cli) — Shell mode integration
- [Continue](https://github.com/continuedev/continue) — IDE patterns
- [Swarms](https://github.com/kyegomez/swarms) — Multi-agent orchestration

---

<p align="center">
  <strong>Opta CLI — What Claude Code should be.</strong>
</p>
