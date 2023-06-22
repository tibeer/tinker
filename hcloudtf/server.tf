resource "hcloud_server" "node" {
  count = var.counter

  name        = "${var.name}-${count.index}"
  image       = var.image
  location    = var.location
  ssh_keys    = [var.ssh_pubkey == null ? hcloud_ssh_key.key[0].name : var.ssh_pubkey]
  server_type = var.server_type

  network {
    network_id = hcloud_network_subnet.subnet.network_id
    alias_ips  = []
  }

  public_net {
    ipv4_enabled = var.ipv4_enabled
    ipv6_enabled = var.ipv6_enabled
  }
}
