#!/bin/bash
ssh ubuntu@oracle.tibeer.de
sudo dhclient -6
sudo swapoff -a
sudo apt-get update
sudo apt-get install -y runc containerd apt-transport-https ca-certificates curl
sudo curl -fsSLo /etc/apt/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [trusted=true signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
net.ipv6.conf.all.forwarding        = 1
net.ipv6.conf.default.forwarding    = 1
EOF
sudo sysctl --system
lsmod | grep br_netfilter
lsmod | grep overlay
sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward net.ipv6.conf.all.forwarding net.ipv6.conf.default.forwarding
sudo mkdir -p /etc/containerd/
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo systemctl restart containerd
sleep 1
#sudo kubeadm init --apiserver-advertise-address 130.61.147.11 --control-plane-endpoint 130.61.147.11 --pod-network-cidr 192.168.0.0/16
sudo kubeadm init --control-plane-endpoint 2603:c020:800e:4c00:3d96:5fca:55ae:e2b1 --pod-network-cidr 192.168.0.0/16
sudo systemctl restart containerd
sudo systemctl restart kubelet
logout
ssh ubuntu@oracle.tibeer.de sudo cat /etc/kubernetes/admin.conf > /Users/columbia/.kube/oracle.yaml
ctx kubernetes-admin@kubernetes
helm install calico projectcalico/tigera-operator --namespace tigera-operator --create-namespace
# unfortunately required for some strange reason
ssh ubuntu@oracle.tibeer.de sudo systemctl restart containerd
ssh ubuntu@oracle.tibeer.de sudo systemctl restart kubelet
kubectl taint nodes free-0 node-role.kubernetes.io/control-plane:NoSchedule-
helm install metallb metallb/metallb --namespace metallb-system --create-namespace --set speaker.frr.enabled=false
kubectl apply -f metallb-config.yaml
helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
helm install foo tibeer/default-helmchart --set ingress.host="test.oracle.tibeer.de"
helm install longhorn longhorn/longhorn \
  --create-namespace --namespace longhorn-system \
  --set persistence.defaultClassReplicaCount=1 \
  --set defaultSettings.replicaSoftAntiAffinity=true \
  --set ingress.enabled=true \
  --set ingress.host=oracle.tibeer.de
#sudo kubeadm reset --cleanup-tmp-dir --force && sudo rm -rf /etc/cni/net.d