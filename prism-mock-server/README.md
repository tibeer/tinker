# Prism getting started

```sh
podman run --init --rm \
  -v $(pwd)/api.yaml:/tmp/api.yaml:ro \
  -p 4010:4010 \
  stoplight/prism:4 \
  mock -h 0.0.0.0 \
  "/tmp/api.yaml"
```
