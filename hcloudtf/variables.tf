variable "name" {}
variable "ssh_pubkey_path" {
  default = "~/.ssh/id_ed25519.pub"
}
variable "ssh_pubkey" {
  default = null
}
variable "ipv4_enabled" {
  default = false
}
variable "ipv6_enabled" {
  default = true
}
variable "counter" {
  default = 3
}
variable "server_type" {
  default = "cax11"
}
variable "location" {
  default = "fsn1"
}
variable "network_zone" {
  default = "eu-central"
}
variable "image" {
  default = "debian-12"
}
variable "network_cidr" {
  default = "10.0.0.0/16"
}
variable "subnet_cidr" {
  default = "10.0.0.0/24"
}
variable "load_balancer_type" {
  default = "lb11"
}
