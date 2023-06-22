resource "hcloud_ssh_key" "key" {
  name       = var.name
  public_key = file(pathexpand(var.ssh_pubkey_path))
}

resource "hcloud_server" "node" {
  count = var.counter

  name        = "${var.name}-${count.index}"
  image       = var.image
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.key.name]
  server_type = var.flavor

  public_net {
    ipv4_enabled = var.ipv4_enabled
    ipv6_enabled = var.ipv6_enabled
  }
}
