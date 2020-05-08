from pyspark.sql import SparkSession, functions, types
import os
import configparser
import logging


topic_schema = types.StructType([
    types.StructField('time', types.DateType()),
    types.StructField('rank', types.IntegerType()),
    types.StructField('title', types.StringType()),
    types.StructField('count', types.IntegerType()),
])


def title_process(batch_df, batch_id):
    pass


def main():
    topic_df = spark.readStream.format('file').option('path', 'file://' + data_dir).schema(topic_schema).load()


if __name__ == '__main__':
    config_file = "../config.ini"

    conf = configparser.ConfigParser()
    conf.read(config_file)

    log_dir = conf.get("title_process", "log_dir")
    data_dir = conf.get("web_scraping", "data_dir")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(level=logging.WARNING,
                        filename=os.path.join(log_dir, 'monitor.log'),
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        )
    logging.info("weibo_data_process launching")

    spark = SparkSession.builder.appName("weibo_topic_title").getOrCreate()
    assert spark.version >= '2.4'
    spark.sparkContext.setLogLevel('WARN')

    main()


