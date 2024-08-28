# Introduction

## CCD pipeline playbooks and Ansible Vault

Most playbooks require access to data encrypted with Ansible Vault. The Vault
password must be passed in to Ansible or the playbook will fail. There are two
ways to do this.

Ansible will prompt for the password in an interactive prompt:

    ansible-playbook --ask-vault-pass <playbook-filename.yml>

Provide the path to a file containing the password for no prompt:

    ansible-playbook --vault-password-file <path_to_secret> <playbook-filename.yml>

> 📝 The rest of this README uses the interactive prompt in the examples.

When running many playbooks it could be helpful to define an alias:

    alias ap='ansible-playbook --vault-password-file <path_to_secret>'

> 📝 For security reasons, the password file option must not be used when
running playbooks on a shared server.

---
# Description of itam-getdata.yml for capo
  Gathers ITAM specific data per cluster re-install
  and uploads to a MinIO store namely
  http://object.athtem.eei.ericsson.se/minio/playbook-reports/itam/itam_target_data.yml
  see https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/CIE/Spike+-+ITAM+for+CCD 

## Prerequisites for playbook
  1. target cloud must exist and have re-installed successfully
  2. MinIO data store must be available at http://object.athtem.eei.ericsson.se/minio/playbook-reports/itam/itam_target_data.yml

## Run playbook
ansible-playbook itam-getdata.yml -ask-vault-pass
ex: /ccd_pipeline/capo_ansible$ ansible-playbook itam-getdata.yml -e deployment_id=ccd-c16c001 -ask-vault-pass

# Description of generate-and-upload-conf.yml for capo
  Creates a capo env file ex: ccd-c16c001.env.yml and
  uploads to the target cluster minio folder
  ex: minio/de-cni/ccd/ccd-c16c001/

## Prerequisites for playbook
  1. target cloud capo network yml ex: /minio/templates/cloud/cloud16c.network-capo.yml
  2. target cloud capo template yml ex: /minio/templates/cloud/cloud16c.template-vmware-capo.yml
  3. target cloud flavor template folder ex: minio/templates/managed-config/capo-std-de-small_2.26.0/
     containing ex: capo-std-de-small_2.26.0.env.yml and capo-std-de-small_2.26.0.template.yml

## Run playbook
ansible-playbook generate-and-upload-conf.yml -ask-vault-pass
ex: /ccd_pipeline/capo_ansible$ ansible-playbook -e deployment_id=ccd-c16c001 generate-and-upload-conf.yml -ask-vault-pass

# Description of recurring-compare-meteo-prometheus.yml
  Compares the total ccd count between Meteo and Prometheus
  and PASSES if both counts match.
  If there is total ccd count mismatch the playbook FAILS.

## Prerequisites for playbook
1. read access to meteo at https://meteo.athtem.eei.ericsson.se/
2. read access to prometheus at http://10.59.130.92:9090

## Run playbook
ansible-playbook recurring-compare-meteo-prometheus.yml -ask-vault-pass

# Description of fastfeedback-predrop-prepare.yml
  Download the fastfeedback PREDROP version on upgrade build server
  and extract as normal in the /ccd/IMAGES/ directory.
  It also verify the size of downloaded PREDROP directory.
  Gives message if size is less than 10GB.

## Prerequisites for playbook
1. The PREDROP release mail has been received.

## Run playbook

   ansible-playbook fastfeedback-predrop-prepare.yml -ask-vault-pass -e deployment_id=<deployment_id>

# Description of fastfeedback-version-dtt-overwrite.yml
  Verify the fastfeedback version image downloaded on upgrade build server.
  Locate the PREDROP on upgrade build server, name ex: capo-2.27.0-000985-296f12c3
  extract the fastfeedback_version instance from the extracted PREDROP iso on the build server.

  ex: 2.27.0-000985 from capo-2.27.0-000985-296f12c3 and write to the target DTT instance ex: fastfeedback_version: * *2.27.0-000985

## Prerequisites for playbook
1. The PREDROP feedback iso has been downloaded and extracted on the build server
2. The PREDROP version is updated in the target DTT deployment fastfeedback_version ex: 2.27.0 (this is manually entered in DTT)

## Run playbook

   ansible-playbook fastfeedback-version-dtt-overwrite.yml -ask-vault-pass -e deployment_id=<deployment_id>

# Description of fastfeedback-delete-predrop-build.yml
  Verify the predrop version image is on build server.
  Delete the image and all accompaying files ex: eccd-2.21.0-1011-e3333973.


## Prerequisites for playbook
1. The image is on the the build server

## Run playbook

   ansible-playbook fastfeedback-delete-predrop-build.yml -ask-vault-pass -e deployment_id=<deployment_id>


# Description of upgrade-check-and-upload-images.yml
  Uploads target ccd images (director + node) when
  those images do not exist on the UpgradeBuildServer.
  The images are uploaded from the UpgradeBuildServer
  using the prefix te (team elementals) and are used
  in the ccd_upgrade_pipeline.

  The images are uploaded as per below naming convention:
  te-ccd-<upgrade_version>-node
  te-ccd-<upgrade_version>-node
  (upgrade_version is available in the DTT target deployment instance)

  example:
  te-ccd-2.13.1-23-node
  te-ccd-2.13.1-23-director

