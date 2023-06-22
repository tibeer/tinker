variable "name" {}
variable "counter" {}
variable "flavor" {
  default = "cax11"
}
variable "image" {
  default = "debian-11"
}
variable "location" {
  default = "fsn1"
}
variable "ssh_pubkey_path" {
  default = "~/.ssh/id_ed25519.pub"
}
variable "ipv4_enabled" {
  default = false
}
variable "ipv6_enabled" {
  default = true
}
