#!/usr/bin/env python3
"""Generate PROOFCHAIN banners + slides + logos in PROOFCHAIN visual style.

PROOFCHAIN palette (cryptographic trust):
- Brand emerald:  #10b981 (verified, the "this is signed" signal)
- Brand dark:     #0a0e1a (background — deep navy, Linear/Vercel grade)
- Card surface:   #131826
- Border:         #1f2937
- Text primary:   #ffffff
- Text muted:     #9ca3af
- Accent blue:    #3b82f6 (Bright Data alignment)
- Signal warn:    #f59e0b
- Signal danger:  #ef4444

Layout principles (from PROOFCHAIN template):
- 1920×1080 hero canvas
- 22px left bar accent in brand color
- KPI strip pattern: large number + label
- Apple system fonts
- Single dominant headline, clean monospace tech detail
"""

import base64
from pathlib import Path
import subprocess

ROOT = Path('/Users/sardorrazikov1/Alish/proofchain/assets')
LOGOS = ROOT / 'external' / 'logos'
SLIDES = ROOT / 'slides'
ROOT.mkdir(parents=True, exist_ok=True)
SLIDES.mkdir(parents=True, exist_ok=True)


# --- Brand constants ---
BG_DARK = '#0a0e1a'
CARD = '#131826'
BORDER = '#1f2937'
WHITE = '#ffffff'
MUTED = '#9ca3af'
EMERALD = '#10b981'
BLUE = '#3b82f6'
AMBER = '#f59e0b'
RED = '#ef4444'

FONT_DEF = '''<defs>
    <style>
      .brand { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-weight: 900; }
      .heading { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-weight: 700; }
      .body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-weight: 400; }
      .mono { font-family: "SF Mono", Menlo, Consolas, monospace; }
    </style>
  </defs>'''


def img_to_base64(path):
    if not path.exists():
        return ""
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    ext = path.suffix[1:].lower()
    return f"data:image/{ext};base64,{b64}"


GITHUB_B64 = img_to_base64(LOGOS / 'github.png')
ANTHROPIC_B64 = img_to_base64(LOGOS / 'anthropic.png')
ZENODO_B64 = img_to_base64(LOGOS / 'zenodo.png')
ORCID_B64 = img_to_base64(LOGOS / 'orcid.png')


def write_svg_and_png(svg_content, name):
    """Write SVG, convert to PNG via rsvg-convert (1920x1080)."""
    svg_path = ROOT / f'{name}.svg' if not name.startswith('slides/') else ROOT / f'{name}.svg'
    png_path = svg_path.with_suffix('.png')
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg_content)
    subprocess.run(
        ['rsvg-convert', '-w', '1920', '-h', '1080', str(svg_path), '-o', str(png_path)],
        check=True, capture_output=True,
    )
    print(f'  ✓ {png_path.name} ({png_path.stat().st_size:,} bytes)')
    return png_path


# ============================================================
# 1. LOGO (1920×1920 square logo, also good as 512×512 favicon source)
# ============================================================
def gen_logo():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1920" width="1920" height="1920">
  {FONT_DEF}
  <rect width="1920" height="1920" fill="{BG_DARK}"/>
  <!-- 4 stacked hash-chain links (Ed25519 signature visualization) -->
  <g transform="translate(560, 460)">
    <!-- Block 1 -->
    <rect x="0" y="0" width="800" height="180" rx="20" fill="{CARD}" stroke="{EMERALD}" stroke-width="4"/>
    <text x="40" y="100" class="mono" fill="{EMERALD}" font-size="40" font-weight="700">SEQ 00</text>
    <text x="40" y="150" class="mono" fill="{MUTED}" font-size="30">prev: 000…000</text>
    <text x="500" y="100" class="mono" fill="{WHITE}" font-size="40" font-weight="700">✓</text>
    <!-- Connector line -->
    <line x1="400" y1="180" x2="400" y2="220" stroke="{EMERALD}" stroke-width="6"/>
    <!-- Block 2 -->
    <rect x="0" y="220" width="800" height="180" rx="20" fill="{CARD}" stroke="{EMERALD}" stroke-width="4"/>
    <text x="40" y="320" class="mono" fill="{EMERALD}" font-size="40" font-weight="700">SEQ 01</text>
    <text x="40" y="370" class="mono" fill="{MUTED}" font-size="30">prev: a3f7…</text>
    <text x="500" y="320" class="mono" fill="{WHITE}" font-size="40" font-weight="700">✓</text>
    <!-- Connector -->
    <line x1="400" y1="400" x2="400" y2="440" stroke="{EMERALD}" stroke-width="6"/>
    <!-- Block 3 -->
    <rect x="0" y="440" width="800" height="180" rx="20" fill="{CARD}" stroke="{EMERALD}" stroke-width="4"/>
    <text x="40" y="540" class="mono" fill="{EMERALD}" font-size="40" font-weight="700">SEQ 02</text>
    <text x="40" y="590" class="mono" fill="{MUTED}" font-size="30">prev: 9eeb…</text>
    <text x="500" y="540" class="mono" fill="{WHITE}" font-size="40" font-weight="700">✓</text>
  </g>
  <!-- Wordmark -->
  <text x="960" y="1280" text-anchor="middle" class="brand" fill="{WHITE}" font-size="120">PROOFCHAIN</text>
  <text x="960" y="1380" text-anchor="middle" class="body" fill="{EMERALD}" font-size="48" font-weight="600">Cryptographic provenance for AI agents</text>
