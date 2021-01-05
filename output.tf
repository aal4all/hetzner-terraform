output "servers_status" {
  value = {
    for server in hcloud_server.buildserver :
    server.name => server.status
  }
}

output "servers_ips" {
  value = {
    for server in hcloud_server.buildserver :
    server.name => server.ipv4_address
  }
}
