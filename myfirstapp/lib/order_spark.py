from pyspark import SparkContext
from pyspark.sql import HiveContext
from pyspark.sql.functions import *
sc = SparkContext()
sqlContext = HiveContext(sc)
orders = sqlContext.read.format("com.databricks.spark.avro").load("/user/skamalj/oozie_test/orders");
order_items = sqlContext.read.format("com.databricks.spark.avro").load("/user/skamalj/oozie_test/order-items");
orders_new = orders.select("order_id",from_unixtime((orders.order_date/1000),'YYYY-MM-dd').alias('order_date'),"order_status");
grouped = orders_new.join(order_items, order_items.order_item_id == orders_new.order_id).groupBy("order_date","order_status");
aggregated =  grouped.agg(count("order_item_subtotal").alias('total_orders'),sum("order_item_subtotal").alias('total_amount'))
ordered = aggregated.orderBy(desc("order_date"),"order_status", desc("total_amount")).persist()
sqlContext.setConf("spark.sql.parquet.compression.codec","gzip")
ordered.write.parquet('/user/skamalj/oozie_test/resultdf_parquet_gzip/')
sqlContext.setConf("spark.sql.parquet.compression.codec","snappy")
ordered.write.parquet('/user/skamalj/oozie_test/resultdf_parquet_snappy/')
ordered.map(lambda row: row[0]+','+row[1]+','+str(row[2])+','+str(row[3])).saveAsTextFile('/user/skamalj/oozie_test/resultdf_text/')
