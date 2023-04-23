az aks create \
    --resource-group enmax \
    --name enmaxCluster \
    --node-count 1 \
    --generate-ssh-keys \
    --attach-acr enmaxacr

# Get AKS cluster credentials
az aks get-credentials --resource-group enmax --name enmaxCluster


kubectl apply -f enmax.yaml