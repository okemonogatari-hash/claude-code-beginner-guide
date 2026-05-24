(function() {
  // Styles for the index menu
  const css = `
    /* Floating Action Button */
    #okemori-index-trigger {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 99999;
      background: linear-gradient(135deg, #4F8CA8 0%, #759A6C 100%);
      color: #ffffff;
      border: none;
      border-radius: 50px;
      padding: 12px 20px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 14px;
      font-weight: bold;
      box-shadow: 0 8px 24px rgba(79, 140, 168, 0.3);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #okemori-index-trigger:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 30px rgba(79, 140, 168, 0.4);
    }
    #okemori-index-trigger:active {
      transform: translateY(0);
    }

    /* Sidebar Drawer */
    #okemori-index-drawer {
      position: fixed;
      top: 0;
      right: 0;
      width: min(380px, 90vw);
      height: 100vh;
      z-index: 999999;
      background: rgba(250, 247, 242, 0.82);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-left: 1px solid rgba(229, 221, 201, 0.5);
      box-shadow: -10px 0 40px rgba(61, 58, 53, 0.08);
      font-family: "Noto Sans JP", -apple-system, BlinkMacSystemFont, sans-serif;
      color: #3D3A35;
      display: flex;
      flex-direction: column;
      transform: translateX(100%);
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #okemori-index-drawer.open {
      transform: translateX(0);
    }

    /* Backdrop Overlay */
    #okemori-index-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(61, 58, 53, 0.3);
      backdrop-filter: blur(2px);
      -webkit-backdrop-filter: blur(2px);
      z-index: 999998;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #okemori-index-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    /* Drawer Header */
    .okemori-drawer-header {
      padding: 24px;
      border-bottom: 1px solid rgba(229, 221, 201, 0.6);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .okemori-drawer-title {
      font-size: 18px;
      font-weight: 700;
      margin: 0;
      letter-spacing: 0.04em;
    }
    .okemori-drawer-close {
      background: none;
      border: none;
      font-size: 20px;
      cursor: pointer;
      color: #7A7468;
      transition: color 0.2s;
      padding: 4px;
    }
    .okemori-drawer-close:hover {
      color: #3D3A35;
    }

    /* Drawer Menu List */
    .okemori-drawer-list {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      list-style: none;
      margin: 0;
    }
    
    /* Menu Item */
    .okemori-drawer-item a {
      display: flex;
      flex-direction: column;
      padding: 12px 16px;
      background: rgba(255, 255, 255, 0.5);
      border: 1px solid rgba(229, 221, 201, 0.6);
      border-radius: 10px;
      text-decoration: none;
      color: inherit;
      transition: all 0.25s ease;
    }
    .okemori-drawer-item a:hover {
      background: rgba(255, 255, 255, 0.95);
      border-color: #7BAEC4;
      transform: translateY(-1px);
    }
    .okemori-drawer-item.active a {
      background: linear-gradient(135deg, rgba(123, 174, 196, 0.12) 0%, rgba(168, 196, 160, 0.12) 100%);
      border-color: #7BAEC4;
      box-shadow: 0 4px 12px rgba(123, 174, 196, 0.1);
    }
    
    /* Title and Meta */
    .okemori-item-title {
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .okemori-item-desc {
      font-size: 11.5px;
      color: #7A7468;
      line-height: 1.4;
    }
    .okemori-item-badge {
      font-size: 10px;
      background: #7BAEC4;
      color: #fff;
      padding: 1px 6px;
      border-radius: 4px;
      font-weight: normal;
    }
    .okemori-drawer-item.active .okemori-item-title {
      color: #4F8CA8;
    }
    .okemori-current-marker {
      font-size: 10px;
      color: #759A6C;
      background: rgba(117, 154, 108, 0.15);
      padding: 1px 6px;
      border-radius: 4px;
      margin-left: auto;
      font-weight: bold;
    }

    @media (max-width: 900px) {
      #okemori-index-trigger {
        right: 16px;
        bottom: 82px;
        padding: 10px 16px;
        font-size: 13px;
      }
      #okemori-index-drawer {
        width: min(360px, 90vw);
      }
    }
  `;

  // Menu items config
  const items = [
    { filename: 'index.html', title: '🏠 虎の巻・本編', desc: 'Claude Code の初期設定から基本的な使い方、運用ルールまとめ。' },
    { filename: 'gakucho-pdm-style.html', title: '📘 別冊①：学長スタイル', desc: 'Claude Code を「会社化」し、メンバーに役職を与えて開発する体制。', badge: '別冊①' },
    { filename: 'gakucho-magic-spell.html', title: '📜 別冊②：魔法の呪文', desc: '安全に自動実行するための CLAUDE.md 設定用プロンプトと記述集。', badge: '別冊②' },
    { filename: 'boris-seminar-30min.html', title: '📺 別冊③：公式セミナー', desc: '開発チーム直伝の「Claude Code を使いこなすための 7 つのコツ」。', badge: '別冊③' },
    { filename: 'gakucho-live-may4-cases.html', title: '🦁 別冊④：AIで稼ぐ実例集', desc: '5月4日の学長ライブ発、電気工事士ゆさんの190万事例など。', badge: '別冊④' },
    { filename: 'libecity-learning-links.html', title: '🔗 別冊⑤：宿題＆リンク集', desc: 'リベシティ宿題リストと、ノウハウ図書館の記事キュレーション。', badge: '別冊⑤' },
    { filename: 'gakucho-live-auto-process.html', title: '📺 別冊⑥：ライブ自動処理', desc: '毎日12:00に自動で字幕取得・要約・事例抽出を行うスキルの仕組み。', badge: '別冊⑥' },
    { filename: 'gakucho-live-30days-database.html', title: '🗓️ 別冊⑦：30日分ライブDB', desc: '自動取得された29日分の実生データ一覧。タイトルやYouTubeリンク。', badge: '別冊⑦' },
    { filename: 'whats-to-build.html', title: '🤔 別冊⑧：で、なに作る？', desc: '「インストールしたけれど何を作ればいいか分からない」人へのアイデア集。', badge: '別冊⑧' },
    { filename: 'offkai-archive.html', title: '🌳 別冊⑨：オフ会アーカイブ', desc: 'Claude Code関連オフ会・シェア会・勉強会の記録とFAQの育ち方。', badge: '別冊⑨' },
    { filename: 'everyone-ai-usage-list.html', title: '🌟 別冊⑩：AI活用事例DB', desc: '学長ライブから抽出したAI活用事例198件の入口マップ。', badge: '別冊⑩' }
  ];

  // Insert CSS
  const styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // Get current page filename
  const currentPath = window.location.pathname;
  const currentFile = currentPath.substring(currentPath.lastIndexOf('/') + 1) || 'index.html';

  // Create overlay
  const overlay = document.createElement('div');
  overlay.id = 'okemori-index-overlay';
  document.body.appendChild(overlay);

  // Create drawer
  const drawer = document.createElement('div');
  drawer.id = 'okemori-index-drawer';
  
  // Create header
  const header = document.createElement('div');
  header.className = 'okemori-drawer-header';
  header.innerHTML = `
    <h3 class="okemori-drawer-title">🗺️ 虎の巻・全巻インデックス</h3>
    <button class="okemori-drawer-close" aria-label="閉じる">✕</button>
  `;
  drawer.appendChild(header);

  // Create list
  const list = document.createElement('ul');
  list.className = 'okemori-drawer-list';

  items.forEach(item => {
    const li = document.createElement('li');
    li.className = 'okemori-drawer-item';
    
    const isActive = currentFile === item.filename || (currentFile === '' && item.filename === 'index.html');
    if (isActive) {
      li.classList.add('active');
    }

    let badgeHtml = item.badge ? `<span class="okemori-item-badge">${item.badge}</span>` : '';
    let markerHtml = isActive ? `<span class="okemori-current-marker">現在地 📍</span>` : '';

    li.innerHTML = `
      <a href="${item.filename}">
        <span class="okemori-item-title">${item.title} ${badgeHtml} ${markerHtml}</span>
        <span class="okemori-item-desc">${item.desc}</span>
      </a>
    `;
    list.appendChild(li);
  });
  drawer.appendChild(list);
  document.body.appendChild(drawer);

  // Create Floating Button
  const trigger = document.createElement('button');
  trigger.id = 'okemori-index-trigger';
  trigger.innerHTML = `🧭 <span>全巻インデックス</span>`;
  document.body.appendChild(trigger);

  // Toggle Function
  function toggleDrawer(open) {
    if (open) {
      drawer.classList.add('open');
      overlay.classList.add('open');
    } else {
      drawer.classList.remove('open');
      overlay.classList.remove('open');
    }
  }

  // Event Listeners
  trigger.addEventListener('click', () => toggleDrawer(true));
  header.querySelector('.okemori-drawer-close').addEventListener('click', () => toggleDrawer(false));
  overlay.addEventListener('click', () => toggleDrawer(false));

  // ESC key close support
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      toggleDrawer(false);
    }
  });

})();
