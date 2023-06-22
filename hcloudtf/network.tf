resource "hcloud_network" "network" {
  name     = var.name
  ip_range = var.network_cidr
}

resource "hcloud_network_subnet" "subnet" {
  type         = "cloud"
  network_id   = hcloud_network.network.id
  network_zone = var.network_zone
  ip_range     = var.subnet_cidr
}
