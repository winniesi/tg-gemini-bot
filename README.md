# tg-gemini-bot

[EN](README.md) | [简中](README_zh-CN.md)

A personal Telegram bot powered by Google Gemini. Deploy to Vercel in one click.

![screen](./screenshots/screen.png)

## Features

- Text chat with conversation memory (use `/new` to reset)
- Multi-media support: photos, videos, audio, voice messages, video notes
- Reply to any media with custom prompts
- System instruction via `SYSTEM_INSTRUCTION` — customize bot personality
- Default model `gemini-2.5-flash` (~1s latency), switchable at runtime
- Typing indicator while waiting for response
- ID-based access control — only authorized users can use the bot
- Multiple Google API keys supported (auto-rotate)

## Supported Media

| Type | How to send | Default prompt (no caption) |
|------|------------|-----------------------------|
| Photo | Send image | "describe this picture" |
| Video | Send video file | "describe what is happening in this video" |
| Audio | Send audio file | "transcribe this audio" |
| Voice | Record voice message | "transcribe this audio" |
| Video Note | Record video circle | "describe what is happening in this video" |

**Custom prompts:** Add a caption when sending media to override the default.

**Reply to media:** Reply to any media message with text — Gemini processes the media using your text as the prompt. For example, reply to a photo with "what color is the car?" or reply to a voice message with "summarize this in 3 words".

## Quick Start

1. Click [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fwinniesi%2Ftg-gemini-bot&env=BOT_TOKEN%2CGOOGLE_API_KEY%2CALLOWED_USERS&project-name=tg-gemini-bot&repository-name=tg-gemini-bot) to deploy.

2. Set the environment variables (see below), then redeploy.

3. Visit your Vercel project's **domain** (use the custom domain, not the `*.vercel.app` deployment URL). You'll see a setup page — enter your bot token to register the webhook.

   ![update_telegram_bot](./screenshots/visit_domains.png)

   ![update_telegram_bot](./screenshots/update_telegram_bot.png)

> **Alternative:** Skip the web page and register the webhook manually by visiting `https://api.telegram.org/bot<your-token>/setWebhook?url=<your-domain>`

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| GOOGLE_API_KEY | Yes | Google Gemini API key(s). Multiple keys supported — separate with commas. Get one at [Google AI Studio](https://makersuite.google.com/app/apikey). |
| BOT_TOKEN | Yes | Telegram bot token from [@BotFather](https://t.me/BotFather). |
| ALLOWED_USERS | Yes | Telegram user ID(s). Separate multiple with commas. Use `/get_my_info` in the bot to find your ID. |
| ALLOWED_GROUPS | No | Telegram group ID(s). Separate multiple with commas. Group IDs are negative numbers (e.g. `-5280543061`). Use `/get_my_info` in a group to find its ID. |
| SYSTEM_INSTRUCTION | No | Custom system prompt to define bot personality and behavior. |
| GEMINI_MODEL | No | Default model. Default: `gemini-2.5-flash`. Change at runtime via `/set_model`. |

## Group Chat Support

The bot supports group chats when configured via `ALLOWED_GROUPS`. In authorized groups, the bot only responds when @mentioned or when a user replies directly to a bot message. When the bot joins a group, it automatically sends the group ID so the admin can add it to `ALLOWED_GROUPS`.

> **Important:** You must disable Group Privacy in [@BotFather](https://t.me/BotFather) for the bot to receive group messages. Go to BotFather → `/mybots` → select your bot → **Bot Settings** → **Group Privacy** → **Turn off**. Then remove and re-add the bot to the group.

## Commands

| Command | Description |
|---------|-------------|
| `/new` | Start a new conversation (clears context) |
| `/set_model <name>` | Switch Gemini model |
| `/get_model` | Show current model |
| `/list_models` | List available models |
| `/get_my_info` | Get your Telegram user ID |
| `/help` | Show help |

## Tips

- **Conversation memory:** The bot remembers your chat history. Use `/new` to start fresh.
- **Cold starts:** On Vercel free tier, the first message after idle may take a few seconds. Subsequent messages are fast.
- **Custom prompts with media:** Don't just send a photo — add a caption like "translate the text in this image" for targeted results.
- **Reply trick:** See a Gemini response you want to follow up on? Reply to the original media with a new question.
- **Multiple API keys:** Separate with commas in `GOOGLE_API_KEY` to rotate keys and avoid rate limits.
- **After env changes:** Redeploy on Vercel (Deployments → ⋯ → Redeploy) to take effect.

## Troubleshooting

1. **Bot not responding?** Check **Deployments** tab for build errors.
2. **Deployed but silent?** Open **Logs** tab, send a test message, check for errors.
3. **Still stuck?** Open an [issue](https://github.com/winniesi/tg-gemini-bot/issues) with the error log.

![screen](./screenshots/vercel_logs.png)
