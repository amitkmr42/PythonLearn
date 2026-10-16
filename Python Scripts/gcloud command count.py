import os
import sys
import html
import shutil
import subprocess
from pathlib import Path

# ----------------------------------------------------------------------
# 1. SETUP OUTPUT DIRECTORIES & LOCATE HEADLESS BROWSER
# ----------------------------------------------------------------------
DESKTOP = Path.home() / "Desktop"
OUTPUT_PDF = DESKTOP / "gcloud_141_services_catalog.pdf"
TEMP_HTML = DESKTOP / "gcloud_services_temp.html"

BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    shutil.which("google-chrome"),
    shutil.which("msedge"),
    shutil.which("chromium"),
]
browser_exe = next((p for p in BROWSER_CANDIDATES if p and os.path.exists(p)), None)

if not browser_exe:
    print("[-] Error: Could not locate Microsoft Edge or Google Chrome.")
    sys.exit(1)

print(f"[+] Using Browser Renderer: {browser_exe}")

# ----------------------------------------------------------------------
# 2. RUN CLI SCAN & AGGREGATE COMMAND COUNTS
# ----------------------------------------------------------------------
gcloud_bin = "gcloud.cmd" if os.name == "nt" else "gcloud"
print("[+] Querying live CLI command tree via 'gcloud meta list-commands'...")

try:
    res = subprocess.run(
        f"{gcloud_bin} meta list-commands",
        shell=True,
        capture_output=True,
        text=True,
        check=True
    )
except Exception as e:
    print(f"[-] Failed to execute gcloud: {e}")
    sys.exit(1)

all_commands = [line.strip() for line in res.stdout.splitlines() if line.strip().startswith("gcloud ")]

# Group commands by the primary service token (parts[1])
service_map = {}
for cmd in all_commands:
    parts = cmd.split()
    if len(parts) >= 2:
        svc = parts[1]
        service_map.setdefault(svc, []).append(cmd)

total_services = len(service_map)
total_commands = len(all_commands)
print(f"[+] Detected {total_services} distinct service groups across {total_commands} total CLI commands.")

