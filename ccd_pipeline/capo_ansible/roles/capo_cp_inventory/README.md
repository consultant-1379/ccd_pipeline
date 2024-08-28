capo_cp_inventory
=================

Role to prepare and get CAPO deployment controlplane inventory by adding controlplane nodes to Ansible host group(s). Currently the nodes are discovered from the specific deployments' openstack, or the controlplane vip depending on role usage.

NB: This is just version 1 of this role. There is plenty of room for improvements/expansion if needed.
Possible Improvement: Add worker nodes as an inventory group.


Role Variables
--------------
- `deployment_id`: String | Required - Example ( ccd-c10a001 )
- `add_group`: list[] - Default( [ vip_node ] )

Host groups available:
--------------
  - `vip_node`: Used for running kubectl or helm commands on a deployment. Adds the controlplane accessed by the vip.
  - `cp_nodes`: Includes all deployment controlplane nodes.


Example Playbooks
----------------
Default usage will add vip_node group which can be used to run kubectl or helm commands on a deployment.

Just add the role to the play directly to get vip node.

```
    - hosts: localhost
      gather_facts: false
      vars:
        deployment_id: <deployment_id>
      roles:
        - capo_cp_inventory

    - hosts: vip_node
      gather_facts: false
      tasks:
        ...
```

Example overriding the `add_group` var which is a list of host group names.

```
    - hosts: localhost
      gather_facts: false
      vars:
        deployment_id: <deployment_id>
      roles:
        - role: capo_cp_inventory
          vars:
            add_groups:
              - cp_nodes

    # Play on all controlplane nodes
    - hosts: cp_nodes
      tasks:
        ...
```