# Ansible Lint GitLab CI

The [ansible-lint](https://github.com/willthames/ansible-lint) JSON output to GitLab friendly JUnit converter.

### Installation

via pip:

```shell
pip install ansible-lint-gitlab-ci
```

### Updating

via pip:

```shell
pip install ansible-lint-gitlab-ci --upgrade
```

### Usage:

- You can run `ansible-lint -f json` on your playbook(s) and redirect output to pipe
  ```shell
  ansible-lint playbook.yml -f json | ansible-lint-gitlab-ci -o ansible-lint-gitlab-ci.xml
  ```
- You can use a temporary file to store the output of `ansible-lint`.
  After that run `ansible-lint-gitlab-ci` and pass generated file to it
  ```shell
  ansible-lint -f json your_fancy_playbook.yml > ansible-lint.json
  ansible-lint-gitlab-ci ansible-lint.json -o ansible-lint-gitlab-ci.xml
  ```

### Output

- If there are any lint errors, full JUnit XML will be created.
- If there are no errors, empty JSON will be created.

### License

The ansible-lint-gitlab-ci project is distributed under the [MIT] license.