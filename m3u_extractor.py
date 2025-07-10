"""
It's a simple script that extracts m3u8 streams from a given webpage
"""
import sys
import re
from playwright.sync_api import sync_playwright

M3U8_REGEX = re.compile(r'\.m3u8(\?.*?)?$', re.IGNORECASE)

def run_firefox_sniffer(url):
    m3u8_links = set()

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def on_request(request):
            if M3U8_REGEX.search(request.url):
                m3u8_links.add(request.url)
                print(f"🎯 Found: {request.url}")

        page.on("request", on_request)

        print(f"🌐 Opening: {url}")
        page.goto(url, wait_until="load", timeout=60000)
        page.wait_for_timeout(10000)  # Give autoplay a chance

        browser.close()

    print("\n🎬 Final list:")
    if m3u8_links:
        for link in sorted(m3u8_links):
            print(link)
    else:
        print("❌ No .m3u8 links found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python m3u_extractor.py <url>")
        sys.exit(1)

    run_firefox_sniffer(sys.argv[1])