# ----------------------------------------------------------------------
# 3. DOMAIN TAXONOMY & SERVICE DICTIONARY MAPPING
# ----------------------------------------------------------------------
SERVICE_METADATA = {
    # Compute & Containers
    "compute": ("Compute Engine & Core IaaS", "Compute"),
    "container": ("Google Kubernetes Engine (GKE)", "Compute"),
    "run": ("Cloud Run (Serverless Containers)", "Compute"),
    "app": ("App Engine (PaaS)", "Compute"),
    "functions": ("Cloud Functions / Cloud Run functions", "Compute"),
    "batch": ("Cloud Batch Job Scheduler", "Compute"),
    "vmware": ("Google Cloud VMware Engine", "Compute"),
    "bare-metal-solution": ("Bare Metal Solution", "Compute"),

    # Storage & Migration
    "storage": ("Cloud Storage (GCS & Storage CLI)", "Storage"),
    "filestore": ("Cloud Filestore (Managed NFS)", "Storage"),
    "backup-dr": ("Backup and Disaster Recovery", "Storage"),
    "transfer": ("Storage Transfer Service", "Storage"),
    "netapp": ("Google Cloud NetApp Volumes", "Storage"),

    # Databases & Caching
    "sql": ("Cloud SQL (MySQL / Postgres / SQL Server)", "Databases"),
    "spanner": ("Cloud Spanner (Global Relational DB)", "Databases"),
    "alloydb": ("AlloyDB for PostgreSQL", "Databases"),
    "firestore": ("Cloud Firestore (NoSQL Document DB)", "Databases"),
    "bigtable": ("Cloud Bigtable (NoSQL Wide-Column DB)", "Databases"),
    "redis": ("Memorystore for Redis", "Databases"),
    "memcache": ("Memorystore for Memcached", "Databases"),
    "database-migration": ("Database Migration Service (DMS)", "Databases"),
    "memorystore": ("Memorystore Cluster Management", "Databases"),

    # Networking & Content Delivery
    "dns": ("Cloud DNS (Authoritative Domain System)", "Networking"),
    "domains": ("Cloud Domains Registration", "Networking"),
    "edge-cache": ("Media CDN Edge Cache", "Networking"),
    "network-connectivity": ("Network Connectivity Center", "Networking"),
    "network-management": ("Network Intelligence Center", "Networking"),
    "network-security": ("Cloud Network Security Policies", "Networking"),
    "network-services": ("Traffic Director & Network Services", "Networking"),
    "certificate-manager": ("SSL / TLS Certificate Manager", "Networking"),
    "service-extensions": ("Cloud Service Extensions", "Networking"),
    "vpc-access": ("Serverless VPC Access", "Networking"),

    # Security, Identity & Compliance
    "iam": ("Identity and Access Management", "Security & IAM"),
    "secrets": ("Secret Manager", "Security & IAM"),
    "kms": ("Cloud Key Management Service (KMS)", "Security & IAM"),
    "scc": ("Security Command Center (SCC)", "Security & IAM"),
    "access-context-manager": ("Access Context Manager (BeyondCorp)", "Security & IAM"),
    "access-approval": ("Access Approval", "Security & IAM"),
    "assured": ("Assured Workloads (Compliance)", "Security & IAM"),
    "identity": ("Cloud Identity & Endpoint Service", "Security & IAM"),
    "iap": ("Identity-Aware Proxy", "Security & IAM"),
    "recaptcha": ("reCAPTCHA Enterprise Defense", "Security & IAM"),
    "privateca": ("Certificate Authority Service (Private CA)", "Security & IAM"),
    "public-ca": ("Public Certificate Authority", "Security & IAM"),
    "ids": ("Cloud Intrusion Detection System", "Security & IAM"),
    "org-policies": ("Organization Policy Service", "Security & IAM"),
    "policy-intelligence": ("Policy Intelligence & Simulator", "Security & IAM"),
    "policy-troubleshoot": ("IAM Policy Troubleshooter", "Security & IAM"),
    "privileged-access-manager": ("Privileged Access Manager (PAM)", "Security & IAM"),
    "securitycentermanagement": ("Security Center Management API", "Security & IAM"),
    "active-directory": ("Managed Service for Microsoft AD", "Security & IAM"),

    # AI & Machine Learning
    "ai": ("Vertex AI Platform", "AI & Machine Learning"),
    "ai-platform": ("Legacy AI Platform / ML Engine", "AI & Machine Learning"),
    "ml": ("Machine Learning Engine APIs", "AI & Machine Learning"),
    "ml-engine": ("Cloud ML Training & Predictions", "AI & Machine Learning"),
    "documentai": ("Document AI Document Processing", "AI & Machine Learning"),
    "dialogflow": ("Dialogflow CX / ES Agents", "AI & Machine Learning"),
    "gemini": ("Gemini Enterprise Platform", "AI & Machine Learning"),
    "colab-enterprise": ("Colab Enterprise Notebooks", "AI & Machine Learning"),
    "workbench": ("Vertex AI Workbench Instances", "AI & Machine Learning"),
    "notebooks": ("Vertex AI Managed Notebooks", "AI & Machine Learning"),
    "transcoder": ("Transcoder Video Encoding API", "AI & Machine Learning"),
    "enterprise-knowledge-graph": ("Enterprise Knowledge Graph", "AI & Machine Learning"),

    # Analytics & Big Data
    "dataproc": ("Cloud Dataproc (Managed Hadoop / Spark)", "Data & Analytics"),
    "dataflow": ("Cloud Dataflow (Batch & Stream)", "Data & Analytics"),
    "pubsub": ("Cloud Pub/Sub Messaging", "Data & Analytics"),
    "dataplex": ("Dataplex Intelligent Data Fabric", "Data & Analytics"),
    "composer": ("Cloud Composer (Managed Airflow)", "Data & Analytics"),
    "data-fusion": ("Cloud Data Fusion (ETL / Pipelines)", "Data & Analytics"),
    "datastream": ("Datastream Change Data Capture (CDC)", "Data & Analytics"),
    "data-catalog": ("Data Catalog Metadata Search", "Data & Analytics"),
    "datashare": ("Datashare Financial Analytics", "Data & Analytics"),
    "looker": ("Looker Business Intelligence", "Data & Analytics"),
    "spatial-analysis": ("Earth Engine & Spatial Analytics", "Data & Analytics"),
    "healthcare": ("Cloud Healthcare API", "Data & Analytics"),

    # Operations & Observability
    "logging": ("Cloud Logging (Stackdriver)", "Operations & Observability"),
    "monitoring": ("Cloud Monitoring (Metrics & Alerts)", "Operations & Observability"),
    "trace": ("Cloud Trace (Distributed Tracing)", "Operations & Observability"),
    "profiler": ("Cloud Profiler (Continuous Profiling)", "Operations & Observability"),
    "error-reporting": ("Cloud Error Reporting", "Operations & Observability"),

    # Developer Tools & CI/CD
    "builds": ("Cloud Build (Continuous Integration)", "Developer Tools"),
    "artifacts": ("Artifact Registry (Package Repository)", "Developer Tools"),
    "deploy": ("Cloud Deploy (Continuous Delivery)", "Developer Tools"),
    "source": ("Cloud Source Repositories", "Developer Tools"),
    "cloud-shell": ("Cloud Shell Terminal Environment", "Developer Tools"),
    "workstations": ("Cloud Workstations (Managed IDEs)", "Developer Tools"),
    "firebase": ("Firebase Cloud Platform", "Developer Tools"),
    "developer-connect": ("Developer Connect Toolchain", "Developer Tools"),
    "secure-source-manager": ("Secure Source Manager (Managed GitLab)", "Developer Tools"),

    # Application Integration & APIs
    "workflows": ("Cloud Workflows Orchestration", "Integration & APIs"),
    "tasks": ("Cloud Tasks (Async Execution Queue)", "Integration & APIs"),
    "scheduler": ("Cloud Scheduler (Cron Automation)", "Integration & APIs"),
    "eventarc": ("Eventarc Event Routing System", "Integration & APIs"),
    "apigee": ("Apigee Enterprise API Management", "Integration & APIs"),
    "endpoints": ("Cloud Endpoints API Management", "Integration & APIs"),
    "api-gateway": ("Cloud API Gateway", "Integration & APIs"),
    "services": ("Service Usage & API Activations", "Integration & APIs"),
    "service-directory": ("Service Directory Registry", "Integration & APIs"),

    # Governance, Resource Management & Migration
    "billing": ("Cloud Billing & Cost Governance", "Governance & Migration"),
    "projects": ("Cloud Projects Hierarchy", "Governance & Migration"),
    "organizations": ("Cloud Organizations Hierarchy", "Governance & Migration"),
    "resource-manager": ("Cloud Resource Manager", "Governance & Migration"),
    "infra-manager": ("Infrastructure Manager (Terraform)", "Governance & Migration"),
    "deployment-manager": ("Cloud Deployment Manager", "Governance & Migration"),
    "recommender": ("Active Assist Recommender", "Governance & Migration"),
    "asset": ("Cloud Asset Inventory", "Governance & Migration"),
    "migration": ("Google Cloud Migration Tools", "Governance & Migration"),
    "vmmigration": ("Migrate to Virtual Machines", "Governance & Migration"),
    "anthos": ("Anthos Multicloud Platform", "Governance & Migration"),
    "edge-cloud": ("Distributed Cloud Edge", "Governance & Migration"),
    "apphub": ("App Hub Unified Application Center", "Governance & Migration"),
    "parametermanager": ("Parameter Manager Config Store", "Governance & Migration"),
    "essential-contacts": ("Essential Contacts Registry", "Governance & Migration"),
    "resource-config": ("Declarative Resource Configuration", "Governance & Migration"),
    "terraform-tools": ("Terraform Tooling & Converters", "Governance & Migration"),
    "telco-automation": ("Telecom Network Automation", "Governance & Migration"),

    # Core CLI & Diagnostic Utilities
    "auth": ("Authentication & Credential Tokens", "Core CLI & Utilities"),
    "config": ("CLI Profile & Configuration Properties", "Core CLI & Utilities"),
    "components": ("Google Cloud SDK Component Manager", "Core CLI & Utilities"),
    "feedback": ("CLI Feedback & Problem Submissions", "Core CLI & Utilities"),
    "help": ("Integrated Command Help Documentation", "Core CLI & Utilities"),
    "info": ("Diagnostic System & Environment Info", "Core CLI & Utilities"),
    "init": ("SDK Initial Setup & Account Login", "Core CLI & Utilities"),
    "meta": ("CLI Metaprogramming & Introspection", "Core CLI & Utilities"),
    "survey": ("Google Cloud CLI Feedback Survey", "Core CLI & Utilities"),
    "topic": ("Gcloud Concept Exploration & Guides", "Core CLI & Utilities"),
    "version": ("SDK Installed Version Verification", "Core CLI & Utilities"),
}

