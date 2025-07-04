<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>compact stage – Blender Custom FX Add‑on</title>
    <style>
      /* ------------------------------
        Minimal, responsive one‑page style
      ------------------------------ */
      :root {
        --bg: #f8f9fb;
        --primary: #4f46e5;
        --accent: #ec4899;
        --text: #1f2937;
        --surface: #ffffff;
      }
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: "Inter", "Noto Sans JP", sans-serif;
      }
      body {
        background: var(--bg);
        color: var(--text);
        line-height: 1.7;
      }
      header {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: #fff;
        padding: 4rem 1rem 5rem;
        clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
        text-align: center;
      }
      header h1 {
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 800;
        letter-spacing: -0.025em;
      }
      header p {
        margin-top: 1rem;
        font-size: 1.1rem;
        opacity: 0.9;
      }
      main {
        max-width: 900px;
        margin: -3rem auto 4rem;
        padding: 0 1rem;
      }
      section {
        background: var(--surface);
        border-radius: 1.25rem;
        padding: 2.5rem 2rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
        margin-bottom: 2.5rem;
      }
      h2 {
        font-size: 1.5rem;
        margin-bottom: 1.25rem;
        position: relative;
      }
      h2::after {
        content: "";
        position: absolute;
        left: 0;
        bottom: -0.4rem;
        width: 3rem;
        height: 3px;
        background: var(--primary);
        border-radius: 2px;
      }
      .feature {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
      }
      .feature img {
        width: 100%;
        border-radius: 0.75rem;
        object-fit: cover;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
      }
      .feature h3 {
        margin-top: 0;
        font-size: 1.25rem;
        color: var(--primary);
      }
      .feature p {
        margin-top: 0.5rem;
      }
      @media (max-width: 700px) {
        .feature {
          grid-template-columns: 1fr;
        }
      }
      table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
      }
      th, td {
        padding: 0.75rem 0.5rem;
        border-bottom: 1px solid #e5e7eb;
        text-align: left;
      }
      th {
        background: var(--bg);
        font-weight: 600;
      }
      footer {
        text-align: center;
        font-size: 0.875rem;
        padding: 2rem 1rem 3rem;
        color: #6b7280;
      }
    </style>
  </head>
  <body>
    <header>
      <h1>compact stage</h1>
      <p>Blender 4.3 カスタムステージ演出アドオン</p>
    </header>

    <main>
      <!-- Overview -->
      <section id="overview">
        <h2>概要</h2>
        <p>
          <strong>compact stage</strong> は、Blender 上で花びらやキラキラ粒子を
          直感的な UI から生成できるインタラクティブ演出ツールです。MV、VTuber
          配信、デジタルライブなど、幅広いシーンで活躍します。
        </p>
        <img src="images/stage.png" alt="Stage preview" style="margin-top:1.5rem;width:100%;border-radius:0.75rem;box-shadow:0 4px 12px rgba(0,0,0,0.06)" />
      </section>

      <!-- Features -->
      <section id="features">
        <h2>ツール機能</h2>

        <div class="feature">
          <div>
            <h3>Ring&nbsp;FX&nbsp;Generator</h3>
            <p>
              画像を円環状に並べ、サイズ・個数・パターンを自在に変更できます。
              アイドルステージのフラワーリング演出に最適です。
            </p>
          </div>
          <img src="images/ring_FX.png" alt="Ring FX UI" />
        </div>

        <div class="feature">
          <img src="images/pink.png" alt="Ring FX Example" />
          <div>
            <h3>Image&nbsp;Particle&nbsp;Tool</h3>
            <p>
              好きな PNG（花・ハート・星など）を複数読み込み、それぞれサイズや枚数を設定した上でランダムに飛散させられます。
            </p>
          </div>
        </div>

        <div class="feature">
          <div>
            <h3>Burst&nbsp;Shape&nbsp;Generator</h3>
            <p>
              図形（Sphere, Star など）を中央から放射状に出現させるツール。テンポよく場面転換を盛り上げます。
            </p>
          </div>
          <img src="images/blue.png" alt="Burst Shape Example" />
        </div>

        <div class="feature">
          <img src="images/blue.png" alt="Glow FX Example" />
          <div>
            <h3>Hologram&nbsp;Glow&nbsp;FX</h3>
            <p>
              ピンクやブルーの発光色を選択し、ホログラム風のグローエフェクトをワンクリックで生成します。
            </p>
          </div>
        </div>
      </section>

      <!-- Tech -->
      <section id="tech">
        <h2>使用技術</h2>
        <table>
          <tr><th>ツール</th><th>バージョン / 用途</th></tr>
          <tr><td>Blender</td><td>4.3.0</td></tr>
          <tr><td>Python (bpy)</td><td>3.10</td></tr>
          <tr><td>VS Code</td><td>開発環境</td></tr>
          <tr><td>GitHub</td><td>ソース管理・公開</td></tr>
        </table>
      </section>

      <!-- Future -->
      <section id="future">
        <h2>今後の展望</h2>
        <ul style="margin-left:1rem; list-style:square;">
          <li>音声・表情センサーと組み合わせたリアルタイム演出</li>
          <li>Unity / Unreal Engine との統合</li>
          <li>Geometry&nbsp;Nodes と連携した高度な FX</li>
        </ul>
      </section>

      <!-- Author -->
      <section id="author" style="text-align:center;">
        <h2>制作者</h2>
        <p>吉田 琳花 (Rinka&nbsp;Yoshida)</p>
        <p style="font-size:0.9rem;color:#6b7280;">© 2025 Rinka&nbsp;Yoshida – All rights reserved.</p>
      </section>
    </main>

    <footer>
      Built with ❤️ &nbsp;and Blender.
    </footer>
  </body>
</html>
