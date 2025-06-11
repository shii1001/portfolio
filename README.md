# compact stage - Blenderカスタムツール紹介

## 🔷 概要
「compact stage」は、Blender 4.3.0上で動作する**インタラクティブなステージ演出ツール**です。  
アニメやライブ演出で見られるような花びら・キラキラ粒子を、直感的なUI操作で制御できるアドオンとして開発しました。

このツールは、MV・VTuber演出などにも応用可能です。

---

## 🔧 ツール機能紹介

### 🎯 Ring FX Generator
円状に画像エフェクトを並べて放出するツールです。  
UIから「画像・サイズ・個数・配置パターン」を設定でき、アイドルステージ風の華やかな演出が可能です。

### 🌸 Image Particle Tool
好きなPNG画像（花・ハート・星など）を複数読み込み、個別にサイズや枚数を設定してランダムに飛散させるツール。  
自然な放物線演出も含まれ、演出のアクセントに使えます。

### 💥 Burst Shape Generator
選択した図形（Sphere, Starなど）を中央から放射状に出現させる演出ツール。  
形状、色、サイズを選べるため、シーンのテンポに合わせて動きを調整できます。

### ✨ Hologram Glow FX
ピンクやブルーなどの発光色を選び、ホログラム風のグローエフェクトを生成します。  
舞台装置やSF的な演出、近未来感を出すシーンに最適です。

---

## 🎬 このアドオンを使って制作した作品：「compact stage」

---

## ⚙ 使用技術・環境

| ツール | バージョン・内容 |
|--------|------------------|
| Blender | 4.3.0 |
| Python  | 3.10（bpy API使用） |
| Visual Studio Code | 開発環境 |
| GitHub | ソース管理・公開 |
| ChatGPT-4o | 構造設計・構文確認補助 |

---

## 💡 テクニカルな工夫点

- `bpy.props`を使ったカスタムUIプロパティ設計
- `layout.template_list()`で複数画像の選択機能を自作
- 粒子の挙動を物理演算で表現することで自然さを向上
- アドオン全体を**モジュール分割**して保守・拡張性を確保
- 実装を通じて、「演出意図」と「操作性」のバランスを追求

---

## 🔭 今後の展望

- 音声や表情など「感情」に反応するリアルタイム演出制御
- UnityやUnrealとの連携、他ソフトでも使える汎用性の高いツール化
- Blenderのノードやジオメトリノードと連携した演出の強化

---

## 📄 補足資料（PDF・コード）

- [GitHub上の全コード](https://github.com/yourusername/portfolio/tree/main/compact_stage)

---

## 👤 制作者情報

吉田 琳花（Rinka Yoshida）  
テクニカルアーティスト志望｜表現と技術の融合を目指して活動中  
Email: your.email@example.com  
GitHub: [https://github.com/yourusername](https://github.com/yourusername)

