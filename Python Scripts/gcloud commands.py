import os
import sys
import shutil
import html
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

DESKTOP = Path.home() / "Desktop"
OUT_DIR = DESKTOP / "gcloud_pdf_manuals"
TEMP_DIR = DESKTOP / "gcloud_temp"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# 1. Locate Microsoft Edge or Google Chrome
BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
browser_exe = next((p for p in BROWSER_CANDIDATES if os.path.exists(p)), None)
if not browser_exe:
    print("Error: Could not locate Microsoft Edge or Chrome.")
    sys.exit(1)

print(f"[+] Using Browser Renderer: {browser_exe}")

# 2. Get all commands
print("[+] Scanning all gcloud commands...")
res = subprocess.run("gcloud.cmd meta list-commands", shell=True, capture_output=True, text=True)
all_commands = [line.strip() for line in res.stdout.splitlines() if line.strip().startswith("gcloud ")]

# Group commands by service (second token)
service_map = {}
for cmd in all_commands:
    parts = cmd.split()
    if len(parts) >= 2:
        svc = parts[1]
        service_map.setdefault(svc, []).append(cmd)

print(f"[+] Found {len(service_map)} services across {len(all_commands)} commands.")

def fetch_help(cmd):
    """Pulls help for a single command via gcloud.cmd"""
    try:
        proc = subprocess.run(f"{cmd} --help", shell=True, capture_output=True, text=True, timeout=25)
        text = proc.stdout if proc.stdout else proc.stderr
    except Exception as e:
        text = f"Failed to retrieve help for {cmd}: {e}"
    return cmd, text

# 3. Process each service
CSS_STYLE = """
@page { size: A4 landscape; margin: 12mm 15mm 12mm 15mm; }
@media print { body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
body { font-family: 'Consolas', 'Courier New', monospace; font-size: 9pt; line-height: 1.35; color: #1f2328; margin: 0; }
.command-card { page-break-after: always; margin-bottom: 20px; }
.command-card:last-child { page-break-after: auto; }
.command-header { background-color: #1a73e8 !important; color: #ffffff !important; padding: 8px 12px; font-size: 13pt; font-weight: bold; border-radius: 4px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin-bottom: 12px; }
pre { white-space: pre-wrap; word-break: break-word; font-family: inherit; font-size: 8.5pt; margin: 0; }
"""

for svc, cmds in sorted(service_map.items()):
    pdf_path = OUT_DIR / f"gcloud_{svc}_manual.pdf"
    html_path = TEMP_DIR / f"gcloud_{svc}.html"
    print(f"[*] Processing [{svc}] ({len(cmds)} commands) in parallel...")

    # Fetch help in parallel using 16 threads
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(fetch_help, cmds))

    # Build HTML document
    cards = []
    for cmd, raw_help in results:
        cards.append(f"""
        <div class="command-card">
            <div class="command-header">COMMAND: {html.escape(cmd)}</div>
            <pre>{html.escape(raw_help)}</pre>
        </div>
        """)

    full_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>gcloud {svc} Manual</title><style>{CSS_STYLE}</style></head>
<body>{''.join(cards)}</body>
</html>"""

    html_path.write_text(full_html, encoding="utf-8")

    # Render HTML to PDF via headless browser
    edge_cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--user-data-dir={os.environ.get('TEMP', '')}\\edge_pdf_profile",
        f"--print-to-pdf={pdf_path}",
        str(html_path)
    ]
    subprocess.run(edge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if html_path.exists():
        html_path.unlink()
    print(f"    -> [✓] Generated: {pdf_path.name}")

shutil.rmtree(TEMP_DIR, ignore_errors=True)
print(f"\n[✓] Completed! All service PDF manuals are in: {OUT_DIR}")