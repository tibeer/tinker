output "ipv6_addresses" {
  value = hcloud_server.node[*].ipv6_address
}
