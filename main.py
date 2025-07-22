import asyncio
from playwright.async_api import async_playwright

EMAIL = ""
PASSWORD = ""

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Ubah ke True jika tidak ingin lihat browser-nya
        context = await browser.new_context()
        page = await context.new_page()

        # 1. Buka halaman login
        await page.goto("https://app.monami.io/users/sign_in")
        await page.wait_for_load_state("networkidle")

        # 2. Isi form login
        await page.fill('input[name="user[email]"]', EMAIL)
        await page.fill('input[name="user[password]"]', PASSWORD)
        await page.click('input[name="commit"]')  # Tombol login

        # 3. Tunggu redirect atau verifikasi
        try:
            await page.wait_for_url("https://app.monami.io/dashboard", timeout=10000)
            print("✅ Berhasil login dan masuk dashboard!")
        except:
            print("❌ Gagal login atau halaman tidak redirect ke dashboard.")
            await page.screenshot(path="login_failed.png")
            await browser.close()
            return

        # 4. Ambil konten dashboard
        content = await page.content()
        print("\n=== Cuplikan Konten Dashboard ===")
        print(content[:1000])  # Cetak sebagian HTML

        # Optional: Simpan screenshot dashboard
        await page.screenshot(path="dashboard.png")
        print("📸 Screenshot disimpan sebagai dashboard.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