## Prerequisites for playbook
1. Target CCD images on the UpgradeBuildServer (ieatsiipccdupg.athtem.eei.ericsson.se)
2. for more details see
   https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/CIE/Spike+-+Upgrade+CCD+Pipeline#SpikeUpgradeCCDPipeline-CompleteCCDImageforUpgradeBuildserver

## Run playbook

   ansible-playbook upgrade-check-and-upload-images.yml --ask-vault-pass -e deployment_id=<deployment_id>

# Description of join-oqs-queue.yml
  Implements CAPO joining the OQS queueing system.
  The playbook remains running until the CAPO
  deployment moves from Status Queued to Active in OQS.

## Prerequisites for playbook

1. access to OQS https://atvoqs.athtem.eei.ericsson.se/
2. for more details see
   https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/CIE/Spike+-+OQS+for+CCD+Pipelines

## Run playbook

   ansible-playbook join-oqs-queue.yml --ask-vault-pass -e deployment_id=<deployment_id>

# Description of Capo leave-oqs-queue.yml
  Implements Capo deployment leaving the OQS queueing system
  The playbook remains running until the Capo deployment
  moves to Status Finished in OQS.

## Prerequisites for playbook

1. access to OQS https://atvoqs.athtem.eei.ericsson.se/
2. for more details see
   https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/CIE/Spike+-+OQS+for+CCD+Pipelines

## Run playbook
   ansible-playbook leave-oqs-queue.yml --ask-vault-pass -e deployment_id=<deployment_id>

# Description of staging-version-flavor-template.yml
  Finds CCD Flavor and CCD Staging Version in DTT then finds the relevant CCD flavor template file in MinIO and
  updates the current version in the template to the staging version from DTT.
  This playbook is not a stage in the ccd pipeline

## Prequisites for playbook

1. DTT entry exists for <deployment_id> and is fully updated
2. CCD Flavor Template file exists on MinIO

## Run staging-version-flavor-template.yml playbook

    ansible-playbook staging-version-flavor-template.yml --ask-vault-pass -e deployment_id=<deployment_id>

