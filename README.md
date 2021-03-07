# MESHカスタムタグ用API集

## API外部仕様

### 休日判定API (holiday)

リクエストを送った時点の日付が土日祝に該当するかどうかを返します。

- 休日判定
	- エンドポイント: /holiday/is_holiday
	- IN: JSON
		- date: 判定対象の日付。yyyy/mm/dd の形式
	- OUT: JSON
		- is_holiday: 土日祝の場合は true、平日の場合は false


### ステータス管理API (status)

ON/OFFのステートを管理します。
ソースファイルごとに管理するステートを分離しています。

- 状態を初期化
	- エンドポイント: /status/reset
	- IN: なし
	- OUT: なし
- フラグをONにセット
	- エンドポイント: /status/on
	- IN: JSON
		- name: ステータス名
	- OUT: なし
- フラグをOFFにセット
	- エンドポイント: /status/off
	- IN: JSON
    - name: ステータス名
	- OUT: なし
- ステータスを指定値にセット
	- エンドポイント: /status/set
	- IN: JSON
		- name: ステータス名
		- value: セットするステータス値
	- OUT: なし
- ステータスを確認
	- エンドポイント: /status/get_status
	- IN: JSON
		- name: ステータス名
	- OUT: JSON
		- result: -1=エラー発生, それ以外=ステータス値
- 最終更新日時を確認
	- エンドポイント: /status/get_latest
	- IN: JSON
		- name: ステータス名
	- OUT: JSON
		- result: -1=エラー発生, それ以外=最終更新日時(yyyy-mm-dd)
- 現在日時と最終更新日時の差分を確認
	- エンドポイント: /status/get_latest_span
	- IN: JSON
		- name: ステータス名
	- OUT: JSON
		- result: -1=エラー発生, それ以外=現在日時と最終更新日時の差分秒数(float)


### 雨傘判定API (weather)

通勤時間帯にあたる9:00-10:00, 18:00-22:00の札幌市の天気予報を返します。
朝に判定して、何らかの手段にてアラートを出すようなユースケースを想定しています。

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

## デプロイ方法

- 各種APIのDockerコンテナーを一式ビルドして起動します。

```bash
$ docker-compose up --build -d
```

- 各種APIにGETもしくはPOSTでアクセスします。
  - 例: `http://HOSTNAME:3001/holiday/is_holiday?date=2020/01/01`
