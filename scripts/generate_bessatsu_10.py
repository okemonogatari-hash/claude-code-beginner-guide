#!/usr/bin/env python3
"""
別冊⑩「みんなのAI活用法リスト」HTML生成スクリプト
JSON（/tmp/bessatsu_10_content.json）から HTML を出力する。

出力先：/Users/monoke/Downloads/claude_tmp/claude-code-beginner-guide/everyone-ai-usage-list.html
作成：2026-05-23 はるか
"""

import json
import html as html_lib
from pathlib import Path
from datetime import datetime

JSON_PATH = Path("/tmp/bessatsu_10_content.json")
HTML_OUT = Path("/Users/monoke/Downloads/claude_tmp/claude-code-beginner-guide/everyone-ai-usage-list.html")

def esc(s):
    if s is None:
        return ""
    return html_lib.escape(str(s))

def render_top20(items):
    """トップ20カード"""
    cards = []
    for i, it in enumerate(items, 1):
        date = esc(it.get("date", ""))
        title = esc(it.get("title", ""))
        income = esc(it.get("income", "") or it.get("impact", "—"))
        summary = esc(it.get("summary", ""))
        tools = it.get("tools", [])
        if isinstance(tools, str):
            tools = [tools]
        tools_html = "".join(f'<span class="tool-chip">{esc(t)}</span>' for t in tools)
        fit = esc(it.get("okemon_fit", ""))
        cards.append(f'''
        <article class="case-card top-card">
          <div class="rank-badge">#{i}</div>
          <div class="case-date">{date}</div>
          <h3 class="case-title">{title}</h3>
          <div class="case-income">{income}</div>
          <p class="case-summary">{summary}</p>
          <div class="case-tools">{tools_html}</div>
          {f'<div class="case-fit">💡 おけもん視点：{fit}</div>' if fit else ''}
        </article>''')
    return "\n".join(cards)

def render_income_map(income_map):
    """収益額別マップ"""
    labels = {
        "0-1man": ("¥0〜¥1万", "時短・自動化のみ", "#A8C4A0"),
        "1-10man": ("¥1万〜¥10万", "副収入入門", "#7BAEC4"),
        "10-50man": ("¥10万〜¥50万", "副業安定", "#C8A86F"),
        "50-100man": ("¥50万〜¥100万", "本業級", "#D68F4A"),
        "100-500man": ("¥100万〜¥500万", "事業級", "#B58A4A"),
        "500man-up": ("¥500万〜", "年商級", "#8A6A30"),
    }
    blocks = []
    for key, (label, sub, color) in labels.items():
        items = income_map.get(key, [])
        cases = "".join(f'''
            <li class="income-case">
              <span class="ic-date">{esc(it.get("date",""))}</span>
              <span class="ic-title">{esc(it.get("title",""))}</span>
              <span class="ic-summary">{esc(it.get("summary",""))}</span>
            </li>''' for it in items)
        blocks.append(f'''
        <div class="income-block" style="border-left-color:{color}">
          <header class="ib-head">
            <h3 class="ib-label" style="color:{color}">{label}</h3>
            <span class="ib-sub">{sub} / {len(items)}件</span>
          </header>
          <ul class="income-list">{cases or '<li class="ic-empty">該当事例なし</li>'}</ul>
        </div>''')
    return "\n".join(blocks)

def render_industry(catalog):
    """業種別カタログ（アコーディオン）"""
    blocks = []
    for industry, items in catalog.items():
        if not items:
            continue
        cases = "".join(f'''
            <li class="ind-case">
              <span class="ic-date">{esc(it.get("date",""))}</span>
              <strong class="ic-title">{esc(it.get("title",""))}</strong>
              <span class="ic-summary">{esc(it.get("summary",""))}</span>
            </li>''' for it in items)
        blocks.append(f'''
        <details class="industry-block">
          <summary class="ind-summary">
            <span class="ind-icon">🧑‍💼</span>
            <span class="ind-name">{esc(industry)}</span>
            <span class="ind-count">{len(items)}件</span>
          </summary>
          <ul class="industry-list">{cases}</ul>
        </details>''')
    return "\n".join(blocks)

