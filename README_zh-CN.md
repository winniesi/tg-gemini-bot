# tg-gemini-bot

[EN](README.md) | [简中](README_zh-CN.md) 

tg-gemini-bot 可让您直接在个人 Telegram 机器人上使用 Google Gemini 服务。

超级简单，只需单击一下，您就可以在 Vercel 上进行设置。

![screen](./screenshots/screen.png)

## 特点

- 这是用 Flask 构建的 - 超级简单且易于开发。
- 这是一个全前端项目，只需单击一下即可在 Vercel 上启动并运行。
- 支持Gemini连续通话。 （由于Vercel的限制，对话可能无法保存很长时间）
- 支持 Gemini 文本、图像界面和电报 Markdown。
- 支持通过 `SYSTEM_INSTRUCTION` 环境变量设置**系统指令** — 自定义机器人性格和行为。
- 默认模型 `gemini-2.5-flash`，响应速度快（约1秒延迟）。

## 准备工作

准备好这些东西，然后将它们作为Vercel中的环境变量填充。

- **GOOGLE_API_KEY**

  申请您的 Google Gemini Pro api: https://makersuite.google.com/app/apikey

- **BOT_TOKEN**

  创建您自己的电报机器人 ([查看教程](https://flowxo.com/how-to-create-a-bot-for-telegram-short-and-simple-guide-for-beginners/)), 获取机器人的token，格式类似: `67295022320:AAHmfuSQb0ZoUq0ycNPvgzqCCX7I1uzzaSE`

- **允许的用户或群组**

  收集有权访问此机器人的用户或群组 ID。 您可以使用`,，;；`中的任何符号或空格分隔它们。

  您还可以关闭身份验证，以便每个人和群组都可以使用它

  [了解更多](#环境变量)

## 开始使用

1. 点击 [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fwinniesi%2Ftg-gemini-bot&env=BOT_TOKEN%2CGOOGLE_API_KEY%2CALLOWED_USERS&project-name=tg-gemini-bot&repository-name=tg-gemini-bot) 部署到 Vercel。

2. 按照下面的说明，**设置环境变量**。

3. 一切完成后，访问您的 Vercel 项目地址的域名。 （访问 Vercel 为项目提供的"Domains"而不是"Deployment Domains"。）

   或者，您只需单击`https://api.telegram.org/bot<bot-token>/setWebhook?url=<vercel-domain>` 即可将 Telegram 机器人连接到 Vercel 服务。 （记得将 `<token>` 和 `<vercel-domain>`替换为您实际对应的参数）

![update_telegram_bot](./screenshots/visit_domains.png)

4. 在页面上填写您的 telegram bot token 以关联 telegram bot 和 vercel。

![update_telegram_bot](./screenshots/update_telegram_bot.png)

## 环境变量

| 环境变量 | 是否必须 | Description                                                                                                                            |
| -------------------- | --- | -------------------------------------------------------------------------------------------------------------------------------------- |
| GOOGLE_API_KEY       | 是 | 你的 Google Gemini Pro api，看起来像 `AI2aS4Cl55F9ni9WN84Qn_KWRSuqXvUWkPq6kovc `                                                  |
| BOT_TOKEN            | 是 | 您申请的 Telegram 机器人token，看起来像 `67295022320:AAHmfuSQb0ZoUq0ycNPvgzqCCX7I1uzzaSE`                                |
| ALLOWED_USERS        | 否 | 列出允许的用户的 Telegram ID。如果有多个，可以使用",，;；"中的任意符号或空格将他们分开。它应该看起来像：`id1,id2`。使用 `/get_my_info` 来获取您的 ID。 |
| SYSTEM_INSTRUCTION | 否 | 自定义系统指令。设定机器人性格、行为规则或专业领域。留空则使用默认行为。 |
| GEMINI_MODEL | 否 | 默认 Gemini 模型，默认 `gemini-2.5-flash`。可通过 `/set_model` 运行时切换。 |

> **注意：** 目前不支持群组模式，此机器人仅支持私聊。

## 模型

默认模型为 `gemini-2.5-flash`（快速，约1秒延迟）。管理员可通过 `/set_model <模型名>` 切换模型，`/get_model` 查看当前模型，`/list_models` 查看可用模型。

提示：修改环境变量后，需要重新部署才能生效。需要进入Vercel项目的内部控制台，点击顶部的`Deployments`按钮，选择列表顶部项右侧的`···`按钮，不是"Deployments"标题正右方的按钮！点击 `Redeploy` 即可重新部署。

## 命令列表

`/new` 开始新的聊天

`/get_my_info` 获取您的 Telegram ID

`/get_model` 显示当前 Gemini 模型

`/set_model` 切换 Gemini 模型

`/list_models` 列出可用模型

`/help` 获取帮助

`/help` 获取帮助

`/5g_test` :)

## 如何找出问题所在

因此，如果您已经按照我们所说的那样一步一步完成了所有操作，但您的 Telegram 机器人仍然没有执行其操作，那么最好查看 Vercel 日志以了解发生了什么情况。

1. 在vercel中打开您的项目，点击**Deployments**选项卡，检查部署是否成功，如果有错误，请根据错误提示进行修改。

2. 如果这里没有发生错误，打开**Logs**选项卡，单击错误日志，程序的输出将显示在右侧。

![screen](./screenshots/vercel_logs.png)

3. 如果有任何错误消息，您可以打开一个issue，然后提供错误信息。
