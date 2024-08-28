## Requirements to run VMware Playbooks ##
* Python (≥ 2.6)
* Ansible (≥ 2.7)
* PyVmomi
* botocore
* boto3

#####################################################################
# Deploy VM from Template with Ansible : deploy-kubernetes-prod.yml #
#####################################################################

## ToDo ##
* <deployment_id>.vmconf.yml to be redefined & refactored in future (currently parallelism not in use)
  - use the add_host to get the parallelism into the playbook
* Find alternative solution to task [sleep for 60 seconds to allow VMs to power up fully]
* Maybe rename playbook & role??
* Add functionality to handle different pods & flavours
* Use specific datastore depending on cluster
* Anti-Affinity Rules
* datastore modification -> VMs to "POD-B_CCD_Cluster1_VV51" change from autoselectdatastore

## Description ##

Playbook and role to deploy & delete multiple vSphere virtual machines detailed in a config file from MinIO.

## Playbook & Role Structure: ##
```
├── ansible.cfg
├── deploy-kubernetes-prod.yml
├── roles
│   └── deploy-vsphere-template
│       ├── tasks
│       │   └── main.yml
│       └── vars
│           └── main.yml
├── vars
│   └── group_vars
│       └── minio.yml
```

## Required: '<deployment_id>.vmconfig.yml' ##
* Configuration file '<deployment_id>.vmconfig.yml' to be created and uploaded into MinIO Object store.
  │
  └─ http://object.athtem.eei.ericsson.se/minio/de-cni/ccd/<deployment_id>/<deployment_id>.vmconfig.yml

## <deployment_id>.vmconfig.yml Format ##
* vm_user: <string>
* vm_pass: <string>
    - Above Credentials used to login to the VMs & Restart the Network service (hopefully only a temporary solution)
* vms_to_deploy: List[] of Dict Objects{}
    - each List item is a Dict object containing all the required parameters for a single Node/VM

```
#~# Login used to restart Network on the VMs #~#
vm_user: XXXX
vm_pass: XXXX

vms_to_deploy:
  #~# Node 1 #~#
  - hostname: XXXX
    guest_memory: XXXX
    guest_vcpu: X
    guest_disk_size_gb: XX
    network_config:
      - name: <vlan_name>
        ip: XX.XX.XX.XX
        netmask: XX.XX.XX.XX
        gateway: XX.XX.XX.XX
        start_connected: true
        connected: true
        state: 'present'
        label: 'Network adapter 1'
  #~# Node 2 #~#
  - hostname: XXXX
    guest_memory: XXXX
    guest_vcpu: X
    guest_disk_size_gb: XX
    network_config:
      - name: <vlan_name>
        ip: XX.XX.XX.XX
        netmask: XX.XX.XX.XX
        gateway: XX.XX.XX.XX
        start_connected: true
        connected: true
        state: 'present'
        label: 'Network adapter 1'
  #~# Node n #~#
  ####
  ###
```

## Required: 'roles/deploy-vsphere-template/vars/main.yml' verification ##
* Vars file 'deploy-vsphere-template/vars/main.yml' Contains the vCenter / vSphere environment file to be fetched from MinIO & the cluster the VMs will be spun up to.
Ensure details are correct or Modify variable values if neccessary.
 - deploy_vsphere_env: 'XXXX-vcenter_env.yml' # Used to decide on the vcenter_env.yml to fetch from MinIO
 - deploy_vsphere_cluster: 'XXXX' # Cluster on which the VMs will be deployed

## Required: 'XXXX-vcenter_env.yml' file Present on MinIO & Matching var <deploy_vsphere_env> ##
* Configuration file 'XXXX-vcenter_env.yml' to be verified as present and uploaded into MinIO Object store.
  │
  └─ http://object.athtem.eei.ericsson.se/minio/templates/cloud/XXXX-vcenter_env.yml

* Configuration file name must also match value given to var <deploy_vsphere_env> in 'deploy-vsphere-template/vars/main.yml'

## XXXX-vcenter_env.yml Format ##
```
# Infrastructure
# - Defines the vCenter / vSphere environment
deploy_vsphere_host: 'xxxx'
deploy_vsphere_user: 'xxxx'
deploy_vsphere_password: 'xxxx'
deploy_vsphere_datacenter: 'xxxx'
deploy_vsphere_folder: 'xxxx'

```

## EXECUTION ##
Unless a tag is specified in the command line, playbook will not run.
* To Deploy VMs [--tags deploy] | To Delete VMs [--tags delete]

Paramateres required.
* deployment_id
* vm_template

* cluster [Optional]
  - Defaults to POD-B-CCD-Cluster1 if not passed in

```
ansible-playbook deploy-kubernetes-prod.yml -e deployment_id=<deployment_id> -e vm_template=<template_name> [-e cluster=XXXXX] --tags [deploy|delete]

```
-------------------------------------------------------------------------------------------------------------------------------------------------------------