</svg>'''
    # Write as 1920x1920 square (force square dimensions)
    svg_path = ROOT / 'logo.svg'
    svg_path.write_text(svg)
    subprocess.run(
        ['rsvg-convert', '-w', '1920', '-h', '1920', str(svg_path), '-o', str(ROOT / 'logo.png')],
        check=True, capture_output=True,
    )
    # Also smaller variants
    subprocess.run(
        ['rsvg-convert', '-w', '512', '-h', '512', str(svg_path), '-o', str(ROOT / 'logo_512.png')],
        check=True, capture_output=True,
    )
    subprocess.run(
        ['rsvg-convert', '-w', '256', '-h', '256', str(svg_path), '-o', str(ROOT / 'logo_256.png')],
        check=True, capture_output=True,
    )
    print(f'  ✓ logo.png + logo_512.png + logo_256.png')


# ============================================================
# 2. HERO BANNER 1920×1080 — LinkedIn / Twitter / GitHub social
# ============================================================
def gen_banner():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {FONT_DEF}
  <rect width="1920" height="1080" fill="{BG_DARK}"/>
  <!-- 22px left brand bar -->
  <rect x="0" y="0" width="22" height="1080" fill="{EMERALD}"/>

  <!-- Headline block -->
  <text x="100" y="220" class="brand" fill="{WHITE}" font-size="96">PROOFCHAIN</text>
  <text x="100" y="290" class="body" fill="{EMERALD}" font-size="40" font-weight="600">Other AI agents claim citations. PROOFCHAIN signs every one.</text>

  <!-- Subline -->
  <text x="100" y="360" class="body" fill="{MUTED}" font-size="28">Ed25519-signed, SHA-256 hash-chained evidence for every Bright Data fetch.</text>
  <text x="100" y="400" class="body" fill="{MUTED}" font-size="28">EU AI Act Article 12 compliant. IETF web-bot-auth aligned.</text>

  <!-- KPI strip -->
  <g transform="translate(100, 500)">
    <!-- KPI 1 -->
    <rect x="0" y="0" width="320" height="200" rx="16" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>
    <text x="40" y="80" class="brand" fill="{EMERALD}" font-size="80">51/51</text>
    <text x="40" y="130" class="body" fill="{WHITE}" font-size="24" font-weight="700">tests passing</text>
    <text x="40" y="165" class="body" fill="{MUTED}" font-size="20">Ed25519 + hash-chain verified</text>
    <!-- KPI 2 -->
    <rect x="350" y="0" width="320" height="200" rx="16" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>
    <text x="390" y="80" class="brand" fill="{EMERALD}" font-size="80">10/10</text>
    <text x="390" y="130" class="body" fill="{WHITE}" font-size="24" font-weight="700">benchmark questions</text>
    <text x="390" y="165" class="body" fill="{MUTED}" font-size="20">100% success rate (mock + live)</text>
    <!-- KPI 3 -->
    <rect x="700" y="0" width="320" height="200" rx="16" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>
    <text x="740" y="80" class="brand" fill="{EMERALD}" font-size="80">4</text>
    <text x="740" y="130" class="body" fill="{WHITE}" font-size="24" font-weight="700">Bright Data products</text>
    <text x="740" y="165" class="body" fill="{MUTED}" font-size="20">SERP · Scraper · Unlocker · Browser</text>
    <!-- KPI 4 -->
    <rect x="1050" y="0" width="320" height="200" rx="16" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>
    <text x="1090" y="80" class="brand" fill="{EMERALD}" font-size="80">~30s</text>
    <text x="1090" y="130" class="body" fill="{WHITE}" font-size="24" font-weight="700">per question</text>
    <text x="1090" y="165" class="body" fill="{MUTED}" font-size="20">SERP→scrape×N→synth, evidence inline</text>
  </g>

  <!-- Footer: hackathon + author -->
  <text x="100" y="980" class="body" fill="{MUTED}" font-size="22">Bright Data Web Data UNLOCKED · Sardor Razikov · github.com/SRKRZ23/proofchain · MIT License</text>

  <!-- Tech stamp top right -->
  <g transform="translate(1620, 60)">
    <rect x="0" y="0" width="280" height="80" rx="8" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="140" y="36" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="18" font-weight="700">ED25519 · SHA-256</text>
    <text x="140" y="62" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">RFC 8785 · IETF draft-05</text>
  </g>
</svg>'''
    write_svg_and_png(svg, 'banner')


