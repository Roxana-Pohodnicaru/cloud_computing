import requests
import json

subscriptionId = "x"
bearer = "x"

defaultUrl = f"https://management.azure.com/subscriptions/{subscriptionId}/"

resourceGroupName = "lab5"
virtualNetworkName= "net4"
subnetName= "snet4"
ipName = "ip4"
vmName = "vm4"
apiVersion = "2021-04-01"

def sendHttpRequest(url, json_data, headers):
    # Sending the POST request with the JSON payload
    response = requests.put(url, data=json_data, headers=headers)

    
# Checking the answer
    if response.status_code == 200:
        print("Successful request")
        response_data = response.json()
        print("Response data:", response_data)
    else:
        print(f"Error in request. Statuscode: {response.status_code}")

def createResourceGroup():
    global json_data, headers
    # create Resourcegroup
    urlCreateResourceGroup = f"{defaultUrl}resourcegroups/{resourceGroupName}?api-version={apiVersion}"
    # JSON data you want to send
    createResourceGroupPayloadData = {
        "location": "westeurope"
    }
    
    # Converting the Python data to JSON
    json_data = json.dumps(createResourceGroupPayloadData)
    # Set the HTTP headers to set the content type to JSON
    headers = {"Authorization": f"Bearer {bearer}",
               'Content-Type': 'application/json'}
    sendHttpRequest(urlCreateResourceGroup, json_data, headers)

def createVirtualNetwork():
    global json_data
    # create virtual network
    urlCreateVirtualNetwork = f"{defaultUrl}resourcegroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}?api-version={apiVersion}"
    payloadDataCreateVirtualNetwork = {
        "properties": {
            "addressSpace": {
                "addressPrefixes": [
                    "10.0.0.0/16"
                ]
            },
            "flowTimeoutInMinutes": 10
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVirtualNetwork)
    sendHttpRequest(urlCreateVirtualNetwork, json_data, headers)

def createSubnet():
    global json_data
    # create subnet
    urlCreateSubnet = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}?api-version=2023-05-01"
    payloadDataCreateSubnet = {
        "properties": {
            "addressPrefix": "10.0.0.0/16"
        }
    }
    json_data = json.dumps(payloadDataCreateSubnet)
    sendHttpRequest(urlCreateSubnet, json_data, headers)

def createPublicIpAdress():
    global json_data
    # create public ip adress
    urlCreatePublicIPAdress = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/publicIPAddresses/{ipName}?api-version=2023-05-01"
    payloadDataCreatePublicIpAdress = {
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreatePublicIpAdress)
    sendHttpRequest(urlCreatePublicIPAdress, json_data, headers)

def createNetworkInterface():
    global networkInterfaceName, json_data
    # create network interface
    networkInterfaceName = "nic4"
    urlCreateNetworkInterface = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}?api-version=2023-05-01"
    payloadDataCreateNetworkInterface = {
        "properties": {
            "ipConfigurations": [
                {
                    "name": "ipconfig1",
                    "properties": {
                        "publicIPAddress": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/publicIPAddresses/{ipName}"
                        },
                        "subnet": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}"
                        }
                    }
                }
            ]
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateNetworkInterface)
    sendHttpRequest(urlCreateNetworkInterface, json_data, headers)

def createVm():
    global json_data
    # create VM
    urlCreateVM = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}?api-version=2023-07-01"
    payloadDataCreateVM = {
        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Compute/virtualMachines/{vmName}",
        "type": "Microsoft.Compute/virtualMachines",
        "properties": {
            "osProfile": {
                "adminUsername": "roxyp",
                "secrets": [

                ],
                "computerName": f"{vmName}",
                "linuxConfiguration": {
                    "ssh": {
                        "publicKeys": [
                            {
                                "path": "/home/roxyp/.ssh/authorized_keys",
                                "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCso3PnZHgEKlbPgU1bRr6n2cMwm/q4G7eFxcUVGpUd2+s66U5b0UM2QkscC71HvM9RNxYGA581omWBN8wpU+pxW8Nmjvre1gJzW/zPJsp0z1YuB7RhblC5z9zC2WEFiPER1f2ZZhT3ob8XZt/PY/BlZ/o0aG6nF7TsfbeUQzwjs3pEBiHiCXl5yL1KsCbSYuGwN6f+dtl9Eqx3/uRDt8Ss5qv7qfUCNWgmM75nSSRAIUjOns4juYvlZaoJtBV72cF5CZawf3w/O5KPl02Md9KurGCOSDxn5a8jSmNEJ3Vat4+/ovqDS4Stya9savBklNNNdRdLJhH6ZdusHC6RUe+q//CM9S0dxwwChJ1aKR++pUhRemJ5jFTe66lIEAGrMtm9y+Gz0tOO8VCto6hPCBRTq2zW4aOZ7bgDc6jFTkRDuSZtLm1iCYhJ6DifrWCw62WWC7sNTQm7hwH/OnYVdezHcVzwAqTbImpuDu8YH8PFLKaX2O2mhfNBmLBGyLSA5UE= roxyp@LAPTOP-Roxi"
                            }
                        ]
                    },
                    "disablePasswordAuthentication": True
                }
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}",
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            },
            "storageProfile": {
                "imageReference": {
                    "sku": "16.04-LTS",
                    "publisher": "Canonical",
                    "version": "latest",
                    "offer": "UbuntuServer"
                },
                "dataDisks": [

                ]
            },
            "hardwareProfile": {
                "vmSize": "Standard_D1_v2"
            },
            "provisioningState": "Creating"
        },
        "name": f"{vmName}",
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVM)
    sendHttpRequest(urlCreateVM, json_data, headers)

createResourceGroup()
createVirtualNetwork()
createSubnet()
createPublicIpAdress()
createNetworkInterface()
createVm()

