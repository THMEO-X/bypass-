import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
import asyncio
import re
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("\u2705 Slash commands synced.")

bot = MyBot()

URLS = {
    "m88": "https://traffic-user.net/GET_MA.php?codexn=taodeptrai&url=https://bet88ec.com/cach-danh-bai-sam-loc&loai_traffic=https://bet88ec.com/&clk=1000",
    "fb88": "https://traffic-user.net/GET_MA.php?codexn=taodeptrai&url=https://fb88mg.com/ty-le-cuoc-hong-kong-la-gi&loai_traffic=https://fb88mg.com/&clk=1000",
    "188bet": "https://traffic-user.net/GET_MA.php?codexn=taodeptrailamnhe&url=https://88betag.com/cach-choi-game-bai-pok-deng&loai_traffic=https://88betag.com/&clk=1000",
    "w88": "https://traffic-user.net/GET_MA.php?codexn=taodeptrai&url=https://188.166.185.213/tim-hieu-khai-niem-3-bet-trong-poker-la-gi&loai_traffic=https://188.166.185.213/&clk=1000",
    "v9bet": "https://traffic-user.net/GET_MA.php?codexn=taodeptrai&url=https://v9betse.com/ca-cuoc-dua-cho&loai_traffic=https://v9betse.com/&clk=1000",
    "vn88": "https://traffic-user.net/GET_MA.php?codexn=bomaydeptrai&url=https://vn88no.com/keo-chap-1-trai-la-gi&loai_traffic=https://vn88no.com/&clk=1000",
    "bk8": "https://traffic-user.net/GET_MA.php?codexn=taodeptrai&url=https://bk8ze.com/cach-choi-bai-catte&loai_traffic=https://bk8ze.com/&clk=1000",
}

cooldowns = {}

PRIVILEGED_USERS = [
1253726505402499203
]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="βγραʂʂ γεμɱσηεγ"))
    print(f"✅ Bot online: {bot.user.name}")

@bot.tree.command(name="yeumoney", description="Lấy mã từ YeuMoney")
@app_commands.describe(site="Chọn trang từ danh sách")
@app_commands.choices(site=[
    app_commands.Choice(name="M88", value="m88"),
    app_commands.Choice(name="FB88", value="fb88"),
    app_commands.Choice(name="188Bet", value="188bet"),
    app_commands.Choice(name="W88", value="w88"),
    app_commands.Choice(name="V9Bet", value="v9bet"),
    app_commands.Choice(name="VN88", value="vn88"),
    app_commands.Choice(name="BK8", value="bk8"),
])
async def yeumoney(interaction: discord.Interaction, site: str):
    user_id = interaction.user.id
    site = site.lower()

    is_admin = interaction.user.guild_permissions.administrator if interaction.guild else False
    if not is_admin and user_id not in PRIVILEGED_USERS:
        last_time = cooldowns.get(user_id, 0)
        now = datetime.now().timestamp()
        if now - last_time < 75:
            remaining = int(75 - (now - last_time))
            return await interaction.response.send_message(
                f"⏳ Vui lòng chờ **{remaining}s** trước khi dùng lại lệnh `/yeumoney`.", ephemeral=True
            )
        cooldowns[user_id] = now

    if site not in URLS:
        return await interaction.response.send_message(
            "❌ Loại không hợp lệ. Vui lòng chọn từ danh sách.", ephemeral=True
        )

    await interaction.response.send_message(embed=discord.Embed(
        title="⏳ Đang xử lý bypass...",
        description=f"Loại: `{site}`\nVui lòng chờ **75 giây**.",
        color=discord.Color.orange()
    ))

    await asyncio.sleep(75)

    try:
        res = requests.post(URLS[site])
        html = res.text
        match = re.search(r'<span id="layma_me_vuatraffic"[^>]*>\s*(\d+)\s*</span>', html)

        if match:
            code = match.group(1)
            embed_done = discord.Embed(
                title="🟢 Hoàn tất Bypass YeuMoney",
                description=(
                    f"🔖 **Loại yêu cầu:** `{site}`\n"
                    f"📬 **Mã** đã được gửi đến **DM** của bạn!\n"
                    f"👤 **Người yêu cầu:** {interaction.user.mention}"
                ),
                color=discord.Color.green(),
                timestamp=datetime.now(timezone.utc)
            )
            embed_done.set_author(name="✅ YeuMoney thành công", icon_url="https://cdn-icons-png.flaticon.com/512/929/929564.png")
            embed_done.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
            embed_done.set_footer(text=f"Server: {interaction.guild.name}" if interaction.guild else "Sử dụng trong DM")

            await interaction.followup.send(embed=embed_done)

            # Gửi qua DM
            embed_dm = discord.Embed(
                title="📩 Mã YeuMoney",
                description=f"📝 **Loại:** `{site}`\n🔐 **Mã nhận được:**\n```{code}```",
                color=discord.Color.blue(),
                timestamp=datetime.now(timezone.utc)
            )
            embed_dm.set_footer(text="Yêu cầu Kx Bot", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            embed_dm.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1087/1087923.png")

            try:
                await interaction.user.send(embed=embed_dm)
            except discord.Forbidden:
                await interaction.followup.send("⚠️ Không thể gửi DM cho bạn. Hãy bật tin nhắn riêng từ server!", ephemeral=True)

        else:
            await interaction.followup.send(embed=discord.Embed(
                title="⚠️ Không tìm thấy mã!",
                description="Link lỗi vui lòng đổi nghiệm vụ.",
                color=discord.Color.red()
            ))

    except Exception as e:
        await interaction.followup.send(embed=discord.Embed(
            title="❌ Lỗi khi lấy mã",
            description=f"```{e}```",
            color=discord.Color.dark_red()
        ))

def parse_duration(duration_str):
    match = re.fullmatch(r"(\d+)([smhd])", duration_str)
    if not match:
        return None
    value, unit = int(match[1]), match[2]
    return value * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]

