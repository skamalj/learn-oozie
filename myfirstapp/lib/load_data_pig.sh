data = load '$job_root_dir/spark/resultdf_parquet_gzip' using parquet.pig.ParquetLoader AS (order_date: chararray, order_status: chararray, total_orders: int, order_amount: float);
data_correct = foreach data generate order_date,order_status, total_orders, order_amount as total_amount;
store data_correct into 'mydb.oozie_test_orders' using org.apache.hive.hcatalog.pig.HCatStorer();
