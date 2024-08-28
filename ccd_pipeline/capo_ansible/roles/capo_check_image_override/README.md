capo_check_image_override
=========================

Role to fetch and return the image version & arm url of a CAPO Build image.
This role allows the functionality to override default playbook/pipeline image url functionality without having to change/update any code.
This will be advantageous in a case where the location of a CAPO Build Image is different from the playbook/pipeline default or we want to specify exact Build Releases for pipeline runs.

Role Pre-Requisites
-------------------
File 'image_overrides.yml' needs to be present on MinIO in bucket /de-cni/capo_image_override/.
See below for file content:
```
---------image_overrides.yml----------

staging:
  state: Active
  image_version:
  image_url:
predrop_fastfeedback:
  state: Active
  image_version:
  image_url:
pra_fastfeedback:
  state: Active
  image_version:
  image_url:
prg_fastfeedback:
  state: Active
  image_version:
  image_url:

-----------------EOF------------------
```

To use this role, the 'image_version' & 'image_url' vars for the specific override item need to be populated.

NB: var 'state' MUST be set to 'Active'. If any other value set, then override will NOT occur.

Example:
```
staging:
  state: Active
  image_version: 2.27.0-001443-7bbf977f
  image_url: https://location/of/image.tgz
```
Once Override done, The role will trigger the updating of the specific 'state' updating it to 'Done' & upload to minio.

Role Variables
--------------
- 'capo_image_override':
    - String | Required
    - Name of image to override - Example ( staging )
    - Used to reference the specific item from image_overrides.yml dict

Generated Vars
--------------
- 'image_version': String - CAPO Build version (2.27.0-001354-13a570c4)
- 'image_url': String - URI to Image (https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-erikube-generic-local/erikube/capo/swPackage/2.27.0-001354-13a570c4//2.29.0-001354-13a570c4.tgz)

NB: These vars are only generated if they are present in the MINIO 'image_overrides.yml' specified.
    If 'image_overrides.yml' content/vars are empty, then no vars will be generated.

Example Playbook
----------------
```
- hosts: localhost
  gather_facts: false
  roles:
    - role: capo_check_image_override
      vars:
        override_file: staging
  tasks:
    - name: Block for when no Override Specified
      when:
        - image_url is not defined
        - image_version is not defined
      block:
        - name: Tasks To fetch/set image_url & image_version another way
          some_task:
            ...
            ..
            .
    - name: Download Image
      ...
      ..
      .
```