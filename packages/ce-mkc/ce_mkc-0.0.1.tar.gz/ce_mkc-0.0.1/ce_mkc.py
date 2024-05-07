import argparse
import glob
import json
import logging
import os
import shutil
import subprocess
import time
from pymongo import MongoClient
from zipfile import ZipFile

import docker
import requests

########################################################################################################################
# Constants
########################################################################################################################

DEFAULT_CONFIG_DATA = {
        "zookeeperVersion" : "6.2.0",
        "kafkaVersion" : "6.2.0",
        "schemaRegistryVersion" : "6.2.0",
        "kafkaConnectVersion" : "6.2.0",
        "kafkaCatVersion" : "1.6.0",
        "mongodbVersion" : "5.2.0",
        "zookeeperVersion" : "6.2.0",
        "akhqVersion" : "0.24.0"
    }

KAFKA_CAT_CONTAINER_NAME = "kafkaCatContainer-mkc"
KAFKA_CONNECT_CONTAINER_NAME = "kafkaConnectContainer-mkc"
SCHEMA_REGISTRY_CONTAINER_NAME = "schemaRegistryContainer-mkc"
KAFKA_BROKER_CONTAINER_NAME = "kafkaBrokerContainer-mkc"
ZOOKEEPER_CONTAINER_NAME = "zookeeperContainer-mkc"
MONGODB_SERVER_CONTAINER_NAME = "mongodContainer-mkc"
AKHQ_SERVER_CONTAINER_NAME = "akhqContainer-mkc"

CONTAINERS = [
    KAFKA_CONNECT_CONTAINER_NAME,
    SCHEMA_REGISTRY_CONTAINER_NAME,
    KAFKA_BROKER_CONTAINER_NAME,
    ZOOKEEPER_CONTAINER_NAME
]

CONTAINER_TEMPLATE_PATH_AKHQ = "templates/akhq/akhq.template"
CONTAINER_TEMPLATE_PATH_KAFKA = "templates/kafka/kafka.template"
CONTAINER_TEMPLATE_PATH_ZOOKEEPER = "templates/kafka/zookeeper.template"
CONTAINER_TEMPLATE_PATH_MONGOD = "templates/mongod/mongod.template"
CONTAINER_TEMPLATE_PATH_KAFKA_CONNECT = "templates/kafkaconnect/kafkaconnect.template"
CONTAINER_TEMPLATE_PATH_SCHEMA_REGISTRY = "templates/schemaregistry/schemaregistry.template"


CONNECTOR_DOWNLOADS_PATH = "connector-downloads"
MDB_KAFKA_CONNECTOR_VERSIONS = [
    "0.1",
    "0.2",
    "1.0.0",
    "1.1.0",
    "1.2.0",
    "1.3.0",
    "1.4.0",
    "1.5.0",
    "1.5.1",
    "1.6.0",
    "1.6.1",
    "1.7.0",
    "1.8.0",
    "1.8.1",
    "1.9.0",
    "1.9.1",
    "1.10.0",
    "1.10.1",
    "1.11.0",
]

CONFLUENT_DATAGEN_CONNECTORS_VERSIONS = [
    "0.1.0",
    "0.1.1",
    "0.1.2",
    "0.1.3",
    "0.1.4",
    "0.1.5",
    "0.1.6",
    "0.1.7",
    "0.2.0",
    "0.3.0",
    "0.3.1",
    "0.3.2",
    "0.3.3",
    "0.4.0",
    "0.4.1",
    "0.5.0",
    "0.5.1",
    "0.5.3",
    "0.5.4",
    "0.6.0",
    "0.6.1",
    "0.6.2"
]

CONNECTOR_META_DATA = {
    "mongodb-kafka-connector" :  {
        "downloadURL" : "https://repo1.maven.org/maven2/org/mongodb/kafka/mongo-kafka-connect/{version}/mongo-kafka-connect-{version}-all.jar",
        "versions" : MDB_KAFKA_CONNECTOR_VERSIONS
    },
    "confluent-datagen-connector" : {
        "downloadURL" : "https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-datagen/versions/{version}/confluentinc-kafka-connect-datagen-{version}.zip",
        "versions" : CONFLUENT_DATAGEN_CONNECTORS_VERSIONS
    }
}


