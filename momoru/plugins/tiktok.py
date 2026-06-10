# momoru/plugins/tiktok.py
import asyncio
from playwright.async_api import async_playwright
from momoru.config import CONFIG

async def fetch_comments(target_url: str):
    """
    Scraping komentar nyata dari URL video TikTok secara dinamis menggunakan Playwright.
    """
    comments_data = []
    headless_setting = CONFIG["app"].get("headless", True)
    timeout_setting = CONFIG["app"].get("timeout", 30) * 1000  # Playwright menggunakan milidetik

    async with async_playwright() as p:
        # Gunakan proxy jika dikonfigurasi di akun pertama untuk proses membaca data umum
        browser_args = []
        proxy_config = None
        
        if CONFIG["accounts"] and CONFIG["accounts"][0]["proxy"]:
            p_string = CONFIG["accounts"][0]["proxy"]
            # Parsing manual string proxy standar http://user:pass@ip:port
            if "@" in p_string:
                creds, ip_port = p_string.replace("http://", "").split("@")
                proxy_config = {
                    "server": f"http://{ip_port}",
                    "username": creds.split(":")[0],
                    "password": creds.split(":")[1]
                }
            else:
                proxy_config = {"server": p_string}

        browser = await p.chromium.launch(headless=headless_setting, args=browser_args)
        
        # Buat konteks browser dengan custom User-Agent agar tidak mudah terblokir anti-bot TikTok
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            proxy=proxy_config
        )
        
        page = await context.new_page()
        
        try:
            # Set timeout batas pemuatan halaman
            page.set_default_timeout(timeout_setting)
            await page.goto(target_url, wait_until="domcontentloaded")
            
            # Tunggu kontainer komentar TikTok termuat di DOM (menggunakan selektor spesifik elemen komentar)
            comment_container_selector = "[class*='CommentItemContainer']"
            await page.wait_for_selector(comment_container_selector, timeout=15000)
            
            # Lakukan scroll perlahan beberapa kali ke bawah untuk memuat lebih banyak komentar (Lazy Load Bypass)
            for _ in range(5):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(1.5)
            
            # Ambil semua elemen teks komentar dan username pembuatnya
            comment_elements = await page.query_selector_all(comment_container_selector)
            
            for element in comment_elements:
                # Selektor untuk teks konten komentar dan nama user di TikTok web
                text_elem = await element.query_selector("[data-e2e='comment-level-1-content']")
                user_elem = await element.query_selector("[class*='UniqueId']")
                
                if text_elem and user_elem:
                    text_content = await text_elem.inner_text()
                    username = await user_elem.inner_text()
                    
                    comments_data.append({
                        "username": username.strip(),
                        "text": text_content.strip()
                    })
                    
        except Exception as e:
            # Jika timeout atau gagal, fungsi mengembalikan data kosong secara aman ke orchestrator
            if CONFIG["app"]["debug"]:
                print(f"[DEBUG] Gagal mengekstrak komentar dari TikTok: {str(e)}")
        
        await context.close()
        await browser.close()
        
    return comments_data