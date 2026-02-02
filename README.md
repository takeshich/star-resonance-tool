# Star Resonance Module Calculator

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/takeshich/star-resonance-tool/blob/main/Colab_Launch.ipynb)

ゲーム「スターレゾナンス」のモジュール装備において、最適な組み合わせ（特に「魔法耐性」「物理耐性」などのLv.6到達）を探索するための計算ツールです。

Python + Streamlit で構築されており、Docker環境またはGoogle Colabですぐに利用可能です。

## Features

- **CSV読み込み**: AIを使用し抽出したモジュールデータのCSV([CSVデータの作成と管理ガイド](CSV_CREATION.md))をドラッグ＆ドロップで読み込みます。
- **最適解の探索**: 指定したステータス（例：魔法耐性、物理耐性）がLv.6（値20以上）になる4つのモジュールの組み合わせを全探索します。
- **柔軟な条件設定**: 必須項目、優先項目、除外項目を設定して検索可能です。
- **シンプルUI**: 計算結果はランク順に表示され、各項目の到達レベルと合計値を一目で確認できます。

## 事前準備

本ツールを使用するには、ゲーム画面から抽出したモジュールデータのCSVファイルが必要です。
Docker版、Colab版どちらの場合も、以下のガイドを参考にCSVを作成して手元に用意してください。

- **[CSVデータの作成と管理ガイド](CSV_CREATION.md)**

## Google Colabでの使い方（推奨）

環境構築不要で、ブラウザ（PC・スマホ）からすぐに利用できます。

1. ページ上部の **[Open In Colab]** ボタンをクリックします。
2. Google Colabの画面が開きます（Googleアカウントへのログインが必要です）。
3. 画面上の **再生ボタン（▶）** を上から順にクリックして実行します。
   - 「警告: このノートブックは Google が作成したものではありません」と表示された場合は「実行」を押してください。
4. 最後のセルを実行後、ログの中に表示されるURLをクリックします。
   - `https://(ランダムな文字列).trycloudflare.com` という形式のリンクです。
5. アプリが起動します。

## Installation & Usage (Local Docker)


### 1. Clone or Download
このリポジトリをクローンするか、ZIPでダウンロードして解凍します。

### 2. Start Application
プロジェクトのルートディレクトリで以下のコマンドを実行し、コンテナを起動します。

```bash
docker compose up -d
```

### 3. Access
ブラウザで以下のURLにアクセスしてください。

http://localhost:8501

> **初期画面**  
> アプリケーションにアクセスすると、左側にサイドバー、右側にメインエリアが表示されます。  
> <img src="docs/images/app_initial.png" width="800" alt="アプリ初期画面">

### 4. Upload & Settings
サイドバーからCSVファイルをアップロードし、探索条件を設定します。

> **設定画面**  
> マスタ画像とモジュール画像を解析して作成したCSVファイルをアップロードし、Lv.6を目指す項目（必須）や優先項目を選択します。  
> <img src="docs/images/app_settings.png" width="400" alt="設定画面">

### 5. Calculation Result
「計算開始」ボタンを押すと、条件を満たす組み合わせが計算され、結果一覧が表示されます。

> **計算結果画面**  
> 組み合わせ候補がランク順に表示されます。到達レベルや合計値を確認できます。  
> <img src="docs/images/app_result.png" width="800" alt="計算結果画面">

### 6. Stop Application
使用を終了する場合は以下のコマンドを実行します。

```bash
docker compose down
```

## CSV Format

本ツールで読み込むCSVファイルには、以下のカラムが必要です。
値が存在しない項目には `0` を入力してください。

> **Note**
> 画像からAIを使って自動でCSVを作成するプロンプトや、手動での管理・修正方法は、 CSVデータの作成と管理ガイド **[CSVデータの作成と管理ガイド](CSV_CREATION.md)** を参照してください。

### 必須カラム一覧
以下の22項目がヘッダーに含まれている必要があります。

```text
ID
魔法耐性
物理耐性
極・HP凝縮
極・絶境守護
極・HP変動
極・HP吸収
筋力強化
敏捷強化
知力強化
特攻ダメージ強化
精鋭打撃
特攻回復強化
マスタリー回復強化
集中・詠唱
集中・攻撃速度
集中・会心
集中・幸運
極・ダメージ増強
極・適応力
極・応急処置
極・幸運会心
```

## License

[MIT License](LICENSE)
