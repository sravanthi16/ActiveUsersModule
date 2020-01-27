[cloudera@quickstart code]$ cat activeusers1.py
from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import explode
from pyspark.sql.functions import unix_timestamp, from_unixtime
import pyspark.sql.functions as f
import ConfigParser as cp
import sys

def main():

    props = cp.RawConfigParser()
    props.read("/home/cloudera/Documents/csvfiles/code/activeusers.properties")
    env=sys.argv[1]
    conf=SparkConf()\
        .setMaster(props.get(env, 'execution.mode')) \
        .setAppName("pyspark job to get no of active users per day")

    sc = SparkContext\
        .getOrCreate(conf=conf)

    sqlcontext=SQLContext(sc)

    log4jLogger = sc._jvm.org.apache.log4j
    LOGGER = log4jLogger.LogManager.getLogger(__name__)
    LOGGER.info("pyspark script logger initialized")
    LOGGER.info("starting spark context")

    input = sqlcontext\
        .read\
        .json(props.get(env,'file.name'))

    df = input\
        .withColumn("event_params",explode('event_params'))\
        .withColumn("user_properties",explode('user_properties'))

    filtereddata = df\
        .filter\
        ("event_name = 'user_engagement' and event_params.key='engagement_time_msec' and event_params.value.int_value >= 3000 and user_properties.key='user_id'")

    finaldata = filtereddata\
        .select\
        ("event_date","user_properties.value.string_value")\
        .dropDuplicates()

    output = finaldata \
        .groupby \
        (from_unixtime
         (unix_timestamp
          ('event_date', 'yyyyMMdd'))
         .alias('date')) \
        .agg(f.count("string_value")
             .alias('active_user_count'))

    output\
        .write\
        .jdbc(props.get(env,'jdbc.url'), table= props.get(env,'table.name') , mode= props.get(env,'write.mode'))

    sc.stop()

if __name__ == '__main__':
    main()