# ============================================================
# 3. ARCHITECTURE DIAGRAM — 4-agent flow
# ============================================================
def gen_architecture():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {FONT_DEF}
  <rect width="1920" height="1080" fill="{BG_DARK}"/>
  <rect x="0" y="0" width="22" height="1080" fill="{EMERALD}"/>

  <!-- Title -->
  <text x="100" y="120" class="brand" fill="{WHITE}" font-size="64">Architecture</text>
  <text x="100" y="170" class="body" fill="{MUTED}" font-size="28">4 named agents · Bright Data MCP · Ed25519 evidence chain</text>

  <!-- Top: User Agent -->
  <g transform="translate(760, 240)">
    <rect x="0" y="0" width="400" height="100" rx="12" fill="{CARD}" stroke="{BLUE}" stroke-width="3"/>
    <text x="200" y="45" text-anchor="middle" class="heading" fill="{WHITE}" font-size="28">AI Agent (Claude / GPT)</text>
    <text x="200" y="78" text-anchor="middle" class="mono" fill="{MUTED}" font-size="18">MCP tool call</text>
  </g>
  <line x1="960" y1="340" x2="960" y2="400" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow)"/>

  <!-- 4 Agents row -->
  <g transform="translate(140, 420)">
    <!-- Searcher -->
    <rect x="0" y="0" width="380" height="180" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="190" y="55" text-anchor="middle" class="heading" fill="{WHITE}" font-size="30">SEARCHER</text>
    <text x="190" y="90" text-anchor="middle" class="body" fill="{EMERALD}" font-size="20">Bright Data SERP API</text>
    <text x="190" y="125" text-anchor="middle" class="body" fill="{MUTED}" font-size="18">Top-N organic results</text>
    <text x="190" y="155" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">→ fetch_serp evidence</text>
    <!-- Scraper -->
    <rect x="420" y="0" width="380" height="180" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="610" y="55" text-anchor="middle" class="heading" fill="{WHITE}" font-size="30">SCRAPER</text>
    <text x="610" y="90" text-anchor="middle" class="body" fill="{EMERALD}" font-size="20">Web Scraper + Unlocker</text>
    <text x="610" y="125" text-anchor="middle" class="body" fill="{MUTED}" font-size="18">Structured content + SHA-256</text>
    <text x="610" y="155" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">→ fetch_scraper evidence</text>
    <!-- Verifier -->
    <rect x="840" y="0" width="380" height="180" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="1030" y="55" text-anchor="middle" class="heading" fill="{WHITE}" font-size="30">VERIFIER</text>
    <text x="1030" y="90" text-anchor="middle" class="body" fill="{EMERALD}" font-size="20">Ed25519 + hash chain</text>
    <text x="1030" y="125" text-anchor="middle" class="body" fill="{MUTED}" font-size="18">Cross-source conflict detect</text>
    <text x="1030" y="155" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">→ source_conflict evidence</text>
    <!-- Synthesizer -->
    <rect x="1260" y="0" width="380" height="180" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="1450" y="55" text-anchor="middle" class="heading" fill="{WHITE}" font-size="30">SYNTHESIZER</text>
    <text x="1450" y="90" text-anchor="middle" class="body" fill="{EMERALD}" font-size="20">Claude Sonnet 4.6</text>
    <text x="1450" y="125" text-anchor="middle" class="body" fill="{MUTED}" font-size="18">Grounded answer + citations</text>
    <text x="1450" y="155" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">→ agent_synthesis evidence</text>
  </g>

  <!-- Connecting arrows between agents -->
  <line x1="520" y1="510" x2="560" y2="510" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="940" y1="510" x2="980" y2="510" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="1360" y1="510" x2="1400" y2="510" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow)"/>

  <!-- All packets flow down to evidence chain -->
  <line x1="330" y1="600" x2="330" y2="700" stroke="{EMERALD}" stroke-width="2" stroke-dasharray="6,4"/>
  <line x1="750" y1="600" x2="750" y2="700" stroke="{EMERALD}" stroke-width="2" stroke-dasharray="6,4"/>
  <line x1="1170" y1="600" x2="1170" y2="700" stroke="{EMERALD}" stroke-width="2" stroke-dasharray="6,4"/>
  <line x1="1590" y1="600" x2="1590" y2="700" stroke="{EMERALD}" stroke-width="2" stroke-dasharray="6,4"/>

  <!-- Bottom: Evidence Chain -->
  <g transform="translate(140, 720)">
    <rect x="0" y="0" width="1640" height="220" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="4"/>
    <text x="40" y="60" class="heading" fill="{WHITE}" font-size="36">Ed25519-signed Evidence Chain</text>
    <text x="40" y="105" class="body" fill="{EMERALD}" font-size="22">Every packet: SHA-256 hash + prev_hash + signed payload + seq number</text>
    <text x="40" y="145" class="body" fill="{MUTED}" font-size="20">Tamper any byte → whole chain verify fails. Public verification with open key.</text>

    <!-- Mini-chain visualization -->
    <g transform="translate(1100, 50)">
      <rect x="0" y="0" width="100" height="60" rx="6" fill="{BG_DARK}" stroke="{EMERALD}" stroke-width="2"/>
      <text x="50" y="38" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="20">#0</text>
      <line x1="100" y1="30" x2="120" y2="30" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow)"/>
      <rect x="120" y="0" width="100" height="60" rx="6" fill="{BG_DARK}" stroke="{EMERALD}" stroke-width="2"/>
      <text x="170" y="38" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="20">#1</text>
      <line x1="220" y1="30" x2="240" y2="30" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow)"/>
      <rect x="240" y="0" width="100" height="60" rx="6" fill="{BG_DARK}" stroke="{EMERALD}" stroke-width="2"/>
      <text x="290" y="38" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="20">#2</text>
      <line x1="340" y1="30" x2="360" y2="30" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow)"/>
      <rect x="360" y="0" width="100" height="60" rx="6" fill="{BG_DARK}" stroke="{EMERALD}" stroke-width="2"/>
      <text x="410" y="38" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="20">…</text>
    </g>

    <text x="40" y="195" class="mono" fill="{MUTED}" font-size="18">EU AI Act Article 12 compliant export · RFC 8785 canonicalization · IETF web-bot-auth aligned</text>
  </g>

  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M0,0 L12,6 L0,12 z" fill="{EMERALD}"/>
    </marker>
  </defs>
