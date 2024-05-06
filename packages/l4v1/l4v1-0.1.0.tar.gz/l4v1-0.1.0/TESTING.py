from l4v1.impact_analysis import impact_plot, impact_table
import polars as pl

df = pl.scan_parquet("data/supermarket_sales.parquet").with_columns(
    pl.col(pl.Categorical).cast(pl.Utf8)
)

sales_week5 = df.filter(pl.col("Datetime").dt.week() == 5)
sales_week6 = df.filter(pl.col("Datetime").dt.week() == 6)

impact_df = impact_table(
    df_primary=sales_week6,
    df_comparison=sales_week5,
    group_by_columns=["Product line"],
    volume_metric_name="Quantity",
    outcome_metric_name="Total",
)

impact_plot(
    impact_table=impact_df,
    format_data_labels="{:,.0f}€", # Optional
    primary_total_label="Revenue Week 2", # Optional
    comparison_total_label="Revenue Week 1", # Optional
    title="Impact Analysis Example", # Optional title
    color_total="lightgray", # Optional for total colors
    color_increase="#00AF00", # Optional for increase color
    color_decrease="#FF0000" # Optional for decrease color
)
