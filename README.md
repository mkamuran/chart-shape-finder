# Chart Shape Finder

手描きしたチャート形状に近い値動きをした日本株を探す Flask Web アプリです。Canvas に描いた線と日経225銘柄の終値系列を同じ点数に整形し、正規化したうえで類似度ランキングを返します。

就活・ポートフォリオでは、フロントエンドの操作体験、Flask API、外部データ取得、時系列データ処理、デプロイをまとめて説明できる題材として使えます。

## Features

- マウスまたは指でチャート形状を自由描画
- 日経225の固定銘柄リストを対象に類似した値動きを検索
- 比較期間は `1ヶ月 / 3ヶ月 / 6ヶ月 / 1年 / 3年 / 5年`
- 基準日を指定し、基準日の位置を `左端 / 中央 / 右端` から選択
- 平均出来高フィルター、上位表示件数の切り替え
- 類似率、銘柄情報、Yahoo株価リンク、みんかぶリンク、重ね合わせグラフを表示
- 同じ市場・期間・基準日の株価データを30分メモリキャッシュ

## Tech Stack

- Backend: Flask, Python
- Data: pandas, numpy, yfinance
- Frontend: HTML, CSS, JavaScript, Canvas API
- Deploy: Render / Gunicorn

## How It Works

1. Canvas で描いた線から Y 座標の系列を取り出す
2. 手描き線と株価終値を同じ点数にリサンプリングする
3. どちらも `0-1` の範囲に正規化する
4. 平均二乗誤差から `0-100%` の類似率に変換する
5. スコア順にランキングし、描画線と株価線を重ねて表示する

複雑な機械学習ではなく、説明しやすい軽量な時系列比較として実装しています。

## Base Date Rules

- 基準日はデフォルトで当日
- 未来の日付は検索時にエラー
- 基準日が休場日の場合は、その銘柄で取得できる直前の取引日に丸める
- `右端`: 基準日までの過去を比較
- `中央`: 基準日前後を比較
- `左端`: 基準日から後の値動きを比較

中央や左端を選んだ場合、基準日より後の株価データが必要です。必要な期間のデータが足りない銘柄は検索対象から外します。

## Project Structure

```text
.
├── app/
│   ├── market_data.py    # 銘柄CSV読み込み、yfinance取得、キャッシュ
│   ├── routes.py         # 画面表示と検索API
│   └── similarity.py     # リサンプリング、正規化、類似度計算
├── data/
│   └── nikkei225.csv     # 検索対象銘柄
├── static/
│   ├── app.js            # Canvas操作、API呼び出し、結果描画
│   └── styles.css
├── templates/
│   └── index.html
├── Procfile
├── requirements.txt
└── run.py
```

銘柄リストは Nikkei Indexes の Components ページを参考にした固定CSVです。ポートフォリオ提出時の安定性を優先し、構成銘柄のスクレイピングはアプリ本体に入れていません。

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

ブラウザで `http://localhost:5000` を開きます。

## Deploy

Render の Web Service で次のように設定します。

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn run:app`

無料枠では初回アクセスや初回検索が遅くなることがあります。

## Portfolio Talking Points

- Canvas のポインターイベントを使ってPC・スマホどちらでも描画できるようにした
- 時系列の長さが違っても比較できるよう、リサンプリングと正規化を分けて実装した
- 基準日と比較位置を変えられるようにして、過去チャート検索だけでなく前後比較にも対応した
- 外部APIへの負荷と待ち時間を抑えるため、検索条件ごとに30分キャッシュしている
- UI、API、データ処理をファイル単位で分け、説明・拡張しやすい構成にした
