oi_tool_api
===========

Role to use for Querying the OI Tool API. see more info here:
https://confluence-oss.seli.wh.rnd.internal.ericsson.com/pages/viewpage.action?spaceKey=CIE&title=Open+API+Calls

Role Variables
--------------
## optional but set to the following defaults
`method`: GET
`body_format`: form-urlencoded
`return_content`: yes
`validate_certs`: no

## To Filter down for more refined serach, params can be passed to API call.
`oi_params`: Dict - Default( {} ) - Dict of key-value pairs used to search for specific OIs


Results returned
--------------
`oi_api_results`: List [] - List of OI Dict Items


Example Playbooks
----------------
Default usage will query for & return all OIs present.

```
- name: Get All OIs from OI Tool API
  hosts: localhost
  gather_facts: false
  roles:
  - oi_tool_api

  tasks:
  - name: Output the Names of OIs Returned
    debug:
      var: oi_api_results|json_query('[*].name')
    ...
```
```
- name: Query for OIs Containing 'Test' in name field from OI Tool API
  hosts: localhost
  gather_facts: false
  roles:
  - role: oi_tool_api
    vars:
      oi_params:
        name: Test

  tasks:
  - name: Output the Names of OIs Returned
    debug:
      var: oi_api_results|json_query('[*].name')
    ...
```
```
- name: Query for a Particular OI from OI Tool API (Can be a subset of below params. Not all needed)
  hosts: localhost
  gather_facts: false
  roles:
  - role: oi_tool_api
    vars:
      oi_params:
        oiid: OI1022
        portfolio: EO
        lifecycle_type: Forecast
        status_type: Test
        status_state: Complete
        responsible: Flexikube
        availability: LA

  tasks:
  - name: Output the Names of OIs Returned
    debug:
      var: oi_api_results
    ...
```
