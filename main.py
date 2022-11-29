# Import PySpark
import pyspark
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder.master("local[1]") \
                    .appName('SparkByExamples.com') \
                    .getOrCreate()

print('PySpark Version :'+spark.version)
print('PySpark Version :'+spark.sparkContext.version)

#============================================================================

# Configuratins related to Cassandra connector & Cluster
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.datastax.spark:spark-cassandra-connector_2.12:3.2.0  pyspark-shell'

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, SparkSession

spark = SparkSession.builder \
  .appName('SparkCassandraApp') \
  .config('spark.cassandra.connection.host', 'cassandra') \
  .config('spark.cassandra.auth.username', 'cassandra') \
  .config('spark.cassandra.auth.password', 'cassandra') \
  .config('spark.cassandra.connection.port', '9042') \
  .config('spark.cassandra.output.consistency.level','ONE') \
  .master('local[2]') \
  .getOrCreate()

x  = spark.sql("""CREATE TEMPORARY VIEW myTable
     USING org.apache.spark.sql.cassandra
     OPTIONS (
     table "cyclist_name",
     keyspace "cycling",
     pushdown "true")""")  

xx = spark.sql("select * from myTable where age > 30")     
xx.show()
xx.explain()

yy = spark.sql("select * from casscatalog.cycling.cyclist_name where id = 'e7ae5cf3-d358-4d99-b900-85902fda9bb0'")
yy.show()
yy.explain()

#============================================================================

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.datastax.spark:spark-cassandra-connector_2.12:3.2.0  pyspark-shell'

from pyspark.sql import SparkSession
#https://github.com/datastax/spark-cassandra-connector/blob/master/doc/14_data_frames.md


spark = SparkSession\
    .builder\
    .appName("SQL example")\
    .master("local[*]")\
    .config("spark.cassandra.connection.host", "cassandra")\
    .config("spark.cassandra.auth.username", "cassandra")\
    .config("spark.cassandra.auth.password", "cassandra")\
    .config("spark.sql.catalog.casscatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")\
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions")\
    .getOrCreate()    

#spark.sparkContext.setLogLevel('TRACE')

x = spark.sql("SELECT * FROM casscatalog.cycling.cyclist_name where age > 30 and age < 50")
x.show()
x.explain()

xx = spark.sql("select * from casscatalog.cycling.cyclist_name where id = 'e7ae5cf3-d358-4d99-b900-85902fda9bb0'")
xx.show()
xx.explain()

#============================================================================
w = spark.read\
  .format("org.apache.spark.sql.cassandra")\
  .option("keyspace", "cycling")\
  .option("table", "cyclist_name")\
  .load()


#============================================================================
spark.sql("CREATE DATABASE IF NOT EXISTS casscatalog.ksname  WITH DBPROPERTIES (class='SimpleStrategy', replication_factor='5')")
spark.sql("CREATE TABLE IF NOT EXISTS casscatalog.ksname.salesfact (key Int, sale_date TIMESTAMP, product STRING, value DOUBLE) USING cassandra PARTITIONED BY (key, product)")
 

a = spark.sql("SELECT * FROM casscatalog.ksname.salesfact where product = 'a' and key= 1 ")
a.show()
a.explain()


# https://blog.softwaremill.com/7-mistakes-when-using-apache-cassandra-51d2cf6df519

# https://github.com/datastax/spark-cassandra-connector

#Filters rows on the server side via the CQL WHERE clause
#Allows for execution of arbitrary CQL statements

#https://github.com/datastax/spark-cassandra-connector/blob/master/doc/3_selection.md

'''
  Adds a CQL `WHERE` predicate(s) to the query.
    * Useful for leveraging secondary indexes in Cassandra.
    * Implicitly adds an `ALLOW FILTERING` clause to the WHERE clause, 
    * however beware that some predicates might be rejected by Cassandra, 
    * particularly in cases when they filter on an unindexed, non-clustering column. 
'''    


#============================================================================

xx = spark.sql("select * from casscatalog.ksname.table_name where cck ='a' ")
xx.show()
xx.explain()