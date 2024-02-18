# tg-gemini-bot

The tg-gemini-bot let's you use Google Gemini services right on your personal Telegram bot.

Super easy, just a single click and you've got it set up on Vercel.

![screen](./screenshots/screen.png)

🚀 If you don't want to deploy it yourself, you can use this deployment-free telegram bot: [GeminiBot](https://t.me/geminipro_api_bot). This bot is a fork from this project, providing completely identical features.

## Features

- This is built with Flask - super straightforward and easy to develop.
- It's an all front-end project, and you can get it up and running on Vercel with just one click.
- Supports Gemini continuous conversation. (Due to Vercel's restrictions, conversations may not be saved for a long time)
- Supports both Gemini text, image interface, and telegram markdown.

## Preparation

Get these things ready, and then fill them in as environment variables in Vercel.

- **GOOGLE_API_KEY**

  apply for your Google gemini pro api: https://makersuite.google.com/app/apikey

- **BOT_TOKEN**

  create your own telegram bot ([check the tutorial](https://flowxo.com/how-to-create-a-bot-for-telegram-short-and-simple-guide-for-beginners/)), obtain the token of the bot, which is in the format similar to: `67295022320:AAHmfuSQb0ZoUq0ycNPvgzqCCX7I1uzzaSE`

- **ALLOWED_USERS**

  Gather the Telegram usernames of users who are permitted to access this bot, separating them with a comma (`,`). The usernames should be formatted like this: `name1,name2`.
  You can also choose to turn off auch. [learn more](#environment-variable)

## Get Started

1. Click [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fwinniesi%2Ftg-gemini-bot&env=BOT_TOKEN%2CGOOGLE_API_KEY%2CALLOWED_USERS&project-name=tg-gemini-bot&repository-name=tg-gemini-bot) to deploy to Vercel.

2. **Set the environment variable** according to the instructions below.

3. Once everything's done, visit the domain name of your Vercel project address. (Visiting the `Domains` instead of the `Deployment Domains` provided by Vercel for the project .)

   Or you could just click on `https://api.telegram.org/bot<bot-token>/setWebhook?url=<vercel-domain> ` to connect your Telegram bot to Vercel services. (remember to replace <token> with your actual corresponding parameters)

![update_telegram_bot](./screenshots/visit_domains.png)

4. Fill in your telegram bot token on the page to associate telegram bot and vercel.

![update_telegram_bot](./screenshots/update_telegram_bot.png)

## Environment Variable

| Environment Variable | Required | Description                                                                                                                            |
| -------------------- | --- | -------------------------------------------------------------------------------------------------------------------------------------- |
| GOOGLE_API_KEY       | YES | Your Google gemini pro api, it looks like `AI2aS4Cl55F9ni9WN84Qn_KWRSuqXvUWkPq6kovc `                                                  |
| BOT_TOKEN            | YES | The Telegram bot token you applied for, it looks like `67295022320:AAHmfuSQb0ZoUq0ycNPvgzqCCX7I1uzzaSE`                                |
| ALLOWED_USERS        | No | List the allowed Telegram usernames. If there's more than one person, just split them with `,` and it should look like: `name1,name2`.Including the `@` symbol is optional, so either `ohmorningsir` or `@ohmorningsir` is acceptable. No need to be case sensitive. If you do not set a username, you can use id instead.use `/get_my_info` to get. |
| IS_DEBUG_MODE | No | Whether to enable debug mode. `0` to disenable. `1` to enable. Default is `0` . |
| ADMIN_ID | No | ten-digit telegramID. If you want to enable debug mode, this value must be set correctly |
| AUCH_ENABLE | No | `0` to disenable auth. Anyone can use this bot. `1` to enable auth. Enabled by default. |

## How to figure out what's wrong

So, if you've done everything step by step just like we talked about and your Telegram bot is still not doing its thing, then it's a good idea to poke around the Vercel logs to see what's up.

1. Open your project in vercel, click on the **Deployments** tab, check whether the deployment is successful, if there is an error, please modify according to the error prompt.

2. If no errors have occurred here, open the **Logs** tab, click on an erroneous log, and the program's output will be displayed on the right.

![screen](./screenshots/vercel_logs.png)

3. If there are any error messages, you can open an issue, and then provide the error information.
