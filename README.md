# Claude Code 初心者向け虎の巻

リベシティ「AI初心者サポートチャット」運営有志による、Claude Code / Claude Cowork 初心者向けの導入・活用ガイドです。

このリポジトリは、オフ会配布、Web公開、共同編集、将来の製本に使うための **正本** です。森側のノートは運用記録・素材メモとして扱い、公開物としての最新版はこのGitHubリポジトリで管理します。

---

## まず見るリンク

| 種別 | リンク |
|---|---|
| 公開ページ | https://okemonogatari-hash.github.io/claude-code-beginner-guide/ |
| GitHub正本 | https://github.com/okemonogatari-hash/claude-code-beginner-guide |
| 共同編集ルール | [`PROJECT_RULES.md`](PROJECT_RULES.md) |
| GitHub標準の編集案内 | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| 参照元リンク集 | [`SOURCES.md`](SOURCES.md) |
| 別冊⑤ リベシティ学習リンク集 | https://okemonogatari-hash.github.io/claude-code-beginner-guide/libecity-learning-links.html |

---

## 公開ページ構成

| 種別 | ファイル | 公開URL | 位置づけ |
|---|---|---|---|
| 本編 | `index.html` | https://okemonogatari-hash.github.io/claude-code-beginner-guide/ | 初心者向けの入口。インストール、最初の一歩、FAQ、楽しみ方カタログ |
| 別冊1 | `gakucho-pdm-style.html` | https://okemonogatari-hash.github.io/claude-code-beginner-guide/gakucho-pdm-style.html | Claude Codeを会社化して扱う発想 |
| 別冊2 | `gakucho-magic-spell.html` | https://okemonogatari-hash.github.io/claude-code-beginner-guide/gakucho-magic-spell.html | 初心者がそのまま使える依頼文・呪文集 |
| 別冊3 | `boris-seminar-30min.html` | https://okemonogatari-hash.github.io/claude-code-beginner-guide/boris-seminar-30min.html | Anthropic公式30分セミナーの初心者向け整理 |
| 別冊4 | `gakucho-live-may4-cases.html` | https://okemonogatari-hash.github.io/claude-code-beginner-guide/gakucho-live-may4-cases.html | AIで稼ぐ実例集。学長ライブ5/4ベース |
| 別冊5 | `libecity-learning-links.html` | https://okemonogatari-hash.github.io/claude-code-beginner-guide/libecity-learning-links.html | リベシティ宿題リスト、AI初心者サポートチャット投稿ログ、ノウハウ図書館への学習導線 |

---

## 共同編集メンバー

| 役割 | 担当 | 主な責任 |
|---|---|---|
| オーナー | おけもん | 方針決定、最終判断、配布・活用先の整理 |
| 共同編集者 | みずやん | 初心者目線のレビュー、チャット運用からの改善提案、GitHub上の直接編集 |
| 進行管理 | はるかCEO | プロジェクト全体の入口整理、森側ハブ更新 |
| 技術管理 | あおいCDO | GitHub Pages、URL、技術的な整合性確認 |
| 発信物管理 | りんCMO | 部会資料、配布導線、発信素材としての管理 |

---

## 編集するときの読み順

他のAI、共同編集者、未来のおけちゃんが触るときは、まずこの順で確認してください。

1. この `README.md` で全体像を確認する
2. [`PROJECT_RULES.md`](PROJECT_RULES.md) で編集ルールを確認する
3. [`SOURCES.md`](SOURCES.md) で素材リンクと会員向けリンクの扱いを確認する
4. 編集対象のHTMLを開く
5. 変更後、公開URLで表示崩れとリンクを確認する

森側で再開する場合は、`はるかCEO/PJ_Claude Code初心者虎の巻/README.md` と `はるかCEO/PJ_Claude Code初心者虎の巻/進捗管理.md` もあわせて確認します。

---

## 編集ルールの要点

詳細は [`PROJECT_RULES.md`](PROJECT_RULES.md) に集約します。ここでは最低限だけ載せます。

- 小さな誤字修正、リンク修正、FAQ追記はそのままコミットOK
- 本編構成、章の追加削除、デザイン方針、URL変更は事前に一声かける
- リベシティ内の記事やチャット内容は全文転載しない。短い要約、短い引用、リンクで残す
- 個人情報、会員の発言、APIキー、ログイン情報は入れない
- 1コミット1目的を目安にする
- 変更した素材リンクは [`SOURCES.md`](SOURCES.md) にも追記する

---

## ファイル構成

```text
claude-code-beginner-guide/
├── README.md                         # このファイル。正本の入口
├── PROJECT_RULES.md                  # 共同編集・AI引き継ぎルール
├── CONTRIBUTING.md                   # GitHub標準の編集案内
├── SOURCES.md                        # 参照元リンク集
├── index.html                        # 本編
├── gakucho-pdm-style.html            # 別冊1
├── gakucho-magic-spell.html          # 別冊2
├── boris-seminar-30min.html          # 別冊3
├── gakucho-live-may4-cases.html      # 別冊4
└── libecity-learning-links.html      # 別冊5
```

---

## バージョン履歴

| Ver | 日付 | 主な変更 |
|---|---|---|
| v1.0 | 2026-04-30 | 初版。7章構成、FAQ、事例カード、公式リンク |
| v1.1 | 2026-05-04 | 別冊1、別冊2、FAQ追記、共同編集体制の開始 |
| v1.2 | 2026-05-05 | 別冊3「公式30分セミナー」を追加 |
| v1.3 | 2026-05-05 | 別冊4「AIで稼ぐ実例集」を追加 |
| v1.4 | 2026-05-07 | 共同編集ルール、素材リンク集、別冊5「リベシティ学習リンク集」を追加 |
| v1.5 | 2026-05-07 | 別冊5のトンマナ整備、AI初心者サポートチャットの記事投稿ログを追加 |

---

Made by リベシティ AI初心者サポートチャット運営チーム
