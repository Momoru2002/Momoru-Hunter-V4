# momoru/commands/report.py
import click
import asyncio
from playwright.async_api import async_playwright
from rich.console import Console
from momoru.themes.cyberpunk import cyberpunk_theme
from momoru.config import CONFIG

# Menghubungkan log automasi dengan skema warna cyberpunk global
console = Console(theme=cyberpunk_theme)

async def run_automated_report(target_username: str, reason: str):
    """
    Eksekutor utama lapisan mitigasi serangan Sybil: melakukan login massal secara berkala
    dan melakukan pelaporan terhadap akun target menggunakan 10 akun tumbal di latar belakang.
    """
    if not CONFIG["accounts"]:
        console.print("[danger][!] Tidak ada akun tumbal yang terkonfigurasi di file .env lu, Bro![/danger]")
        return

    headless_setting = CONFIG["app"].get("headless", True)
    
    # Jalankan loop pelaporan untuk setiap akun yang terdeteksi di lingkungan .env
    for idx, account in enumerate(CONFIG["accounts"], start=1):
        console.print(f"[info][*] [{idx}/{len(CONFIG['accounts'])}] Menggerakkan Bot: {account['username']}...[/info]")
        
        # Konfigurasi proxy terisolasi untuk tiap-tiap entitas akun
        proxy_config = None
        if account["proxy"]:
            p_string = account["proxy"]
            if "@" in p_string:
                creds, ip_port = p_string.replace("http://", "").split("@")
                proxy_config = {
                    "server": f"http://{ip_port}",
                    "username": creds.split(":")[0],
                    "password": creds.split(":")[1]
                }
            else:
                proxy_config = {"server": p_string}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless_setting)
            context = await browser.new_context(proxy=proxy_config)
            page = await context.new_page()
            
            try:
                # 1. Navigasi ke Gerbang Login TikTok Web
                await page.goto("https://www.tiktok.com/login/phone-or-email/email", wait_until="networkidle")
                
                # Input kredensial ke form isian login secara mekanis
                await page.fill("input[name='username']", account["email"])
                await page.fill("input[type='password']", account["password"])
                await page.click("button[type='submit']")
                
                # Beri jeda waktu sinkronisasi sesi pasca-login (dan penanganan interupsi captcha jika headless=False)
                await asyncio.sleep(5)
                
                # 2. Masuk langsung ke profil target buzzer yang akan dimitigasi
                await page.goto(f"https://www.tiktok.com/@{target_username}", wait_until="networkidle")
                
                # 3. Eksekusi Trigger Tombol Report Menu TikTok
                more_button_selector = "[data-e2e='user-more-actions']"
                await page.wait_for_selector(more_button_selector, timeout=5000)
                await page.click(more_button_selector)
                
                # Klik opsi "Laporkan / Report"
                await page.click("text=Report")
                await asyncio.sleep(2)
                
                # Pilih jenis pelanggaran berdasarkan parameter (misal: Spam, Pelecehan, Informasi Palsu)
                if "spam" in reason.lower():
                    await page.click("text=Spam")
                else:
                    await page.click("text=Misleading Information")
                
                # Klik tombol konfirmasi akhir kirim laporan
                await page.click("button:has-text('Submit')")
                
                console.print(f"[success][+] Akun {account['username']} BERHASIL mengirimkan laporan ke target.[/success]")
                
            except Exception as e:
                console.print(f"[danger][─] Akun {account['username']} GAGAL memproses tindakan: Keamanan internal mendeteksi interupsi/captcha.[/danger]")
                if CONFIG["app"]["debug"]:
                    console.print(f"[muted][DEBUG ERROR]: {str(e)}[/muted]")
            
            await context.close()
            await browser.close()
            
        # Atur jeda interval (Cool-down) antar akun sejauh 10 detik agar tidak dicurigai sebagai serangan bot serentak
        await asyncio.sleep(10)

@click.command()
@click.argument("username")
@click.option("--reason", default="Spam/Buzzer Activity", help="Alasan pelaporan akun target")
def cli(username, reason):
    """Trigger Sybil Automated Attack Layer (Multi-Account Mitigations)"""
    console.print(f"[warning][*] Menginisialisasi serangan pelaporan mitigasi terhadap target: @{username}[/warning]")
    
    # Jalankan loop async engine menggunakan runner standard asyncio Windows/Linux
    asyncio.run(run_automated_report(username, reason))