def render_method(patterns):
    """やり方別パターン（アコーディオン＋型説明）"""
    blocks = []
    icons = {
        "LP・HP制作": "🎨", "せどり・物販自動化": "📦", "AI業務代行・効率化請負": "🛠",
        "動画・BGMコンテンツ": "🎬", "D2C（商品開発・販売）": "🛍",
        "コンサル・提案資料生成": "📊", "自社内省力化（経理・スケジュール等）": "⚙️",
        "教育・コーチング": "🎓", "データ分析・スクレイピング": "🔍",
        "アプリ・ツール自作": "📱"
    }
    for pattern, content in patterns.items():
        icon = icons.get(pattern, "💡")
        desc = ""
        examples = []
        if isinstance(content, dict):
            desc = content.get("description", "")
            examples = content.get("examples", [])
        elif isinstance(content, list):
            examples = content
        cases = "".join(f'''
            <li class="mth-case">
              <span class="ic-date">{esc(it.get("date",""))}</span>
              <strong class="ic-title">{esc(it.get("title",""))}</strong>
              <span class="ic-summary">{esc(it.get("summary",""))}</span>
            </li>''' for it in examples)
        blocks.append(f'''
        <details class="method-block">
          <summary class="mth-summary">
            <span class="mth-icon">{icon}</span>
            <span class="mth-name">{esc(pattern)}</span>
            <span class="mth-count">{len(examples)}件</span>
          </summary>
          {f'<p class="mth-desc">{esc(desc)}</p>' if desc else ''}
          <ul class="method-list">{cases}</ul>
        </details>''')
    return "\n".join(blocks)

def render_entry5(items):
    """入口5選カード"""
    cards = []
    for i, it in enumerate(items, 1):
        cards.append(f'''
        <article class="entry-card">
          <div class="entry-num">入口 {i}</div>
          <h3 class="entry-title">{esc(it.get("title",""))}</h3>
          <div class="entry-date">{esc(it.get("date",""))}</div>
          <p class="entry-summary">{esc(it.get("summary",""))}</p>
          {f'<div class="entry-why">なぜこれが入口に良い：{esc(it.get("why",""))}</div>' if it.get("why") else ''}
        </article>''')
    return "\n".join(cards)

def render_quotes(quotes):
    """学長名言バナー"""
    items = []
    for q in quotes:
        text = esc(q.get("text", ""))
        date = esc(q.get("date", ""))
        context = esc(q.get("context", ""))
        items.append(f'''
        <blockquote class="quote-card">
          <p class="quote-text">"{text}"</p>
          <footer class="quote-meta">— 両学長 {date}{f' / {context}' if context else ''}</footer>
        </blockquote>''')
    return "\n".join(items)

def render_tool_chart(tool_freq):
    """ツール頻度のバーチャート"""
    bars = []
    # 数値順にソート（"約N件"から数字抽出）
    import re
    def extract_num(v):
        m = re.search(r"(\d+)", str(v))
        return int(m.group(1)) if m else 0
    sorted_tools = sorted(tool_freq.items(), key=lambda x: -extract_num(x[1]))
    if not sorted_tools:
        return ""
    max_n = extract_num(sorted_tools[0][1]) or 1
    for name, freq in sorted_tools:
        n = extract_num(freq)
        pct = max(5, int(n / max_n * 100))
        bars.append(f'''
        <div class="tool-row">
          <span class="tool-name">{esc(name)}</span>
          <div class="tool-bar-wrap">
            <div class="tool-bar" style="width:{pct}%"></div>
            <span class="tool-num">{esc(freq)}</span>
          </div>
        </div>''')
    return "\n".join(bars)

def render_industry_dist(dist):
    """業種分布"""
    rows = []
    for name, freq in dist.items():
        rows.append(f'<div class="dist-row"><span class="d-name">{esc(name)}</span><span class="d-val">{esc(freq)}</span></div>')
    return "\n".join(rows)

