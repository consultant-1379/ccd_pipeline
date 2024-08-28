capo_upgrade
============

Role to perform a CAPO Upgrade against an existing deployment.
Using the Required Vars, This Role will Execute the Upgrade Procedure Steps.
These Steps are Executed using Required Var 'upgrade_image_bin'.

NB: To perform CAPO Upgrade, the Deployment Config Files must be located
    in the current deployed Image Version ( 'deployed_image_path' ) on the CAPO Build Server.

Role Variables
--------------
- 'deployment_id': String | Required - Example ( ccd-c10a001 )
- 'deployed_image_path': String | Required - Example ( /ccd/IMAGES/capo-2.26.0-000393-fc474230 )
- 'upgrade_image_path': String | Required - Example ( /ccd/IMAGES/capo-2.27.0-001354-13a570c4 )
- 'upgrade_image_bin': String | Required - Example ( /ccd/IMAGES/capo-2.27.0-001354-13a570c4/bin/ccdadm )

Example Playbook
----------------
```
    - hosts: localhost
      gather_facts: false
      vars:
        deployment_id: <deployment_id>
      roles:
        - role: add_buildserver_host
          vars:
            use_upgrade_build_server: true
      tasks:
        - name: Perform CAPO Upgrade
          include_role:
            name: capo_upgrade
            apply:
              delegate_to: "{{ build_server_ip }}"
          vars:
            deployed_image_path: /ccd/IMAGES/capo-2.26.0-000393-fc474230
            upgrade_image_path: /ccd/IMAGES/capo-2.27.0-001354-13a570c4
            upgrade_image_bin: /ccd/IMAGES/capo-2.27.0-001354-13a570c4/bin/ccdadm
```