########################################################################
# Generate CCD Deploy config for VMware : ccd-vmware-deploy-config.yml #
########################################################################

## ToDo ##
* Do I upload Jinja templates to MinIO or leave in Repo?
  - probably MinIO
* Add functionality to handle different pods & flavours
* Create multiple params J2 template files as we could pull down the correct template based on pod / cluster

## Description ##

Playbook to Generate Inventory file & parameters file for CCD Deploy playbook.

## Playbook & Role Structure: ##
```
├── ansible.cfg
├── ccd-vmware-deploy-config.yml
├── vars
│   └── group_vars
│       └── minio.yml
```

## Required: 'podb-ipplan.csv' verification ##
* IP Address file 'podb-ipplan.csv' to be pulled down from MinIO and updated with the Deployment IP address allocations
  Once updates made to file, upload back into MinIO Object store.
  │
  └─ http://object.athtem.eei.ericsson.se/minio/cloud/
      - podb-ipplan.csv


## EXECUTION ##
Paramateres required.
* deployment_id

* cluster [Optional]
  - Defaults to POD-B-CCD-Cluster1 if not passed in


```
ansible-playbook ccd-vmware-deploy-config.yml -e deployment_id=<deployment_id> [-e cluster=XXXXX]

```

-------------------------------------------------------------------------------------------------------------------------------------------------------------


################################################################
# Upload CCD IBD into vcenter : ccd-vmware-upload-template.yml #
################################################################

## ToDo ##
*

## Description ##

Playbook to Automate the conversion and upload of the CCD IBD into vcenter.

## Playbook & Role Structure: ##
```
├── ansible.cfg
├── ccd-vmware-upload-template.yml
├── roles
│   └── install-govc-dependency
│       ├── tasks
│       │   └── main.yml
│       └── vars
│           └── main.yml
├── vars
│   └── group_vars
│       └── minio.yml
```
## Required: qcow image present verification ##
* The qcow image file should be present in it's own qcow_dir on the server qcow_dir=/absolute/path/to/directory/
  Once image is present, playbook can be ran passing in the qcow_dir


## EXECUTION ##
Paramateres required.
* qcow_dir
  - Directory in which the qcow image is located.
    - eg.. qcow_dir=/absolute/path/to/eccd-2.8.0-318/ would mean image is located in /absolute/path/to/eccd-2.8.0-318/

* cluster [Optional]
  - Defaults to POD-B-CCD-Cluster1 if not passed in


```
ansible-playbook ccd-vmware-upload-template.yml -e qcow_dir=</absolute/path/to/directory/> [-e cluster=XXXXX]

```

-------------------------------------------------------------------------------------------------------------------------------------------------------------


###########################################################################
# Perform template Post-Upload steps : ccd-vmware-template-post-steps.yml #
###########################################################################

## ToDo ##
* Figure out how to programatically change the Guest OS root password

## Description ##

Playbook to perform Post-upload configuration to an uploaded template.

## Playbook & Role Structure: ##
```
├── ansible.cfg
├── ccd-vmware-template-post-steps.yml
├── vars
│   └── group_vars
│       └── minio.yml
```
## Required: Root password set & VM fully booted ##
* Root password needs to be manually set as per the documented manual step:
  - https://www.youtube.com/watch?v=YlJoCQ-OBYI
* This playbook assumes that the root password of the VM has been set to the usual default credentials
* The uploaded VM needs to be booted up for this playbook to work


## EXECUTION ##
Paramateres required.
* node_name
  - Name of the uploaded VM


```
ansible-playbook ccd-vmware-template-post-steps.yml -e node_name=<node_name>

```

-------------------------------------------------------------------------------------------------------------------------------------------------------------


############################################################################
# Generate CCD Deploy config for VMware : ccd-vmware-generate-vmconfig.yml #
############################################################################

## ToDo ##
*

## Description ##

Playbook to Generate CCD Deploy config for VMware.
<deployment_id>.vmconfig.yml

## Playbook & Role Structure: ##
```
├── ansible.cfg
├── ccd-vmware-generate-vmconfig.yml
├── vars
│   └── group_vars
│       └── minio.yml
```
## Required: pod[x]-ipplan.csv Populated ##
* The IP address management CSV file (pod[x]-ipplan.csv) must be populated with the following for each node to be deployed:
    - Hostname
    - IP Address

* pod[x]-ipplan.csv location: http://object.athtem.eei.ericsson.se/minio/cloud/<pod[x]-ipplan.csv>

## Deployment present on DTT ##
* Before execution of the playbook, an entry for the <deployment_id> must be present in DTT
  - http://atvdtt/

* 2 parameters are required be present with values in the DTT entry:
 - flavour_name
 - vcenterCluster


## EXECUTION ##
Paramateres required.
* deployment_id


```
ansible-playbook ccd-vmware-generate-vmconfig.yml -e deployment_id=<deployment_id>

```