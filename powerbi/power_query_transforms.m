// ============================================================================
// POWER QUERY M-CODE TRANSFORMATION SCRIPTS
// Project: Retail Inventory & Supply Chain Performance Analysis
// Connection Mode: CSV Folder Ingestion & Data Type Formatting
//
// IMPORTANT:
// This file contains the individual Power Query definitions used by the
// Power BI report. Each section represents a separate Power Query query.
//
// Before using these queries on another machine, update the DataPath below
// to point to the project's data/processed/ folder.
//
// Example:
//   DataPath =
//   "C:\Your\Path\retail-inventory-supply-chain-analysis\data\processed\"
// ============================================================================

// ============================================================================
// CONFIGURATION
// ============================================================================

// Update this path when using the Power BI report on another machine.
// The path must end with a backslash (\).

DataPath =
    "C:\Your\Path\retail-inventory-supply-chain-analysis\data\processed\";

    // ============================================================================
    // 1. QUERY: dim_product
    // Purpose: Load product catalog dimension table with price & cost data
    // types.
    // ============================================================================

    let Source = Csv.Document(File.Contents(DataPath & "dim_product.csv"),
                              [
                                Delimiter = ",", Columns = 8, Encoding = 65001,
                                QuoteStyle = QuoteStyle.None
                              ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"product_id", type text},
             {"product_name", type text},
             {"category", type text},
             {"subcategory", type text},
             {"brand", type text},
             {"supplier_id", type text},
             {"unit_cost", Currency.Type},
             {"selling_price", Currency.Type}}) in
#"Changed Type";

        // ============================================================================
        // 2. QUERY: dim_store
        // Purpose: Load retail store dimension table with geographic
        // hierarchies.
        // ============================================================================

        let Source = Csv.Document(File.Contents(DataPath & "dim_store.csv"),
                                  [
                                    Delimiter = ",", Columns = 7,
                                    Encoding = 65001,
                                    QuoteStyle = QuoteStyle.None
                                  ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"store_id", type text},
             {"store_name", type text},
             {"city", type text},
             {"state", type text},
             {"region", type text},
             {"store_type", type text},
             {"target_inventory_turnover", type number}}) in
#"Changed Type";

        // ============================================================================
        // 3. QUERY: dim_supplier
        // Purpose: Load vendor/supplier catalog table with SLA baseline
        // metrics.
        // ============================================================================

        let Source = Csv.Document(File.Contents(DataPath & "dim_supplier.csv"),
                                  [
                                    Delimiter = ",", Columns = 6,
                                    Encoding = 65001,
                                    QuoteStyle = QuoteStyle.None
                                  ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"supplier_id", type text},
             {"supplier_name", type text},
             {"supplier_region", type text},
             {"supplier_type", type text},
             {"base_lead_time", Int64.Type},
             {"base_fill_rate", type number}}) in
#"Changed Type";

        // ============================================================================
        // 4. QUERY: dim_date
        // Purpose: Load full calendar date dimension with year, quarter, month,
        // week.
        // ============================================================================

        let Source = Csv.Document(File.Contents(DataPath & "dim_date.csv"),
                                  [
                                    Delimiter = ",", Columns = 11,
                                    Encoding = 65001,
                                    QuoteStyle = QuoteStyle.None
                                  ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"date_id", Int64.Type},
             {"date", type date},
             {"day", Int64.Type},
             {"month", Int64.Type},
             {"month_name", type text},
             {"quarter", Int64.Type},
             {"year", Int64.Type},
             {"week", Int64.Type},
             {"weekday", Int64.Type},
             {"weekday_name", type text},
             {"is_weekend", Int64.Type}}) in
#"Changed Type";

        // ============================================================================
        // 5. QUERY: fact_sales
        // Purpose: Load core transaction fact table with sales revenue, COGS &
        // profit.
        // ============================================================================

        let Source = Csv.Document(File.Contents(DataPath & "fact_sales.csv"),
                                  [
                                    Delimiter = ",", Columns = 12,
                                    Encoding = 65001,
                                    QuoteStyle = QuoteStyle.None
                                  ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"sale_id", type text},
             {"date_id", Int64.Type},
             {"date", type date},
             {"product_id", type text},
             {"store_id", type text},
             {"customer_id", type text},
             {"quantity_sold", Int64.Type},
             {"unit_price", Currency.Type},
             {"discount", type number},
             {"sales_amount", Currency.Type},
             {"cost_amount", Currency.Type},
             {"gross_profit", Currency.Type}}) in