async def get_or_create_mute_role(guild: discord.Guild):
    role = discord.utils.get(guild.roles, name="Muted")
    if not role:
        role = await guild.create_role(name="Muted", reason="Auto Mute Role")
        for channel in guild.channels:
            try:
                await channel.set_permissions(role, send_messages=False, speak=False)
            except:
                pass
    return role

@bot.tree.command(name="mute", description="Mute thành viên trong thời gian")
@app_commands.describe(user="Người cần mute", duration="Thời gian như 10m, 1h", reason="Lý do")
async def mute(interaction: discord.Interaction, user: discord.Member, duration: str, reason: str = "Không ghi rõ"):
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ Bạn không có quyền.", ephemeral=True)

    seconds = parse_duration(duration)
    if seconds is None:
        return await interaction.response.send_message("❌ Sai định dạng thời gian. VD: `10m`, `2h`", ephemeral=True)

    role = await get_or_create_mute_role(interaction.guild)
    await user.add_roles(role, reason=reason)
    await interaction.response.send_message(f"🔇 Đã mute {user.mention} trong `{duration}`. 🕒 Lý do: {reason}")

    await asyncio.sleep(seconds)
    if role in user.roles:
        await user.remove_roles(role, reason="Hết thời gian mute")
        try:
            await user.send(f"🔊 Bạn đã được unmute sau `{duration}`.")
        except:
            pass

@bot.command(name="mute")
async def mute_cmd(ctx, member: discord.Member, duration: str, *, reason="Không ghi rõ"):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ Bạn không có quyền.")

    seconds = parse_duration(duration)
    if seconds is None:
        return await ctx.send("❌ Sai định dạng thời gian. VD: `10m`, `2h`")

    role = await get_or_create_mute_role(ctx.guild)
    await member.add_roles(role, reason=reason)
    await ctx.send(f"🔇 Đã mute {member.mention} trong `{duration}`. 🕒 Lý do: {reason}")

    await asyncio.sleep(seconds)
    if role in member.roles:
        await member.remove_roles(role, reason="Hết thời gian mute")
        try:
            await member.send(f"🔊 Bạn đã được unmute sau `{duration}`.")
        except:
            pass

@bot.tree.command(name="unmute", description="Bỏ mute thành viên")
@app_commands.describe(user="Người cần unmute")
async def unmute(interaction: discord.Interaction, user: discord.Member):
    role = await get_or_create_mute_role(interaction.guild)
    await user.remove_roles(role)
    await interaction.response.send_message(f"🔊 Đã unmute {user.mention}.")

@bot.command(name="unmute")
async def unmute_cmd(ctx, member: discord.Member):
    role = await get_or_create_mute_role(ctx.guild)
    await user.remove_roles(role)
    await ctx.send(f"🔊 Đã unmute {member.mention}.")

@bot.tree.command(name="ban", description="Ban thành viên")
@app_commands.describe(user="Người cần ban", reason="Lý do")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "Không ghi rõ"):
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ Bạn không có quyền ban.", ephemeral=True)
    try:
        await user.ban(reason=reason)
        await interaction.response.send_message(f"🔨 Đã ban {user.mention}. Lý do: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("❌ Bot không đủ quyền để ban.", ephemeral=True)

@bot.command(name="ban")
async def ban_cmd(ctx, member: discord.Member, *, reason="Không ghi rõ"):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ Bạn không có quyền.")
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Đã ban {member.mention}. Lý do: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ Bot không đủ quyền để ban.")

@bot.tree.command(name="unban", description="Unban bằng user ID")
@app_commands.describe(user_id="ID người dùng")
async def unban(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"♻️ Đã unban {user}.")
    except Exception:
        await interaction.response.send_message("❌ Không tìm thấy người dùng hoặc lỗi.", ephemeral=True)

@bot.command(name="unban")
async def unban_cmd(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"♻️ Đã unban {user}.")
    except:
        await ctx.send("❌ Không tìm thấy người dùng hoặc lỗi.")

@bot.tree.command(name="ping", description="Xem ping bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Ping: `{round(bot.latency * 1000)}ms`")

@bot.tree.command(name="invite", description="Link mời bot")
async def invite(interaction: discord.Interaction):
    url = f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot+applications.commands"
    await interaction.response.send_message(f"🤖 Mời bot: <{url}>")

@bot.tree.command(name="help", description="Xem danh sách lệnh")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📘 Danh sách lệnh",
        description=(
            "`/mute`, `/unmute`, `/ban`, `/unban`, `/ping`, `/invite`, `/help`\n"
            "`!mute`, `!unmute`, `!ban`, `/yeumoney`."
        ),
        color=discord.Color.blurple()
    )
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)