DOCKER_COMPOSE_TEMPLATE_PATH = "templates/docker-compose.template"
MONGODB_CONF_TEMPLATE_PATH = "templates/mongod/mongod.conf.template"

MONGODB_CONN_STR = "localhost:27017"
KAFKA_CONNECT_CONFIG_URL = "http://localhost:8083"
SCHEMA_REGISTRY_CONFIG_URL = "http://localhost:8081"

########################################################################################################################
# Helper Methods
########################################################################################################################

def createMongoDBConfFromTemplate(config):
    """
    Create MongoDB Conf From Template

    :return:
    """
    with open(MONGODB_CONF_TEMPLATE_PATH, 'r') as f:
        templateData = f.read()

    mongodbConfFile = templateData.format()
    logging.debug("Created docker-compose file data {}".format(mongodbConfFile))

    return mongodbConfFile

def downloadConnectorJar(connectorName, downloadUrl, connectorVersion="latest", forceDownload=False):
    """
    Download Connector JAR

    :param connectorName:
    :param connectorVersion:
    :param url:
    :param forceDownload:
    :return:
    """
    # Check if version exists when possible
    if connectorName in CONNECTOR_META_DATA:
        versions = CONNECTOR_META_DATA[connectorName]["versions"]
        if "latest" == connectorVersion:
            connectorVersion = CONFLUENT_DATAGEN_CONNECTORS_VERSIONS[len(MDB_KAFKA_CONNECTOR_VERSIONS) - 1]
        else:
            if connectorVersion not in versions:
                errorMessage = f"Version {connectorVersion} is not an acceptable version of the {connectorName} Connector"
                logging.error(errorMessage)
                raise Exception(errorMessage)

    url = downloadUrl.format(version=connectorVersion)
    urlParts = url.split("/")
    fileName = urlParts[len(urlParts)-1]
    localFileName = f"{CONNECTOR_DOWNLOADS_PATH}/{fileName}"

    # If the jar is already downloaded locally, do not redownload it, unless we are forcing the redownload
    if not forceDownload and os.path.exists(localFileName) and os.path.isfile(localFileName):
        logging.info(f"File already {fileName} exists!")
        return localFileName, fileName

    if not os.path.exists(CONNECTOR_DOWNLOADS_PATH):
        os.mkdir(CONNECTOR_DOWNLOADS_PATH)

    logging.info("Downloading {} to {}".format(fileName, localFileName))
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(localFileName, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return localFileName, fileName

def createDockerComposeFileFromTemplate(config):
    """
    Create Docker Compose Template

    :return:
    """
    dockerComposeBase = "---\nversion: '2'\nservices:\n"
    if "kafkaVersion" in config:
        zookeeperContainerConfig = readTemplate(CONTAINER_TEMPLATE_PATH_ZOOKEEPER)
        zookeeperContainerConfig = zookeeperContainerConfig.format(zookeeper_version=config["zookeeperVersion"], zookeeper_container_name=ZOOKEEPER_CONTAINER_NAME)
        dockerComposeBase += "\n{}\n".format(zookeeperContainerConfig)
        kafkaContainerConfig = readTemplate(CONTAINER_TEMPLATE_PATH_KAFKA)
        kafkaContainerConfig = kafkaContainerConfig.format(kafka_version=config["kafkaVersion"], kafka_broker_container_name=KAFKA_BROKER_CONTAINER_NAME)
        dockerComposeBase += "\n{}\n".format(kafkaContainerConfig)

    if "schemaRegistryVersion" in config:
        schemaRegistryContainerConfig = readTemplate(CONTAINER_TEMPLATE_PATH_SCHEMA_REGISTRY)
        schemaRegistryContainerConfig = schemaRegistryContainerConfig.format(schema_registry_version=config["schemaRegistryVersion"], schema_registry_container_name=SCHEMA_REGISTRY_CONTAINER_NAME)
        dockerComposeBase += "\n{}\n".format(schemaRegistryContainerConfig)

    if "kafkaConnectVersion" in config:
        kafkaConnectContainerConfig = readTemplate(CONTAINER_TEMPLATE_PATH_KAFKA_CONNECT)
        kafkaConnectContainerConfig = kafkaConnectContainerConfig.format(kafka_connect_version=config["kafkaConnectVersion"], kafka_connect_container_name=KAFKA_CONNECT_CONTAINER_NAME)
        dockerComposeBase += "\n{}\n".format(kafkaConnectContainerConfig)

    if "mongodbVersion" in config:
        mongodContainerConfig = readTemplate(CONTAINER_TEMPLATE_PATH_MONGOD)
        mongodContainerConfig = mongodContainerConfig.format(mongodb_version=config["mongodbVersion"], mongodb_container_name=MONGODB_SERVER_CONTAINER_NAME)
        dockerComposeBase += "\n{}\n".format(mongodContainerConfig)

    if "akhqVersion" in config:
        akhqContainerConfig = readTemplate(CONTAINER_TEMPLATE_PATH_AKHQ)
        akhqContainerConfig = akhqContainerConfig.format(akhq_version=config["akhqVersion"], akhq_container_name=AKHQ_SERVER_CONTAINER_NAME)
        dockerComposeBase += "\n{}\n".format(akhqContainerConfig)

    logging.debug("Created docker-compose file data {}".format(dockerComposeBase))

    currentPID = os.getpid()
    dockerFile = f"docker-compose.{currentPID}.yml"
    with open(dockerFile, "w") as f:
        f.write(dockerComposeBase)
    return dockerFile

def readTemplate(templatePath):
    """
    Read Template
    :param templatePath:
    :return:
    """
    with open(templatePath, 'r') as f:
        templateData = f.read()
    return templateData


def parseConfigFile(configFile, launchFullStack=False):
    """
    Parse Config File

    :return:
    """
    if configFile is None:
        return DEFAULT_CONFIG_DATA
    if not os.path.exists(configFile):
        raise Exception(f"Config file {configFile} does not exist!")

    configFileData = { }
    with open(configFile, 'r') as f:
        configFileData = f.read()
        configFileData = json.loads(configFileData)

    # Override any default with the config.json values from the file
    if launchFullStack:
        fullConfigData = { **DEFAULT_CONFIG_DATA, **configFileData }
    else:
        fullConfigData = configFileData
    return fullConfigData


def installStackViaDocker(dockerFilePath):
    """
    Install Kafka Stack Via Docker

    :return:
    """
    logging.info(f"Running docker-compose to setup stack using file {dockerFilePath}")
    dockerComposeUp = subprocess.run(["docker-compose", "-f", dockerFilePath, "up", "-d"])
    logging.debug(f"Got return code {dockerComposeUp.returncode}")
    return dockerComposeUp.returncode

def shudownStackViaDocker(dockerFilePath):
    """
    Shut Down Kafka Stack via Docker

    :param dockerFilePath:
    :return:
    """
    logging.info(f"Running docker-compose to shut down stack using file {dockerFilePath}")
    dockerComposeDown = subprocess.run(["docker-compose", "-f", dockerFilePath, "down"])
    logging.debug(f"Got return code {dockerComposeDown.returncode}")
    return dockerComposeDown.returncode

def mountMongoDBConfigFile(fileData):
    """
    Mount MongoDB Config File

    :return:
    """
    logging.info("Putting mongod.conf in container volume...")
    mongoDBContainerDir = "data/mongodContainer-mkc/mongodata"
    dataSubDirectory = f"{mongoDBContainerDir}/data"
    if not os.path.exists(dataSubDirectory):
        os.makedirs(dataSubDirectory)

    mongodbFilePathFull = f"{mongoDBContainerDir}/mongod.conf"
    with open(mongodbFilePathFull,'w') as f:
        f.write(fileData)

def mountConnectorJar(connectorName, connectorJarPath, fileName):
    """
    Mount Connector Jar

    :param connectorName:
    :param connectorJarPath:
    :param fileName:
    :return:
    """
    logging.info(f"Mounting jar for connector {connectorName}...")
    if not os.path.exists(connectorJarPath):
        errMessage = f"Cannot find jar at {connectorJarPath}"
        logging.error(errMessage)
        raise Exception(errMessage)

    downloadsDir = f"data/connect-mkc/connect-jars/{connectorName}"
    if not os.path.exists(downloadsDir):
        os.makedirs(downloadsDir)

    if "*" == fileName:
        containerMappedVolumePath = f"{downloadsDir}"
        logging.debug(f"Copying {connectorJarPath} to {containerMappedVolumePath}...")
        files = os.listdir(connectorJarPath)
        logging.debug("Found the following under {}: {}".format(connectorJarPath, files))
        if os.path.exists(containerMappedVolumePath):
            shutil.rmtree(containerMappedVolumePath)
        shutil.copytree(connectorJarPath, containerMappedVolumePath)
    else:
        containerMappedVolumePath = f"{downloadsDir}/{fileName}"
        logging.debug(f"Copying {connectorJarPath} to {containerMappedVolumePath}...")
        shutil.copyfile(connectorJarPath, containerMappedVolumePath)

def mountMongoDBKafkaConnectorUberJar(mongoDBKafkaConnectorUberJarPath, fileName):
    """
    Mount MongoDB Kafka Connector Uber Jar onto Container

    Mounts the MongoDB Kafka Connector uber jar onto the kafka connect container

    :param mongoDBKafkaConnectorUberJarPath:
    :return:
    """
    logging.info("Mounting kafka uber jar...")
    if not os.path.exists(mongoDBKafkaConnectorUberJarPath):
        errMessage = f"Cannot find uber jar at {mongoDBKafkaConnectorUberJarPath}"
        logging.error(errMessage)
        raise Exception(errMessage)

    downloadsDir = "data/connect-mkc/connect-jars/mongodb/"
    if not os.path.exists(downloadsDir):
        os.makedirs(downloadsDir)

    containerMappedVolumePath = f"{downloadsDir}{fileName}"
    logging.debug(f"Copying {mongoDBKafkaConnectorUberJarPath} to {containerMappedVolumePath}...")
    shutil.copyfile(mongoDBKafkaConnectorUberJarPath, containerMappedVolumePath)


def installConnectors(connectors, kafkaConnectAPIUrl):
    """
    Install Connectors

    :param connectors:
    :return:
    """
    logging.info("Installing connectors")
    for connector in connectors:
        connectorName = connector["name"]
        connectorConfig = connector["config"]
        connectorInstanceName = connectorConfig["name"]
        logging.debug("Installing connector with name {} and instance name {} ".format(
            connectorName,
            connectorInstanceName
        ))

        numConnectorInstances = 1
        if "num" in connectorConfig:
            numConnectorInstances = int(connectorConfig["num"])
        for i in range(0, numConnectorInstances):
            connectorInstanceNameNumbered = "{}-{}".format(connectorInstanceName, i)
            connectorConfig["name"] = connectorInstanceName if numConnectorInstances == 1 else connectorInstanceNameNumbered
            connectorEndpoint = f"{kafkaConnectAPIUrl}/connectors"
            headers = {
                'Content-Type': 'application/json'
            }
            result = requests.post(url=connectorEndpoint, json=connectorConfig, headers=headers)
            logging.debug("Got status code {} result {}".format(result.status_code, json.dumps(result.json())))

    logging.info("Done installing connectors")
    connectorsResp = requests.get(url=connectorEndpoint, headers=headers)
    logging.debug("Found connector: {}".format(json.dumps(connectorsResp.json())))


def registerSchemas(schemas, kafkaSchemaRegistryAPIUrl):
    """
    Install Connectors

    :param connectors:
    :return:
    """
    headers = {
        'Content-Type': 'application/vnd.schemaregistry.v1+json'
    }
    logging.info("Registering schemas")
    for schema in schemas:
        logging.debug("Registering schema from file {} ".format(schema))
        schemaPath = schema

        with open(schemaPath) as f:
            schemaData = json.load(f)
        logging.debug("Fetched schema {}".format(json.dumps(schemaData)))

        schema = { "schema" : json.dumps(schemaData["schema"]) }
        schemaStr = json.dumps(schema)
        subjectName = schemaData["subjectName"]
        keyOrValue = schemaData["keyOrValue"]

        logging.debug(f"Registering schema for subject {subjectName}-{keyOrValue}")
        schemaSubjectsEndpoint = f"{kafkaSchemaRegistryAPIUrl}/subjects/{subjectName}-{keyOrValue}/versions"
        result = requests.post(url=schemaSubjectsEndpoint,
                               data=schemaStr,
                               headers=headers)

        logging.debug("Got status code {} result {}".format(result.status_code, json.dumps(result.json())))
    logging.info("Done registering schemas")

    schemaSubjectsEndpoint = f"{kafkaSchemaRegistryAPIUrl}/subjects"
    connectorsResp = requests.get(url=schemaSubjectsEndpoint, headers=headers)
    logging.debug("Found schema subjects: {}".format(json.dumps(connectorsResp.json())))

def deployStack(config):
    """
    Deploy Stack

    :return:
    """
    dockerFile = createDockerComposeFileFromTemplate(config)
    respCode = installStackViaDocker(dockerFile)
    if respCode != 0:
        errMessage = f"Docker-compose up did not complete successfully. Got return code {respCode}"
        logging.error(errMessage)
        raise Exception(errMessage)

def waitUntilContainersUp():
    """
    Wait Until Containers Up

    :return:
    """
    allRunning = False
    dockerClient = docker.from_env() # <-- TODO: https://github.com/docker/docker-py/issues/3059
    # workaround:
    # sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock
    while not allRunning:
        logging.info("Waiting until all containers are running...")
        allRunning = True
        for container in CONTAINERS:
            logging.debug(f"Looking for container with name {container}")
            containerObj = dockerClient.containers.get(container)
            containerRunning = (containerObj.status == "running")
            allRunning = allRunning and containerRunning
        time.sleep(5)
    logging.info("All containers have started!")

    # Check if kafka connect is up
    kafkaConnectRunning = False
    while not kafkaConnectRunning:
        logging.info("Checking whether kafka connect is running")
        try:
            resp = requests.get("http://localhost:8083/")
            resp = resp.json()
            kafkaConnectRunning = "kafka_cluster_id" in resp
        except Exception as e:
            errMessage = "Encountered exception {} while checking whether kafka connect is up".format(e)
            logging.error(errMessage)
            kafkaConnectRunning = False
        time.sleep(5)

    logging.info("Kafka connect is reachable...")


def cleanUpArtifacts():
    """
    Clean Up Artifacts

    :return:
    """
    # If we do not remove the data directory, it can corrupt the mongod container that subsequently uses it
    try:
        for f in glob.glob("docker-compose*"):
            os.remove(f)
        shutil.rmtree("data")
    except Exception as ie:
        logging.error(f"Found exception {ie} while attempting to clean up")

def extractJarsFromZipFile(zipFilePath):
    """
    Extract Jars from Zip File

    :param zipFilePath:
    :return:
    """
    # Unzip
    with ZipFile(zipFilePath) as zObject:
        zipFileNameParts = zipFilePath.split(".")
        unzippedPath = ".".join(zipFileNameParts[0:len(zipFileNameParts)-1])
        zObject.extractall(path="connector-downloads")

    # Look for a subdirectory named lib
    newJarPath = f"{unzippedPath}/lib"
    if not os.path.exists(newJarPath):
        return None, None
    else:
        return newJarPath, "*"


def createAndDeployStack(args):
    """
    Create and Deploy Stack

    :param args:
    :return:
    """
    try:
        cleanUpArtifacts()

        # Parse config.json
        config = None if args.config is None else args.config
        config = parseConfigFile(config, bool(args.launchFullStack))

        # Extract connector configuration
        connectors = []
        if args.connectors is not None:
            connectorStrParts = args.connectors.split(",")
            for connectorConfigFilePath in connectorStrParts:
                logging.debug(f"Loading connector config at path {connectorConfigFilePath}")
                with open(connectorConfigFilePath) as f:
                    connectorConfig = json.load(f)
                    connectors.append(connectorConfig)

        # Download connectors and move jars into container directory
        for connector in connectors:
            logging.debug("Fetching jar for connector with name {}".format(connector["name"]))
            if "path" in connector:
                logging.debug("Using connector jar {} for connector {}".format(connector["path"], connector["name"]))
                connectorPathParts = connector["path"].split("\\")
                connectorJarPath = connectorPathParts[0:len(connectorPathParts)-1]
                fileName = connectorPathParts[len(connectorPathParts)-1]
            else:
                logging.debug("Downloading connector jar for connector {}".format(connector["name"]))
                connectorJarPath, fileName = downloadConnectorJar(
                    connector["name"],
                    connector["downloadURL"],
                    connector["version"],
                    bool(args.forceDownload)
                )
            if fileName.endswith(".zip"):
                connectorJarPath, fileName = extractJarsFromZipFile(connectorJarPath)
            mountConnectorJar(connector["name"], connectorJarPath, fileName)

        # Put mongod.config.json file in data directory
        mongodbConfig = createMongoDBConfFromTemplate(config)
        mountMongoDBConfigFile(mongodbConfig)

        # Setting up stack
        deployStack(config)
        waitUntilContainersUp()

        # Start replica set
        mongoClient = MongoClient(MONGODB_CONN_STR, directConnection=True)
        mongoClient.admin.command("replSetInitiate")

        # Create schemas
        if args.schemas is not None:
            schemas = args.schemas.split(",")
            registerSchemas(schemas, SCHEMA_REGISTRY_CONFIG_URL)

        # Creating connectors
        installConnectors(connectors, KAFKA_CONNECT_CONFIG_URL)

    except Exception as e:
        logging.error("Stopping due to exception {}".format(e))

########################################################################################################################
# Base Methods
########################################################################################################################

def setupArgs():
    """
    Setup args
    Parses all command line arguments to the script
    """
    parser = argparse.ArgumentParser(description='Command line utility to set up Kafka, MongoDB, and MongoDB Kafka Connector environments')

    parser.add_argument('--config',
                        required=False,
                        action="store",
                        dest='config',
                        default="config/config.json",
                        help='A string representing the path to the config.json file')

    # Connector spec json:
    # {
    #     "name" : <Connector name>
    #     "downloadUrl" : <tokenized url (with version) from which to download jar},
    #     "verion" : <version of jar desired},
    #     "path" : <path to jar file, if not using url>,
    #     "num" : <number of instances to deploy>,
    #     "config" : <connector instance configuration>
    # }
    parser.add_argument('--connectors',
                        required=False,
                        action="store",
                        dest='connectors',
                        default=None,
                        help='A comma separated string of paths to the configs describing the MongoDB connectors to install')

    parser.add_argument('--schemas',
                        required=False,
                        action="store",
                        dest='schemas',
                        default=None,
                        help='A comma separated string of paths to the configs describing the schemas to register')

    parser.add_argument('--forceDownload',
                        required=False,
                        action="store_true",
                        dest='forceDownload',
                        default=False,
                        help='Include this flag to force mkc to download the mongodb kafka connector')

    parser.add_argument('--launchFullStack',
                        required=False,
                        action="store_true",
                        dest='launchFullStack',
                        default=False,
                        help='Include this flag to launch the full stack (kafka/zookeeper, kafka connect, schema registry, akhq, mongod)')

    parser.add_argument('--logLevel',
                        required=False,
                        action="store",
                        dest='logLevel',
                        default='info',
                        help='Log level. Possible values are [none, info, verbose]')

    return parser.parse_args()

def _configureLogger(logLevel):
    format = '%(message)s'
    if logLevel != 'INFO':
        format = '%(levelname)s: %(message)s'
    logging.basicConfig(format=format, level=logLevel.upper())

def main():
    args = setupArgs()
    _configureLogger(args.logLevel.upper())
    createAndDeployStack(args)

if __name__ == "__main__":
    main()


# TODO
# Get schema registry to work
# Get the data gen connector to work
