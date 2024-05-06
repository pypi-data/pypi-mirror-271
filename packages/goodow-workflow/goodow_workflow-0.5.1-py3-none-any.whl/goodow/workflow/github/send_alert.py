from __future__ import annotations
import json
import logging
import os
import shlex
import subprocess
import asyncio

from telegram import Message, MessageEntity
from telegram.ext import Application, AIORateLimiter
from telegram.helpers import escape_markdown

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s:%(levelname)s:%(message)s"
)

# 频率限制: https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
async def send_message(telegram_token: str, markdown_text: str, chat_id: int | str):
    application = Application.builder().token(telegram_token).updater(None).rate_limiter(AIORateLimiter(max_retries=5)).build()
    message: Message = await application.bot.send_message(chat_id=chat_id, text=markdown_text, parse_mode="MarkdownV2")
    logging.info(f"{message=}")
    await application.shutdown()
    return message

def short_sha():
    process = subprocess.run(
        shlex.split(f'git rev-parse --short {os.environ["GITHUB_SHA"]}'),
        capture_output=True,
        text=True,
    )
    return process.stdout.strip()


if __name__ == "__main__":
    github = json.loads(os.environ["GITHUB_CONTEXT"])
    job = json.loads(os.environ["JOB_CONTEXT"])
    head_commit = github["event"]["head_commit"]
    url = f'{head_commit["url"]}/checks'

    labels = {
        "workflow": github["workflow"],
        "git_sha": short_sha(),
        "commit": head_commit["message"],
    }

    repo = github['repository'].split('/')[-1].replace('-', '_')
    tags = escape_markdown(f"#github_action #{job['status']} #{repo}", 2)
    block_quote = '\n'.join(f">*{escape_markdown(key, 2)}*: " + escape_markdown(value, 2) for key, value in labels.items())
    url = f"[日志]({escape_markdown(url, 2, entity_type=MessageEntity.TEXT_LINK)})"

    text = f'''
    {tags}\n{block_quote}\n{url}
    '''.strip()
    logging.info(f"{text=}")
    asyncio.run(send_message(os.environ["TELEGRAM_BOT_TOKEN"], text, os.environ["TELEGRAM_CHAT_ID"]))

