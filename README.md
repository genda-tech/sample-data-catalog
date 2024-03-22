# sample-data-catalog
  # データカタログ
  ## 事前に必要な準備
  ローカル or AWS上のどちらでも動かせるように作成してあります。
  ## ローカルで動かす場合に必要な準備
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



  ## AWSで動かす場合に必要な準備
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

  ## ローカル・AWSで動かす場合に共通で必要な準備
  ### S3バケットの用意
  tfstateを配置するためのバケットが必要です。
  本サンプルコードはAmazon S3にtfstateを配置することを想定しています。
  なお、`terraform/tfroot/backend.tf`にて、tfstateの配置場所を指定します。
  ### GitHubのSecretsの設定
  以下の項目をGitHubのSecretsに設定してください。
  GitHub Actionsが使用するAWSやSnowflakeの認証情報を設定します。
  * AWS_REGION
  * AWS_IAM_ROLE_ARN
  * SNOWFLAKE_ACCOUNT
  * SNOWFLAKE_REGION
  * SNOWFLAKE_USER
  * SNOWFLAKE_PASSWORD

  ## 主な機能
  ### ログイン画面
  以下を入力してログインします。
  `config.yaml`や`data_catalog_login`シークレットに登録したものです。

  * Username
  * Password
  ![image](https://github.com/genda-tech/sample-data-catalog/assets/974175/e8d633ac-23b8-4a43-acfa-26b771fa4ef8)


  ### データカタログ画面
  サイドバーの以下の機能を使ってデータを検索します。
  * テキストボックス
  * ドロップボックス
  ![image](https://github.com/genda-tech/sample-data-catalog/assets/974175/8e1bc67a-5a40-4942-9e8c-8ca633e15af6)

  ### メタデータ自動更新機能
  データカタログに表示するメタデータの管理を自動化する機能です。
  メタデータを管理している該当のyamlを編集します。そして、GitHubのmainブランチへのマージをトリガーとしてGitHub Actionsが実行され、自動的にメタデータが更新されます。

  メタデータは以下のようなフォーマットで作成してください。
  ```employees.yaml
  name: "EMPLOYEES"
  comment: "従業員マスター"
  change_tracking: false
  columns:
    - name: "EMPLOYEE_ID"
      type: "NUMBER(38,0)"
      comment: "従業員のID。このテーブルの主キー。"
      nullable: false
    - name: "FIRST_NAME"
      type: "VARCHAR(50)"
      comment: "名前。"
      nullable: true
    - name: "LAST_NAME"
      type: "VARCHAR(50)"
      comment: "苗字。"
      nullable: true
    - name: "SALARY"
      type: "NUMBER(10,2)"
      comment: "給与。ドル単位で格納。"
      nullable: true
    - name: "HIRE_DATE"
      type: "DATE"
      comment: "雇用した日。日本時間にて格納。"
      nullable: true
  ```


  ### 参考

  * Snowflake Authenticatorについて: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/README.md