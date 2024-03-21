# データ定義フロー
  # 事前に必要な準備
tfstateを配置するためのバケットが必要です。
本サンプルコードはAmazon S3にtfstateを配置することを想定しています。
なお、`terraform/tfroot/backend.tf`にて、tfstateの配置場所を指定します。

  # 機能
メタデータを管理している該当のyamlを編集します。そして、GitHubのmainブランチへのマージをトリガーとしてGitHub Actionsが実行され、自動的にメタデータが更新されます。
  ## メタデータ
```employees.yaml
name: "EMPLOYEES"
comment: "従業員マスター"
change_tracking: false
columns:
  - name: "EMPLOYEE_ID"
    type: "NUMBER(38,0)"
    comment: "従業員ID"
    nullable: false
  - name: "FIRST_NAME"
    type: "VARCHAR(50)"
    comment: "名"
    nullable: true
  - name: "LAST_NAME"
    type: "VARCHAR(50)"
    comment: "姓"
    nullable: true
  - name: "SALARY"
    type: "NUMBER(10,2)"
    comment: "給与"
    nullable: true
  - name: "HIRE_DATE"
    type: "DATE"
    comment: "入社日"
    nullable: true
```
  # GitHubのSecretsに設定する項目
  以下の項目をGitHubのSecretsに設定してください。
  * AWS_REGION
  * AWS_IAM_ROLE_ARN
  * SNOWFLAKE_ACCOUNT
  * SNOWFLAKE_REGION
  * SNOWFLAKE_USER
  * SNOWFLAKE_PASSWORD