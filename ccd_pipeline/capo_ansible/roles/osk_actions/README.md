osk_actions
===========

Role to perform a series of actions against an Openstack of a particular deployment.
The purpose of this role is to centralise the automation against Openstack into one place.
This will help in removing duplication of code/tasks across the repo.

NB: This is just version 1 of this role. There is plenty of room for improvements/expansion.

Role Variables
--------------
- `deployment_id`: String | Required - Example ( ccd-c10a001 )

Each file in this role performs a different action & requires differing vars.
Regardless of action being performed, 'deployment_id' is universally required.
See below:

search_vms.yml
--------------
`vm_pattern`: String | Required - Example ( '.*controlplane.*' )

upload_image.yml
----------------
- `image_name`: String | Required - Example ( 'capo_client_ubuntu_20.04' )
- `image_file`: String | Required - Example ( '/path/to/upload_image/file' )

create_flavor.yml
-----------------
- `flavor_name`: String | Required - Example ( 'flavor_name' )
- `ram`: Required - Example ( 4096 ) # Size in MiB
- `vcpus`: Required - Example ( 2 )
- `disk`: Optional - Example ( 50 ) # Size in GB

create_vm_instance.yml
----------------------
- `instance_name`: String | Required - Example ( 'c10a001_client_vm' )
- `image_name`: String | Required - Example ( 'capo_client_ubuntu_20.04' )
- `flavor_name`: String | Required - Example ( 'client_medium' )
- 'network': String | Required - Example ( 'p0-opstk-10-de-cni-ggn4' )

delete_vm_instance.yml
----------------------
- `instance_name`: String | Required - Example ( 'c10a001_client_vm' )

create_volume.yml
-----------------
- `volume_name`: String | Required - Example ( 'c10a001_client_vm-vol' )
- `volume_size`: Required - Example ( 50 ) # Size in GB

delete_volume.yml
-----------------
- `volume_name`: String | Required - Example ( 'c10a001_client_vm' )

create_security_group.yml
-------------------------
NB: This tasks file requires a build server IP being defined as inventory host.
    One of the tasks runs an OpenStack command from a build server.

- `security_group_name`: String | Required - Example ( 'c10a001_open' )

enable_port_security.yml & disable_port_security.yml
----------------------------------------------------
- `network`: String | Required - Example ( 'p0-opstk-10-de-cni-ggn4' )

Generated Vars
--------------
Vars generated differ for each file. Please see file for var generated

Example Playbooks
-----------------
```
    - name: Playbook to Create Flavor on Openstack
      hosts: localhost
      gather_facts: false
      vars:
        deployment_id: <deployment_id>
      tasks:
        - include_role:
            name: osk_actions
            tasks_from: create_flavor
          vars:
            flavor:
              name: 'some_flavor_name'
              vcpus: 2
              ram: 4096
              disk: 50
              ephemeral: 0

        - debug:
            var: osk_flavor_results
```
```
    - name: Playbook to search Openstack for certain VMs
      hosts: localhost
      gather_facts: false
      vars:
        deployment_id: <deployment_id>
      tasks:
        - include_role:
            name: osk_actions
            tasks_from: search_vms
          vars:
            vm_pattern: ".*{{ deployment_id }}-.*"

        - debug:
            var: osk_vm_results

```