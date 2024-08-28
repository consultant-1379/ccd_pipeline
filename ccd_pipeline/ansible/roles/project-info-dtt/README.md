Role Name
=========

project-info-dtt

This role is used to gather openstack  project related information from DTT. Information is saved in the form of below variables that can be used in other ansible modules like os_stack,os_voume and os_keypairs to provide authentication informaton for openstack project. This role returns below variable 

    # proj_username  it privides project username
    # proj_password  it provides project password
    # proj_name      it provides project name
    # proj_uuid      it provides project uuid
    # cloud_auth_url it provides required clouds' authentication url


N/A

Role Variables
--------------
Role defines two default variables
dtt_url: http://atvdtt.athtem.eei.ericsson.se
dit_url: http://atvdit.athtem.eei.ericsson.se
user_domain: default
proj_domain: default

Dependencies
------------

Role needs variable deployment_id that is supplied through playbook that uses this role e.g deployment_id=ccd-c10a001
Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         -  role: project-info-dtt


Author Information
------------------
DE-CNI
