import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import asyncio
import discord
from discord.ext import commands

# Web server siêu nhẹ dùng thư viện chuẩn, tương thích mọi phiên bản Python
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Chạy web server ở luồng nền để không nghẽn bot
threading.Thread(target=run_web, daemon=True).start()

# Cấu hình Selfbot
bot = commands.Bot(command_prefix="!", self_bot=True)

GUILD_ID = 1537507317459718289
CHANNEL_ID = 1558846850415599616

@bot.event
async def on_ready():
    print(f"[+] Đã đăng nhập thành công: {bot.user}")
    await asyncio.sleep(3)
    try:
        guild = bot.get_guild(GUILD_ID) or await bot.fetch_guild(GUILD_ID)
        channel = guild.get_channel(CHANNEL_ID) or await guild.fetch_channel(CHANNEL_ID)
        
        if channel:
            if not channel.guild.voice_client:
                await channel.connect()
                print(f"[+] Đã kết nối vào phòng voice thành công: {channel.name}")
        else:
            print("[-] Không tìm thấy kênh voice!")
    except Exception as e:
        print(f"[-] Lỗi join voice: {e}")

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("[-] LỖI: Chưa cấu hình DISCORD_TOKEN trong Environment!")
