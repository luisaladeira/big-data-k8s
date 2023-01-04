CKC_VERSION="0.11.0"
STRIMZI_IMG="strimzi/kafka:latest-kafka-3.1.0"
REGISTRY_URL="registrybigdatadev.azurecr.io"
REGISTRY_USR="registrybigdatadev"

az aks update -n aks-llkafka-bigdata -g rg-llkafka --attach-acr REGISTRY_USR

TMP="/tmp/my-connect"
BASEURL="https://repo1.maven.org/maven2/org/apache/camel/kafkaconnector"
PLUGINS=(
    "$BASEURL/camel-azure-storage-datalake-kafka-connector/$CKC_VERSION/camel-file-kafka-connector-$CKC_VERSION-package.tar.gz"
)

# download connect plugins
rm -rf $TMP && mkdir -p $TMP/plugins
for url in "${PLUGINS[@]}"; do
    curl -sL $url -o $TMP/plugins/file.tar.gz && tar -xf $TMP/plugins/file.tar.gz -C $TMP/plugins
    rm -f $TMP/plugins/file.tar.gz
done

# build and push the custom image
echo -e "FROM $STRIMZI_IMG\nCOPY ./plugins/ /opt/kafka/plugins/\nUSER 1001" > $TMP/Dockerfile
sudo podman build --layers=false -t $REGISTRY_USR/llkafka-kafka-connect-strimzi:3.1.0 -f $TMP/Dockerfile
sudo podman login -u $REGISTRY_USR $REGISTRY_URL
sudo podman push localhost/$REGISTRY_USR/llkafka-kafka-connect-strimzi:3.1.0 $REGISTRY_URL/$REGISTRY_USR/llkafka-kafka-connect-strimzi:3.1.0