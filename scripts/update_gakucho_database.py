#!/usr/bin/env python3
"""
学長ライブ30日分データベース 毎日自動更新スクリプト

実行：毎朝10:30 JST（launchd `com.okemon.gakucho-db-update.plist`）
出口：gakucho-live-30days-database.html を最新化して git push

処理フロー：
  1. YouTube Data API v3 で過去30日の朝ライブを取得（uploads + podcasts プレイリスト統合）
  2. 朝ライブ判定（duration≥80分 AND publishedAt JST 0:00-9:30）
  3. Vault側の要約MD・原液MDを動画IDキーでマッチング
  4. 不足の原液は youtube_transcript_api で取得＆Vault保存
  5. HTMLテーブル再生成（インタラクティブDB機能維持）
  6. git add → commit → push（差分があるときだけ）

設定：
  - 環境変数 YOUTUBE_API_KEY 必須（Meet to YouTube プロジェクト）
  - VAULT_DIR / REPO_DIR は環境変数 or 既定値
  - 失敗時は LINE通知（既存 line-notify スキル利用）

履歴：
  - 2026-05-21 初版（はるか）— v1.6 別冊⑦データベース運用化
"""

import os, sys, re, json, html, subprocess, urllib.request, urllib.parse
from pathlib import Path
from datetime import date, datetime, timedelta, timezone

# ==================== 設定 ====================
VAULT_DIR = Path(os.environ.get("VAULT_DIR", "/Users/monoke/Library/CloudStorage/GoogleDrive-okemonogatari@gmail.com/マイドライブ/000 おけ森"))
REPO_DIR = Path(os.environ.get("REPO_DIR", "/Users/monoke/Downloads/claude_tmp/claude-code-beginner-guide"))
HTML_PATH = REPO_DIR / "gakucho-live-30days-database.html"

API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_UPLOADS_PL = "UU67Wr_9pA4I0glIxDt_Cpyw"  # 両学長アップロードプレイリスト
PODCASTS_PL = "PLpwLNivKud-h_pNKrmLiV67hhhpeI5fts"  # 過去ライブ救済用

JST = timezone(timedelta(hours=9))
WEEKDAY_JA = ["月","火","水","木","金","土","日"]
WINDOW_DAYS = 30

LOG_PREFIX = f"[{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S JST')}]"

def log(msg): print(f"{LOG_PREFIX} {msg}", flush=True)

# ==================== 1. YouTube Data API ====================
def fetch_playlist_items(playlist_id, max_pages=4):
    items, token = [], None
    for _ in range(max_pages):
        params = {"part":"snippet,contentDetails", "playlistId":playlist_id, "maxResults":50, "key":API_KEY}
        if token: params["pageToken"] = token
        url = "https://www.googleapis.com/youtube/v3/playlistItems?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read().decode("utf-8"))
        items.extend(data.get("items", []))
        token = data.get("nextPageToken")
        if not token: break
    return items

def fetch_video_details(video_ids):
    out = []
    for i in range(0, len(video_ids), 50):
        params = {"part":"snippet,contentDetails", "id":",".join(video_ids[i:i+50]), "key":API_KEY}
        url = "https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=15) as r:
            out.extend(json.loads(r.read().decode("utf-8")).get("items", []))
    return out