#"Changed Type";

        // ============================================================================
        // 6. QUERY: fact_inventory
        // Purpose: Load daily closing inventory snapshot fact table with
        // stockout flags.
        // ============================================================================

        let Source = Csv.Document(File.Contents(DataPath &
                                                "fact_inventory.csv"),
                                  [
                                    Delimiter = ",", Columns = 12,
                                    Encoding = 65001,
                                    QuoteStyle = QuoteStyle.None
                                  ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"inventory_date", type date},
             {"date_id", Int64.Type},
             {"product_id", type text},
             {"store_id", type text},
             {"opening_stock", Int64.Type},
             {"received_quantity", Int64.Type},
             {"quantity_sold", Int64.Type},
             {"closing_stock", Int64.Type},
             {"safety_stock", Int64.Type},
             {"reorder_point", Int64.Type},
             {"stockout_flag", Int64.Type},
             {"excess_inventory_flag", Int64.Type}}) in
#"Changed Type";

        // ============================================================================
        // 7. QUERY: fact_purchase
        // Purpose: Load vendor purchase order fact table with actual lead
        // times.
        // ============================================================================

        let Source = Csv.Document(File.Contents(DataPath & "fact_purchase.csv"),
                                  [
                                    Delimiter = ",", Columns = 12,
                                    Encoding = 65001,
                                    QuoteStyle = QuoteStyle.None
                                  ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"purchase_id", type text},
             {"date_id", Int64.Type},
             {"product_id", type text},
             {"store_id", type text},
             {"supplier_id", type text},
             {"order_date", type date},
             {"expected_delivery_date", type date},
             {"actual_delivery_date", type date},
             {"quantity_ordered", Int64.Type},
             {"quantity_received", Int64.Type},
             {"unit_cost", Currency.Type},
             {"lead_time_days", Int64.Type}}) in
#"Changed Type";

        // ============================================================================
        // 8. QUERY: product_operational_metrics
        // Purpose: Load pre-aggregated SKU operational metrics, ABC class & DIO
        // values.
        // ============================================================================

        let Source = Csv.Document(
            File.Contents(DataPath & "product_operational_metrics.csv"),
            [
              Delimiter = ",", Columns = 25, Encoding = 65001,
              QuoteStyle = QuoteStyle.None
            ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"product_id", type text},
             {"product_name", type text},
             {"category", type text},
             {"subcategory", type text},
             {"brand", type text},
             {"supplier_id", type text},
             {"unit_cost", Currency.Type},
             {"selling_price", Currency.Type},
             {"total_units_sold", Int64.Type},
             {"total_sales_amount", Currency.Type},
             {"total_cogs", Currency.Type},
             {"total_gross_profit", Currency.Type},
             {"avg_closing_stock", type number},
             {"avg_inventory_value", Currency.Type},
             {"gross_margin_pct", type number},
             {"avg_daily_demand", type number},
             {"inventory_turnover", type number},
             {"days_of_inventory", type number},
             {"stockout_rate_pct", type number},
             {"sell_through_rate_pct", type number},
             {"abc_class", type text},
             {"fast_moving_flag", Int64.Type},
             {"slow_moving_flag", Int64.Type},
             {"excess_inventory_flag", Int64.Type},
             {"stockout_prone_flag", Int64.Type}}) in
#"Changed Type";

        // ============================================================================
        // 9. QUERY: supplier_operational_metrics
        // Purpose: Load supplier scorecard performance metrics
        //          (Fill Rate %, SLA On-Time %).
        // ============================================================================

        let Source = Csv.Document(
            File.Contents(DataPath & "supplier_operational_metrics.csv"),
            [
              Delimiter = ",", Columns = 10, Encoding = 65001,
              QuoteStyle = QuoteStyle.None
            ]),

#"Promoted Headers" =
        Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

#"Changed Type" =
        Table.TransformColumnTypes(
#"Promoted Headers",
            {{"supplier_id", type text},
             {"supplier_name", type text},
             {"supplier_region", type text},
             {"supplier_type", type text},
             {"total_po_count", Int64.Type},
             {"total_ordered_units", Int64.Type},
             {"total_received_units", Int64.Type},
             {"avg_actual_lead_time", type number},
             {"on_time_delivery_rate_pct", type number},
             {"fill_rate_pct", type number}}) in
#"Changed Type";