def resolve_service_info(svc_name):
    """Returns (Formal Service Title, Domain Category) with automatic fallbacks."""
    if svc_name in SERVICE_METADATA:
        return SERVICE_METADATA[svc_name]
    
    # Heuristic fallback for any newly installed alpha/beta groups
    title = svc_name.replace("-", " ").title()
    category = "Extended Cloud Services"
    
    if any(k in svc_name for k in ["net", "dns", "route", "vpc"]):
        category = "Networking"
    elif any(k in svc_name for k in ["sec", "policy", "auth", "cert", "guard", "key"]):
        category = "Security & IAM"
    elif any(k in svc_name for k in ["data", "query", "lake", "stream"]):
        category = "Data & Analytics"
    elif any(k in svc_name for k in ["ai", "model", "learn", "intel"]):
        category = "AI & Machine Learning"
        
    return (f"{title} Service", category)

# ----------------------------------------------------------------------
# 4. SORT AND FORMAT CATALOG ROWS
# ----------------------------------------------------------------------
catalog_records = []
for svc, cmds in service_map.items():
    title, domain = resolve_service_info(svc)
    catalog_records.append({
        "cli_group": f"gcloud {svc}",
        "title": title,
        "domain": domain,
        "count": len(cmds)
    })

# Sort primarily by Domain, secondarily by Command Count (descending)
DOMAIN_ORDER = [
    "Compute", "Storage", "Databases", "Networking",
    "Security & IAM", "AI & Machine Learning", "Data & Analytics",
    "Operations & Observability", "Developer Tools", "Integration & APIs",
    "Governance & Migration", "Core CLI & Utilities", "Extended Cloud Services"
]

