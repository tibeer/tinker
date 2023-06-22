resource "local_file" "ansible_inventory" {
  content = templatefile("inventory.ini.tpl",
    {
      hosts = hcloud_server.node[*].ipv6_address
    }
  )
  filename = "../inventory.ini"
}
