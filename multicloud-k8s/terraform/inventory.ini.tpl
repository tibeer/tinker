%{ for index, ip in hosts ~}
${ip} wireguard_ip=10.100.100.${index}
%{ endfor ~}
