# MESHカスタムタグ用API集


## 休日判定API (holiday)

リクエストを送った時点の日付が土日祝に該当するかどうかを返します。

- 休日判定
	- エンドポイント: is_holiday
	- IN: JSON
		- date: 判定対象の日付。yyyy/mm/dd の形式
	- OUT: JSON
		- result: 平日の場合は0, 土日祝の場合は1


### APIデプロイ方法

- holiday ディレクトリーを (裸で) zipに固める
- Google Cloud Functions にアップロード
	- 実行する関数: is_holiday
<br>


## ステータス管理API (status)

ON/OFFのステートを管理します。
ソースファイルごとに管理するステートを分離しています。

### 忘れ物防止アラート (所持管理)

- 状態リセット
	- エンドポイント: /status/has_item/reset
	- IN: なし
	- OUT: なし
- 所持状態にセット
	- エンドポイント: /status/has_item/get
	- IN: なし
	- OUT: なし
- 所持状態を解除
	- エンドポイント: /status/has_item/put
	- IN: なし
	- OUT: なし
- 所持状態を確認
	- エンドポイント: /status/has_item/check
	- IN: なし
	- OUT: JSON
		- result: -1=エラー発生, 0=解除状態, 1=セットされた状態

### お薬アラート (服用管理)

- 状態リセット
	- エンドポイント: /status/medicine/reset
	- IN: なし
	- OUT: なし
- 服用状態にセット
	- エンドポイント: /status/medicine/get
	- IN: なし
	- OUT: なし
- 服用状態を解除
	- エンドポイント: /status/medicine/put
	- IN: なし
	- OUT: なし
- 服用状態を確認
	- エンドポイント: /status/medicine/check
	- IN: なし
	- OUT: JSON
		- result: -1=エラー発生, 0=解除状態, 1=セットされた状態

### APIデプロイ方法

- status ディレクトリーをWebサーバーの公開ディレクトリーにアップロードする
- WebサーバーのWSGIを有効化する
- venv等で status 内にPython3.7環境を構築する
- $ pip install -r requirements.txt
- Webサーバーを再起動した上で、所定のエンドポイントを呼び出す

<br>


## 雨傘判定API (weather)

通勤時間帯にあたる9:00-10:00, 18:00-22:00の札幌市の天気予報を返します。
朝に判定して、何らかの手段にてアラートを出すのがオススメです。

- 雨傘判定
	- エンドポイント: /weather/check
	- IN: なし
	- OUT: JSON
		- result: 以下のうちいずれか
			- 5: 4 を満たしており、かつ大雨警報/大雨特別警報/洪水警報のいずれかが発令されている
			- 4: 雨という天気が66%以上含むか、判定期間の降水確率平均が60%を超える
			- 3: 雨を含むか、判定期間の降水確率平均が40%を超える
			- 2: 曇りを含むか、判定期間の降水確率平均が0%を超える
			- 1: 晴れを含むか、判定期間の降水確率平均が0%
			- -1: エラー発生
<br>

### APIデプロイ方法

- status ディレクトリーをWebサーバーの公開ディレクトリーにアップロードする
- WebサーバーのWSGIを有効化する
- venv等で status 内にPython3.7環境を構築する
- $ pip install -r requirements.txt
- Webサーバーを再起動した上で、所定のエンドポイントを呼び出す

---

## 備忘録
python -m venv [newenvname]
他の作り方だとWSGIサーバーがうまく動作しないっぽいので注意
