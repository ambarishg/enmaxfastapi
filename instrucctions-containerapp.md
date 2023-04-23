# Install the Azure Container Apps extension to the CLI.         
az extension add \
  --source https://workerappscliextension.blob.core.windows.net/azure-cli-extension/containerapp-0.2.0-py2.py3-none-any.whl      
  
# Install the Azure Container Apps extension for the CLI.
az extension add --name containerapp --upgrade

# Now that the extension is installed, register the Microsoft.App namespace.
az provider register --namespace Microsoft.App

# Register the Microsoft.OperationalInsights provider for the Azure Monitor Log Analytics Workspace if you have not used it before.
az provider register --namespace Microsoft.OperationalInsights       

RESOURCE_GROUP="enmax"         
LOCATION="eastus"                 
CONTAINERAPPS_ENVIRONMENT="enmax-env"  


# Create a Resource Group           
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create an Environment
az containerapp env create --name $CONTAINERAPPS_ENVIRONMENT --resource-group $RESOURCE_GROUP --location $LOCATION

# Create a Azure Container Registry   ( Run in Console )   
az acr create --resource-group enmax --name enmaxacr --sku Basic 

# Login into the Azure Container Registry ( Run in Console)     
az acr login -n enmaxacr   

# Tag image ( Run in Console)      

docker tag enmaxfastapi:latest enmaxacr.azurecr.io/enmaxfastapi:v1   

# Push image ( Run in Console)    
docker push enmaxacr.azurecr.io/enmaxfastapi:v1

# Update the  Azure Container Registry ( Run in Console) 
az acr update -n enmaxacr --admin-enabled true       

# Get the password of the Azure CLI ( Run in Azure CLI )   
password=$(az acr credential show --name enmaxacr --query passwords[0].value --output tsv)

# Create the Container App           
az containerapp create \
--name enmaxfastapiapp \
--resource-group $RESOURCE_GROUP \
--environment $CONTAINERAPPS_ENVIRONMENT \
--image enmaxacr.azurecr.io/enmaxfastapi:v1  \
--registry-server enmaxacr.azurecr.io \
--registry-username enmaxacr \
--registry-password $password  \
--target-port 8000 \
--ingress 'external' \
--cpu 2.0 --memory 4.0Gi \
--query configuration.ingress.fqdn 