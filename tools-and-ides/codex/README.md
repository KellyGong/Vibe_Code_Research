<h1 align="center">OpenAI Codex</h1>

<p align="center">
  <b>OpenAI's coding agent — Desktop, Extension & CLI</b><br>
  <sub>Three ways to use the same powerful model</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenAI-Codex-412991?logo=openai" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/Desktop_%7C_Extension_%7C_CLI-3_forms-blue" alt="Forms"/>
</p>

---

<details open>
<summary><b>English</b></summary>

## What It Is

**Codex** is OpenAI's coding agent. It comes in three forms so you can code in the IDE, in the terminal, or in a standalone app.

## Three Forms

| Form | Description |
|------|-------------|
| **Codex Desktop** | Standalone app with full IDE-like editing and agent flow |
| **Codex Extension** | VS Code extension — use Codex inside VS Code (or Cursor) |
| **Codex CLI** | Open-source terminal agent; run from the command line |

## Limits & Pricing

- **5-hour rolling limit** — Usage is capped over a rolling 5-hour window
- **Weekly cap** — Additional weekly limit applies
- For typical usage, these limits feel **effectively unlimited**; heavy sustained use may hit the caps

Pricing is tied to your OpenAI account; within the above limits, cost is low (often negligible for normal use).

## Codex Extension on Remote Servers (Reverse Proxy Setup)

When you use VS Code / Cursor to SSH into a remote server (e.g. HPC cluster, cloud VM), the Codex Extension runs on the **remote side** and needs to reach OpenAI's API. If the remote server has no direct internet access (or can't reach OpenAI), you need a **reverse SSH tunnel** to route traffic through your local machine's proxy.

### How It Works

```
[Remote Server]  →  SSH reverse tunnel  →  [Your Mac/PC localhost:7891 (Clash proxy)]  →  OpenAI API
     :17890       ←────────────────────        :7891
```

The remote server sends requests to its own `localhost:17890`, which is tunneled back to your local machine's proxy (e.g. Clash on port 7891), and from there out to the internet.

### Step 1: SSH Config (on your local machine)

Add a `-proxy` variant of your SSH host in `~/.ssh/config`:

```ssh-config
# Normal connection (no proxy)
Host my-server
    HostName your.server.address
    User your_username
    IdentityFile ~/.ssh/id_rsa

# Connection with reverse tunnel for Codex
Host my-server-proxy
    HostName your.server.address
    User your_username
    IdentityFile ~/.ssh/id_rsa
    RemoteForward 17890 127.0.0.1:7891
    ExitOnForwardFailure no

    # Disable connection multiplexing to avoid tunnel conflicts
    ControlMaster no
    ControlPersist no
    ControlPath none
```

**Key line:** `RemoteForward 17890 127.0.0.1:7891` — this forwards the remote server's port `17890` to your local Clash proxy on port `7891`. Adjust `7891` to match your local proxy's port.

### Step 2: Connect via the proxy host

In VS Code / Cursor, connect to `my-server-proxy` (not `my-server`). This establishes the reverse tunnel automatically.

### Step 3: Set proxy env vars on the remote server

On the remote server, tell the Codex Extension to use the tunnel:

```bash
# Add to ~/.bashrc or ~/.zshrc on the remote server
export HTTP_PROXY="http://127.0.0.1:17890"
export HTTPS_PROXY="http://127.0.0.1:17890"
export http_proxy="http://127.0.0.1:17890"
export https_proxy="http://127.0.0.1:17890"
```

Then `source ~/.bashrc` or reconnect. The Codex Extension will now route API calls through the tunnel → your local proxy → OpenAI.

### Step 4: Verify

On the remote server, test that the tunnel is working:

```bash
curl -x http://127.0.0.1:17890 https://api.openai.com
```

If you get a response (even an auth error), the tunnel is working. If it times out, check that your local proxy (Clash) is running and listening on the correct port.

## Pros

- **Cheap / free within limits** — Most users stay under the caps
- **Strong model** — Same capable coding model across all three forms
- **Choice of interface** — Pick Desktop, Extension, or CLI to match your workflow

## Cons

- **Slower execution** — Agent steps can feel slower than some alternatives
- **Extension + SSH/remote** — Using the VS Code extension on a remote server requires a reverse tunnel setup (see above)

## Links

