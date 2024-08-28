# Description of cleandown-project.yml playbook
# Prerequisites for playbook

1. Deployment id is needed to perform the operations.
2.  Playbook will fail itself if deployment_id not provided
3. Heat stack should be deleted.
4. Playbook will fail itself if stack is not deleted or partially deleted

# Run cleandown-project.yml

    ansible-playbook cleandown-project.yml -e deployment_id=<deployment_ID>


Example:


    ansible-playbook cleandown-project.yml -e deployment_id=ccd-c10a001


----------------------------------------------------------------------------------------------------------

1) healthcheck.yml
Run this playbook on ansible control plane to run Healthcheck.yml playbook from ECCD cluster on director node remotely.

## How to run this playbook: ##

ansible-playbook -e deployment_id={{deployment_id}} healthcheck.yml

<u>Example</u>:

ansible-playbook -e deployment_id=ccd-c13a001 healthcheck.yml

# Playbooks to add/delete CCD target in DE-CNI prometheus #
Playbook that will add a CCD target to the DE-CNI monitoring solution.
Requires the prometheus to have target defined as file-based service discovery.
Details can be found here:
https://prometheus.io/docs/guides/file-sd/

On the prometheus it is assumed the file to be used for service discovery is ccd-list.json
Can be configure using the ansible variable
ccd_list_file: ccd-list.json

1) add-ccd-to-prom.yml
Playbook will add a CCD target to the prometheus server

2) delete-ccd-to-prom.yml
Playbook will delete a CCD target from the prometheus server

## How to run the add/delete CCD target in prometheus playbooks: ##
```
ansible-playbook -e deployment_id=< CCD Deployment ID > add-ccd-to-prom.yml

ansible-playbook -e deployment_id=< CCD Deployment ID > delete-ccd-to-prom.yml
```

# Description of generate_admin_conf.yml playbook: #

1) generate-admin-conf.yml
Main playbook to generate k8s admin.conf file and upload to MinIO. deployment_id is considered as input from Jenkins

2) vars/group_vars/minio.yml
MinIO access credentials. May use other way to store this credentials in the future

## How to run generate_admin_conf.yml: ##

ansible-playbook generate-admin-conf.yml -e deployment_id={deployment id}

<u>Example</u>:

ansible-playbook generate-admin-conf.yml -e deployment_id=ccd-c13a001


# Description of deploy-monitoring-components.yml playbook: #

1) deploy-monitoring-components.yml
Main playbook to install DE-CNI monitoring components on CCD. deployment_id is considered as input from Jenkins

## How to run deploy-monitoring-components.yml: ##
## General
  ansible-playbook deploy-monitoring-components.yml -e deployment_id={ccd deployment ID}
## For cENM deployment
  ansible-playbook deploy-monitoring-components.yml -e deployment_id={ccd deployment ID} -e is_cenm=yes

<u>Example</u>:
## General
  ansible-playbook deploy-monitoring-components.yml -e deployment_id=ccd-c13a001
## For cENM deployment
  ansible-playbook deploy-monitoring-components.yml -e deployment_id=ccd-c13a001 -e is_cenm=yes


# Description of deploy-ccd-stack.yml playbook: #
## Prerequisites to use this playbook

1. ccdFlavor filed is defined in DTT.
2. CCD flavor templates are created in MinIO
3. OpenStack flavors and images have been created on OpenStack
4. CCD Image folder should exist on build server.
5. CCD stack environment file (config file) is ready in MinIO server

## How to run deploy-ccd-stack.yml: ##
  ansible-playbook deploy-ccd-stack.yml -e deployment_id={ccd deployment ID}

<u>Example</u>:
  ansible-playbook deploy-ccd-stack.yml -e deployment_id=ccd-c13a001

# Description of deploy-eventrouter.yml playbook
## Prerequisites for playbook

1. The K8s cluster is deployed
2. An Elasticsearch/Kibana server is available to forward cluster events

## Run deploy-eventrouter.yml playbook

    ansible-playbook deploy-eventrouter.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook deploy-eventrouter.yml -e deployment_id=ccd-c13a001

# Description of delete-ccd-stack.yml playbook
## Prerequisites for playbook

1. The K8s cluster is deployed
2. CCD stack environment file (config file) is ready in MinIO server

