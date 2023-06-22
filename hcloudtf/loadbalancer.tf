resource "hcloud_load_balancer" "load_balancer" {
  name               = var.name
  load_balancer_type = var.load_balancer_type
  location           = var.location
}

resource "hcloud_load_balancer_target" "load_balancer_target" {
  count = length(hcloud_server.node[*])

  type             = "server"
  load_balancer_id = hcloud_load_balancer.load_balancer.id
  server_id        = element(hcloud_server.node[*].id, count.index)
  use_private_ip   = true
}

resource "hcloud_load_balancer_network" "load_balancer_network" {
  load_balancer_id = hcloud_load_balancer.load_balancer.id
  network_id       = hcloud_network_subnet.subnet.network_id
}

resource "hcloud_load_balancer_service" "load_balancer_service" {
    load_balancer_id = hcloud_load_balancer.load_balancer.id
    protocol         = "http"
}
