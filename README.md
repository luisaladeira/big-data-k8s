# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# create namespaces
kubectl create namespace ingestion-realtime
kubectl create namespace ingestion-batch
kubectl create namespace monitoring
kubectl create namespace cicd

# add & update helm list repos
helm repo add argo https://argoproj.github.io/argo-helm
helm repo add strimzi https://strimzi.io/charts/
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add airbyte https://airbytehq.github.io/helm-charts
helm repo update

# install argo-cd
https://artifacthub.io/packages/helm/argo/argo-cd
https://github.com/argoproj/argo-helm
helm install argocd argo/argo-cd --namespace cicd --version 3.26.8

# create a load balancer to argocd
kubectl patch svc argocd-server -n cicd -p '{"spec": {"type": "LoadBalancer"}}'

# retrieve load balancer ip
kubectl get services -l app.kubernetes.io/name=argocd-server,app.kubernetes.io/instance=argocd -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}" -n cicd

# get password to log into argocd portal
ARGOCD_LB=<ip-adress>
kubectl get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" -n cicd | base64 -d | xargs -t -I {} argocd login $ARGOCD_LB --username admin --password {} --insecure

# create cluster role binding for admin user [sa]
kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=system:serviceaccount:cicd:argocd-application-controller -n cicd

# register cluster
CLUSTER=""
argocd cluster add $CLUSTER --in-cluster

# add repo into argo-cd repositories
REPOSITORY=""
argocd repo add $REPOSITORY --username <username> --password <password> --port-forward

# install strimzi
helm install kafka strimzi/strimzi-kafka-operator --namespace ingestion --version 0.26.0

# apply config maps kafka to metrics
kubectl apply -f repository/yamls/ingestion/metrics/kafka-metrics-config.yaml
kubectl apply -f repository/yamls/ingestion/metrics/zookeeper-metrics-config.yaml
kubectl apply -f repository/yamls/ingestion/metrics/connect-metrics-config.yaml
kubectl apply -f repository/yamls/ingestion/metrics/cruise-control-metrics-config.yaml

# ingestion
kubectl apply -f repository/app-manifests/ingestion/kafka-broker.yaml
kubectl apply -f repository/app-manifests/ingestion/schema-registry.yaml
kubectl apply -f repository/app-manifests/ingestion/kafka-connect.yaml
kubectl apply -f repository/app-manifests/ingestion/cruise-control.yaml
kubectl apply -f repository/app-manifests/ingestion/kafka-connectors.yaml

# ingestion batch
kubectl apply -f repository/app-manifests/ingestion/airbyte.yaml


# monitoring
kubectl apply -f repository/app-manifests/monitoring/prometheus-alertmanager-grafana-botkube.yaml

# create svc loadBalances to external access 
kubectl apply -f repository/svc-lbs/svc-lb-grafana.yaml

# get user and password to access grafana
kubectl get secrets prometheus-alertmanager-grafana -o jsonpath="{.data.admin-user}" -n monitoring | base64 -d; echo
kubectl get secrets prometheus-alertmanager-grafana -o jsonpath="{.data.admin-password}" -n monitoring | base64 -d; echo


kubectl get secret llkafka-cluster-ca-cert -o jsonpath='{.data.ca\.crt}' | base64 -d > /home/luisa/kafka-project-1/apps/consumer-datalake/

kubectl get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" -n cicd | base64 -d; echo

kubectl get secrets app-bandplay -o jsonpath="{.data.password}" -n ingestion | base64 -d; echo
kubectl get secrets consumer-datalake -o jsonpath="{.data.password}" -n ingestion | base64 -d; echo


