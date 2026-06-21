# Agnes API Key Setup

Use this reference when `AGNES_API_KEY` is missing, when the user asks how to get an Agnes API key, or when the user sends an API key and wants help configuring it.

## Getting an API Key

Official links:

- Agnes homepage: https://agnes-ai.com/
- Agnes documentation: https://agnes-ai.com/doc
- Quick start document: https://agnes-ai.com/doc/quick-start

Tell the user:

English:

1. Open https://agnes-ai.com/ and sign in or create an Agnes AI account.
2. Open the developer console or platform dashboard.
3. Go to `Settings` -> `API Keys`.
4. Click `Create new secret key`.
5. Copy the key once and keep it private.
6. Send the key here only if you want me to configure it for this machine/session.

中文：

1. 打开 https://agnes-ai.com/ 并登录或注册 Agnes AI 账号。
2. 进入开发者控制台或平台面板。
3. 进入 `Settings` -> `API Keys`。
4. 点击 `Create new secret key`。
5. 复制密钥并妥善保存，不要公开分享。
6. 如果希望我帮你配置，可以把 key 发给我，并说明是临时使用还是持续使用。

## If the User Sends a Key

Do not repeat the full key. Confirm with a masked form only.

Ask the user to choose:

- **Temporary / 临时使用**: use the key only for the current Agnes command, without saving it.
- **Persistent / 持续使用**: store it as the user-level `AGNES_API_KEY` environment variable for future Agnes commands.

If the user already clearly asked for temporary or persistent setup, proceed with that choice. For persistent setup, ask for explicit confirmation if not already given because it writes outside the project.

## Temporary Configuration

Use `--api-key` for the single command:

```bash
python scripts/agnes_image.py --api-key "USER_KEY" --prompt "..." --size 1024x768
```

or:

```bash
python scripts/agnes_video.py --api-key "USER_KEY" --prompt "..." --num-frames 121 --frame-rate 24
```

Do not save the key in files. Do not include the key in final output.

## Persistent Configuration

Preferred helper:

```bash
python scripts/agnes_key.py --set-user --stdin
```

Pass the key on stdin rather than printing it in the command line when possible. The helper stores a user-level environment variable and prints only a masked key.

After persistent setup, tell the user that new terminals may need to be reopened before `AGNES_API_KEY` is visible.

### Windows Manual Option

PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("AGNES_API_KEY", "USER_KEY", "User")
```

Current PowerShell session only:

```powershell
$env:AGNES_API_KEY = "USER_KEY"
```

### macOS/Linux Manual Option

Current shell session only:

```bash
export AGNES_API_KEY="USER_KEY"
```

Persistent shell profile example:

```bash
printf '\nexport AGNES_API_KEY=%q\n' "USER_KEY" >> ~/.zshrc
```

Use the user's actual shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.profile`) and ask before editing it.

## Checking Configuration

Run:

```bash
python scripts/agnes_key.py --check
```

or in PowerShell:

```powershell
$env:AGNES_API_KEY
```

Only report whether a key is present and a masked form. Never print the full key.
