# Base image from Confluent Kafka Connect
FROM confluentinc/cp-kafka-connect:latest

# Set environment variables
ENV CONNECT_PLUGIN_PATH="/usr/share/java,/etc/kafka-connect/jars"

# Define the build argument for the Snowflake connector version (default to 1.9.0)
ARG SNOWFLAKE_CONNECTOR_VERSION=1.9.0
ARG SNOWFLAKE_JDBC_VERSION=3.13.14
ARG SNOWFLAKE_INGEST_VERSION=0.10.1

# Create the directory for Snowflake connector
RUN mkdir -p /usr/share/java/snowflake

# Download the Snowflake Kafka Connector
ADD https://repo1.maven.org/maven2/com/snowflake/snowflake-kafka-connector/${SNOWFLAKE_CONNECTOR_VERSION}/snowflake-kafka-connector-${SNOWFLAKE_CONNECTOR_VERSION}.jar /usr/share/java/snowflake/
ADD https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/${SNOWFLAKE_JDBC_VERSION}/snowflake-jdbc-${SNOWFLAKE_JDBC_VERSION}.jar /usr/share/java/snowflake/
ADD https://repo1.maven.org/maven2/com/snowflake/snowflake-ingest-sdk/${SNOWFLAKE_INGEST_VERSION}/snowflake-ingest-sdk-${SNOWFLAKE_INGEST_VERSION}.jar /usr/share/java/snowflake/

# Expose Kafka Connect REST port
EXPOSE 8083

# Start Kafka Connect with Snowflake connector
CMD ["/etc/confluent/docker/run"]