A = load '$table' using  org.apache.hive.hcatalog.pig.HCatLoader();
store A into '/user/skamalj/learn-oozie/coord_output/$table' USING parquet.pig.ParquetStorer;
