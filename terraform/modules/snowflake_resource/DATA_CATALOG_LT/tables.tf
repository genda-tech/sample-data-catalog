locals {
  table_files = fileset("${path.module}/tables", "*.yaml")
  tables      = { for file in local.table_files : replace(file, ".yaml", "") => yamldecode(file("${path.module}/tables/${file}")) }
}

resource "snowflake_table" "tables" {
  for_each = local.tables

  database = "DEV_YAMAGUCHI_DBT"
  schema   = "DATA_CATALOG_LT"
  name     = each.value.name
  comment  = each.value.comment

  dynamic "column" {
    for_each = each.value.columns
    content {
      name     = column.value.name
      type     = column.value.type
      comment  = column.value.comment
      nullable = column.value.nullable
    }
  }
}