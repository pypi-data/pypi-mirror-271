from l4v1.price_volume_mix import PVM
import polars as pl

sales_week_1 = pl.read_parquet("data/supermarket_sales.parquet").filter(
    pl.col("Datetime").dt.week() == 1
)
sales_week_2 = pl.read_parquet("data/supermarket_sales.parquet").filter(
    pl.col("Datetime").dt.week() == 2
)


pvm = PVM(
    df_primary=sales_week_2,
    df_comparison=sales_week_1,
    group_by_columns=["Product line", "Customer type", "Gender"],
    volume_column_name="Quantity",
    outcome_column_name="Total",
)

pvm.waterfall_plot(
    primary_total_label="Week 2 Sales",
    comparison_total_label="Week 1 Sales",
    format_data_labels="{:,.0f}€",
    title="Sales Week 2 vs 1",
    color_total = "#F1F1F1",
)




# pvm.get_table()


# pvm.write_xlsx_table("/mnt/c/Users/mirol/Downloads/testing.xlsx")

pvm.get_table().schema