import os
from aiohttp import web
import discord
from discord.ext import commands

# Tạo web server ảo để Render không bị sleep (bắt buộc phải có để Render không tắt ứng dụng)
async def handle(request):
    return web.Response(text="Bot is running!")

async def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# Cấu hình Selfbot
bot = commands.Bot(command_prefix="!", self_bot=True)

GUILD_ID = 1537507317459718289
CHANNEL_ID = 1558846850415599616

@bot.event
async def on_ready():
    print(f"[+] Đã đăng nhập thành công: {bot.user}")
    try:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            guild = await bot.fetch_guild(GUILD_ID)

        channel = guild.get_channel(CHANNEL_ID)
        if not channel:
            channel = await bot.fetch_channel(CHANNEL_ID)

        if channel:
            await channel.connect()
            print(f"[+] Đã kết nối vào phòng voice thành công: {channel.name}")
        else:
            print("[-] Không tìm thấy kênh voice!")
    except Exception as e:
        print(f"[-] Lỗi join voice: {e}")

import asyncio
async def main():
    await run_web()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        await bot.start(token)
    else:
        print("[-] LỖI: Chưa cấu hình DISCORD_TOKEN trong Environment!")

if __name__ == "__main__":
    asyncio.run(main())
