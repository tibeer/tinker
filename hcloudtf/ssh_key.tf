resource "hcloud_ssh_key" "key" {
  count = var.ssh_pubkey == null ? 1 : 0

  name       = var.name
  public_key = file(pathexpand(var.ssh_pubkey_path))
}
