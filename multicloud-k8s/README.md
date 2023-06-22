# How To

## Create Infrastructure

- [x] Terraform Script zum erstellen der Infrastruktur schreiben

## Enable VPN interconnect

- [x] Zwei CAX11 IPv6 only VMs mit Wireguard verdrahten
- [x] Automation zur VPN erzeugung
- [x] DoD: Curl von Server A auf Nginx Server B

## Deploy

- [ ] Zwei CAX11 IPv6 only VMs mit Wireguard automatisch verdrahten
- [ ] Server A mit IPv6 only deployment versehen
- [ ] Server B als node joinen

```sh
terraform -chdir=terraform apply -auto-approve
for i in $(cat inventory.ini | cut -d ' ' -f 1); do ssh -o StrictHostKeyChecking=accept-new "root@${i}" exit >> ~/.ssh/known_hosts; done
ansible-playbook -i inventory.ini ansible/playbook.yml
terraform -chdir=terraform apply -auto-approve -destroy
```

spawn the cluster on wireguard ips, maybe this helps in connectivity
