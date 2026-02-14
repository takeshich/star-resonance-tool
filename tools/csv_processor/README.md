# Star Resonance Tool - CSV Processor Kit

このディレクトリは、ゲーム「Star Resonance」のスクリーンショットからデータを抽出し、`master_data.csv` を作成するためのツールセットです。
**AIエージェント（Antigravity, Claude, ChatGPT, Gemini等）にこのディレクトリの `AI_AGENT_MANUAL.md` を読み込ませることで、高精度なCSV作成を依頼できます。**

## ディレクトリ構成

- **`AI_AGENT_MANUAL.md`**: **重要**。AIエージェントへの作業指示書（SOP）。これをAIに渡してください。
- **`input/`**: 解析したいスクリーンショット（.png）をここに置いてください。
- **`assets/master.png`**: アイコン識別のためのマスタ画像（辞書）。
- **`Workflows/csv_creation.md`**: スラッシュコマンド `/csv_creation` の定義ファイル。
- **`master_data.csv`**: 出力されるCSVファイル（UTF-8, カンマ区切り）。

## 使い方 (User Guide)

### 1. 準備
- `input/` フォルダに、データ化したいスクリーンショットを全て入れます。

### 2. AIへの指示
お使いのインターフェースに応じて、以下のいずれかの方法で実行してください。

#### A. Antigravity（サポーター/開発者モード）を使用する場合
チャット欄で以下のコマンドを入力するだけで、自動的に画像解析とCSV作成が開始されます。
> `/csv_creation`

#### B. 一般的なAIエージェント（ChatGPT/Claude等）を使用する場合
1. `AI_AGENT_MANUAL.md` と `input/` 内の画像をアップロードしてください。
2. 以下のプロンプトを入力してください：
   > 「`AI_AGENT_MANUAL.md` の手順に従って、`input/` フォルダの画像をデータ化し、`master_data.csv` を作成してください。欠損値は `0` で埋めてください。」

## 注意事項
- **本手法の強み (AI-Driven Visual Extraction)**:
    - 従来のOCRプログラムでは誤認識しやすいゲーム特有のアイコンや数値を、AIが「目」で見て厳密に判断します。
- **環境構築不要**:
    - ユーザーはPython環境やライブラリをインストールする必要はありません。AIとの対話だけで完結します。