</svg>'''
    write_svg_and_png(svg, 'architecture')


# ============================================================
# 4. EVIDENCE PACKET VISUAL — cryptography deep-dive image
# ============================================================
def gen_evidence_packet():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {FONT_DEF}
  <rect width="1920" height="1080" fill="{BG_DARK}"/>
  <rect x="0" y="0" width="22" height="1080" fill="{EMERALD}"/>

  <text x="100" y="120" class="brand" fill="{WHITE}" font-size="64">Evidence Packet Anatomy</text>
  <text x="100" y="170" class="body" fill="{MUTED}" font-size="28">Inside every Bright Data fetch wrapped by PROOFCHAIN</text>

  <!-- Big JSON-style packet visualization -->
  <g transform="translate(140, 240)">
    <rect x="0" y="0" width="1640" height="700" rx="20" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="60" y="80" class="mono" fill="{EMERALD}" font-size="26">{{</text>
    <text x="120" y="130" class="mono" fill="{WHITE}" font-size="24">"content":</text>
    <text x="380" y="130" class="mono" fill="{MUTED}" font-size="24">"&lt;scraped HTML or JSON&gt;",</text>
    <text x="120" y="180" class="mono" fill="{WHITE}" font-size="24">"url":</text>
    <text x="260" y="180" class="mono" fill="{MUTED}" font-size="24">"https://sec.gov/10-K/TSLA",</text>
    <text x="120" y="230" class="mono" fill="{WHITE}" font-size="24">"sha256_hash":</text>
    <text x="430" y="230" class="mono" fill="{EMERALD}" font-size="24">"a3f7b29c8d…e4f1c8d2",</text>
    <text x="120" y="280" class="mono" fill="{WHITE}" font-size="24">"timestamp":</text>
    <text x="380" y="280" class="mono" fill="{MUTED}" font-size="24">"2026-05-30T15:00:00Z",</text>
    <text x="120" y="330" class="mono" fill="{WHITE}" font-size="24">"retrieval_method":</text>
    <text x="540" y="330" class="mono" fill="{BLUE}" font-size="24">"BRIGHT_DATA_SERP_API",</text>
    <text x="120" y="380" class="mono" fill="{WHITE}" font-size="24">"robots_txt_status":</text>
    <text x="540" y="380" class="mono" fill="{EMERALD}" font-size="24">"allowed",</text>
    <text x="120" y="430" class="mono" fill="{WHITE}" font-size="24">"ed25519_signature":</text>
    <text x="540" y="430" class="mono" fill="{EMERALD}" font-size="24">"9eebe2f126…83b3082dea01",</text>
    <text x="120" y="480" class="mono" fill="{WHITE}" font-size="24">"prev_hash":</text>
    <text x="380" y="480" class="mono" fill="{EMERALD}" font-size="24">"&lt;hash of seq-1 packet&gt;",</text>
    <text x="120" y="530" class="mono" fill="{WHITE}" font-size="24">"seq":</text>
    <text x="260" y="530" class="mono" fill="{MUTED}" font-size="24">42</text>
    <text x="60" y="580" class="mono" fill="{EMERALD}" font-size="26">}}</text>

    <!-- Side annotations -->
    <line x1="1280" y1="230" x2="1480" y2="230" stroke="{EMERALD}" stroke-width="2"/>
    <text x="1490" y="237" class="body" fill="{EMERALD}" font-size="22" font-weight="700">SHA-256 of content</text>

    <line x1="1280" y1="430" x2="1480" y2="430" stroke="{EMERALD}" stroke-width="2"/>
    <text x="1490" y="437" class="body" fill="{EMERALD}" font-size="22" font-weight="700">Ed25519 signature</text>

    <line x1="1280" y1="480" x2="1480" y2="480" stroke="{EMERALD}" stroke-width="2"/>
    <text x="1490" y="487" class="body" fill="{EMERALD}" font-size="22" font-weight="700">Hash-chain link</text>

    <text x="60" y="660" class="body" fill="{MUTED}" font-size="22">Tamper any field → signature fails. Mutate prev_hash → whole chain breaks downstream.</text>
  </g>

  <text x="100" y="1010" class="body" fill="{MUTED}" font-size="20">RFC 8785 JCS canonicalization · libsodium Ed25519 · SHA-256 commit · MIT licensed</text>
</svg>'''
    write_svg_and_png(svg, 'evidence_packet')


# ============================================================
# 5-9. PITCH DECK SLIDES (5 slides, 1920×1080 each)
# ============================================================

def gen_slide_1_hero():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {FONT_DEF}
  <rect width="1920" height="1080" fill="{BG_DARK}"/>
  <rect x="0" y="0" width="22" height="1080" fill="{EMERALD}"/>
  <!-- Big hero title -->
  <text x="960" y="400" text-anchor="middle" class="brand" fill="{WHITE}" font-size="140">PROOFCHAIN</text>
  <text x="960" y="490" text-anchor="middle" class="body" fill="{EMERALD}" font-size="48" font-weight="600">Cryptographic provenance for AI agents on the live web</text>
  <text x="960" y="560" text-anchor="middle" class="body" fill="{MUTED}" font-size="32">Other AI agents claim citations. PROOFCHAIN signs every one.</text>
  <!-- Subtitle box -->
  <g transform="translate(360, 700)">
    <rect x="0" y="0" width="1200" height="120" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="600" y="55" text-anchor="middle" class="body" fill="{WHITE}" font-size="30">Ed25519 + SHA-256 hash chain on every Bright Data fetch</text>
    <text x="600" y="95" text-anchor="middle" class="body" fill="{MUTED}" font-size="24">EU AI Act Article 12 compliant · IETF web-bot-auth aligned · MIT licensed</text>
  </g>
  <!-- Footer -->
  <text x="960" y="980" text-anchor="middle" class="body" fill="{MUTED}" font-size="22">Bright Data Web Data UNLOCKED · Sardor Razikov · github.com/SRKRZ23/proofchain</text>
