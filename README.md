# 🌸 compact stage - Blenderカスタムツール紹介

## 🔷 概要
「compact stage」は、Blender 4.3.0上で動作する**インタラクティブなステージ演出ツール**です。  
アニメやライブ演出で見られるような花びら・キラキラ粒子を、直感的なUI操作で制御できるアドオンとして開発しました。

このツールは、観客の感情や季節の移り変わりに合わせて演出を変える設計を意識しており、舞台・MV・VTuber演出などにも応用可能です。

---

## 🧩 主な機能（アドオン構成）

### 1. `ui_panel.py` - ユーザーインターフェースパネル
- Blenderのサイドパネル（Nキー）に「Petal Generator」タブを追加
- 以下のようなUIを実装：
  - 粒子画像の読み込み（複数可）
  - 枚数・サイズ・飛距離の設定
  - 配置方法（円形・スパイラル）や飛散アニメの選択

### 2. `petal_effect.py` - 花びらエフェクト生成
- 読み込んだ画像を平面に貼り付け、ランダムな向き・タイミングで放出
- アニメーションはランダム＋放物線制御（フレーム単位 or 物理演算）
- エフェクト用コレクションを自動生成し、シーンを汚さず管理

### 3. `stage_switcher.py` - 四季背景の切り替え
- UIボタン1つで背景を「春→夏→秋→冬」と変更
- 各季節に応じて色味・エフェクト素材・照明を切り替える
- リアルタイムの舞台演出や映像演出を想定した構成

---

## 🎥 デモ映像
![デモGIF](demo/compact_stage_demo.gif)

▶️ YouTube動画リンク：[https://youtube.com/your_demo_link](https://youtube.com/your_demo_link)

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

- [エントリーシートPDF](documents/entrysheet_ufotable.pdf)
- [GitHub上の全コード](https://github.com/yourusername/portfolio/tree/main/compact_stage)

---

## 👤 制作者情報

吉田 琳花（Rinka Yoshida）  
テクニカルアーティスト志望｜表現と技術の融合を目指して活動中  
Email: your.email@example.com  
GitHub: [https://github.com/yourusername](https://github.com/yourusername)

