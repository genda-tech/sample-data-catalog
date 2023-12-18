# data-catalog

# 事前に必要な準備
ローカル or AWS上のどちらでも動かせるように作成してあります。
## ローカルの場合
`config.yaml`と`secrets.toml`を作成して、以下のようなディレクトリ構成にします。
```
streamlit-data-catalog/
  ├ .streamlit/config.toml/ streamlitの背景の色などを設定
  ├ data-catalog.py/ データカタログのコード 
  ├ requirements.txt/ 必要なライブラリをインストールするのに使うrequirement.txt
 　　├ secrets.toml/ snowflakeの接続情報を記載する。
  └ config.yaml/ ログイン機能用の設定を記載する。
```
### config.yamlに記載すること
```yaml
credentials:
  usernames:
    [ユーザー名]:
      name: [ログイン時に使うuser名を指定]
      password: [パスワードをハッシュ化した文字列]
cookie:
  expiry_days: 1
  key: some_signature_key
  name: some_cookie_name
```
### secrets.tomlに記載すること
Snowflakeの接続情報を記載します。
以下のようなファイルを作成して、user~roleまで全て記載しておきます。
```toml
[snowflake]
user      = 
account   = 
password  = 
warehouse = 
role      =
```



## AWSで動かす場合
AWS Secrets Managerにて、シークレットを登録しておく必要があります。


### data_catalog_login
`data_catalog_login`というシークレット名でシークレットを作成し、
`CREDENTIAL`というシークレット値のシークレットを作成して、以下を登録しておきます。
```yaml
"credentials":
  "usernames":
    "[ユーザー名]":
      "name": "[ログイン時に使うuser名を指定]"
      "password": "[パスワードをハッシュ化した文字列]"
"cookie":
  "expiry_days": 1
  "key": "some_signature_key"
  "name": "some_cookie_name"
```

### snowflake_data_catalog
`snowflake_data_catalog`というシークレット名でシークレットを作成し、
`secrets.toml`で入力した内容と同じく、Snowflakeの接続情報を以下のシークレットキーで登録しておきます。
* USER
* ACCOUNT
* PASSWORD
* WAREHOUSE
* ROLE


# 主な機能
## ログイン画面
以下を入力してログインします。
`config.yaml`や`data_catalog_login`シークレットに登録したものです。

* Username
* Password
![image](https://github.com/gussan-me/streamlit-data-catalog/assets/75415556/1259c13d-8dfa-4438-91ac-375da6b9c251)

## データカタログ画面
サイドバーの以下の機能を使ってデータを検索します。
* テキストボックス
* ドロップボックス
![image](https://github.com/gussan-me/streamlit-data-catalog/assets/75415556/ca5e6e91-2254-47b5-aa20-e73c929b3377)



#### 参考
* Snowflake Authenticatorについて: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/README.md