</svg>'''
    write_svg_and_png(svg, 'slides/slide_1_hero')


def gen_slide_2_problem():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {FONT_DEF}
  <rect width="1920" height="1080" fill="{BG_DARK}"/>
  <rect x="0" y="0" width="22" height="1080" fill="{EMERALD}"/>
  <text x="100" y="120" class="brand" fill="{WHITE}" font-size="72">Three forces converging</text>
  <text x="100" y="180" class="body" fill="{MUTED}" font-size="28">Why agent-web provenance becomes regulatory infrastructure in 2026</text>

  <!-- 3 columns -->
  <g transform="translate(100, 280)">
    <!-- Force 1 -->
    <rect x="0" y="0" width="540" height="640" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="40" y="80" class="brand" fill="{EMERALD}" font-size="48">1</text>
    <text x="40" y="150" class="heading" fill="{WHITE}" font-size="34">Throwaway code</text>
    <text x="40" y="210" class="body" fill="{MUTED}" font-size="22">"Code is suddenly free, ephemeral,</text>
    <text x="40" y="240" class="body" fill="{MUTED}" font-size="22">malleable, discardable after use"</text>
    <text x="40" y="280" class="body" fill="{EMERALD}" font-size="20" font-weight="700">— Andrej Karpathy, Sequoia 2026</text>
    <text x="40" y="350" class="body" fill="{MUTED}" font-size="22">"30% of apps on Vercel already</text>
    <text x="40" y="380" class="body" fill="{MUTED}" font-size="22">come from agents"</text>
    <text x="40" y="420" class="body" fill="{EMERALD}" font-size="20" font-weight="700">— Guillermo Rauch, Vercel</text>
    <text x="40" y="510" class="body" fill="{WHITE}" font-size="24" font-weight="700">When code disappears,</text>
    <text x="40" y="540" class="body" fill="{WHITE}" font-size="24" font-weight="700">evidence is what remains.</text>

    <!-- Force 2 -->
    <rect x="570" y="0" width="540" height="640" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="610" y="80" class="brand" fill="{EMERALD}" font-size="48">2</text>
    <text x="610" y="150" class="heading" fill="{WHITE}" font-size="34">IETF web-bot-auth</text>
    <text x="610" y="200" class="body" fill="{MUTED}" font-size="22">draft-meunier-web-bot-auth-05</text>
    <text x="610" y="230" class="body" fill="{MUTED}" font-size="22">March 2026</text>
    <text x="610" y="300" class="body" fill="{WHITE}" font-size="22">Cloudflare + Google co-authored</text>
    <text x="610" y="350" class="body" fill="{MUTED}" font-size="22">Every AI bot gets Ed25519 keypair</text>
    <text x="610" y="380" class="body" fill="{MUTED}" font-size="22">RFC 9421 HTTP signing</text>
    <text x="610" y="450" class="body" fill="{MUTED}" font-size="22">Amazon, Cloudflare, Akamai, OpenAI</text>
    <text x="610" y="480" class="body" fill="{MUTED}" font-size="22">all aligned with the direction</text>
    <text x="610" y="560" class="body" fill="{EMERALD}" font-size="20" font-weight="700">No hash chain, no content evidence,</text>
    <text x="610" y="590" class="body" fill="{EMERALD}" font-size="20" font-weight="700">no compliance overlay → our space.</text>

    <!-- Force 3 -->
    <rect x="1140" y="0" width="540" height="640" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="1180" y="80" class="brand" fill="{EMERALD}" font-size="48">3</text>
    <text x="1180" y="150" class="heading" fill="{WHITE}" font-size="34">EU AI Act Article 12</text>
    <text x="1180" y="200" class="body" fill="{MUTED}" font-size="22">Enforcement begins August 2026</text>
    <text x="1180" y="270" class="body" fill="{WHITE}" font-size="22">6-month minimum log retention</text>
    <text x="1180" y="340" class="brand" fill="{RED}" font-size="56">€35M</text>
    <text x="1180" y="380" class="body" fill="{MUTED}" font-size="22">or 7% of turnover — whichever higher</text>
    <text x="1180" y="450" class="body" fill="{MUTED}" font-size="22">High-risk AI systems require</text>
    <text x="1180" y="480" class="body" fill="{MUTED}" font-size="22">tamper-evident audit trails</text>
    <text x="1180" y="560" class="body" fill="{EMERALD}" font-size="20" font-weight="700">Regulator-mandated infrastructure.</text>
    <text x="1180" y="590" class="body" fill="{EMERALD}" font-size="20" font-weight="700">Non-optional, not opt-in.</text>
  </g>

  <text x="960" y="1010" text-anchor="middle" class="body" fill="{EMERALD}" font-size="28" font-weight="700">PROOFCHAIN sits at the intersection of all three.</text>
</svg>'''
    write_svg_and_png(svg, 'slides/slide_2_problem')