def render_operation_patterns(patterns):
    """運用パターン（ボーナス）"""
    if not patterns:
        return ""
    blocks = []
    if isinstance(patterns, dict):
        for name, content in patterns.items():
            if isinstance(content, dict):
                desc = content.get("description", "")
                examples = content.get("examples", [])
                ex_html = "".join(f'<li>{esc(e if isinstance(e, str) else e.get("title", str(e)))}</li>' for e in examples[:3])
                blocks.append(f'''
                <article class="op-card">
                  <h4>{esc(name)}</h4>
                  <p>{esc(desc)}</p>
                  {f'<ul class="op-examples">{ex_html}</ul>' if ex_html else ''}
                </article>''')
            else:
                blocks.append(f'<article class="op-card"><h4>{esc(name)}</h4><p>{esc(content)}</p></article>')
    elif isinstance(patterns, list):
        for p in patterns:
            if isinstance(p, dict):
                blocks.append(f'<article class="op-card"><h4>{esc(p.get("name",""))}</h4><p>{esc(p.get("description",""))}</p></article>')
    return "\n".join(blocks)

def render_warnings(warnings):
    """警告事例"""
    if not warnings:
        return ""
    items = []
    if isinstance(warnings, dict):
        for name, content in warnings.items():
            if isinstance(content, str):
                desc = content
            elif isinstance(content, dict):
                desc = content.get("description", "")
            elif isinstance(content, list):
                # リストの場合は中の要素を結合
                parts = []
                for c in content:
                    if isinstance(c, str):
                        parts.append(c)
                    elif isinstance(c, dict):
                        parts.append(c.get("description", c.get("title", str(c))))
                desc = " ／ ".join(parts)
            else:
                desc = str(content)
            items.append(f'<li><strong>{esc(name)}</strong>：{esc(desc)}</li>')
    elif isinstance(warnings, list):
        for w in warnings:
            if isinstance(w, dict):
                items.append(f'<li><strong>{esc(w.get("name", w.get("title","")))}</strong>：{esc(w.get("description",""))}</li>')
            else:
                items.append(f'<li>{esc(w)}</li>')
    return "\n".join(items)

def render_milestones(milestones):
    """マイルストーン"""
    if not milestones:
        return ""
    items = []
    if isinstance(milestones, list):
        for m in milestones:
            if isinstance(m, dict):
                items.append(f'<li><span class="ms-date">{esc(m.get("date",""))}</span> {esc(m.get("event", m.get("description","")))}</li>')
            else:
                items.append(f'<li>{esc(m)}</li>')
    return "\n".join(items)


def build_html(data):
    summary = data.get("summary", {})
    top20_html = render_top20(data.get("top20", []))
    income_html = render_income_map(data.get("income_map", {}))
    industry_html = render_industry(data.get("industry_catalog", {}))
    method_html = render_method(data.get("method_pattern", {}))
    entry5_html = render_entry5(data.get("entry_5", []))
    quotes_html = render_quotes(data.get("quotes", []))
    tool_chart = render_tool_chart(summary.get("tool_frequency", {}))
    industry_dist = render_industry_dist(summary.get("industry_distribution", {}))
    op_html = render_operation_patterns(data.get("operation_patterns", {}))
    warn_html = render_warnings(data.get("rejected_patterns_warnings", {}))
    ms_html = render_milestones(data.get("key_milestones_in_period", []))

    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>別冊⑩ みんなはこうやってAI使って稼いでるよ！｜虎の巻</title>