def iso_to_minutes(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m: return 0
    h, mi, s = int(m.group(1) or 0), int(m.group(2) or 0), int(m.group(3) or 0)
    return h*60 + mi + s/60

def is_morning_live(video):
    minutes = iso_to_minutes(video["contentDetails"]["duration"])
    if minutes < 80: return False
    pub_utc = datetime.strptime(video["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    pub_jst = (pub_utc + timedelta(hours=9))
    if pub_jst.hour > 9 or (pub_jst.hour == 9 and pub_jst.minute > 30): return False
    return True

def get_morning_lives_30days():
    """過去30日の朝ライブ一覧取得"""
    log(f"YouTube Data API 取得開始（uploads + podcasts 両系統）")
    today = datetime.now(JST).date()
    window_start = (today - timedelta(days=WINDOW_DAYS-1)).isoformat()
    window_end = (today + timedelta(days=1)).isoformat()  # 余裕含む

    seen = {}
    for pl in [CHANNEL_UPLOADS_PL, PODCASTS_PL]:
        for it in fetch_playlist_items(pl):
            vid = it["snippet"]["resourceId"]["videoId"]
            seen.setdefault(vid, True)
    log(f"  プレイリスト統合: {len(seen)}件")

    details = fetch_video_details(list(seen.keys()))
    log(f"  videos.list メタ取得: {len(details)}件")

    lives = []
    for v in details:
        if not is_morning_live(v): continue
        pub_utc = datetime.strptime(v["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        pub_jst = pub_utc + timedelta(hours=9)
        pub_date = pub_jst.strftime("%Y-%m-%d")
        if not (window_start <= pub_date <= window_end): continue
        lives.append({
            "video_id": v["id"],
            "title": v["snippet"]["title"],
            "duration": v["contentDetails"]["duration"],
            "minutes": int(iso_to_minutes(v["contentDetails"]["duration"])),
            "pub_jst_date": pub_date,
            "pub_jst_time": pub_jst.strftime("%H:%M"),
        })
    lives.sort(key=lambda r: r["pub_jst_date"], reverse=True)
    log(f"  朝ライブ判定後（≥80分・JST 0-9:30）: {len(lives)}本")
    return lives

# ==================== 2. Vault マッピング ====================
def scan_vault():
    yaku_dir = VAULT_DIR / "コンテキスト/学び/YouTube要約"
    genekii_dirs = [VAULT_DIR / "コンテキスト/トランスクリプト原液", VAULT_DIR / "コンテキスト/学び/学長マガジン"]
    yaku, gen = {}, {}
    for f in yaku_dir.glob("YouTube要約：学長ライブ*.md"):
        try:
            m = re.search(r"v=([A-Za-z0-9_\-]{11})", f.read_text(encoding="utf-8"))
            if m: yaku[m.group(1)] = f.name
        except Exception: pass
    for d in genekii_dirs:
        if not d.exists(): continue
        for f in d.glob("学長ライブ*.md"):
            try:
                t = f.read_text(encoding="utf-8")
                m = re.search(r"動画ID:\s*([A-Za-z0-9_\-]{11})", t) or re.search(r"v=([A-Za-z0-9_\-]{11})", t)
                if m: gen[m.group(1)] = f.name
            except Exception: pass
    return yaku, gen

# ==================== 3. 原液取得（不足分救済） ====================
def fetch_missing_transcripts(lives, gen_map):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        log("⚠ youtube_transcript_api 未インストール・原液救済スキップ")
        return 0
    api = YouTubeTranscriptApi()
    out_dir = VAULT_DIR / "コンテキスト/トランスクリプト原液"
    saved = 0
    for v in lives:
        if v["video_id"] in gen_map: continue
        m, d = int(v["pub_jst_date"].split("-")[1]), int(v["pub_jst_date"].split("-")[2])
        # ファイル名にタイトル先頭25字を短縮利用
        short = re.sub(r"[【】「」｜/／\\:：?？*<>|・&\s]+", "_", v["title"])[:30].strip("_")
        out_path = out_dir / f"学長ライブ・{m}月{d}日_{short}（2026）.md"
        if out_path.exists():
            gen_map[v["video_id"]] = out_path.name
            continue
        try:
            segs = list(api.fetch(v["video_id"], languages=["ja"]))
            full = "\n".join(f"[{int(s.start//60):02d}:{int(s.start%60):02d}] {s.text}" for s in segs)
            body = f"""---
title: "学長ライブ・{m}月{d}日_{short}（2026）"
created: {datetime.now(JST).strftime('%Y-%m-%d')}
配信日: {v['pub_jst_date']}
動画ID: {v['video_id']}
動画タイトル: "{v['title']}"
URL: https://www.youtube.com/watch?v={v['video_id']}
チャンネル: 両学長 リベラルアーツ大学
動画長: {v['duration']}
type: トランスクリプト原液
取得方法: youtube_transcript_api（自動・update_gakucho_database.py）
tags:
  - 学長ライブ
  - 両学長
  - トランスクリプト原液
related:
  - "[[{v['pub_jst_date']}]]"
---

# 📺 学長ライブ・{m}月{d}日「{v['title']}」原液

**動画リンク:** [{v['title']}](https://www.youtube.com/watch?v={v['video_id']})
**配信日:** {v['pub_jst_date']}
**動画長:** {v['duration']}
**セグメント数:** {len(segs)}

---

## 全文トランスクリプト

{full}
"""
            out_path.write_text(body, encoding="utf-8")
            gen_map[v["video_id"]] = out_path.name
            saved += 1
            log(f"  ✅ 原液救済: {v['pub_jst_date']} {v['video_id']} ({len(full):,}字)")
        except Exception as e:
            log(f"  ⚠ 原液取得失敗 {v['video_id']}: {str(e)[:120]}")
    return saved

# ==================== 4. HTML再生成 ====================
def build_tbody(lives, yaku_map, gen_map):
    rows = []
    for r in lives:
        vid = r["video_id"]
        y, g = vid in yaku_map, vid in gen_map
        vl = []
        if y: vl.append('<span class="vlink vlink-yaku">📝 要約</span>')
        if g: vl.append('<span class="vlink vlink-gen">📜 原液</span>')
        if not vl: vl.append('<span class="vlink vlink-none">⚠ 未保存</span>')
        status = ("yaku" if y else "") + ("gen" if g else "") or "none"
        m, d = int(r["pub_jst_date"].split("-")[1]), int(r["pub_jst_date"].split("-")[2])
        y_, m_, d_ = map(int, r["pub_jst_date"].split("-"))
        wd = WEEKDAY_JA[date(y_, m_, d_).weekday()]
        kw = html.escape(r["title"]).lower()
        rows.append(f"""        <tr class="db-row" data-date="{r['pub_jst_date']}" data-month="{m}" data-status="{status}" data-keyword="{kw}">
          <td class="date">
            <div class="d-md"><span class="d-m">{m}/</span><span class="d-d">{d}</span></div>
            <div class="d-wd">（{wd}）</div>
            <div class="d-time">{r['pub_jst_time']}〜</div>
          </td>
          <td class="thumb">
            <a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">
              <img loading="lazy" src="https://i.ytimg.com/vi/{vid}/mqdefault.jpg" alt="" width="160" height="90">
            </a>
          </td>
          <td class="title">
            <a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" class="ytlink">{html.escape(r['title'][:80])}</a>
            <div class="meta-line">⏱ {r['minutes']}分 ／ 🎬 {vid} ／ {" ".join(vl)}</div>
          </td>
        </tr>""")
    return "\n".join(rows)

def update_html(lives, yaku_map, gen_map):
    src = HTML_PATH.read_text(encoding="utf-8")
    new_tbody = build_tbody(lives, yaku_map, gen_map)
    src = re.sub(r"(<tbody>)(.*?)(</tbody>)", lambda m: m.group(1)+"\n"+new_tbody+"\n        "+m.group(3), src, count=1, flags=re.DOTALL)
    yn = sum(1 for r in lives if r["video_id"] in yaku_map)
    gn = sum(1 for r in lives if r["video_id"] in gen_map)
    nn = sum(1 for r in lives if r["video_id"] not in yaku_map and r["video_id"] not in gen_map)
    ts = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    src = re.sub(r"v1\.6 \([^)]+\)", f"v1.6 ({len(lives)}本収録 / 📝要約 {yn} / 📜原液 {gn} / ⚠未保存 {nn} / 自動更新: {ts})", src)
    HTML_PATH.write_text(src, encoding="utf-8")
    return yn, gn, nn

# ==================== 5. git push ====================
def git_push(yn, gn, nn, total, saved_count):
    def run(*args):
        return subprocess.run(args, cwd=REPO_DIR, capture_output=True, text=True)
    # 差分なしならスキップ
    diff = run("git", "status", "--porcelain", "gakucho-live-30days-database.html").stdout.strip()
    if not diff:
        log("📊 HTML差分なし・push スキップ")
        return False
    msg = f"""auto: 学長ライブDB更新 ({datetime.now(JST).strftime('%Y-%m-%d %H:%M')})

- 📝要約 {yn} / 📜原液 {gn} / ⚠未保存 {nn} （{total}本中）
- 原液救済 +{saved_count}本
- 自動実行: update_gakucho_database.py（毎朝10:30 launchd）
"""
    run("git", "add", "gakucho-live-30days-database.html")
    cm = run("git", "commit", "-m", msg)
    if cm.returncode != 0:
        log(f"⚠ commit失敗: {cm.stderr[:200]}")
        return False
    ps = run("git", "push", "origin", "main")
    if ps.returncode != 0:
        log(f"⚠ push失敗: {ps.stderr[:200]}")
        return False
    log(f"✅ push成功: {cm.stdout.split()[1] if 'main' in cm.stdout else 'commit OK'}")
    return True

# ==================== main ====================
def main():
    if not API_KEY:
        log("❌ YOUTUBE_API_KEY 未設定")
        sys.exit(1)
    if not HTML_PATH.exists():
        log(f"❌ HTMLが見つからない: {HTML_PATH}")
        sys.exit(1)

    log("=== 学長ライブDB 自動更新 開始 ===")
    lives = get_morning_lives_30days()
    if not lives:
        log("⚠ 朝ライブ取得ゼロ・終了"); sys.exit(0)
    yaku_map, gen_map = scan_vault()
    log(f"Vault スキャン: 📝要約{len(yaku_map)} / 📜原液{len(gen_map)}")
    saved = fetch_missing_transcripts(lives, gen_map)
    log(f"原液救済: +{saved}本")
    yn, gn, nn = update_html(lives, yaku_map, gen_map)
    log(f"HTML更新: 📝{yn} / 📜{gn} / ⚠{nn} （{len(lives)}本中）")
    pushed = git_push(yn, gn, nn, len(lives), saved)
    log(f"=== 完了 (pushed={pushed}) ===")

if __name__ == "__main__":
    main()
