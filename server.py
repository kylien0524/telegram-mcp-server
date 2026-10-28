import os
from fastmcp import FastMCP
from telegram import Bot

mcp = FastMCP("Telegram MCP Server")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEFAULT_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TOKEN) if TOKEN else None

@mcp.tool()
async def send_telegram_message(message: str, chat_id: str = None) -> str:
    """Send a message to a Telegram chat."""
    target_id = chat_id or DEFAULT_CHAT_ID
    if not bot:
        return "Error: TELEGRAM_BOT_TOKEN is not set."
    if not target_id:
        return "Error: TELEGRAM_CHAT_ID is not provided."
    await bot.send_message(chat_id=target_id, text=message)
    return "Message sent successfully."

@mcp.tool()
async def get_latest_updates(limit: int = 5) -> str:
    """Get the latest incoming Telegram messages."""
    if not bot:
        return "Error: TELEGRAM_BOT_TOKEN is not set."
    updates = await bot.get_updates(limit=limit)
    if not updates:
        return "No recent messages found."
    return "\n".join([f"[{u.message.chat.title or u.message.chat.id}] {u.message.from_user.first_name}: {u.message.text}" for u in updates if u.message and u.message.text])

if __name__ == "__main__":
    # Render의 환경변수 PORT를 감지해 SSE 서버 구동
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
