utils_jira_actions
=====================

Role to perform different actions against JIRA.
Actions currently availeble in Role:
- Create Issue (create.yml)
- Comment on an Issue (comment.yml)
- Attach File to an Issue (attach_file.yml)
- Close an Issue (close.yml)
- Delete an Issue (delete.yml)

NB: This is just a very basic version 1 of this role. Can be further developed/improved in the future.

Role Variables
--------------
All variables have default values that can be overridden when included in playbook

- 'project': String - Default ( CIS )
- 'issue_type': String - Default ( Support )
- 'priority': String - Default ( Minor )
- 'pdg_area': String - Default ( DE )
- 'sub_area_team': String - Default ( DE-CNI )
- 'site_location': String - Default ( Athlone )
- 'components': List of Dicts - Default ( [{name: DE-CloudNative}] )
- 'summary': String - Default (Ansible Generated JIRA)
- 'description': String - Default (This is a Dummy JIRA created by ansible)
- 'comment': String - Default (This is a Dummy comment created by ansible)


Required Variables
------------------
Each file in this role performs a different action & requires differing vars.
See below:

- 'jira_ticket' - Example('CIS-123456') - Required in comment.yml, attach_file.yml, close.yml, delete.yml
- 'attachment' - Example('/path/to/file') - Required in attach_file.yml

Variables returned
--------------
- 'jira_create_result' - returned from create.yml
- 'jira_comment_result' - returned from comment.yml
- 'jira_attach_result' - returned from attach_file.yml
- 'jira_close_result' - returned from close.yml
- 'jira_delete_result' - returned from delete.yml


Example Playbooks
----------------

```
- name: Create, Comment, Attach & Close a JIRA
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create JIRA
      include_role:
        name: utils_jira_actions
        tasks_from: create
      vars:
        summary: Jira to do something
        description: Description of something to be done

    - debug:
        var: jira_create_result

    - include_role:
        name: utils_jira_actions
        tasks_from: comment
      vars:
        jira_ticket: "{{ jira_create_result.key }}"
        comment: |
          That thing you wanted done
          is now done!
          Cheers!

    - include_role:
        name: utils_jira_actions
        tasks_from: attach_file
      vars:
        attachment: /path/to/file
        jira_ticket: "{{ jira_create_result.key }}"

    - include_role:
        name: utils_jira_actions
        tasks_from: close
      vars:
        jira_ticket: "{{ jira_create_result.key }}"


```