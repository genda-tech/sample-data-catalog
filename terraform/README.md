# データ定義フロー
# 事前に必要な準備
tfstateを置いておくバケットを用意しておく必要があります。
今回はAWSのS3にtfstateを置く想定としてコードを作成してあります。
`terraform/tfroot/backend.tf`にて、tfstateを置く場所を指定してあります。

# 機能
メタデータを管理しているyamlを編集して、GitHubのmainにマージするとGitHub Actionsがトリガーされて自動的にメタデータが更新されます。
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