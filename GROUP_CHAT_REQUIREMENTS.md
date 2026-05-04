# Group Chat Support Requirements

## Overview
Add Telegram group chat support to the bot. Currently only private chats work.

## Environment Variable
- `ALLOWED_GROUPS`: Comma-separated group IDs (e.g. `-5280543061,-123456789`)
- Empty or unset = no groups allowed

## Behavior Rules

### In authorized groups (group_id in ALLOWED_GROUPS):
- Only respond when bot is @mentioned (e.g. `@tg_ai_test_bot what is 1+1`)
- Only respond when user replies directly to a bot message
- Ignore all other group messages

### In unauthorized groups:
- When bot is @mentioned, reply with the group ID and instructions to add it to ALLOWED_GROUPS

### Bot joins a new group / group just created:
- Automatically send a message with the group ID, so the admin knows what to add to ALLOWED_GROUPS

### /get_my_info command:
- In private chat: return user ID (existing behavior)
- In group: return group ID

## Technical Notes
- Group IDs are negative numbers (e.g. `-5280543061`)
- Telegram Update structure for groups: `message.chat.type` = `"group"` or `"supergroup"`, `message.chat.id` is the group ID
- Bot @mention detection: check `message.entities` for type `mention` with bot username, or `text` starts with `@bot_username`
- `new_chat_members` field in update indicates bot was added to a group
- Vercel serverless, no persistence

## Files to modify
- `api/config.py` — add ALLOWED_GROUPS, group-related messages
- `api/telegram.py` — add group detection helpers to Update class (chat_type, is_mentioned, replied_to_bot)
- `api/auth.py` — add group authorization
- `api/handle.py` — group message routing, new member detection
- `api/command.py` — /get_my_info returns group ID in group context
- `README.md` + `README_zh-CN.md` — document ALLOWED_GROUPS

## Git
- Commit message: `feat: add group chat support`
- Push to `main` branch after implementation
- GitHub token is in git remote URL already
