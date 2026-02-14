# CSV Processor Task Rules

このディレクトリ `tools/csv_processor/` での作業に関するルールです。

## 1. 基本方針
- **AI支援型ユーザーワークフロー**: ユーザーが提供した画像 (`input/`) を元に、AIがその「目」を使ってCSVデータ (`output/` または `tools/csv_processor/`) を作成します。
- **シンプルさと実用性**: 過度なルール（旧SOP）に縛られず、画像から読み取れる情報を素直にデータ化してください。
- **参照ルール**: このファイルに記載されたルールを最優先とします。

## 2. 運用ルール (Operational Rules)
AIエージェントは、対話的な確認を最小限に抑え、自律的にタスクを完遂してください。

1.  **確認不要 (No Confirmation Needed)**
    - 画像の読み込み、解析、CSVへの書き込み (`cat >> ...`) は、ユーザーの許可を待たずに連続して実行してください。
    - 「保存していいですか？」「次の画像を処理しますか？」といった確認は不要です。マニュアルの手順に従って最後まで自動で進めてください。

2.  **エラーハンドリング**
    - 読み取り不可能な画像があった場合は、その旨をログに残し、停止せずに次の画像の処理に進んでください。

## 3. 処理フロー
1. `tools/csv_processor/RULES.md` (本ファイル) および `tools/csv_processor/AI_AGENT_MANUAL.md` を熟読する。
2. `tools/csv_processor/input/` 内の全画像を順次確認する。
3. `tools/csv_processor/reasoning_log.md` に推論を記述する。
4. `tools/csv_processor/master_data.csv` にデータを追記する。
5. 全画像の処理が完了するまで止まらないこと。
