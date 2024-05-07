# mkc 
#### A command line utility to set up Kafka, MongoDB, and MongoDB Kafka Connector environments.

mkc is a python script to create small stacks that pertain to MongoDB and the kafka connector. It uses docker-compose (specifically [this compose file](https://github.com/confluentinc/cp-all-in-one/blob/7.5.0-post/cp-all-in-one/docker-compose.yml) maintained by confluent) to achieve this. You can configure which pieces of the stack you want to deploy, which connectors (if applicable), and which schemas to register (if applicable).

### Setup mkc

#### 1. Install/Start Docker.

For more information, please visit [docker's installation page](https://docs.docker.com/engine/install/)

#### 2. Install Docker compose

```
curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o docker-compose
sudo mv docker-compose /usr/local/bin && sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

Test with 

```
docker-compose -v
```

#### 3. Install python3
#### 4. Install packages:
````
pip install -r requirements.txt
````
#### 5. Script usage:
````
$ python3 mkc.py --help 
usage: mkc.py [-h] [--config CONFIG] [--connectors CONNECTORS]
              [--forceDownload] [--cleanOldFiles] [--logLevel LOGLEVEL]

Command line utility to set up Kafka, MongoDB, and MongoDB Kafka Connector
environments

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       A string representing the path to the config.json file
  --connectors CONNECTORS
                        A comma separated string of paths to the configs
                        describing the MongoDB connectors to install
  --forceDownload       Include this flag to force mkc to download the mongodb
                        kafka connector
  --logLevel LOGLEVEL   Log level. Possible values are [none, info, verbose]

````

## Example

### Create config:

```
echo '{
    "zookeeperVersion" : "6.2.0",
    "kafkaVersion" : "6.2.0",
    "schemaRegistryVersion" : "6.2.0",
    "kafkaConnectVersion" : "6.2.0",
    "mongodbVersion" : "5.0.20",
    "akhqVersion" : "0.24.0"
}' >> config/config.test.json
```

### Run mkc:

```
python3 mkc --config config/config.test.json \
   --logLevel debug \
   --connectors  "config/connectors/sample.sink.connector.errol.json,config/connectors/sample.source.connector.errol.json" \
   --schemas "config/schemas/topic1.value.avro.json"
```

Note that this may take longer than usual the first time you run mkc on a machine, as it must pull down all docker images locally. 

### Once the script has run, check the containers running:
```
$ docker ps 
CONTAINER ID   IMAGE                                      COMMAND                   CREATED         STATUS                   PORTS                                                                NAMES
1dddf9756695   confluentinc/cp-kafka-connect-base:6.2.0   "bash -c 'echo \"Inst…"   3 minutes ago   Up 3 minutes (healthy)   0.0.0.0:8083->8083/tcp, 0.0.0.0:9201->9201/tcp, 9092/tcp             kafkaConnectContainer-mkc
a3baf7ebf92f   confluentinc/cp-schema-registry:6.2.0      "/etc/confluent/dock…"    3 minutes ago   Up 3 minutes             0.0.0.0:8081->8081/tcp                                               schemaRegistryContainer-mkc
92dad29f2f08   confluentinc/cp-kafka:6.2.0                "/etc/confluent/dock…"    3 minutes ago   Up 3 minutes             0.0.0.0:9092->9092/tcp, 0.0.0.0:9101->9101/tcp                       kafkaBrokerContainer-mkc
d9627518aeb0   mongo:5.0.20                               "mongod --config /mo…"    3 minutes ago   Up 3 minutes             0.0.0.0:27017->27017/tcp                                             mongodContainer-mkc
c10e59470405   tchiotludo/akhq:0.24.0                     "docker-entrypoint.s…"    3 minutes ago   Up 3 minutes (healthy)   0.0.0.0:8082->8080/tcp                                               akhqContainer-mkc
fdc9f6e0eb5a   confluentinc/cp-zookeeper:6.2.0            "/etc/confluent/dock…"    3 minutes ago   Up 3 minutes             2888/tcp, 0.0.0.0:2181->2181/tcp, 0.0.0.0:9001->9001/tcp, 3888/tcp   zookeeperContainer-mkc
```

Here we have launched,
* Kafka (broker)
* Zookeeper for kafka broker
* The kafka schema registry server
* The kafka connect server 
* A container running akhq

On the connect server, we have several connectors running:

```
 $ curl -s -X GET -H "Content-Type:application/json" http://localhost:8083/connectors | jq . 
[
  "simple-sink",
  "mongo-source-connector"
]
```

One sink connector:
```
 $ curl -s -X GET -H "Content-Type:application/json" http://localhost:8083/connectors/simple-sink | jq . 
{
  "name": "simple-sink",
  "config": {
    "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
    "mongo.errors.log.enable": "true",
    "namespace.mapper.value.collection.field": "ns.coll",
    "tasks.max": "1",
    "topics": "test",
    "namespace.mapper": "com.mongodb.kafka.connect.sink.namespace.mapping.FieldPathNamespaceMapper",
    "mongo.errors.tolerance": "all",
    "database": "landmark",
    "namespace.mapper.error.if.invalid": "true",
    "connection.uri": "mongodb+srv://<username>:<pass>@cluster0.bfbxg.mongodb.net/myFirstDatabase",
    "name": "simple-sink",
    "config.action.reload": "restart",
    "errors.log.enable": "true"
  },
  "tasks": [
    {
      "connector": "simple-sink",
      "task": 0
    }
  ],
  "type": "sink"
}
```

One source connector:
```
$ curl -s -X GET -H "Content-Type:application/json" http://localhost:8083/connectors/mongo-source-connector | jq .  
{
  "name": "mongo-source-connector",
  "config": {
    "connector.class": "com.mongodb.kafka.connect.MongoSourceConnector",
    "tasks.max": "1",
    "batch.size": "0",
    "change.stream.full.document": "updateLookup",
    "collection": "source",
    "pipeline": "[]",
    "database": "kafka",
    "topic.prefix": "mongo",
    "topic.separator": "-",
    "poll.await.time.ms": "5000",
    "connection.uri": "mongodb+srv://<username>:<pass>@cluster0.bfbxg.mongodb.net/myFirstDatabase",
    "name": "mongo-source-connector",
    "change.stream.full.document.before.change": "whenAvailable",
    "collation": "",
    "topic.suffix": "topic",
    "poll.max.batch.size": "1000"
  },
  "tasks": [
    {
      "connector": "mongo-source-connector",
      "task": 0
    }
  ],
  "type": "source"
}
```

We also have a schema in our schema registry:

```
curl -X GET http://localhost:8081/subjects | jq . 
[
  "source-value"
]
```

We can see the configured value matches the schema file:

```
curl -X GET http://localhost:8081/subjects/source-value/versions/latest | jq . 
{
  "subject": "source-value",
  "version": 1,
  "id": 1,
  "schema": "{\"type\":\"record\",\"name\":\"Purchase\",\"namespace\":\"io.confluent.developer.avro\",\"fields\":[{\"name\":\"item\",\"type\":\"string\"},{\"name\":\"totalCost\",\"type\":\"double\"},{\"name\":\"customerID\",\"type\":\"string\"},{\"name\":\"itemOptions\",\"type\":{\"type\":\"map\",\"values\":\"double\"}}]}"
}
```


### 6. Write to Kafka and Check Mongo

In this example, we will write to the kafka topic sink and it will be produced to MongoDB:

sink topic --> MongoDB Sink Connector (simple-mongo-sink) --> kafkaconnector.sink collection

Run the following to insert data into the sink topic in our broker:

```
python3 test/testKafkaProducer --bootstrapServers "localhost:9092" --topic "sink" --loglevel debug
```

Check that the data was written to MongoDB via mongosh:

```
mongosh --quiet --eval 'db.getSiblingDB("kafkaconnector").getCollection("sink").findOne()'
{
  _id: '539d483a-8482-481a-96bb-60704430b5ca',
  array: [ { field1: Long("1") }, { field1: 'String1' } ],
  keyConverterType: 'jsonconverter',
  keyConverterEnableSchemas: false
}
```
<br>

#### 7. Write to Mongo and Check Kafka

In this example, we will write to the kafkaconnector.source namespace. 

kafkaconnector.source --> MongoDB source connector (simple-mongo-source) --> mongo-kafkaconnector-source-topic
kafkaconnector.source --> MongoDB source connector (simple-mongo-source-fulldoconly) --> mongo-kafkaconnector-topic-source-fulldoc-only

Once the stack is up. Run the following insert statement via the mongosh command:

```
mongosh --quiet --eval 'db.getSiblingDB("kafkaconnector").getCollection("source").insertOne({"testMessage" : 1})'\
{
  acknowledged: true,
  insertedId: ObjectId("6532db9367a1a8a0b943c8d9")
}
```

Run the following to read data from our kafka topic:

```
python3 test/testKafkaConsumer --bootstrapServers "localhost:9092" --topics "mongo-kafkaconnector-source-topic" --groupId consumerGroup1 --loglevel debug
```

You should see an INFO log message displaying the documented produced from the connector to the topic:

```
INFO: Found message {"_id": {"_data": "826532DB93000000022B022C0100296E5A10049099BCB8684E41D0827CF2FD0F8B88A046645F696400646532DB9367A1A8A0B943C8D90004"}, "operationType": "insert", "clusterTime": {"$timestamp": {"t": 1697831827, "i": 2}}, "fullDocument": {"_id": {"$oid": "6532db9367a1a8a0b943c8d9"}, "testMessage": 1}, "ns": {"db": "kafkaconnector", "coll": "source"}, "documentKey": {"_id": {"$oid": "6532db9367a1a8a0b943c8d9"}}}
```

After that, the consumer will block waiting for new messages. You can kill it with [CTRL] + C
<br>
<br>

#### 8. Examine Setup with AKHQ

AKHQ is a web-based application for monitoring various parts of the confluent platform. Our container is bound to port 8082. To access it, please visit localhost:8082. You will see a place like this:

![img.png](img.png)

Here we can see the various topics created in our Kafka broker and configuration/architecture metadata. If we click on the magnifying glass icon for one of the topics (say, mongo-kafkaconnect-source-topic, for example), we can see information about the topic and data therein:  

![img_1.png](img_1.png)

If we click on the gear icon for that topic, we can set configurations:

![img_2.png](img_2.png)

We can also see logs, ACLS, anc consumer groups for this topic. 

One the left-hand side, we can select "Consumer Groups" to see all the consumer groups for all topics:

![img_3.png](img_3.png)

You can read more about AKHQ and its capabilities [here](https://akhq.io/).


<br>

#### 9. Shutting Down Stack

To shut down the stack, simply run docker-compose down on the docker-compose file in the 
present working directory:

```
docker-compose -f docker-compose.XXXX.yml down 
```
<br>

### Configuration

mkc allows you to configure it in several ways

#### Specify container configurations via --config flag  

Here you can specify which containers to launch and what versions. The containers possible are:

* Kafka Broker (& Zookeeper)
* Kafka Connect 
* Schema Registry 
* AKHQ 
* MongoDB
<br><br>
Omission of any of these will result in that particular container not being deployed. This allows users to only launch some pieces of the stack. 
For example, here is one sample configuration:
 
```
{
  "zookeeperVersion" : "6.2.0",
  "kafkaVersion" : "6.2.0",
  "schemaRegistryVersion" : "6.2.0",
  "kafkaConnectVersion" : "6.2.0",
  "kafkaCatVersion" : "1.6.0",
  "mongodbVersion" : "5.0.20",
  "akhqVersion" : "0.24.0"
}
```

<br>

#### Specify connectors via the --connectors flag <br><br>

This is a comma-delimited list of paths to config files specifying the following:
* The connector configuration
* The connector download URL
* The number of instances of this connector
<br><br>
Here is a sample config file:

```{
 "name" : "mongodb-kafka-connector",
 "version" : "1.10.0",
 "config" : {
   "name" : "simple-mongo-sink",
   "config" : {
    "connector.class" : "com.mongodb.kafka.connect.MongoSinkConnector",
    "database" : "simple-kafka-sink",
    "tasks.max" : 1,
    "topics" : "purchases",
    "connection.uri" : "mongodb://mongodContainer-mkc:27017/test?replicaSet=testRS",
    "mongo.errors.log.enable" : "true",
    "mongo.errors.tolerance" : "all",
    "config.action.reload" : "restart",
     "errors.log.enable" : "true",
     "key.converter" : "org.apache.kafka.connect.json.JsonConverter",
     "value.converter" : "org.apache.kafka.connect.json.JsonConverter",
     "key.converter.schemas.enable" : false,
     "value.converter.schemas.enable" : false
  }
 },
 "num" : 1,
 "downloadURL" : "https://repo1.maven.org/maven2/org/mongodb/kafka/mongo-kafka-connect/{version}/mongo-kafka-connect-{version}-all.jar"
}
```
<br>

#### Specify schemas via the --schema flag

This is a comma separated string of paths to the configs describing the schemas to register

One sample schema is :

```
{
  "schema" : {
    "type" : "record",
    "namespace" : "io.confluent.developer.avro",
    "name" : "Purchase",
    "fields" : [
      { "name" :  "item", "type" :  "string" },
      { "name" :  "totalCost", "type" :  "double" },
      { "name" :  "customerID", "type" :  "string" },
      { "name" :  "itemOptions", "type" :  {
            "type" : "map",
            "values" : "double"
        }
      }
    ]
  },
  "subjectName": "source",
  "keyOrValue" : "value"
}
```

Note that this must include the following fields:
* A "subjectName" field that indicates the subject for the schema,
* A "schema" field that indicates the schema itself (currently, only Avro is supported by mkc) 
* A "keyOrValue" field that indicates whether the schema is for a value or key

Following the creation, we can send a GET request to the schema registry to see the schema:

```
curl -X GET http://localhost:8081/subjects/source-value/versions/latest | jq . 
{
  "subject": "source-value",
  "version": 1,
  "id": 1,
  "schema": "{\"type\":\"record\",\"name\":\"Purchase\",\"namespace\":\"io.confluent.developer.avro\",\"fields\":[{\"name\":\"item\",\"type\":\"string\"},{\"name\":\"totalCost\",\"type\":\"double\"},{\"name\":\"customerID\",\"type\":\"string\"},{\"name\":\"itemOptions\",\"type\":{\"type\":\"map\",\"values\":\"double\"}}]}"
}
```

<br>

### Known Issues

#### Stopping due to exception Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))

This issue can occur when docker-compose cannot authenticate to dockerd. To resolve this, run the following command

```
sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock
```


## Contributing 

Please make all changes in the development branch. We will use the [gitflow workflow](https://veerasundar.com/blog/gitflow-animated/) with git for SCM:
1. There's a master branch.
2. You create a develop branch off of master. This develop branch is your bread and butter as most of your changes go in here.
3. feature and release branches are created off of develop.
4. Once you are done with feature, you merge it to develop.
5. Once you are done with release, you merge it to both develop and master. And you tag the release.
6. If there's a issue in production, you create a hotfix branch off of master.
7. Once hotfix is done, you merge it back to master and develop and tag the release.


## TODO
* Switch to docker sdk, individually launching containers
* Ability to have multiple kafka connect workers to test fault tolerance
* Stack needs to automatically preclude zookeeper for newer versions of kafka
