resource "hcloud_ssh_key" "default" {
  name       = "Falko"
  public_key = file("~/.ssh/id_rsa.pub")
  #fingerprint = "PASTE_ADDED_SSH_KEY_FINGERPRINT_HERE"
}
