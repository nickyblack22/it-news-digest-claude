 #!/usr/bin/env python3
  import re
  import feedparser
  import google.generativeai as genai
  import os
  import html as html_lib
  from datetime import datetime, timezone, timedelta

  THAILAND_TZ = timezone(timedelta(hours=7))

  NEWS_SOURCES = [
      {"name": "TechCrunch",      "url": "https://techcrunch.com/feed/",                             "category": "IT
  ทั่วไป"},
      {"name": "The Verge",       "url": "https://www.theverge.com/rss/index.xml",                   "category": "IT
  ทั่วไป"},
      {"name": "Ars Technica",    "url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "category": "IT
  ทั่วไป"},
      {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/",                   "category": "AI /
  ML"},
      {"name": "Hacker News",     "url": "https://news.ycombinator.com/rss",                         "category":
  "Developer"},
  ]

  MAX_PER_SOURCE = 5
  SNIPPET_CHARS = 400


  def fetch_articles():
      articles = []
      for source in NEWS_SOURCES:
          try:
              feed = feedparser.parse(source["url"])
              for entry in feed.entries[:MAX_PER_SOURCE]:
                  raw = entry.get("summary", entry.get("description", ""))
                  clean = re.sub(r"<[^>]+>", " ", raw).strip()[:SNIPPET_CHARS]
                  articles.append({
                      "title":    entry.get("title", "").strip(),
                      "link":     entry.get("link", "#"),
                      "snippet":  clean,
                      "source":   source["name"],
                      "category": source["category"],
                  })
          except Exception as e:
              print(f"[WARN] {source['name']}: {e}")
      return articles


  def summarize(articles):
      genai.configure(api_key=os.environ["GEMINI_API_KEY"])
      model = genai.GenerativeModel("gemini-2.0-flash")
      lines = [f"[{a['source']}] {a['title']}\n{a['snippet']}" for a in articles]
      text = "\n\n".join(lines)
      prompt = f"""คุณคือบรรณาธิการข่าว IT ภาษาไทย
  จงสรุปรายการข่าวต่อไปนี้โดย:
  1. จัดกลุ่มตามหมวด: IT ทั่วไป / AI-ML / Developer
  2. เลือกข่าวสำคัญ 3-5 ข่าวต่อหมวด
  3. สรุปแต่ละข่าวเป็น 2 ประโยคภาษาไทย กระชับและได้ใจความ
  4. ใช้รูปแบบ Markdown

  ข่าว:
  {text}
  """
      response = model.generate_content(prompt)
      return response.text


  def md_to_html(md):
      lines = md.splitlines()
      out = []
      for line in lines:
          line = line.rstrip()
          if line.startswith("### "):
              out.append(f'<h3>{html_lib.escape(line[4:])}</h3>')
          elif line.startswith("## "):
              out.append(f'<h2>{html_lib.escape(line[3:])}</h2>')
          elif line.startswith("- ") or line.startswith("* "):
              out.append(f'<li>{html_lib.escape(line[2:])}</li>')
          elif line == "":
              out.append("<br>")
          else:
              out.append(f'<p>{html_lib.escape(line)}</p>')
      return "\n".join(out)


  def generate_html(articles, summary_md, now):
      months = ["","มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน",
                "กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]
      date_th = f"{now.day} {months[now.month]} {now.year}"
      summary_html = md_to_html(summary_md)

      categories = {}
      for a in articles:
          categories.setdefault(a["category"], []).append(a)

      cards_html = ""
      for cat, items in categories.items():
          cards_html += f'<section class="category"><h2 class="cat-title">{html_lib.escape(cat)}</h2><div
  class="cards">'
          for a in items:
              cards_html += f"""
              <article class="card">
                <span class="source-badge">{html_lib.escape(a['source'])}</span>
                <h3><a href="{html_lib.escape(a['link'])}" target="_blank"
  rel="noopener">{html_lib.escape(a['title'])}</a></h3>
                <p class="snippet">{html_lib.escape(a['snippet'])}</p>
              </article>"""
          cards_html += "</div></section>"

      return f"""<!DOCTYPE html>
  <html lang="th">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT News Digest — {now.strftime('%Y-%m-%d')}</title>
    <style>
      :root{{--bg:#0f1117;--surface:#1a1d27;--border:#2a2d3e;--accent:#7c6af7;--accent2:#56cfb2;--text:#e2e8f0;--muted:#
  8892a4;}}
      *{{box-sizing:border-box;margin:0;padding:0;}}
      body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.7;}}
      a{{color:var(--accent);text-decoration:none;}}a:hover{{text-decoration:underline;}}
      header{{background:linear-gradient(135deg,#1a1d27,#0f1117);border-bottom:1px solid var(--border);padding:2rem
  1rem;text-align:center;}}
      header h1{{font-size:2rem;font-weight:700;}}
      header h1 span{{color:var(--accent);}}
      .date{{color:var(--muted);margin-top:.4rem;font-size:.9rem;}}
      .container{{max-width:1100px;margin:0 auto;padding:2rem 1rem;}}
      .summary-box{{background:var(--surface);border:1px solid var(--border);border-left:4px solid
  var(--accent);border-radius:8px;padding:1.5rem 2rem;margin-bottom:2.5rem;}}
      .summary-box .label{{font-size:.75rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--acce
  nt);margin-bottom:.75rem;}}
      .summary-box h2{{font-size:1.05rem;color:var(--accent2);margin:1rem 0 .3rem;}}
      .summary-box h3{{font-size:.95rem;color:var(--text);margin:.8rem 0 .2rem;}}
      .summary-box p,.summary-box li{{color:var(--muted);font-size:.9rem;}}
      .summary-box li{{margin-left:1.2rem;}}
      .category{{margin-bottom:2.5rem;}}
      .cat-title{{font-size:.8rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent2);pad
  ding-bottom:.5rem;border-bottom:1px solid var(--border);margin-bottom:1rem;}}
      .cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem;}}
      .card{{background:var(--surface);border:1px solid
  var(--border);border-radius:8px;padding:1.2rem;transition:border-color .2s;}}
      .card:hover{{border-color:var(--accent);}}
      .source-badge{{font-size:.7rem;font-weight:600;text-transform:uppercase;color:var(--accent);background:rgba(124,10
  6,247,.12);border-radius:4px;padding:2px 7px;display:inline-block;margin-bottom:.5rem;}}
      .card h3{{font-size:.95rem;font-weight:600;line-height:1.4;margin-bottom:.5rem;}}
      .card h3 a{{color:var(--text);}}
      .card h3 a:hover{{color:var(--accent);}}
      .snippet{{font-size:.82rem;color:var(--muted);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical
  ;overflow:hidden;}}
      footer{{text-align:center;padding:2rem;color:var(--muted);font-size:.8rem;border-top:1px solid var(--border);}}
    </style>
  </head>
  <body>
    <header>
      <h1>IT News <span>Digest</span></h1>
      <div class="date">ประจำวันที่ {date_th} · อัปเดตอัตโนมัติทุกวัน · สรุปโดย Gemini AI</div>
    </header>
    <div class="container">
      <div class="summary-box">
        <div class="label">สรุปข่าวเด่นวันนี้โดย AI</div>
        {summary_html}
      </div>
      {cards_html}
    </div>
    <footer>สร้างอัตโนมัติโดย GitHub Actions · แหล่งข่าว: TechCrunch, The Verge, Ars Technica, MIT Tech Review, Hacker
  News</footer>
  </body>
  </html>"""

  </html>"""


  def main():
      now = datetime.now(THAILAND_TZ)
      print(f"[{now.strftime('%Y-%m-%d %H:%M')} ICT] Fetching articles...")
      articles = fetch_articles()
      print(f"  Fetched {len(articles)} articles")
      print("  Summarizing with Gemini...")
      summary_md = summarize(articles)
      print("  Generating HTML...")
      page = generate_html(articles, summary_md, now)
      with open("index.html", "w", encoding="utf-8") as f:
          f.write(page)
      print("  Saved index.html")


  if __name__ == "__main__":
      main()
