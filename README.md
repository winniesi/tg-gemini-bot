# tg-gemini-bot

[EN](README.md) | [简中](README_zh-CN.md) 

The tg-gemini-bot let's you use Google Gemini services right on your personal Telegram bot.

Super easy, just a single click and you've got it set up on Vercel.

![screen](./screenshots/screen.png)

## Features

- This is built with Flask - super straightforward and easy to develop.
- It's an all front-end project, and you can get it up and running on Vercel with just one click.
- Supports Gemini continuous conversation. (Due to Vercel's restrictions, conversations may not be saved for a long time)
- Supports Gemini text, images, videos, audio, voice messages, and video notes.
- Supports **system instruction** via `SYSTEM_INSTRUCTION` env var — customize bot personality and behavior.
- Supports replying to media messages with custom prompts.
- Default model `gemini-2.5-flash` for fast response (~1s latency).
- Shows typing indicator while waiting for Gemini response.

## Preparation

Get these things ready, and then fill them in as environment variables in Vercel.

- **GOOGLE_API_KEY**

  apply for your Google gemini pro api: https://makersuite.google.com/app/apikey

- **BOT_TOKEN**

  create your own telegram bot ([check the tutorial](https://flowxo.com/how-to-create-a-bot-for-telegram-short-and-simple-guide-for-beginners/)), obtain the token of the bot, which is in the format similar to: `67295022320:AAHmfuSQb0ZoUq0ycNPvgzqCCX7I1uzzaSE`

- **allowed USERS or GROUPS**

  Collect the user or group IDs that have access to this bot. You can separate them using any symbol in `,，;；` or spaces.

  You can also turn off authentication so everyone and groups can use it

  [learn more](#environment-variable)

## Get Started

1. Click [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fwinniesi%2Ftg-gemini-bot&env=BOT_TOKEN%2CGOOGLE_API_KEY%2CALLOWED_USERS&project-name=tg-gemini-bot&repository-name=tg-gemini-bot) to deploy to Vercel.

2. **Set the environment variable** according to the instructions below.

3. Once everything's done, visit the domain name of your Vercel project address. (Visiting the `Domains` instead of the `Deployment Domains` provided by Vercel for the project .)

   Or you could just click on `https://api.telegram.org/bot<bot-token>/setWebhook?url=<vercel-domain> ` to connect your Telegram bot to Vercel services. (remember to replace `<token>` and `<vercel-domain>` with your actual corresponding parameters)

![update_telegram_bot](./screenshots/visit_domains.png)

4. Fill in your telegram bot token on the page to associate telegram bot and vercel.

![update_telegram_bot](./screenshots/update_telegram_bot.png)

## Environment Variable

| Environment Variable | Required | Description                                                                                                                            |
| -------------------- | --- | -------------------------------------------------------------------------------------------------------------------------------------- |
| GOOGLE_API_KEY       | YES | Your Google gemini pro api, it looks like `AI2aS4Cl55F9ni9WN84Qn_KWRSuqXvUWkPq6kovc `                                                  |
| BOT_TOKEN            | YES | The Telegram bot token you applied for, it looks like `67295022320:AAHmfuSQb0ZoUq0ycNPvgzqCCX7I1uzzaSE`                                |
| ALLOWED_USERS        | YES | List the allowed user's Telegram IDs. If there's more than one person, you can separate them using any symbol in `,，;；` or spaces. and it should look like: `id1,id2`. Use `/get_my_info` to get your ID. |
| SYSTEM_INSTRUCTION | No | Custom system instruction for Gemini. Define bot personality, behavior rules, or domain expertise. Leave empty to use default behavior. |
| GEMINI_MODEL | No | Default Gemini model. Default is `gemini-2.5-flash`. Can be changed at runtime via `/set_model`. |

> **Note:** Group mode is not supported yet. This bot only works in private chats.

## Model

Default model is `gemini-2.5-flash` (fast, ~1s latency). Admins can switch models via `/set_model <model_name>` and check with `/get_model`. Use `/list_models` to see available options.

Tip: After modifying the environment variables, you need to redeploy them to take effect. You need to enter the internal console of the Vercel project, click the `Deployments` button at the top, select the `···` button to the right of the top item in the list, not the button directly to the right of the "Deployments" title! click `Redeploy` to redeploy.

## Command list

`/new` Start a new chat

`/get_my_info` Get your Telegram ID

`/get_model` Show current Gemini model

`/set_model` Switch Gemini model

`/list_models` List available models

`/help` Get help

## How to figure out what's wrong

So, if you've done everything step by step just like we talked about and your Telegram bot is still not doing its thing, then it's a good idea to poke around the Vercel logs to see what's up.

1. Open your project in vercel, click on the **Deployments** tab, check whether the deployment is successful, if there is an error, please modify according to the error prompt.

2. If no errors have occurred here, open the **Logs** tab, click on an erroneous log, and the program's output will be displayed on the right.

![screen](./screenshots/vercel_logs.png)

3. If there are any error messages, you can open an issue, and then provide the error information.