<meta name="description" content="学長ライブで報告された198件のAI活用リアル事例DB。トップ20＋収益別＋業種別＋やり方別＋初心者入口＋学長名言で「自分にもできるかも」を見つける別冊。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;700;900&family=Noto+Sans+JP:wght@400;500;700;900&family=Caveat:wght@600&display=swap" rel="stylesheet">
<style>
:root{{--main:#b58a4a;--main-deep:#8a6a30;--accent:#e8b57a;--accent-deep:#c89758;--ink:#2f2a24;--muted:#746d64;--line:#ead9bf;--ribbon:#d68f4a;--bg-soft:#fff8ed;--bg-page:#fdfaf2;--yaku:#7BAEC4;--gen:#A8C4A0;--coin:#C89758}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:"Noto Sans JP",sans-serif;background:linear-gradient(180deg,var(--bg-page) 0%,#fbfaf7 44%,#fff 100%);color:var(--ink);line-height:1.85}}
a{{color:var(--main-deep);font-weight:700;text-underline-offset:4px;text-decoration:none}}
a:hover{{color:var(--accent-deep);text-decoration:underline}}
.wrap{{width:min(1180px,94vw);margin:0 auto}}

/* Header */
header{{padding:64px 0 38px;border-bottom:1px solid var(--line);position:relative;overflow:hidden}}
header::before{{content:"";position:absolute;top:-40px;right:-40px;width:280px;height:280px;background:radial-gradient(circle,rgba(232,181,122,.25),transparent 70%);border-radius:50%}}
header::after{{content:"";position:absolute;bottom:-60px;left:-60px;width:240px;height:240px;background:radial-gradient(circle,rgba(123,174,196,.15),transparent 70%);border-radius:50%}}
.eyebrow{{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--main-deep);font-weight:900;margin-bottom:14px;position:relative;z-index:2}}
h1{{font-family:"Noto Serif JP",serif;font-size:clamp(28px,5vw,52px);line-height:1.25;color:var(--ink);position:relative;z-index:2}}
.title-em{{background:linear-gradient(180deg,transparent 60%,#f8e5c4 60%);padding:0 6px}}
.lead{{margin-top:24px;font-size:16px;color:var(--muted);max-width:860px;position:relative;z-index:2;line-height:1.95}}
.kicker{{font-family:"Caveat",cursive;font-size:22px;color:var(--coin);margin-top:10px;position:relative;z-index:2}}
.metrics{{display:flex;gap:32px;flex-wrap:wrap;margin-top:28px;position:relative;z-index:2}}
.metric{{display:flex;flex-direction:column;gap:4px}}
.metric .v{{font-family:"Noto Serif JP",serif;font-size:38px;font-weight:900;color:var(--main-deep);line-height:1;letter-spacing:-.02em}}
.metric .l{{font-size:12px;color:var(--muted);letter-spacing:.06em}}
.back{{display:inline-flex;align-items:center;margin-top:30px;padding:10px 20px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);font-size:14px;font-weight:600;transition:.3s;position:relative;z-index:2}}
.back:hover{{background:var(--accent);color:#fff;border-color:var(--accent);text-decoration:none}}

main{{padding:42px 0 60px}}
section{{padding:52px 0;border-bottom:1px solid var(--line)}}
section:last-child{{border-bottom:none}}
h2{{font-family:"Noto Serif JP",serif;font-size:28px;line-height:1.4;margin-bottom:6px;color:var(--ink);display:flex;align-items:center;gap:12px}}
.h2-sub{{font-size:14px;color:var(--muted);margin-bottom:28px;font-weight:400}}

/* Callout */
.callout{{background:var(--bg-soft);border-left:4px solid var(--accent);padding:20px 26px;border-radius:8px;color:#6b5742;margin:24px 0;font-size:14.5px;line-height:1.9}}
.callout strong{{color:var(--main-deep)}}

/* Top20 cards */
.cards-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px;margin-top:24px}}
.case-card{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px;box-shadow:0 6px 18px rgba(181,138,74,.07);transition:.3s;display:flex;flex-direction:column;gap:8px;position:relative}}
.case-card:hover{{transform:translateY(-3px);box-shadow:0 14px 32px rgba(181,138,74,.14)}}
.top-card{{padding-top:26px}}
.rank-badge{{position:absolute;top:-10px;right:18px;background:linear-gradient(135deg,var(--main),var(--main-deep));color:#fff;font-family:"Noto Serif JP",serif;font-weight:900;font-size:14px;padding:6px 12px;border-radius:999px;letter-spacing:.04em;box-shadow:0 4px 10px rgba(138,106,48,.25)}}
.case-date{{font-size:12px;color:var(--main-deep);font-weight:700;letter-spacing:.04em}}
.case-title{{font-family:"Noto Serif JP",serif;font-size:16px;line-height:1.5;color:var(--ink);margin:2px 0}}
.case-income{{font-family:"Noto Serif JP",serif;font-size:18px;font-weight:900;color:var(--coin)}}
.case-summary{{font-size:13.5px;color:#4a4540;line-height:1.75}}
.case-tools{{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}}
.tool-chip{{font-size:11px;background:#f0e8d8;color:var(--main-deep);padding:3px 9px;border-radius:999px;font-weight:600}}
.case-fit{{font-size:12px;background:#fff8ed;border-left:3px solid var(--accent);padding:8px 12px;color:#6b5742;margin-top:8px;border-radius:4px;line-height:1.6}}

/* Income Map */
.income-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:18px;margin-top:24px}}
.income-block{{background:#fff;border:1px solid var(--line);border-left:6px solid var(--main);border-radius:10px;padding:20px 22px}}
.ib-head{{margin-bottom:14px}}
.ib-label{{font-family:"Noto Serif JP",serif;font-size:18px;font-weight:900}}
.ib-sub{{font-size:12px;color:var(--muted);margin-left:6px}}
.income-list{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px}}
.income-case{{font-size:13.5px;line-height:1.65;color:#4a4540;border-bottom:1px dashed #f0e6cf;padding-bottom:8px}}
.income-case:last-child{{border-bottom:none}}
.ic-date{{display:inline-block;font-size:11px;font-weight:700;color:var(--main-deep);background:#fff8ed;padding:2px 7px;border-radius:4px;margin-right:6px}}
.ic-title{{font-weight:700;color:var(--ink);display:inline}}
.ic-summary{{display:block;color:var(--muted);font-size:12.5px;margin-top:3px;line-height:1.7}}
.ic-empty{{color:var(--muted);font-size:12.5px;font-style:italic}}

/* Industry */
.accordion-stack{{display:flex;flex-direction:column;gap:10px;margin-top:24px}}
.industry-block,.method-block{{background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}}
.industry-block[open],.method-block[open]{{box-shadow:0 6px 18px rgba(181,138,74,.08)}}
.ind-summary,.mth-summary{{padding:16px 22px;cursor:pointer;display:flex;align-items:center;gap:14px;font-weight:700;font-size:15px;color:var(--ink);list-style:none;background:#fffefa;transition:.2s}}
.ind-summary:hover,.mth-summary:hover{{background:var(--bg-soft)}}
.ind-summary::-webkit-details-marker,.mth-summary::-webkit-details-marker{{display:none}}
.ind-icon,.mth-icon{{font-size:22px}}
.ind-name,.mth-name{{flex:1;font-family:"Noto Serif JP",serif;font-size:17px}}
.ind-count,.mth-count{{font-size:12px;background:var(--accent);color:#fff;padding:3px 10px;border-radius:999px;font-weight:700}}
.industry-list,.method-list{{list-style:none;padding:16px 26px 20px;margin:0;display:flex;flex-direction:column;gap:12px;background:#fbfaf7}}
.ind-case,.mth-case{{font-size:13.5px;line-height:1.75;color:#4a4540;border-bottom:1px dashed #ead9bf;padding-bottom:10px}}
.ind-case:last-child,.mth-case:last-child{{border-bottom:none}}
.mth-desc{{padding:14px 26px;background:var(--bg-soft);color:#6b5742;font-size:13.5px;line-height:1.85;border-top:1px solid var(--line)}}

/* Entry5 */
.entry-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-top:24px}}
.entry-card{{background:linear-gradient(135deg,#fff,#fffaf0);border:1.5px solid var(--accent);border-radius:14px;padding:22px;display:flex;flex-direction:column;gap:8px;transition:.3s;position:relative}}
.entry-card:hover{{transform:translateY(-3px);box-shadow:0 12px 26px rgba(232,181,122,.25)}}
.entry-num{{font-family:"Caveat",cursive;font-size:22px;color:var(--accent-deep);font-weight:700}}
.entry-title{{font-family:"Noto Serif JP",serif;font-size:17px;line-height:1.5;color:var(--ink)}}
.entry-date{{font-size:11.5px;color:var(--main-deep);font-weight:700}}
.entry-summary{{font-size:13.5px;color:#4a4540;line-height:1.75;margin-top:4px}}
.entry-why{{font-size:12.5px;background:#fff;border-left:3px solid var(--accent-deep);padding:9px 13px;color:#6b5742;border-radius:4px;margin-top:6px;line-height:1.7}}

/* Quotes */
.quotes-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;margin-top:24px}}
.quote-card{{background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px 26px;border-left:5px solid var(--coin);transition:.3s}}
.quote-card:hover{{transform:translateY(-2px);box-shadow:0 8px 22px rgba(181,138,74,.1)}}
.quote-text{{font-family:"Noto Serif JP",serif;font-size:15.5px;line-height:1.85;color:var(--ink);font-weight:500}}
.quote-meta{{font-size:11.5px;color:var(--muted);margin-top:10px;letter-spacing:.04em}}

/* Tool chart */
.tool-chart{{margin-top:24px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:24px 28px}}
.tool-row{{display:grid;grid-template-columns:200px 1fr;gap:14px;align-items:center;margin-bottom:11px}}
.tool-name{{font-size:13.5px;font-weight:700;color:var(--ink)}}
.tool-bar-wrap{{position:relative;height:26px;background:#fbfaf7;border-radius:6px;overflow:hidden}}
.tool-bar{{position:absolute;top:0;left:0;height:100%;background:linear-gradient(90deg,var(--accent),var(--main));border-radius:6px;transition:.4s}}
.tool-num{{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:11.5px;color:#4a4540;font-weight:700;z-index:2}}

/* Industry distribution */
.dist-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px;margin-top:18px}}
.dist-row{{background:#fff;border:1px solid var(--line);border-radius:8px;padding:11px 16px;display:flex;justify-content:space-between;font-size:13px}}
.d-name{{color:var(--ink);font-weight:600}}
.d-val{{color:var(--main-deep);font-weight:700}}

/* Operations */
.op-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:18px}}
.op-card{{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 22px}}
.op-card h4{{font-family:"Noto Serif JP",serif;font-size:15px;color:var(--main-deep);margin-bottom:8px}}
.op-card p{{font-size:13px;color:#4a4540;line-height:1.75}}
.op-examples{{margin-top:8px;padding-left:18px;font-size:12px;color:var(--muted)}}

/* Warnings */
.warn-box{{background:#fdf3e6;border:1px solid #f0c890;border-radius:10px;padding:20px 26px;margin-top:18px}}
.warn-box h3{{font-family:"Noto Serif JP",serif;font-size:16px;color:#8a5a20;margin-bottom:10px}}
.warn-box ul{{padding-left:22px;font-size:13.5px;color:#6b4f24;line-height:1.85}}

/* Milestones */
.ms-list{{list-style:none;padding:0;margin-top:18px;display:flex;flex-direction:column;gap:8px}}
.ms-list li{{font-size:13.5px;color:#4a4540;line-height:1.75;padding:10px 16px;background:#fffefa;border-left:3px solid var(--accent);border-radius:4px}}
.ms-date{{display:inline-block;font-size:11.5px;font-weight:700;color:var(--main-deep);background:#fff8ed;padding:2px 8px;border-radius:4px;margin-right:8px}}

/* CTA / Related */
.related-block{{background:linear-gradient(135deg,#fff8ed,#fdf0dc);border-radius:18px;padding:34px 40px;margin-top:32px}}
.related-block h3{{font-family:"Noto Serif JP",serif;font-size:21px;color:var(--ink);margin-bottom:12px;text-align:center}}
.related-block p{{color:#4a4540;font-size:14.5px;text-align:center;margin-bottom:20px}}
.cta-btns{{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}}
.cta-btn{{display:inline-block;padding:12px 24px;background:linear-gradient(135deg,var(--main),var(--main-deep));color:#fff;border-radius:999px;font-weight:700;font-size:13.5px;transition:.3s}}
.cta-btn:hover{{transform:translateY(-2px);box-shadow:0 10px 22px rgba(138,106,48,.3);color:#fff;text-decoration:none}}
.cta-btn.alt{{background:#fff;color:var(--main-deep);border:1.5px solid var(--main)}}
.cta-btn.alt:hover{{background:var(--accent);color:#fff;border-color:var(--accent)}}

footer{{padding:38px 0 56px;color:var(--muted);font-size:13px;text-align:center;background:var(--bg-soft);margin-top:40px}}

@media(max-width:680px){{
  header{{padding-top:42px}}
  .metrics{{gap:18px}}
  .metric .v{{font-size:26px}}
  .cards-grid,.income-grid,.entry-grid,.quotes-grid,.dist-grid,.op-grid{{grid-template-columns:1fr}}
  .tool-row{{grid-template-columns:1fr;gap:6px}}
  section{{padding:38px 0}}
}}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <div class="eyebrow">Bonus Chapter 10 · everyone's AI usage</div>
    <h1>みんなはこうやって<br><span class="title-em">AI使って稼いでるよ！</span></h1>
    <p class="lead">
      学長ライブで報告された <strong>198件のリアル事例</strong>を、トップ20＋収益額別＋業種別＋やり方別＋初心者入口＋学長名言の<strong>6軸で整理</strong>したDB。<br>
      「Claude Code触ったけど何作ればいいかわからない…」が、ここを読んだら 1個は <strong>「これやってみよう」</strong>に変わる別冊。
    </p>
    <p class="kicker">"AIは関係しますか？じゃなくて、関係させていくもの" — 両学長</p>
    <div class="metrics">
      <div class="metric"><span class="v">198</span><span class="l">CASES</span></div>
      <div class="metric"><span class="v">44</span><span class="l">DAYS COVERED</span></div>
      <div class="metric"><span class="v">11</span><span class="l">INDUSTRIES</span></div>
      <div class="metric"><span class="v">10</span><span class="l">PATTERNS</span></div>
      <div class="metric"><span class="v">25</span><span class="l">QUOTES</span></div>
    </div>
    <a href="index.html" class="back">← 虎の巻トップへ戻る</a>
  </div>
</header>

<main>

<!-- 🏆 TOP20 -->
<section id="top20">
  <div class="wrap">
    <h2>🏆 おけもん厳選トップ20</h2>
    <p class="h2-sub">198件から「再現性・インパクト・自分にもできるかも感」で厳選した今すぐ動ける事例。</p>
    <div class="callout">
      <strong>選定基準：</strong>①再現性高い ②収益・時短のインパクト大 ③おけもんカンパニーが提供するコーチング／irodori／AI業務代行と接続できる ④「自分にもできるかも」と思える親近感
    </div>
    <div class="cards-grid">
      {top20_html}
    </div>
  </div>
</section>

<!-- 💰 Income Map -->
<section id="income">
  <div class="wrap">
    <h2>💰 収益額別マップ</h2>
    <p class="h2-sub">「いくら稼げるか」から見つけるAI活用。¥0〜年商級までフラットに並べた現実的な見取り図。</p>
    <div class="income-grid">
      {income_html}
    </div>
  </div>
</section>

<!-- 🧑‍💼 Industry Catalog -->
<section id="industry">
  <div class="wrap">
    <h2>🧑‍💼 業種・職業別カタログ</h2>
    <p class="h2-sub">「自分の業界の人はどう使ってる？」を11業種から探せるアコーディオン。</p>
    <div class="accordion-stack">
      {industry_html}
    </div>
  </div>
</section>

<!-- 🛠 Method Pattern -->
<section id="method">
  <div class="wrap">
    <h2>🛠 やり方別パターン</h2>
    <p class="h2-sub">「型」で分類した10パターン。LP制作・せどり自動化・AI業務代行など、まず1つ選んで掘る用。</p>
    <div class="accordion-stack">
      {method_html}
    </div>
  </div>
</section>

<!-- 🎯 Entry5 -->
<section id="entry5">
  <div class="wrap">
    <h2>🎯 「自分にもできるかも」の入口5選</h2>
    <p class="h2-sub">完全初心者OK・スキル不要・1日で手応えがある事例だけ抽出。最初の1個はここから。</p>
    <div class="entry-grid">
      {entry5_html}
    </div>
    <div class="related-block">
      <h3>📘 もっとパターンを見たい人は</h3>
      <p>別冊⑧「で、なに作る？」で<strong>5つのパターン</strong>に整理してある。気になるやつから一個ずつ。</p>
      <div class="cta-btns">
        <a href="whats-to-build.html" class="cta-btn">別冊⑧ で、なに作る？へ</a>
      </div>
    </div>
  </div>
</section>

<!-- 💌 Quotes -->
<section id="quotes">
  <div class="wrap">
    <h2>💌 学長の名言・パワーワード集</h2>
    <p class="h2-sub">44日分のライブから「これは保存版」を25本抽出。発信ネタにも自分の背中押しにも。</p>
    <div class="quotes-grid">
      {quotes_html}
    </div>
  </div>
</section>

<!-- 📊 Stats -->
<section id="stats">
  <div class="wrap">
    <h2>📊 全体統計：何が使われてる？誰が使ってる？</h2>
    <p class="h2-sub">198件の事例から見えた、2026年Q2のAI活用の地形図。</p>

    <h3 style="font-family:'Noto Serif JP',serif;font-size:18px;color:var(--main-deep);margin:30px 0 4px">🔧 ツール頻度ランキング</h3>
    <p style="font-size:13px;color:var(--muted);margin-bottom:8px">学長ライブ報告で登場した回数（推定）。Claude Codeが圧倒的1位。</p>
    <div class="tool-chart">
      {tool_chart}
    </div>

    <h3 style="font-family:'Noto Serif JP',serif;font-size:18px;color:var(--main-deep);margin:30px 0 4px">🧑‍💼 業種分布</h3>
    <div class="dist-grid">
      {industry_dist}
    </div>
  </div>
</section>

<!-- ⚙️ Operation Patterns -->
<section id="ops">
  <div class="wrap">
    <h2>⚙️ 学長たちの運用パターン（応用編）</h2>
    <p class="h2-sub">「事例」より一歩深い、AIを"どう運用するか"の型。おけもんカンパニーの「はるか経由フロー」もこの一つ。</p>
    <div class="op-grid">
      {op_html}
    </div>
  </div>
</section>

<!-- ⚠️ Warnings -->
<section id="warn">
  <div class="wrap">
    <h2>⚠️ 失敗・警告・落とし穴</h2>
    <p class="h2-sub">学長ライブで学長や視聴者が「これはダメだった」と報告したやつ。先回りで踏むな。</p>
    <div class="warn-box">
      <ul>
        {warn_html}
      </ul>
    </div>
  </div>
</section>

<!-- 📅 Milestones -->
<section id="milestones">
  <div class="wrap">
    <h2>📅 期間中（4/3〜5/20）のAI業界マイルストーン</h2>
    <p class="h2-sub">事例の背景にある「なぜ今この活用が爆発したか」を時系列で。</p>
    <ul class="ms-list">
      {ms_html}
    </ul>
  </div>
</section>

<!-- Related -->
<section id="related">
  <div class="wrap">
    <h2>🔗 関連別冊</h2>
    <p class="h2-sub">事例を見たら次は「動く」。手を動かす入口はここから。</p>
    <div class="related-block">
      <h3>事例DB → 実装ステップへ</h3>
      <p>「やってみたい」が見つかったら、別冊⑧で型に当てはめ、別冊⑥の仕組みで継続蓄積、別冊⑦で過去ライブを横断検索。</p>
      <div class="cta-btns">
        <a href="whats-to-build.html" class="cta-btn">別冊⑧ で、なに作る？</a>
        <a href="gakucho-live-30days-database.html" class="cta-btn alt">別冊⑦ 30日DB</a>
        <a href="gakucho-live-auto-process.html" class="cta-btn alt">別冊⑥ 自動取得の仕組み</a>
        <a href="gakucho-live-may4-cases.html" class="cta-btn alt">別冊④ 5/4回 深掘り版</a>
        <a href="libecity-learning-links.html" class="cta-btn alt">別冊⑤ ノウハウ図書館</a>
      </div>
    </div>
  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <p>別冊⑩ みんなはこうやってAI使って稼いでるよ！ ── 学長ライブAI活用事例DB</p>
    <p style="margin-top:8px">© 2026 Okemon Company · Bonus Chapter 10 · 生成: {today} / 44日分・198件構造化 / by はるか</p>
    <p style="margin-top:6px;font-size:11.5px">データソース：学長ライブ 4/3〜5/20の活用事例MD（Vault: あおいCDO/活用事例/）／自動取得は別冊⑥参照</p>
  </div>
</footer>
</body>
</html>
'''


def main():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    html_out = build_html(data)
    HTML_OUT.write_text(html_out, encoding="utf-8")
    print(f"✅ 生成完了: {HTML_OUT}")
    print(f"   ファイルサイズ: {HTML_OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