def sort_key(item):
    domain_idx = DOMAIN_ORDER.index(item["domain"]) if item["domain"] in DOMAIN_ORDER else 99
    return (domain_idx, -item["count"], item["cli_group"])

catalog_records.sort(key=sort_key)

# ----------------------------------------------------------------------
# 5. GENERATE PROFESSIONAL HTML WITH PAGINATION & PRINT STYLING
# ----------------------------------------------------------------------
rows_html = []
for idx, item in enumerate(catalog_records, start=1):
    badge_class = item["domain"].split()[0].lower().replace("&", "")
    rows_html.append(f"""
    <tr>
        <td class="col-num">{idx}</td>
        <td class="col-cmd"><code>{html.escape(item['cli_group'])}</code></td>
        <td class="col-title">{html.escape(item['title'])}</td>
        <td class="col-domain"><span class="badge badge-{badge_class}">{html.escape(item['domain'])}</span></td>
        <td class="col-count"><strong>{item['count']:,}</strong></td>
    </tr>
    """)

HTML_CONTENT = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Google Cloud CLI - 141 Services & Commands Inventory</title>
<style>
    @page {{
        size: A4 portrait;
        margin: 10mm 12mm 12mm 12mm;
        @bottom-right {{
            content: "Page " counter(page);
        }}
    }}
    @media print {{
        body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
        thead {{ display: table-header-group; }}
        tr {{ page-break-inside: avoid; }}
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #202124;
        margin: 0;
        font-size: 8.5pt;
        line-height: 1.25;
    }}
    .header {{
        border-bottom: 2px solid #1a73e8;
        padding-bottom: 8px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}
    .title {{
        font-size: 16pt;
        font-weight: 700;
        color: #1a73e8;
        letter-spacing: -0.3px;
        margin: 0;
    }}
    .subtitle {{
        font-size: 9pt;
        color: #5f6368;
        margin-top: 3px;
    }}
    .stats-box {{
        display: flex;
        gap: 12px;
    }}
    .stat-pill {{
        background: #f1f3f4;
        border: 1px solid #dadce0;
        border-radius: 6px;
        padding: 4px 10px;
        text-align: right;
    }}
    .stat-val {{
        font-size: 11pt;
        font-weight: 700;
        color: #1a73e8;
        line-height: 1.1;
    }}
    .stat-lbl {{
        font-size: 7pt;
        text-transform: uppercase;
        color: #5f6368;
        font-weight: 600;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }}
    th {{
        background-color: #f8f9fa;
        color: #3c4043;
        font-size: 7.8pt;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        border-bottom: 2px solid #dadce0;
        padding: 5px 6px;
        text-align: left;
    }}
    td {{
        padding: 4px 6px;
        border-bottom: 1px solid #e8eaed;
        vertical-align: middle;
    }}
    tr:nth-child(even) td {{
        background-color: #fafbfc;
    }}
    .col-num {{ width: 5%; text-align: center; color: #70757a; font-weight: 600; font-size: 8pt; }}
    .col-cmd {{ width: 22%; }}
    .col-cmd code {{
        font-family: "Consolas", "Courier New", monospace;
        background: #eef3fc;
        color: #174ea6;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 8pt;
        font-weight: 600;
    }}
    .col-title {{ width: 40%; font-weight: 500; color: #202124; }}
    .col-domain {{ width: 23%; }}
    .col-count {{ width: 10%; text-align: right; padding-right: 8px; color: #188038; font-size: 8.5pt; }}
    
    .badge {{
        display: inline-block;
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 7pt;
        font-weight: 600;
        background: #e8f0fe;
        color: #1967d2;
        border: 1px solid #d2e3fc;
        white-space: nowrap;
    }}
    .badge-compute {{ background: #e8f0fe; color: #1967d2; border-color: #d2e3fc; }}
    .badge-storage {{ background: #fef7e0; color: #b06000; border-color: #feefc3; }}
    .badge-databases {{ background: #e6f4ea; color: #137333; border-color: #ceead6; }}
    .badge-networking {{ background: #fce8e6; color: #c5221f; border-color: #fad2cf; }}
    .badge-security {{ background: #feefe3; color: #b06000; border-color: #fedfc8; }}
    .badge-ai {{ background: #f3e8fd; color: #7627bb; border-color: #e9d2fd; }}
    .badge-data {{ background: #e0f2fe; color: #0369a1; border-color: #bae6fd; }}
    .badge-operations {{ background: #f1f3f4; color: #3c4043; border-color: #dadce0; }}
</style>
</head>
<body>

<div class="header">
    <div>
        <div class="title">Google Cloud CLI (gcloud) - Services & Commands Catalog</div>
        <div class="subtitle">Complete inventory of active service groups, architectural classification, and available commands count</div>
    </div>
    <div class="stats-box">
        <div class="stat-pill">
            <div class="stat-val">{total_services}</div>
            <div class="stat-lbl">Services</div>
        </div>
        <div class="stat-pill">
            <div class="stat-val">{total_commands:,}</div>
            <div class="stat-lbl">Commands</div>
        </div>
    </div>
</div>

<table>
    <thead>
        <tr>
            <th class="col-num">#</th>
            <th class="col-cmd">CLI Group</th>
            <th class="col-title">Service Name / Description</th>
            <th class="col-domain">Architectural Domain</th>
            <th class="col-count">Commands</th>
        </tr>
    </thead>
    <tbody>
        {''.join(rows_html)}
    </tbody>
</table>

</body>
</html>
"""

TEMP_HTML.write_text(HTML_CONTENT, encoding="utf-8")
print(f"[+] Formatted HTML saved to temporary file: {TEMP_HTML.name}")

# ----------------------------------------------------------------------
# 6. RENDER PDF USING HEADLESS BROWSER
# ----------------------------------------------------------------------
print("[+] Generating high-resolution PDF document...")

render_args = [
    browser_exe,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--user-data-dir={os.environ.get('TEMP', '')}\\headless_pdf_gen",
    f"--print-to-pdf={OUTPUT_PDF}",
    str(TEMP_HTML)
]

try:
    subprocess.run(render_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n[✓] SUCCESS: Generated {OUTPUT_PDF.name}")
    print(f"    Total Services Documented: {total_services}")
    print(f"    Total Individual Commands: {total_commands:,}")
    print(f"    Saved directly to: {OUTPUT_PDF}")
finally:
    if TEMP_HTML.exists():
        TEMP_HTML.unlink()