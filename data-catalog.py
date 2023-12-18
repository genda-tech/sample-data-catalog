import streamlit as st
import streamlit_authenticator as stauth
import snowflake.connector
import pandas as pd
from snowflake.snowpark import Session
import boto3
import ast
import json
import yaml
from yaml.loader import SafeLoader
import os

st.set_page_config( 
    page_title="データカタログ",
    layout="wide",
    )


# AWS Secrets Managerからシークレットを取得する場合に使用
@st.cache_data(experimental_allow_widgets=True)
def get_secret(secret_name):
    client = boto3.client(
        service_name='secretsmanager',
        region_name='ap-northeast-1'
    )
    get_secret_value = client.get_secret_value(
        SecretId=secret_name
    )
    return get_secret_value


# クエリを実行するために使用
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


# ローカルの場合はconfig.yamlから、AWS Secrets Managerから取得する場合はsecrets managerからシークレットを取得
@st.cache_data(experimental_allow_widgets=True)
def get_config():
    if os.path.exists('./config.yaml'):
        with open('./config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
            snowflake_connection_params = {
                "account": st.secrets["snowflake"]["account"],
                "user": st.secrets["snowflake"]["user"],
                "password": st.secrets["snowflake"]["password"],
                "warehouse": st.secrets["snowflake"]["warehouse"],
                "role": st.secrets["snowflake"]["role"]
            }
        return {"snowflake_connection_params": snowflake_connection_params, "config": config}
    else:
        get_secret_value = get_secret('snowflake_data_catalog')
        secret = ast.literal_eval(get_secret_value['SecretString'])
        snowflake_connection_params = {
            "account": secret['ACCOUNT'],
            "user": secret['USER'],
            "password": secret['PASSWORD'],
            "warehouse": secret['WAREHOUSE'],
            "role": secret['ROLE']
        }
        config = None
        return {"snowflake_connection_params": snowflake_connection_params, "config": config}


# 認証。ローカルの場合はconfig.yamlから、AWS環境の場合はsecrets managerから認証情報取得
def get_authenticator():
    if local_config:
        authenticator = stauth.Authenticate(
            local_config['credentials'],
            local_config['cookie']['name'],
            local_config['cookie']['key'],
            local_config['cookie']['expiry_days'],
        )
        return authenticator
    else:
        get_secret_value = get_secret('data_catalog_login')
        secret = ast.literal_eval(get_secret_value['SecretString'])
        secret = secret['CREDENTIAL']
        secret = json.loads(secret)

        authenticator = stauth.Authenticate(
            secret['credentials'],
            secret['cookie']['name'],
            secret['cookie']['key'],
            secret['cookie']['expiry_days'],
        )
        return authenticator


def init_connection(connection_params):
    return snowflake.connector.connect(
        **connection_params,
        client_session_keep_alive=True
    )


configs = get_config()
snowflake_connection_params = configs["snowflake_connection_params"]
local_config = configs["config"]
conn = init_connection(snowflake_connection_params)
session = Session.builder.configs(snowflake_connection_params).create()

authenticator = get_authenticator()

with st.sidebar:
    name, authentication_status, user_name = authenticator.login("Login", "main")

if authentication_status:

    with st.sidebar:
        # スキーマ内のテーブル一覧から概要を検索できるようにするため文字列変数に入れておけるようにしておく
        st.markdown('# テーブル概要検索')
        table_details_search = st.text_input('テーブル一覧の概要を検索')

        st.markdown('# テーブル選択')

        # データベースの一覧をリスト型で取得してselectboxで一つ選択
        show_databases = run_query("SHOW DATABASES;")
        database_rows = [row[1] for row in show_databases]
        # SNOWFLAKEとSNOWFLAKE_SAMPLE_DATAは選択肢から除外
        strings_to_remove = ["SNOWFLAKE", "SNOWFLAKE_SAMPLE_DATA"]
        for string_to_remove in strings_to_remove:
            if string_to_remove in database_rows:
                database_rows.remove(string_to_remove)
        select_database = st.selectbox('データベースを選択してください', database_rows)

        # スキーマの一覧をリスト型で取得してselectboxで一つ選択
        show_schemas = run_query(f"SHOW SCHEMAS IN DATABASE {select_database};")
        schema_rows = [row[1] for row in show_schemas]
        # INFORMATION_SCHEMAは選択肢から除外
        string_to_remove = "INFORMATION_SCHEMA"
        if string_to_remove in schema_rows:
            schema_rows.remove(string_to_remove)
        select_schema = st.selectbox('スキーマを選択してください', schema_rows)

        # テーブルとビューの一覧をリスト型で取得してselectboxで一つ選択
        # SHOW TABLESだけだとviewの情報を抽出することができないので、SHOW TABLESとSHOW VIEWSを別々に実行
        show_tables = run_query(f"SHOW TABLES IN {select_database}.{select_schema}")
        show_views = run_query(f"SHOW VIEWS IN {select_database}.{select_schema}")
        table_rows = [row[1] for row in show_tables]
        view_rows = [row[1] for row in show_views]
        table_view_rows = table_rows + view_rows
        select_table = st.selectbox('テーブルを選択してください', table_view_rows)

    # ページのタイトル
    st.markdown(f"# {select_database}.{select_schema}")
    show_schemas = run_query(f"SHOW SCHEMAS IN DATABASE {select_database};")
    # selectboxで選択したスキーマの概要を表示
    show_schemas = [row for row in show_schemas if row[1] == select_schema]
    show_schemas = show_schemas[0][6]
    st.write(show_schemas)

    # 指定したスキーマのテーブルの一覧
    st.markdown(f'## テーブル一覧')
    show_tables_df = pd.DataFrame(show_tables)
    show_views_df = pd.DataFrame(show_views)
    tables_df = show_tables_df.rename(columns={1: 'column_name', 5: 'comment'})
    views_df = show_views_df.rename(columns={1: 'column_name', 6: 'comment'})
    tables_views_df = pd.concat([tables_df, views_df])
    tables_views_df = tables_views_df.loc[:, ['column_name', 'comment']]
    # サイドバーにてinputboxに文字列を入れた場合、その文字列が入っているデータをデータフレームから抽出できるように実装
    if table_details_search is None:
        st.dataframe(
            tables_views_df,
            column_config={
                "column_name": st.column_config.TextColumn("テーブル名"),
                "comment": st.column_config.TextColumn("概要", width="large")
            },
            hide_index=True,
        )
    else:
        tables_views_df = tables_views_df[tables_views_df['comment'].str.contains(table_details_search, case=False)]
        st.dataframe(
            tables_views_df,
            column_config={
                "column_name": st.column_config.TextColumn("テーブル名"),
                "comment": st.column_config.TextColumn("概要", width="large")
            },
            hide_index=True,
        )

    # テーブルのカラムの詳細を表示
    st.markdown(f"## {select_table}テーブルのカラム情報")
    columns_details = run_query(f"DESC TABLE {select_database}.{select_schema}.{select_table}")
    column_detail_df = pd.DataFrame(columns_details)
    column_detail_df = column_detail_df.rename(columns={0: 'column_name', 1: 'data_type', 9: 'comment'})
    column_detail_df = column_detail_df.loc[:, ['column_name', 'data_type', 'comment']]
    st.dataframe(
        column_detail_df,
        column_config={
            "column_name": st.column_config.TextColumn("カラム名"),
            "data_type": st.column_config.TextColumn("データタイプ", width="medium"),
            "comment": st.column_config.TextColumn("概要", width="large")
        },
        hide_index=True,
    )

    # テーブルのプレビューを表示
    st.markdown(f'## プレビュー：{select_table}')
    query = f"SELECT * FROM {select_database}.{select_schema}.{select_table} limit 50"
    preview = session.sql(query)
    st.dataframe(preview, hide_index=True)
 
    # ログアウト
    with st.sidebar:
        if authentication_status:
            authenticator.logout('Logout', 'main', key='unique_key')
        elif authentication_status is False:
            st.error('Username/password is incorrect')
        elif authentication_status is None:
            st.error("Username/password is incorrect")


elif authentication_status is None:
    st.title("データカタログ")
    with st.sidebar:
        st.warning("Please enter your username and password")

elif authentication_status is False:
    st.title("データカタログ")
    with st.sidebar:
        st.warning("Username/password is incorrect")
