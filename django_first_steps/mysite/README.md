# Model

Missing functionality:
- [ ] update deployment details
- [ ] during deployment creating assign deployment details
- [ ] base-data terraform params
- [ ] creating new "terraform params" <-> "terraform module" associations
- [ ] creating new "deployment param"

Tables:

- tf_module
  - name
  - path
  - creation_date
  - deletion_date
  - is_useable
- param
  - name
  - description
  - type # bool, string, number, list, touple, map, object, null
- module_params
  - fk:module_id
  - fk:param_id
- deployment
  - fk:module_id
  - name
  - comment
  - apply_date
  - destroy_date
  - username
- deployment_param
  - fk:deployment_id
  - fk:param_id
  - value