# Description of post-ccd-upgrade-cleanup.yml
  Removes the upgrade_version value from <deployment_id> DTT entry.
  Deletes the upgrade image for a particular <deployment_id> from the Upgrade Build server.
  Verifies that *_<deployment_id> image exists on the Upgrade build server in /ccd/IMAGES/UPGRADE/.
  Deletes /ccd/IMAGES/UPGRADES/*_<deployment_id> from Upgrade Build server
  This playbook is a stage in the ccd upgrade pipeline

## Prerequisites for playbook

1. ccd deployment <deployment_id> exists on DTT
2. ccd upgrade image is present on the Upgrade Build server in /ccd/IMAES/UPGRADE/

## Run post-ccd-upgrade-cleanup.yml playbook

    ansible-playbook post-ccd-upgrade-cleanup.yml -e deployment_id=<deployment_id> --ask-vault-pass

# Description of upgrade-ccd-stack.yml
  Performs the CCD update on a target CCD stack
  This playbook is a stage in the ccd upgrade pipeline

## Prerequisites for playbook

1. A target pre-existing CCD stack
2. A corresonding pre-existing ENV file in Minio at /minio/de-cni/ccd/<deployment_id>/

## Run upgrade-ccd-stack.yml playbook
    ansible-playbook upgrade-ccd-stack.yml --ask-vault-pass -e deployment_id=ccd-c16a030

# Description of prepare-ccd-upgrade.yml
  Prepares the upgrade image for a particular <deployment_id> on the Build server.
  Retrieves the deployments current ccd_version & upgrade_ccd_version from DTT.
  Verifies that upgrade_ccd_version image exists on the build server.
  Copies content of upgrade_ccd_version image to /ccd/IMAGES/UPGRADES & renames to <ccd_version>
  This playbook is a stage in the ccd upgrade pipeline

## Prerequisites for playbook

1. ccd deployment <deployment_id> exists on DTT
2. ccd upgrade version key:value defined in the target DTT deployment

## Run prepare-ccd-upgrade.yml playbook

    ansible-playbook prepare-ccd-upgrade.yml -e deployment_id=<deployment_id> --ask-vault-pass

# Description of upgrade-generate-config.yml
  Updates the MinIO <deployment_id>.env.yml with the DTT upgrade version for
  master,director and worker images.
  This playbook is a stage in the ccd upgrade pipeline

## Prerequisites for playbook

1. ccd <deployment_id>.env.yml exists in MinIO in de-cni/ccd/<deployment_id>/
2. ccd upgrade version key:value defined in the target DTT deployment

## Run upgrade-generate-config.yml playbook

    ansible-playbook upgrade-generate-config.yml -e deployment_id=ccd-c11a008 --ask-vault-pass

# Description of cleanup-docker-containers.yml
  Verifies docker containers on server to those on keep list to find out which are eligible for removal
  Highlights if a docker container on the keep list is not found on the server, highlighting possible deletion
  Lists docker containers on server that are greater than 199Mb in size, highlighting for examination
  Lists docker containers on server that were created 12 or more months ago, highlighting for examination
  This playbook is not a stage in the ccd pipeline


## Prerequisites for playbook

1. builder-server-docker-yml is up to date
2. docker containers are running on the server

## Run cleanup-docker-container.yml playbook

    ansible-playbook --ask-vault-pass docker_cleanup.yml


# Description of upgrade-version-dtt-check.yml
  Verifies the upgrade version instance integrity in the target DTT deployment
  This playbook is a stage in the ccd upgrade pipeline

## Prerequisites for playbook

1. ccd upgrade version key:value defined in the target DTT deployment

## Run upgrade-version-dtt-check.yml playbook

    ansible-playbook upgrade-version-dtt-check.yml --ask-vault-pass -e deployment_id=ccd-c5a003

# Description of capo remove-pvc-volumes.yml playbook
## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided.

## Run remove-pvc-volumes.yml

    ansible-playbook --ask-vault-pass remove-pvc-volumes.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass  remove-pvc-volumes.yml -e deployment_id=ccd-c10a001


----------------------------------------------------------------------------------------------------------

1) healthcheck.yml
Run this playbook on ansible control plane to run Healthcheck.yml playbook from ECCD cluster on director node remotely.

## How to run this playbook: ##

    ansible-playbook --ask-vault-pass -e deployment_id=<deployment_id> healthcheck.yml

<u>Example</u>:

    ansible-playbook --ask-vault-pass -e deployment_id=ccd-c13a001 healthcheck.yml

# Playbooks to add/delete CAPO target in DE-CNI prometheus #
Playbook that will add a CAPO target to the DE-CNI monitoring solution.
Requires the prometheus to have target defined as file-based service discovery.
Details can be found here:
https://prometheus.io/docs/guides/file-sd/

On the prometheus it is assumed the file to be used for service discovery is ccd-list.json
Can be configure using the ansible variable
ccd_list_file: ccd-list.json

1) add-ccd-to-prom.yml
Playbook will add a CAPO target to the prometheus server

2) delete-ccd-from-prom.yml
Playbook will delete a CCD target from the prometheus server

## How to run the add/delete CAPO target in prometheus playbooks: ##
```
ansible-playbook --ask-vault-pass -e deployment_id=< CCD Deployment ID > add-ccd-to-prom.yml

ansible-playbook --ask-vault-pass -e deployment_id=< CCD Deployment ID > delete-ccd-from-prom.yml
```

# Description of generate_admin_conf.yml playbook: #

Main playbook to generate k8s admin.conf file and upload to MinIO. deployment_id is considered as input from Jenkins

## How to run generate_admin_conf.yml: ##

    ansible-playbook --ask-vault-pass generate-admin-conf.yml -e deployment_id={deployment id}

<u>Example</u>:

    ansible-playbook --ask-vault-pass generate-admin-conf.yml -e deployment_id=ccd-c13a001


# Description of deploy-monitoring-components.yml playbook: #

Main playbook to install DE-CNI monitoring components on CCD. deployment_id is considered as input from Jenkins
for more details, see page:
https://confluence-oss.seli.wh.rnd.internal.ericsson.com/pages/viewpage.action?spaceKey=CIE&title=Monitoring

## How to run deploy-monitoring-components.yml: ##

    ansible-playbook --ask-vault-pass deploy-monitoring-components.yml -e deployment_id={ccd deployment ID}

<u>Example</u>:

    ansible-playbook --ask-vault-pass deploy-monitoring-components.yml -e deployment_id=ccd-c13a001

# Description of undeploy-monitoring-components.yml playbook: #

Main playbook to uninstall DE-CNI monitoring components from CCD. deployment_id is considered as input from Jenkins

## How to run undeploy-monitoring-components.yml: ##

    ansible-playbook --ask-vault-pass undeploy-monitoring-components.yml -e deployment_id={ccd deployment ID}

<u>Example</u>:

    ansible-playbook --ask-vault-pass undeploy-monitoring-components.yml -e deployment_id=ccd-c13a001

# Description of deploy-capo-cluster.yml playbook: #
## Prerequisites to use this playbook

1. ccdFlavor filed is defined in DTT.
2. CCD flavor templates are created in MinIO
3. OpenStack flavors and images have been created on OpenStack
4. CAPO Image folder should exist on build server.
5. CAPO cluster environment file (config file) is ready in MinIO server

Optional Vars:
- search_image_dir
    > String - Path to Images Location
    > Default - /ccd/IMAGES
    > Example Override - /ccd/IMAGES/STAGING

## How to run deploy-capo-cluster.yml: ##

    ansible-playbook --ask-vault-pass deploy-capo-cluster.yml -e deployment_id={ccd deployment ID} [ -e search_image_dir=/path/to/images ]

<u>Example</u>:

    ansible-playbook --ask-vault-pass deploy-capo-cluster.yml -e deployment_id=ccd-c13a001

# Description of deploy-eventrouter.yml playbook
## Prerequisites for playbook

1. The K8s cluster is deployed
2. An Elasticsearch/Kibana server is available to forward cluster events

## Run deploy-eventrouter.yml playbook

    ansible-playbook --ask-vault-pass deploy-eventrouter.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass deploy-eventrouter.yml -e deployment_id=ccd-c13a001

# Description of delete-capo-cluster.yml playbook
Delete capo cluster from a given deployment
If the directory for the deployment does not exist in ccd/IMAGES/capo-<image>/
Playbook will create the directory and download the env file(config file) from MinIo server/deployment bucket
## Prerequisites for playbook

1. The K8s cluster is deployed
2. CAPO environment file (config file) is ready in MinIO server

## Run delete-capo-cluster.yml playbook

    ansible-playbook --ask-vault-pass delete-capo-cluster.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass delete-capo-cluster.yml -e deployment_id=ccd-c11a001

# Description of capo dtt-delete-ccd-productinfo.yml playbook
## Prerequisites for playbook

1. An existing target DTT deployment
2. A DTT CCD product-type

## Run dtt-delete-ccd-productinfo.yml playbook

    ansible-playbook --ask-vault-pass dtt-delete-ccd-productinfo.yml  -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass dtt-delete-ccd-productinfo.yml  -e deployment_id=ccd-c13a001

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

    ansible-playbook --ask-vault-pass dtt-check-ccd-status.yml  -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass dtt-check-ccd-status.yml  -e deployment_id=ccd-c13a001

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

    ansible-playbook --ask-vault-pass dtt-change-ccd-status.yml  -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass dtt-change-ccd-status.yml  -e deployment_id=ccd-c13a001

# Description of check-and-upload-images.yml playbook
Playbook to Verify that the required CAPO Images for a Deployment are present.
Check is performed against the Deployments OpenStack Tenancy.
If Images not Present:
Playbook attempts to locate Images on Build Server & Uploads to OpenStack.
If Images already Present:
No action taken & Playbook Completes Successfully

Required Vars:
- deployment_id = String - Example ( ccd-c10a001 )

Optional Vars:
- search_image_dir
    > String - Path to Images Location
    > Default - /ccd/IMAGES
    > Example Override - /ccd/IMAGES/STAGING

Example usage
-------------
Manually enter ansible vault passwd:
 $ ansible-playbook check-and-upload-images.yml -e deployment_id=<deployment_id> --ask-vault-pass [ -e search_image_dir=/path/to/dir ]

Retrieve ansible vault passwd from file:
 $ ansible-playbook check-and-upload-images.yml -e deployment_id=<deployment_id> --vault-password-file /path/to/file [ -e search_image_dir=/path/to/dir ]

# Verify new CCD release version

## Steps

1. Run `prepare-ccd-image.yml` playbook with new CCD version

        ansible-playbook --ask-vault-pass prepare-ccd-image.yml -e ccd_version=2.17.0

    This playbook will find the newly released IBD image and download to build server.

2. Run `prepare-ccd-version.yml` playbook with new version and deployment ID. This step might need to be done manually until we decide how to handle CCD versions in flavour templates.

        ansible-playbook --ask-vault-pass prepare-ccd-version.yml -e ccd_version=2.17.0 -e deployment_id=ccd-c7a001

    This playbook will create a new CCD flavour template in Minio with the new release and update the deployment in DTT to use this new flavour.

3. Execute the CCD deploy Spinnaker pipeline with the deployment ID

4. Run `validate-prometheus-targets.yml` playbook with the deployment ID

        ansible-playbook --ask-vault-pass validate-prometheus-targets.yml -e deployment_id=ccd-c7a001

    This playbook will validate that Prometheus targets are up for the deployment and that there are no unexpected alerts firing.

5. Run `validate-test-application.yml` playbook with the deployment ID

        ansible-playbook --ask-vault-pass validate-test-application.yml -e deployment_id=ccd-c7a001

    This playbook will validate that a service with ingress can be run on the deployment.

# Description of capo prune-ccd-info-from-minio.yml
  Used in the reinstall pipline to prune all
  objects from minio in the target ccd-<deployment_id>
  except <deployment_id>.env.yml

## Prerequisites for playbook

1. A populated ccd-<deployment> in minio inc. the CCD stack environment file

## Run prune-ccd-info-from-minio.yml playbook

    ansible-playbook --ask-vault-pass prune-ccd-info-from-minio.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass prune-ccd-info-from-minio.yml -e deployment_id=ccd-c5a003

# Description of assign-ccd-dtt-networking.yml
  Populates DTT with cluster networkGGN and/or networkECN
  This playbook is standalone and not part of the ccd_pipeline

## Prerequisites for playbook

1. minIO de-cni/ccd/dtt-ccd-networking/dtt-deployments.yml
   - lists clusters in format eg. ccd-c11a008 to be updated in DTT with networkGGN and/or networkECN
2. tasks-ccd-dtt-networking.yml
   - called by dtt-deployments.yml
3. for more details
   https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/CIE/Spike+-+CCD+networking+defined+in+DTT

## Run assign-ccd-dtt-networking.yml playbook

    ansible-playbook --ask-vault-pass assign-ccd-dtt-networking.yml

# Description of teardown-and-delete-project.yml
  Used to teardown and delete the Openstack Project when a CCD Project
  is being decommissioned.
  Makes a call to the Meteo tool which deletes the project from Openstack
  along with the project admin user.
  deployment_id is considered as input from Jenkins.

## Prerequisites for playbook
1. CCD project is removed from Prometheus

2. CCD stack is deleted

## Run teardown-and-delete-project.yml playbook

    ansible-playbook --ask-vault-pass teardown-and-delete-project.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass teardown-and-delete-project.yml -e deployment_id=ccd-c5a003

# Description of prepare-ccd-prebuild-image-weekly.yml
  Download the last Successful pre-build of CCD image from artifactory to build server

## Prerequisites for playbook
1.  /ccd/IMAGES/PREDROP folder is present on build server. Playbook checks for this folder and will fail if folder is not present.


## Run prepare-ccd-prebuild-image-weekly.yml playbook

    ansible-playbook --ask-vault-pass prepare-ccd-image-weekly.yml


# Description of dtt-deployment-audit.yml playbook
Playbook for performing an audit of the current fleet of managed DTT deployments.
To be run as a sprintly housekeeping task.
The Audit procedure will extract a select set of parameters from each dtt deployment &
compare/check for any value changes that may have occurred since the playbook/audit was last ran.
Playbook can be ran against the entire fleet of managed deployments or just against a single
deployment by passing an optional deployment_id parameter on execution

Confluence Page for Playbook :
https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/CIE/Ansible+Playbook+to+Audit+DTT+Managed+Deployments

## Prerequisites for playbook

1. Existing DTT deployments

2. File 'dtt_audit_params.yml' present on MinIO in 'de-cni/dtt-audit/' bucket

## OPTIONAL playbook parameters

1. deployment_id
     " -e deployment_id=<deployment_id> "

## Run dtt-change-ccd-status.yml playbook

    #~# Run against Entire fleet #~#
    ansible-playbook --ask-vault-pass dtt-deployment-audit.yml

    #~# Run against Single deployment #~#
    ansible-playbook --ask-vault-pass dtt-deployment-audit.yml -e deployment_id=<deployment_id>

Example:

    ansible-playbook --ask-vault-pass dtt-deployment-audit.yml
    ansible-playbook --ask-vault-pass dtt-deployment-audit.yml -e deployment_id=ccd-c13a001

# Description of minio-server-audit.yml playbook
Playbook for performing an audit of the deployments & flavors currently present on MinIO.
To be run as a sprintly housekeeping task.
The Audit procedure will extract a list of deployments & flavors from MinIO.
Pulls down a list of CCD deployments from DTT.
The lists are then compared & any flavors/deployments missing from any of the lists are documented in a log file "minio_audit.log"
This log file is stored on MinIO:
http://object.athtem.eei.ericsson.se/minio/playbook-reports/minio-audit/

## Prerequisites for playbook

1. Existing DTT deployments

2. Existing MinIO deployments & Flavors

## Run minio-server-audit.yml playbook

    ansible-playbook --ask-vault-pass minio-server-audit.yml

# Description of build-server-check.yml playbook
This playbook is part of the build server and MinIO sprintly check.
Following items will be checked in this playbook. If any of these item fails, the playbook will fail.
1. Build server folder/mounts disk spaces usage are below 90%
2. Python2 Check
3. Python3 Check
4. OpenStack client check

## Run build-server-check.yml playbook
    ansible-playbook --ask-vault-pass build-server-check.yml

# Description of upgrade-version-flavor-template.yml playbook
Upgrades the target deployment flavor template ccd version with the upgrade version
This playbook is a stage in the ccd upgrade pipeline

## Prerequisites for playbook

1. ccd Flavor key:value defined in the target DTT deployment
2. ccd upgrade version key:value defined in the target DTT deployment

## Run upgrade-version-flavor-template.yml playbook

    ansible-playbook upgrade-version-flavor-template.yml --ask-vault-pass -e deployment_id=<deployment_id>

# Description of allocate-pm-resources.yml playbook
Workaround for allocation of pm resources on the targeted cluster.
Allocates additional memory and volume_size for pm_server pods and pvc.
Reinstalls the charts through two ansible playbooks on the targeted cluster.
This playbook is a stage in the ccd upgrade pipeline

## Run allocate-pm-resources.yml playbook
    ansible-playbook --ask-vault-pass allocate-pm-resources.yml -e deployment_id=<deployment_id>

# Description of deploy-k8set.yml playbook

Installs the Kubernetes Evaluation Toolkit (K8set) helm chart to a K8s cluster. If the
helm chart is already installed, the existing chart is first removed.

K8set performs configuration checks and benchmarks and gives a pass/fail based
on the results.

## Run deploy-k8set.yml playbook
    ansible-playbook --ask-vault-pass deploy-k8set.yml -e deployment_id=<deployment_id>

# Description of prepare-ccd-staging-image-weekly.yml
Download the last Successful weekly staging build of CCD image from artifactory to build server.
If there is no new weekly staging build CCD image, i.e. the image on the build server is at the lastest staging build version,
the playbook will output this message and exit.
All old staging builds on the build server will also be deleted.

## Prerequisites for playbook
1.  /ccd/IMAGES/STAGING folder is present on build server. Playbook checks for this folder and will fail if folder is not present.


## Run prepare-ccd-prebuild-image-weekly.yml playbook

    ansible-playbook --ask-vault-pass prepare-ccd-staging-image-weekly.yml

# Description of dtt-update-ccd-staging-version.yml playbook
## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided.
2. Playbook assumes there is /ccd/IMAGES/STAGING folder exists on build server
3. Playbook will fail if there is no or more than one staging version folders exist in /ccd/IMAGES/STAGING folder
4. Playbook assumes staging folder name convention is eccd-x.y.z-abc-* e.g.  eccd-2.19.0-812-68456b5d


## Run dtt-update-ccd-staging-version.yml

    ansible-playbook --ask-vault-pass dtt-update-ccd-staging-version.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass dtt-update-ccd-staging-version.yml -e deployment_id=ccd-c13a001

# Description of dtt-update-ccd-deployment.yml playbook
## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided.
2. Playbook uses product-configuration-template.json (located in capo_ansible/json-files/) key value pairs to update deployment on dtt
3. Playbook will fail if the file paths in product-configuration-template.json do not exist or incorrect


## Run dtt-update-ccd-deployment.yml

    ansible-playbook --ask-vault-pass dtt-update-ccd-deployment.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass dtt-update-ccd-deployment.yml -e deployment_id=ccd-c13a001

# Description of fastfeedback-dtt-update-ccd-deployment.yml playbook
  Checks the fastfeedback version and updates the ccd version for dtt deployment
  Will also update the rest of dtt values as per dtt-update-ccd-deployment.yml
## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided.
2. Playbook uses product-configuration-template.json (located in capo_ansible/json-files/) key value pairs to update deployment on dtt
3. Playbook will fail if the file paths in product-configuration-template.json do not exist or incorrect


## Run dtt-update-ccd-deployment.yml

    ansible-playbook --ask-vault-pass fastfeedback-dtt-update-ccd-deployment.yml -e deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass fastfeedback-dtt-update-ccd-deployment.yml -e deployment_id=ccd-c16a001


# Description of deploy-staging-stack.yml playbook
## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided.
2. Playbook assumes there is /ccd/IMAGES/STAGING folder exists on build server
3. Playbook assumes staging folder name convention is eccd-x.y.z-abc-* e.g.  eccd-2.19.0-812-68456b5d

## Run deploy-staging-stack.yml

    ansible-playbook --ask-vault-pass deploy-staging-stack.yml deployment_id=<deployment_ID>

Example:

    ansible-playbook --ask-vault-pass deploy-staging-stack.yml -e deployment_id=ccd-c13a001


# Description of fastfeedback-version-dtt-verify.yml
  Verifies the fastfeedback version instance integrity in the target DTT deployment
  This playbook is a stage in the ccd prafastfeedback pipeline

## Prerequisites for playbook

1. ccd fastfeedback version key:value defined in the target DTT deployment

## Run fastfeedback-version-dtt-verify.yml playbook

    ansible-playbook fastfeedback-version-dtt-verify.yml --ask-vault-pass -e deployment_id=ccd-c5a003

# Description of checklist-version-dtt-verify.yml
  Verifies the checklist version instance integrity in the target DTT deployment

## Prerequisites for playbook

1. ccd checklist version key:value defined in the target DTT deployment


## Run checklist-version-dtt-verify.yml playbook

    ansible-playbook checklist-version-dtt-verify.yml --ask-vault-pass -e deployment_id=ccd-c5a003


# Description of checklistpreupgrade-dtt-verify.yml
  Verifies the neccesary dtt entries exist in the target DTT deployment

## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided

## Run checklistpreupgrade-dtt-verify.yml playbook

    ansible-playbook checklistpreupgrade-dtt-verify.yml --ask-vault-pass -e deployment_id=ccd-c5a003
1. ccd checklist version key:value defined in the target DTT deployment

# Description of checklistpreupgrade-osflavors-verify.yml
  Verifies the target deployments env file flavors exist in openstack


## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided

## Run checklistpreupgrade-osflavors-verify.yml playbook

    ansible-playbook checklistpreupgrade-osflavors-verify.yml --ask-vault-pass -e deployment_id=ccd-c5a003

# Description of checklistpreupgrade-dit-verify.yml
  Verifies  target deployment exists in DIT and has an ipv4 range


## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided


## Run checklistpreupgrade-dit-verify.yml playbook

    ansible-playbook checklistpreupgrade-dit-verify.yml --ask-vault-pass -e deployment_id=ccd-c5a003
1. ccd checklist version key:value defined in the target DTT deployment

# Description of checklistpreupgrade-minio-verify.yml
  Verifies the ccdFlavor dtt value exists and that the corresponding env ant template files exists on
  minio and that the template file ccd_version matches dtt cdd_version for the target deployment
  This playbook is a stage in the checklistpreupgrade pipeline


## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided


## Run checklistpreupgrade-minio-verify.yml playbook

    ansible-playbook checklistpreupgrade-minio-verify.yml --ask-vault-pass -e deployment_id=ccd-c5a003



# Description of checklistpreupgrade-upgradebuildserver-verify.yml
  Verifies the upgrade build server UPGRADE directory is empty for the target DTT deployment
  This playbook is a stage in the ccd preupgradechecklist pipeline

## Prerequisites for playbook

1. Deployment ID is needed. Playbook will fail if deployment_id not provided

## Run checklistpreupgrade-upgradebuildserver-verify.yml playbook

    ansible-playbook checklistpreupgrade-upgradebuildserver-verify.yml --ask-vault-pass -e deployment_id=ccd-c5a003

# Description of checklist-version-dtt-remove.yml
  Removes the checklist version instance in the target DTT deployment
  This playbook is a stage in the checklistpreupgrade pipeline

## Prerequisites for playbook

1. ccd checklist version key:value defined in the target DTT deployment

## Run checklist-version-dtt-remove.yml playbook

    ansible-playbook checklist-version-dtt-remove.yml --ask-vault-pass -e deployment_id=ccd-c5a003

# Description of upload-ccd-info-to-minio.yml playbook
  Pushes files created from a deployment installation and created from the playbook to relevant minio location e.g. de-cni/ccd/ccd-c10a001
## Prerequisites for playbook

1. An existing target DTT deployment
2. Existing files (target_kubeconfig, cp_ssh_key) in directory e.g. /ccd/IMAGES/capo-2.26.0-000004-5dd676cf/ccd-c10a001/ccd-c10a001/

Optional Vars:
- search_image_dir
    > String - Path to Images Location
    > Default - /ccd/IMAGES
    > Example Override - /ccd/IMAGES/STAGING

## Run upload-ccd-info-to-minio.yml playbook
    ansible-playbook --ask-vault-pass upload-ccd-info-to-minio.yml  -e deployment_id=<deployment_ID> [ -e search_image_dir=/path/to/images ]

Example:

    ansible-playbook --ask-vault-pass upload-ccd-info-to-minio.yml  -e deployment_id=ccd-c10a001

# Description of checklistpreupgrade-envfile-verify.yml
  Ensure the target ENV file exist on MINIO path for CCD.
  check the director,master and worker images contain the DTT version.

  e.g: master_image: de-ccd-2.17.2-3-node would need a DTT version:2.17.2-3 to be valid

## Prerequisites for playbook

1. ccd version key:value defined in the target DTT deployment

## Run playbook

   ansible-playbook checklistpreupgrade-envfile-verify.yml -ask-vault-pass -e deployment_id=<deployment_id>

# Description of util-dtt-add-vrouter-vmware.yml
  Add "vrouter:vmware" key:pair tag to DTT deployment instance provided as a input deployment_id.

## Prerequisites for playbook

1. cloud networks are setup and available in vmware
2. minio cloud network.yml networks updated as appropriate
3. minio cloud template-vmware.yml updated as appropriate
4. the cluster ccd installs have not taken place yet (StackCentric)

## Run playbook

   ansible-playbook util-dtt-add-vrouter-vmware.yml -ask-vault-pass -e deployment_id=<deployment_id>

# Description of recurring-verify-ccd-external-access.yml
  Verifies external access to all ccds by curling each ccd api endpoint
  This playbook is a stage in the recurring pipeline

## Prerequisites for playbook

1. target deployment id supplied if running in signle deployment mode otherwise will test all de-cni ccds in prometheus

## Run recurring-verify-ccd-external-access.yml playbook

    ansible-playbook reccuring-verify-ccd-external-access.yml --ask-vault-pass -e deployment_id=ccd-c5a003

# Description of recurring-cleanup-minio-flavors.yml
  To archive unused (ie. not active/named in DTT deployments) in Minio ensuring only DTT active flavor are defined in Minio at http://object.athtem.eei.ericsson.se/minio/templates/managed-config/

## Prerequisites for playbook
1. access to Minio at http://object.athtem.eei.ericsson.se/minio/templates/managed-config/
2. an existing ARCHIVE folder in http://object.athtem.eei.ericsson.se/minio/templates/managed-config/
3. this feature for Minio flavor archive support should run in the ccd_recurring pipeline as the second to last stage

## Run playbook

   ansible-playbook recurring-cleanup-minio-flavors.yml --vault-password-file <path_to_secret>

# Description of test-recurring-cleanup-minio-flavors.yml
  Script to copy content of managed-config to devang-test to test recurring-cleanup-minio-flavors.yml

## Prerequisites for playbook

## Run playbook

   ansible-playbook test-recurring-cleanup-minio-flavors.yml --vault-password-file <path_to_secret>


## Prerequisites for playbook
1. access to Minio at http://object.athtem.eei.ericsson.se/minio/de-cni/
3. this feature for Minio flavor metrics support should run in the ccd_recurring pipeline as the last stage

## Run playbook

   ansible-playbook recurring-get-ccd-fleet-per-flavor-ttlcount.yml --vault-password-file <path_to_secret>

# Description of test-recurring-cleanup-minio-flavors.yml
  Script to calculate count of deployments using flavors - count per flavor - and store the data in minio at http://object.athtem.eei.ericsson.se/minio/de-cni/de-cni-fleet-metrics/ccd-fleet-metrics.(json/csv) for grafana and excel representations respectively


# Description of recurring-get-ccd-oi-edge-cases.yml
  Script to calculate count of deployments using decommissioned flavors and pull the edge case business case descriptions from dtt - and store the data in minio at http://object.athtem.eei.ericsson.se/minio/de-cni/de-cni-fleet-metrics/ccd-fleet-metrics-oi-edge-cases.(json/csv) for grafana and excel representations respectively

## Prerequisites for playbook
1. access to Minio at http://object.athtem.eei.ericsson.se/minio/de-cni/
3. this feature for Minio oi edge case metrics support should run in the ccd_recurring pipeline as the last stage

## Run playbook

   ansible-playbook recurring-get-ccd-oi-edge-cases.yml --vault-password-file <path_to_secret>

# Description of recurring-get-ccd-fleet-cluster-ages.yml
  Script to calculate age of deployments - and store the data in minio at http://object.athtem.eei.ericsson.se/minio/de-cni/de-cni-fleet-metrics/ccd-fleet-metrics-stack-ages.(json/csv) for grafana and excel representations respectively

## Prerequisites for playbook
1. access to Minio at http://object.athtem.eei.ericsson.se/minio/de-cni/
3. this feature for stack age metrics support should run in the ccd_recurring pipeline as the last stage

## Run playbook

   ansible-playbook recurring-get-ccd-fleet-cluster-ages.yml --vault-password-file <path_to_secret>


# Description for CAPO healthcheck.yml
Run this playbook on ansible control plane to run Healthcheck.yml playbook for CAPO cluster.

Optional Vars:
- search_image_dir
    > String - Path to Images Location
    > Default - /ccd/IMAGES
    > Example Override - /ccd/IMAGES/STAGING

## How to run this playbook: ##

    ansible-playbook --ask-vault-pass -e deployment_id=<deployment_id> healthcheck.yml [ -e search_image_dir=/path/to/images ]


    ansible-playbook --ask-vault-pass -e deployment_id=ccd-c13a001 healthcheck.yml

# Description of capo_deploy_client_vm.yml
Playbook to deploy a client VM on the relevant Openstack for a passed in deployment_id
Resources for Client VM deployed are specified in the following location:
- templates/capo_clientvm/capo_clientvm_flavors.j2
New Flavors can be added to file & will need to be commited to Repo with team approval via code review.

Dependancies:
- Product Configuration Item 'client_vm' needs to be present on DTT for Deployment.
  > Format: 'true-<flavor>', 'deployed-<flavor>' (true if deploy/redeploy vm needed, deployed to do nothing)
  > Current Valid Flavors are ( client_medium, client_large )
  > Example: to deploy / redeploy a client VM, 'client_vm' would look as follows:
    - true-client_medium or true-client_large
  > Example: to keep existing client VM upon cluster reinstall, 'client_vm' would look as follows:
    - deployed-client_medium or deployed-client_large

Required Vars:
- deployment_id = String - Example ( ccd-c10a001 )

NB: Vars files used in this playbook require ansible-vault decrypting

<u>Example</u>:
 -------------
Manually enter ansible vault passwd:
  $ ansible-playbook capo_deploy_client_vm.yml -e deployment_id=<deployment_id> --ask-vault-pass

Retrieve ansible vault passwd from file:
  $ ansible-playbook capo_deploy_client_vm.yml -e deployment_id=<deployment_id> --vault-password-file /path/to/file
c


# Description of prepare-capo-staging-image-weekly.yml
Playbook to pull down & extract the last successful weekely pre-build of CAPO.
This playbook is used as part of the staging pipeline:
https://confluence-oss.seli.wh.rnd.internal.ericsson.com/pages/viewpage.action?pageId=620298892

Playbook will pull down & extract the image from artifactory to the Upgrade Build Server

Example usage
-------------
Manually enter ansible vault passwd:
 $ ansible-playbook prepare-capo-staging-image-weekly.yml --ask-vault-pass

Retrieve ansible vault passwd from file:
 $ ansible-playbook prepare-capo-staging-image-weekly.yml --vault-password-file /path/to/file

# Description of capo_staging_delete_old_images.yml
Playbook to delete old & unused pre-build Images of CAPO.
Current in-use image is extracted from the staging deployment_id.
All other Images present in STAGING dir on the Build Server will be deleted.

This playbook is used as part of the staging pipeline:
https://confluence-oss.seli.wh.rnd.internal.ericsson.com/pages/viewpage.action?pageId=620298892

Required Vars:
- deployment_id = String - Example ( ccd-c10a001 )

Example usage
-------------
Manually enter ansible vault passwd:
 $ ansible-playbook capo_staging_delete_old_images.yml -e deployment_id=<deployment_id> --ask-vault-pass

Retrieve ansible vault passwd from file:
 $ ansible-playbook capo_staging_delete_old_images.yml -e deployment_id=<deployment_id> --vault-password-file /path/to/file

# Description of fastfeedback-version-template.yml
Upgrade the target deployment flavor template ccd_version with the fastfeeback_version

## Prerequisites for playbook
fastfeedback version is on deployment DTT
check CCD template file is on Minio (see managed config e.g. playbook will take value from DTT ccdFlavor: capo-std-de-medium_2.26.0-000393 and will get the template file on minio and have the ccd version updated with another value taken from DTT, version: 2.26.0-000393)

## Run playbook

 $ ansible-playbook fastfeedback-version-template.yml -ask-vault-pass -e deployment_id=<deployment_id>

# Description of fastfeedback-delete-predrop-build.yml
Delete predrop build from upgrade build server

Prerequisites for playbook
The image is on the the upgrade build server
Run playbook
ansible-playbook fastfeedback-delete-predrop-build.yml -ask-vault-pass -e deployment_id=<deployment_id>
