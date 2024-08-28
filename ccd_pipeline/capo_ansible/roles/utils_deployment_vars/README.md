utils_deployment_vars
=====================

Role to load all deployment variables into memory so they can be used in a playbook.
The purpose of this role is to centralise the generation & fetching of deployment vars into one place.
This will help in removing duplication of code/tasks that set deployment specific vars.

NB: This role is solely for setting Deployment Related Vars.

Role Variables
--------------
- 'deployment_id': String | Required - Example ( ccd-c10a001 )
- 'add_vars': list[] - Default( [ dtt,minio,dit ] ), Available Options (dtt, minio, dit)

Generated Vars
--------------
- 'deployment_vip': String - VIP address for accessing Controlplane/Director (minio)
- 'deployment_pem': String - SSH Key String Required for accessing Controlplane/Director (minio)
- 'deployment_kubeconfig': YAML - Contents of deployment kubeconfig file (minio)
- 'deployment_env': YAML - Contents of deployment ENV file (minio)
- 'dtt_deployment': YAML - Deployment data fetched from DTT (dtt)
- 'dtt_deployment_id': String - DTT ID of Deployment (dtt)
- 'dtt_deployment_type': String - Type of Deployment (dtt)
- 'dtt_clientvm_deploy': String - Deployed state of Client VM (dtt)
- 'dtt_clientvm_flavor': String - Flavor of Client VM (dtt)
- 'dtt_ccd_version': String - CCD Version of Deployment (dtt)
- 'dtt_staging_ccd_version': String - Staging CCD Version of Deployment (dtt)
- 'dtt_upgrade_ccd_version': String - Upgrade CCD Version of Deployment (dtt)
- 'dtt_ccd_flavor': String - CCD Flavor of Deployment (dtt)
- 'dtt_network_ggn': String - Deployment GGN Network (dtt)
- 'dtt_vrouter': String - vrouter of Deployment (dtt)
- 'dtt_ip_version': String - IP Version of Deployment (dtt)
- 'dit_project_link': String - Link to Deployment DIT Project (dit)
- 'dit_project': YAML - Contents of Deployment DIT Project Data (dit)

NB: Some of the above vars may not get generated.
    This will occur if the required paramaters are not present on the queried source (dtt/dit).

Example Playbook
----------------
```
    - hosts: localhost
      gather_facts: false
      vars:
        deployment_id: <deployment_id>
      roles:
        - utils_deployment_vars
      tasks:
        - debug:
            msg:
              - "{{ deployment_vip }}"
              - "{{ deployment_pem }}"
              - "{{ deployment_kubeconfig }}"
              - "{{ deployment_env }}"
              - "{{ dtt_deployment }}"
```
```
    - name: Playbook to override utils_deployment_vars 'add_vars' to only generate dtt vars
      hosts: localhost
      gather_facts: false
      vars:
        deployment_id: <deployment_id>
      roles:
        - role: utils_deployment_vars
          vars:
            add_vars:
              - dtt
      tasks:
        - debug:
            msg:
              - "{{ dtt_deployment }}"
```