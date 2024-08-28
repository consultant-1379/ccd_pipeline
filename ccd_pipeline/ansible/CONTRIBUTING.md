## General rules to contribute ccd pipeline

* No underscores in filenames. Use hyphen instead.
* YAML files should end in the file extension .yml in GIT repo and in MinIO
* All playbook should pass the ansible lint and comply to the [**design rules**](https://ansible-lint.readthedocs.io/en/latest/default_rules.html)
   You can choose to skip certain design rule checks.
   These  exceptions are defined  in "./ccd_pipeline/anisble/.ansible_lint" file.
   Currently the following is skipped:
   - tasks with the tag "skip_ansible_lint"
   - Design rule 204 , "Lines should be no longer than 160 chars"
   - Design rule 701, "meta/main.yml should contain relevant info"

* Before pushing your codes to master, check if you have followed [**code review rules**](https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/CIE/DE-CNI+Code+Review)
* Update README.md to describe how to use your playbook
* No passwords should be stored in GIT repo. Store node credentails in MinIO.
* Playbooks should reuse the existing roles as much as possible. Current avaialable roles should be found on [**DE-CNI Gerrit Repo**](https://gerrit.ericsson.se/plugins/gitiles/OSS/com.ericsson.de.cni/ccd_pipeline/+/refs/heads/master/ansible/roles)