## Run delete-ccd-stack.yml playbook

    ansible-playbook delete-ccd-stack.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook delete-ccd-stack.yml -e deployment_id=ccd-c5a003

# Description of dtt-delete-ccd-productinfo.yml playbook
## Prerequisites for playbook

1. An existing target DTT deployment
2. A DTT CCD product-type

## Run dtt-delete-ccd-productinfo.yml playbook

    ansible-playbook dtt-delete-ccd-productinfo.yml  -e deployment_id=<deployment_ID>

Example:

    ansible-playbook dtt-delete-ccd-productinfo.yml  -e deployment_id=ccd-c13a001

# Description of dtt-check-ccd-status.yml playbook
Playbook for checking the status of a deployment in DTT at the start of the CCD Delete pipeline.
Required Status being checked is "Blocked/In Maintenance"
The playbook ensures that the DDT deployment status is "Blocked/In Maintenance" , if not the playbook fails

## Prerequisites for playbook

1. An existing target DTT deployment

## Required playbook parameters

1. deployment_id
     " -e deployment_id=<deployment_id> "

## Run dtt-check-ccd-status.yml playbook

    ansible-playbook dtt-check-ccd-status.yml  -e deployment_id=<deployment_ID>

Example:

    ansible-playbook dtt-check-ccd-status.yml  -e deployment_id=ccd-c13a001

# Description of dtt-change-ccd-status.yml playbook
Playbook for changing status in DTT at the end of the CCD Deploy pipeline.
Required Status being updated to is "In Use"
The playbook will check the current DTT deployment status & if it is not "In Use" it will update the entry
If already "In Use", the update tasks are skipped

## Prerequisites for playbook

1. An existing target DTT deployment

## Required playbook parameters

1. deployment_id
     " -e deployment_id=<deployment_id> "

## Run dtt-change-ccd-status.yml playbook

    ansible-playbook dtt-change-ccd-status.yml  -e deployment_id=<deployment_ID>

Example:

    ansible-playbook dtt-change-ccd-status.yml  -e deployment_id=ccd-c13a001

# Description of check-and-upload-images.yml playbook
## Prerequisites for playbook

1. Specific CCD Images exist on the build server
2. Image names in deployment env.yml file must correspond to correct naming convention
   eg. ( de-ccd-2.7.0-296-node )
3. OpenStack project de-cni-images must exist in the cloud along with the corresponding user

## Run check-and-upload-images.yml playbook

    ansible-playbook check-and-upload-images.yml -e deployment_id=<deployment_ID>

# Verify new CCD release version

## Steps

1. Run `prepare-ccd-image.yml` playbook with new CCD version

        ansible-playbook prepare-ccd-image.yml -e ccd_version=2.17.0

    This playbook will find the newly released IBD image and download to build server.

2. Run `prepare-ccd-version.yml` playbook with new version and deployment ID. This step might need to be done manually until we decide how to handle CCD versions in flavour templates.

        ansible-playbook prepare-ccd-version.yml -e ccd_version=2.17.0 -e deployment_id=ccd-c7a001

    This playbook will create a new CCD flavour template in Minio with the new release and update the deployment in DTT to use this new flavour.

3. Execute the CCD deploy Spinnaker pipeline with the deployment ID

4. Run `validate-prometheus-targets.yml` playbook with the deployment ID

        ansible-playbook validate-prometheus-targets.yml -e deployment_id=ccd-c7a001

    This playbook will validate that Prometheus targets are up for the deployment and that there are no unexpected alerts firing.

5. Run `validate-test-application.yml` playbook with the deployment ID

        ansible-playbook validate-test-application.yml -e deployment_id=ccd-c7a001

    This playbook will validate that a service with ingress can be run on the deployment.

# Description of prune-ccd-info-from-minio.yml
  Used in the reinstall pipline to prune all
  objects from minio in the target ccd-<deployment_id>
  except <deployment_id>.env.yml

## Prerequisites for playbook

1. A populated ccd-<deployment> in minio inc. the CCD stack environment file 

## Run prune-ccd-info-from-minio.yml playbook

    ansible-playbook prune-ccd-info-from-minio.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook prune-ccd-info-from-minio.yml -e deployment_id=ccd-c5a003
