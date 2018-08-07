create database if not exists mydb;
drop table if exists mydb.oozie_test_orders purge;
create table mydb.oozie_test_orders (order_date string, total_orders int, total_amount float) partitioned by (order_status string) stored as avro location '/user/skamalj/oozie_test/result_hive_avro';