def gen_slide_3_architecture():
    """Slide 3 reuses the architecture diagram."""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {FONT_DEF}
  <rect width="1920" height="1080" fill="{BG_DARK}"/>
  <rect x="0" y="0" width="22" height="1080" fill="{EMERALD}"/>

  <text x="100" y="100" class="brand" fill="{WHITE}" font-size="64">How it works</text>
  <text x="100" y="150" class="body" fill="{MUTED}" font-size="28">4 named agents · 4 Bright Data products · 1 cryptographic chain</text>

  <!-- Compact 4-agent row -->
  <g transform="translate(100, 250)">
    <rect x="0" y="0" width="420" height="240" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="210" y="70" text-anchor="middle" class="heading" fill="{WHITE}" font-size="36">SEARCHER</text>
    <text x="210" y="115" text-anchor="middle" class="body" fill="{EMERALD}" font-size="22">Bright Data SERP API</text>
    <text x="210" y="160" text-anchor="middle" class="body" fill="{MUTED}" font-size="20">Top-N organic results</text>
    <text x="210" y="200" text-anchor="middle" class="mono" fill="{MUTED}" font-size="18">→ fetch_serp</text>

    <rect x="440" y="0" width="420" height="240" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="650" y="70" text-anchor="middle" class="heading" fill="{WHITE}" font-size="36">SCRAPER</text>
    <text x="650" y="115" text-anchor="middle" class="body" fill="{EMERALD}" font-size="22">Web Scraper API + Unlocker</text>
    <text x="650" y="160" text-anchor="middle" class="body" fill="{MUTED}" font-size="20">Structured content + SHA-256</text>
    <text x="650" y="200" text-anchor="middle" class="mono" fill="{MUTED}" font-size="18">→ fetch_scraper</text>

    <rect x="880" y="0" width="420" height="240" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="1090" y="70" text-anchor="middle" class="heading" fill="{WHITE}" font-size="36">VERIFIER</text>
    <text x="1090" y="115" text-anchor="middle" class="body" fill="{EMERALD}" font-size="22">Ed25519 + hash chain</text>
    <text x="1090" y="160" text-anchor="middle" class="body" fill="{MUTED}" font-size="20">Cross-source conflict detect</text>
    <text x="1090" y="200" text-anchor="middle" class="mono" fill="{MUTED}" font-size="18">→ source_conflict</text>

    <rect x="1320" y="0" width="420" height="240" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="3"/>
    <text x="1530" y="70" text-anchor="middle" class="heading" fill="{WHITE}" font-size="36">SYNTHESIZER</text>
    <text x="1530" y="115" text-anchor="middle" class="body" fill="{EMERALD}" font-size="22">Claude Sonnet 4.6</text>
    <text x="1530" y="160" text-anchor="middle" class="body" fill="{MUTED}" font-size="20">Grounded answer + citations</text>
    <text x="1530" y="200" text-anchor="middle" class="mono" fill="{MUTED}" font-size="18">→ agent_synthesis</text>
  </g>

  <!-- Below: chain visualization -->
  <g transform="translate(100, 600)">
    <rect x="0" y="0" width="1720" height="280" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="4"/>
    <text x="40" y="70" class="heading" fill="{WHITE}" font-size="40">Ed25519-signed Evidence Chain</text>
    <text x="40" y="120" class="body" fill="{EMERALD}" font-size="24">Every packet: SHA-256 hash + prev_hash + Ed25519 signature + monotonic seq</text>

    <g transform="translate(40, 160)">
      <rect x="0" y="0" width="130" height="80" rx="8" fill="{BG_DARK}" stroke="{EMERALD}" stroke-width="2"/>
      <text x="65" y="36" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="24">SEQ 00</text>
      <text x="65" y="62" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">genesis</text>
      <line x1="130" y1="40" x2="180" y2="40" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow2)"/>
      <rect x="180" y="0" width="130" height="80" rx="8" fill="{BG_DARK}" stroke="{EMERALD}" stroke-width="2"/>
      <text x="245" y="36" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="24">SEQ 01</text>
      <text x="245" y="62" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">prev: a3f7…</text>
      <line x1="310" y1="40" x2="360" y2="40" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow2)"/>
      <rect x="360" y="0" width="130" height="80" rx="8" fill="{BG_DARK}" stroke="{EMERALD}" stroke-width="2"/>
      <text x="425" y="36" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="24">SEQ 02</text>
      <text x="425" y="62" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">prev: 9eeb…</text>
      <line x1="490" y1="40" x2="540" y2="40" stroke="{EMERALD}" stroke-width="3" marker-end="url(#arrow2)"/>
      <rect x="540" y="0" width="130" height="80" rx="8" fill="{BG_DARK}" stroke="{EMERALD}" stroke-width="2"/>
      <text x="605" y="36" text-anchor="middle" class="mono" fill="{EMERALD}" font-size="24">SEQ 03</text>
      <text x="605" y="62" text-anchor="middle" class="mono" fill="{MUTED}" font-size="16">prev: 8c12…</text>

      <text x="800" y="50" class="body" fill="{MUTED}" font-size="22">…N more packets, all hash-chained, all signed.</text>

      <text x="800" y="100" class="body" fill="{EMERALD}" font-size="22" font-weight="700">Tamper any byte → chain breaks downstream → public verify fails.</text>
    </g>
  </g>

  <defs>
    <marker id="arrow2" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M0,0 L12,6 L0,12 z" fill="{EMERALD}"/>
    </marker>
  </defs>
