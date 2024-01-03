# sample-data-catalog

# 事前に必要な準備
ローカル or AWS上のどちらでも動かせるように作成してあります。
## ローカルの場合
`config.yaml`と`secrets.toml`を作成して、以下のようなディレクトリ構成にします。
```
sample-data-catalog/
  ├ .streamlit/config.toml streamlitの背景の色などを設定
  ├ data-catalog.py データカタログのコード 
  ├ requirements.txt 必要なライブラリをインストールするのに使うrequirement.txt
 　　├ secrets.toml snowflakeの接続情報を記載する。
  └ config.yaml ログイン機能用の設定を記載する。
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
![image](https://github.com/genda-tech/sample-data-catalog/assets/974175/e8d633ac-23b8-4a43-acfa-26b771fa4ef8)


## データカタログ画面
サイドバーの以下の機能を使ってデータを検索します。
* テキストボックス
* ドロップボックス
![image](https://github.com/genda-tech/sample-data-catalog/assets/974175/8e1bc67a-5a40-4942-9e8c-8ca633e15af6)




#### 参考
* Snowflake Authenticatorについて: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/README.md
