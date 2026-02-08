# Star Resonance Tool - CSV Processor Kit

このディレクトリは、ゲーム「Star Resonance」のスクリーンショットからデータを抽出し、`master_data.csv` を作成するためのツールセットです。
**AIエージェント（Claude, ChatGPT, Gemini等）にこのディレクトリの `AI_AGENT_MANUAL.md` を読み込ませることで、高精度なCSV作成を依頼できます。**

## ディレクトリ構成

- **`AI_AGENT_MANUAL.md`**: **重要**。AIエージェントへの作業指示書（SOP）。これをAIに渡してください。
- **`input/`**: 解析したいスクリーンショット（.png）をここに置いてください。
- **`assets/master.png`**: アイコン識別のためのマスタ画像（辞書）。
- **`master_data.csv`**: 出力されるCSVファイル。
- **`batch_log.md`**: 作業進捗の記録ログ。


## 使い方 (User Guide)

1.  **準備**:
    - `input/` フォルダに、データ化したいスクリーンショットを全て入れます。
    - `tools/csv_processor/` ディレクトリを開きます。

2.  **AIへの指示**:
    - AIエージェントに以下のプロンプトを投げてください。
      > 「`tools/csv_processor/AI_AGENT_MANUAL.md` の手順に従って、`input/` フォルダの画像をデータ化し、`master_data.csv` を作成してください。」

3.  **完了**:
    - AIが処理を完了すると、`master_data.csv` にデータが追記されます。

## 注意事項
- **本手法の強み (AI-Driven Visual Extraction)**:
    - 従来のOCRプログラムでは誤認識しやすいゲーム特有のアイコンや数値を、AIが「目」で見て厳密に判断します。
    - これにより、限りなく100%に近い精度を実現しています。
- **環境構築不要**:
    - ユーザーはPython環境やライブラリをインストールする必要はありません。AIとのチャットだけで完結します。
