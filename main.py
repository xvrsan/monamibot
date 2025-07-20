import requests
from bs4 import BeautifulSoup

BASE_URL = "https://monami.network"
APP_SIGNIN = "https://app.monami.io/users/sign_in"

def get_csrf_token(session, url):
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Cari input hidden yang kemungkinan berisi CSRF/token nonce
    token_input = soup.find("input", {"type": "hidden", "name": True, "value": True})
    if token_input:
        return token_input["name"], token_input["value"]
    return None, None

def login(email, password):
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    # Ambil token jika ada di endpoint login Monami App
    name, value = get_csrf_token(session, APP_SIGNIN)
    payload = {
        "user[email]": email,
        "user[password]": password,
    }
    if name:
        payload[name] = value

    resp = session.post(APP_SIGNIN, data=payload, allow_redirects=True)
    if resp.url != APP_SIGNIN and resp.status_code == 200:
        print("✅ Login berhasil — ter-redirect ke app URL.")
        return session
    print("❌ Gagal login — cek email/password atau token.")
    return None

def fetch_dashboard(session):
    url = "https://app.monami.io/dashboard"
    resp = session.get(url)
    if resp.status_code == 200 and "Sign out" in resp.text:
        print("🔒 Dashboard berhasil dibuka.")
    else:
        print("⚠️ Gagal membuka dashboard — mungkin belum login.")

if __name__ == "__main__":
    EMAIL = input("Email: ").strip()
    PASSWORD = input("Password: ").strip()
    sess = login(EMAIL, PASSWORD)
    if sess:
        fetch_dashboard(sess)
