# compact stage – Blender Custom FX Add-on

## 🔷 概要

**compact stage** は、Blender 4.3.0 上で動作するインタラクティブなステージ演出ツールです。花びら・キラキラ粒子などを直感的な UI から生成でき、MV・VTuber 配信・ライブ演出などで活躍します。

![stage](images/stage.png)

---

## 🪄 ツール機能

### 🌸 Ring FX Generator

画像を円状に並べて放出するツール。サイズ・枚数・配置パターンを UI で調整可能で、華やかなステージ演出が簡単に作れます。

![ring FX](images/ring_FX.png)
![pink example](images/pink.png)

### 💫 Image Particle Tool

複数の PNG（花・ハート・星など）を個別にサイズ・枚数指定して飛ばせます。自然な放物線も演出でき、ランダム感と美しさを両立。

![img particle](images/img_partucle.png)

### 🌟 Burst Shape Generator

選んだ図形（Sphere, Starなど）を中央から放射状に展開するツール。テンポ感ある演出切り替えに活用できます。

![burst example](images/blue.png)

### 🔮 Hologram Glow FX

ピンクやブルーの発光色を選択し、ホログラム風のグローエフェクトを生成。SFや近未来的な演出にも対応。

![glow FX](images/blue.png)

---

## ⚙ 使用技術・環境

| ツール | バージョン・用途         |
|--------|--------------------------|
| Blender | 4.3.0                   |
| Python  | 3.10（bpy API 使用）    |
| VS Code | 開発環境                |
| GitHub  | ソース管理・公開        |

---

## 🔧 技術面での工夫

- **画像を複数スパイラル状に配置**：回転数や高さを UI から調整できるよう設計。
- **自然な粒子落下**：Rigid Body との連携でリアルな落下感を演出。
- **UIカスタマイズ**：画像ごとのサイズ・枚数設定などを柔軟に操作可能に。
- **放物線飛散エフェクト**：0.5倍の放物線にしてより自然な演出に対応。

---

## 🚀 今後の展望

- 音声や表情に反応するリアルタイム演出
- Unity / Unreal Engine との統合
- Geometry Nodes との連携による高度なビジュアル制御

---

## 👤 制作者

**吉田 琳花 (Rinka Yoshida)**  
© 2025 Rinka Yoshida – All rights reserved.

---

Built with ❤️ and Blender.
