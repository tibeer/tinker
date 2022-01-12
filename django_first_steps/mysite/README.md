# Timon

Missing functionality:

- [ ] terraform wrapper - terraform pieces
- [x] provider selection
  - [x] secrets
- [x] prevent duplicate module-params
- [x] recheck datatype validation
- [ ] s3 for state
  - [ ] states should never be deleted, even after successul deployment
  - [ ] s3-versioning will be required
- [ ] tf-modules should work via git
  - [ ] remote-backend will be dynamic
    - [ ] execution environment
  - [ ] py-git
  - [ ] never do checkouts (maybe inside the container later)
  - [ ] Django should trigger a container build when a deployment is created. this container is an exact replication of this deployment (including terraform binary, git code, ansible, etc.)
  - [ ] TF_VAR_secret
- [ ] no scaling of deployments at first (later for sure)
- [ ] integrations
  - [ ] terraform should be implemented in a way, that it can be replaced
  - [ ] ansible, etc., shall not be triggered via terraform
  - [ ] outputs shall be read/used from the S3 state
  - [ ] user management is something for v2