</svg>'''
    write_svg_and_png(svg, 'slides/slide_3_architecture')


def gen_slide_4_results():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {FONT_DEF}
  <rect width="1920" height="1080" fill="{BG_DARK}"/>
  <rect x="0" y="0" width="22" height="1080" fill="{EMERALD}"/>

  <text x="100" y="120" class="brand" fill="{WHITE}" font-size="72">Verified, not claimed</text>
  <text x="100" y="180" class="body" fill="{MUTED}" font-size="28">Every number below produced by a passing test or benchmark run</text>

  <!-- 6 KPI cards -->
  <g transform="translate(100, 260)">
    <rect x="0" y="0" width="540" height="180" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="40" y="100" class="brand" fill="{EMERALD}" font-size="100">51/51</text>
    <text x="40" y="145" class="body" fill="{WHITE}" font-size="26" font-weight="700">tests passing</text>
    <text x="280" y="100" class="body" fill="{MUTED}" font-size="20">Ed25519 + hash chain +</text>
    <text x="280" y="125" class="body" fill="{MUTED}" font-size="20">tamper detection + API</text>
    <text x="280" y="150" class="body" fill="{MUTED}" font-size="20">endpoints + 1000-record stress</text>

    <rect x="580" y="0" width="540" height="180" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="620" y="100" class="brand" fill="{EMERALD}" font-size="100">10/10</text>
    <text x="620" y="145" class="body" fill="{WHITE}" font-size="26" font-weight="700">enterprise questions</text>
    <text x="860" y="100" class="body" fill="{MUTED}" font-size="20">5.0 avg citations</text>
    <text x="860" y="125" class="body" fill="{MUTED}" font-size="20">0.82 avg confidence</text>
    <text x="860" y="150" class="body" fill="{MUTED}" font-size="20">100% success rate</text>

    <rect x="1160" y="0" width="540" height="180" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="1200" y="100" class="brand" fill="{EMERALD}" font-size="100">40</text>
    <text x="1200" y="145" class="body" fill="{WHITE}" font-size="26" font-weight="700">evidence packets</text>
    <text x="1380" y="100" class="body" fill="{MUTED}" font-size="20">Generated in benchmark</text>
    <text x="1380" y="125" class="body" fill="{MUTED}" font-size="20">Chain verifies end-to-end</text>
    <text x="1380" y="150" class="body" fill="{MUTED}" font-size="20">Tamper detected on demo</text>
  </g>

  <g transform="translate(100, 480)">
    <rect x="0" y="0" width="540" height="180" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="40" y="100" class="brand" fill="{EMERALD}" font-size="100">4</text>
    <text x="40" y="145" class="body" fill="{WHITE}" font-size="26" font-weight="700">Bright Data products</text>
    <text x="180" y="100" class="body" fill="{MUTED}" font-size="20">SERP API</text>
    <text x="180" y="125" class="body" fill="{MUTED}" font-size="20">Web Scraper API</text>
    <text x="180" y="150" class="body" fill="{MUTED}" font-size="20">Web Unlocker + Scraping Browser</text>

    <rect x="580" y="0" width="540" height="180" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="620" y="100" class="brand" fill="{EMERALD}" font-size="100">87</text>
    <text x="620" y="120" class="body" fill="{MUTED}" font-size="22">KB</text>
    <text x="620" y="155" class="body" fill="{WHITE}" font-size="26" font-weight="700">frontend bundle</text>
    <text x="800" y="100" class="body" fill="{MUTED}" font-size="20">Next.js 14 production build</text>
    <text x="800" y="125" class="body" fill="{MUTED}" font-size="20">5 static pages</text>
    <text x="800" y="150" class="body" fill="{MUTED}" font-size="20">TypeScript clean (0 errors)</text>

    <rect x="1160" y="0" width="540" height="180" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="1200" y="100" class="brand" fill="{EMERALD}" font-size="100">MIT</text>
    <text x="1200" y="145" class="body" fill="{WHITE}" font-size="26" font-weight="700">open source</text>
    <text x="1380" y="100" class="body" fill="{MUTED}" font-size="20">Pre-hackathon committed</text>
    <text x="1380" y="125" class="body" fill="{MUTED}" font-size="20">github.com/SRKRZ23/proofchain</text>
    <text x="1380" y="150" class="body" fill="{MUTED}" font-size="20">SDK on PyPI + npm (planned)</text>
  </g>

  <!-- Bottom: Stress test bar -->
  <g transform="translate(100, 720)">
    <rect x="0" y="0" width="1720" height="180" rx="16" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="40" y="60" class="heading" fill="{WHITE}" font-size="34">Stress test: 1000 records</text>
    <text x="40" y="110" class="body" fill="{EMERALD}" font-size="24">Whole-chain Ed25519 verification: TRUE · &lt;1s wall time</text>
    <text x="40" y="150" class="body" fill="{MUTED}" font-size="22">Production-grade reliability validated · no GC pressure · constant memory</text>
  </g>

  <text x="960" y="1010" text-anchor="middle" class="body" fill="{MUTED}" font-size="22">Reproduce: `python3 -m pytest tests/ backend/tests/ -v` · `python3 benchmarks/run_benchmark.py`</text>
</svg>'''
    write_svg_and_png(svg, 'slides/slide_4_results')


def gen_slide_5_traction():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {FONT_DEF}
  <rect width="1920" height="1080" fill="{BG_DARK}"/>
  <rect x="0" y="0" width="22" height="1080" fill="{EMERALD}"/>

  <text x="100" y="120" class="brand" fill="{WHITE}" font-size="72">Built for the regulated stack</text>
  <text x="100" y="180" class="body" fill="{MUTED}" font-size="28">Where PROOFCHAIN delivers measurable value today</text>

  <!-- Left: 5 verticals -->
  <g transform="translate(100, 280)">
    <text x="0" y="40" class="heading" fill="{EMERALD}" font-size="32">Five verticals — one engine</text>
    <g transform="translate(0, 80)">
      <text x="0" y="0" class="mono" fill="{WHITE}" font-size="22">1.</text>
      <text x="60" y="0" class="body" fill="{WHITE}" font-size="22" font-weight="700">Equity research analyst copilot</text>
      <text x="60" y="30" class="body" fill="{MUTED}" font-size="20">Flagship · $30B/yr labor waste · AlphaSense $4B comp</text>

      <text x="0" y="90" class="mono" fill="{WHITE}" font-size="22">2.</text>
      <text x="60" y="90" class="body" fill="{WHITE}" font-size="22" font-weight="700">AML / KYC bank surveillance</text>
      <text x="60" y="120" class="body" fill="{MUTED}" font-size="20">$3B+ fines on table · Recorded Future $2.65B comp</text>

      <text x="0" y="180" class="mono" fill="{WHITE}" font-size="22">3.</text>
      <text x="60" y="180" class="body" fill="{WHITE}" font-size="22" font-weight="700">Regulatory monitoring (RegTech)</text>
      <text x="60" y="210" class="body" fill="{MUTED}" font-size="20">Market $14.9B → $107B by 2035</text>

      <text x="0" y="270" class="mono" fill="{WHITE}" font-size="22">4.</text>
      <text x="60" y="270" class="body" fill="{WHITE}" font-size="22" font-weight="700">Vendor risk (TPCRM)</text>
      <text x="60" y="300" class="body" fill="{MUTED}" font-size="20">F500 cascade exposure · Mastercard RiskRecon</text>

      <text x="0" y="360" class="mono" fill="{WHITE}" font-size="22">5.</text>
      <text x="60" y="360" class="body" fill="{WHITE}" font-size="22" font-weight="700">Publisher provenance enforcement</text>
      <text x="60" y="390" class="body" fill="{MUTED}" font-size="20">NYT v Perplexity (Dec 2025) · Adobe Content Credentials</text>
    </g>
  </g>

  <!-- Right side: Acquirer landscape -->
  <g transform="translate(1000, 280)">
    <text x="0" y="40" class="heading" fill="{EMERALD}" font-size="32">Acquirer landscape</text>
    <g transform="translate(0, 80)">
      <rect x="0" y="0" width="800" height="60" rx="8" fill="{CARD}" stroke="{BORDER}" stroke-width="1"/>
      <text x="20" y="38" class="body" fill="{WHITE}" font-size="22" font-weight="700">Bright Data</text>
      <text x="220" y="38" class="body" fill="{MUTED}" font-size="20">natural compliance for 100M+ daily agents</text>

      <rect x="0" y="70" width="800" height="60" rx="8" fill="{CARD}" stroke="{BORDER}" stroke-width="1"/>
      <text x="20" y="108" class="body" fill="{WHITE}" font-size="22" font-weight="700">Cloudflare</text>
      <text x="220" y="108" class="body" fill="{MUTED}" font-size="20">IETF web-bot-auth co-authored architecture</text>

      <rect x="0" y="140" width="800" height="60" rx="8" fill="{CARD}" stroke="{BORDER}" stroke-width="1"/>
      <text x="20" y="178" class="body" fill="{WHITE}" font-size="22" font-weight="700">AlphaSense / Bloomberg</text>
      <text x="380" y="178" class="body" fill="{MUTED}" font-size="20">equity research vertical</text>

      <rect x="0" y="210" width="800" height="60" rx="8" fill="{CARD}" stroke="{BORDER}" stroke-width="1"/>
      <text x="20" y="248" class="body" fill="{WHITE}" font-size="22" font-weight="700">Anthropic</text>
      <text x="220" y="248" class="body" fill="{MUTED}" font-size="20">MCP provenance gap demand signal</text>

      <rect x="0" y="280" width="800" height="60" rx="8" fill="{CARD}" stroke="{BORDER}" stroke-width="1"/>
      <text x="20" y="318" class="body" fill="{WHITE}" font-size="22" font-weight="700">RegTech (NAVEX / Diligent)</text>
      <text x="380" y="318" class="body" fill="{MUTED}" font-size="20">EU AI Act forcing function</text>
    </g>
  </g>

  <!-- Footer CTA -->
  <g transform="translate(100, 940)">
    <rect x="0" y="0" width="1720" height="80" rx="12" fill="{CARD}" stroke="{EMERALD}" stroke-width="2"/>
    <text x="40" y="50" class="body" fill="{WHITE}" font-size="26" font-weight="700">Try it:</text>
    <text x="180" y="50" class="body" fill="{EMERALD}" font-size="26">proofchain.dev/demo</text>
    <text x="620" y="50" class="body" fill="{WHITE}" font-size="26" font-weight="700">Author:</text>
    <text x="760" y="50" class="body" fill="{EMERALD}" font-size="26">Sardor Razikov</text>
    <text x="1100" y="50" class="body" fill="{WHITE}" font-size="26" font-weight="700">Contact:</text>
    <text x="1250" y="50" class="body" fill="{EMERALD}" font-size="26">razikovsardor1@gmail.com</text>
  </g>
