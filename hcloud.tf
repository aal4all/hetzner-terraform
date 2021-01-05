# Set the variable value in *.tfvars file
# or using the -var="hcloud_token=..." CLI option
variable "hcloud_token" {}

# Configure the Hetzner Cloud Provider
provider "hcloud" {
  token = var.hcloud_token
}

# Create a server
resource "hcloud_server" "buildserver" {
  count       = var.instances
  name = "buildserver-${count.index}"
  image = var.os_type
  server_type = var.server_type
  location = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]
  user_data = file("user_data.yml")
  
  provisioner "file" {
    source      = "specfiles/crmsh.spec"
    destination = "/home/falko/crmsh.spec"
    connection {
      type     = "ssh"
      host     = self.ipv4_address
      user     = "falko"
      private_key = file("~/.ssh/id_rsa")
      #timeout = "60s"
    }
  }
  provisioner "file" {
    source      = "specfiles/python-parallax.spec"
    destination = "/home/falko/python-parallax.spec"
    connection {
      type     = "ssh"
      host     = self.ipv4_address
      user     = "falko"
      private_key = file("~/.ssh/id_rsa")
      #timeout = "60s"
    }
  }
  provisioner "remote-exec" {
    inline = [
      "while [ ! -f /usr/bin/rpmdev-setuptree ] ; do sleep 2 ; done",
      "/usr/bin/rpmdev-setuptree",
    ]
  }
  connection {
      type     = "ssh"
      host     = self.ipv4_address
      user     = "falko"
      private_key = file("~/.ssh/id_rsa")
      #timeout = "60s"
    }
}