- [Codex](https://codex.openai.com) / [OpenAI Codex](https://openai.com/codex)
- [Codex CLI (open-source)](https://github.com/openai/codex)

</details>

---

<details>
<summary><b>中文</b></summary>

## 简介

**Codex** 是 OpenAI 的编程智能体，提供三种形态：桌面应用、VS Code 扩展和命令行 CLI，可在 IDE、终端或独立应用中编码。

## 三种形态

| 形态 | 说明 |
|------|------|
| **Codex Desktop** | 独立桌面应用，具备类 IDE 编辑与智能体流程 |
| **Codex Extension** | VS Code 扩展，在 VS Code（或 Cursor）内使用 Codex |
| **Codex CLI** | 开源终端智能体，在命令行中运行 |

## 额度与定价

- **5 小时滚动额度** — 在滚动 5 小时窗口内有限制
- **周额度** — 另有每周上限
- 对多数用户而言，这些限制相当于 **几乎无限**；长时间高负载可能触顶

费用与 OpenAI 账户绑定；在额度内成本很低（日常使用常可忽略）。

## Codex Extension 远程服务器配置（反向代理）

通过 VS Code / Cursor SSH 连接远程服务器（如 HPC 集群、云主机）时，Codex Extension 运行在 **远程端**，需要访问 OpenAI API。如果远程服务器无法直接上网（或无法访问 OpenAI），需要通过 **SSH 反向隧道** 把流量转回本地代理。

### 原理

```
[远程服务器]  →  SSH 反向隧道  →  [你的 Mac/PC localhost:7891 (Clash 代理)]  →  OpenAI API
   :17890      ←──────────────       :7891
```

远程服务器把请求发到自己的 `localhost:17890`，通过隧道转回本地 Clash 代理（7891 端口），再由本地出网。

### 第一步：SSH 配置（本地机器）

在本地 `~/.ssh/config` 中添加一个带反向隧道的 Host：

```ssh-config
# 普通连接（不走代理）
Host my-server
    HostName your.server.address
    User your_username
    IdentityFile ~/.ssh/id_rsa

# 带反向隧道的连接（用于 Codex）
Host my-server-proxy
    HostName your.server.address
    User your_username
    IdentityFile ~/.ssh/id_rsa
    RemoteForward 17890 127.0.0.1:7891
    ExitOnForwardFailure no

    # 禁用连接复用，避免隧道冲突
    ControlMaster no
    ControlPersist no
    ControlPath none
```

**关键行：** `RemoteForward 17890 127.0.0.1:7891` — 把远程的 17890 端口转发到本地 Clash 代理的 7891 端口。请根据你本地代理的实际端口调整 `7891`。

### 第二步：用 proxy Host 连接

在 VS Code / Cursor 中连接 `my-server-proxy`（不是 `my-server`），这样 SSH 连接时会自动建立反向隧道。

### 第三步：在远程服务器设置代理环境变量

在远程服务器上，让 Codex Extension 走这个隧道：

```bash
# 写入远程服务器的 ~/.bashrc 或 ~/.zshrc
export HTTP_PROXY="http://127.0.0.1:17890"
export HTTPS_PROXY="http://127.0.0.1:17890"
export http_proxy="http://127.0.0.1:17890"
export https_proxy="http://127.0.0.1:17890"
```

然后 `source ~/.bashrc` 或重新连接。Codex Extension 的 API 请求就会走：隧道 → 本地代理 → OpenAI。

### 第四步：验证

在远程服务器上测试隧道是否通畅：

```bash
curl -x http://127.0.0.1:17890 https://api.openai.com
```

如果有响应（哪怕是认证错误），说明隧道正常。如果超时，检查本地 Clash 是否运行且监听正确端口。

## 优点

- **在额度内便宜/免费** — 多数用户不会超限
- **模型强** — 三种形态共用同一套强编码模型
- **接口可选** — 按习惯选 Desktop、Extension 或 CLI

## 缺点

- **执行偏慢** — 智能体步骤可能比部分替代方案慢
- **Extension + SSH/远程** — 远程服务器上使用需配置反向隧道（见上方教程）

## 链接

- [Codex](https://codex.openai.com) / [OpenAI Codex](https://openai.com/codex)
- [Codex CLI（开源）](https://github.com/openai/codex)

</details>