</svg>'''
    write_svg_and_png(svg, 'slides/slide_5_traction')


# ============================================================
# 10. SOCIAL CARD 1200×630 — Twitter/LinkedIn link preview
# ============================================================
def gen_social_card():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  {FONT_DEF}
  <rect width="1200" height="630" fill="{BG_DARK}"/>
  <rect x="0" y="0" width="14" height="630" fill="{EMERALD}"/>

  <text x="60" y="140" class="brand" fill="{WHITE}" font-size="72">PROOFCHAIN</text>
  <text x="60" y="200" class="body" fill="{EMERALD}" font-size="30" font-weight="600">Cryptographic provenance for AI agents</text>

  <text x="60" y="290" class="body" fill="{MUTED}" font-size="22">Ed25519-signed evidence on every Bright Data fetch.</text>
  <text x="60" y="320" class="body" fill="{MUTED}" font-size="22">Hash-chained. EU AI Act Article 12 compliant. MIT.</text>

  <!-- KPI strip compact -->
  <g transform="translate(60, 400)">
    <text x="0" y="50" class="brand" fill="{EMERALD}" font-size="64">51/51</text>
    <text x="0" y="85" class="body" fill="{WHITE}" font-size="20" font-weight="700">tests</text>
    <text x="220" y="50" class="brand" fill="{EMERALD}" font-size="64">10/10</text>
    <text x="220" y="85" class="body" fill="{WHITE}" font-size="20" font-weight="700">questions</text>
    <text x="500" y="50" class="brand" fill="{EMERALD}" font-size="64">40+</text>
    <text x="500" y="85" class="body" fill="{WHITE}" font-size="20" font-weight="700">evidence packets</text>
  </g>

  <text x="60" y="580" class="body" fill="{MUTED}" font-size="18">github.com/SRKRZ23/proofchain · Bright Data UNLOCKED Hackathon</text>
</svg>'''
    # Output at 1200x630 (Twitter/LinkedIn card aspect)
    svg_path = ROOT / 'social_card.svg'
    svg_path.write_text(svg)
    subprocess.run(
        ['rsvg-convert', '-w', '1200', '-h', '630', str(svg_path), '-o', str(ROOT / 'social_card.png')],
        check=True, capture_output=True,
    )
    print(f'  ✓ social_card.png (1200×630)')


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print('Generating PROOFCHAIN visual assets in PROOFCHAIN style...\n')

    print('LOGO:')
    gen_logo()

    print('\nBANNERS:')
    gen_banner()
    gen_architecture()
    gen_evidence_packet()

    print('\nPITCH DECK SLIDES (5 slides):')
    gen_slide_1_hero()
    gen_slide_2_problem()
    gen_slide_3_architecture()
    gen_slide_4_results()
    gen_slide_5_traction()

    print('\nSOCIAL CARD:')
    gen_social_card()

    print('\n✓ All assets generated.')
    print(f'  Location: {ROOT}/')
    print(f'  Slides:   {SLIDES}/')
