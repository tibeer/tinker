output "public_node_ipv4_addresses" {
  value = [
    for public_ip in hcloud_server.node[*]:
      public_ip.ipv4_address if public_ip.ipv4_address != "<nil>"
  ]
}

output "public_node_ipv6_addresses" {
  value = [
    for public_ip in hcloud_server.node[*]:
      public_ip.ipv6_address if public_ip.ipv6_address != "<nil>"
  ]
}

output "private_node_ipv4_addresses" {
  value = [
    for private_ip in hcloud_server.node[*].network:
      one(private_ip).ip
  ]
}

output "public_lb_ipv4_address" {
  value = hcloud_load_balancer.load_balancer.ipv4
}

output "public_lb_ipv6_address" {
  value = hcloud_load_balancer.load_balancer.ipv6
}
