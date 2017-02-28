# How to configure SSH access for your backup server to your Linux servers (hosts).

## 1. Create a SSH key for root on your backup server

Preconditions:
* You are logged in as user "root" in a terminal of your backup server.
Enter:
```bash
ssh-keygen -t rsa -b 4096
```
Leave the password empty! - With this command you generate a public private key pair for logging in via SSH. You only
have to do this once! - If you have already done this step once, please continue with Step 2.


## 2. Allow SSH access for "root" using a password to login to your host.

Preconditions:
* You are able to login as "root" to your host.
* You are logged in as user "root" in a terminal of your host.
Enter:
```bash
sudo sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
```
This changes SSH daemon configuration to allow "root" to login via SSH using a password.
Enter:
```bash
service ssh restart
```
First line is to restart SSH daemon on a system with System V Init.
Second line should only work on systems using Systemd.


## 3. Install SSH key on you host.

Preconditions:
* You are logged in as user "root" in a terminal of your backup server.
Enter:
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub root@<HOST>
```
Replace <HOST> with the host name or IP address of the host you want to backup. 
With this command you install the key on your host which grants root access to your host
to backup servers root user.

## 4. Allow SSH access for "root" using a password to login to your host.

Preconditions:
* You are able to login as "root" to your host.
* You are logged in as user "root" in a terminal of your host.
Enter:
```bash
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
```
This changes SSH daemon configuration back to not allow "root" to login via SSH using a password.
Enter:
```bash
service ssh restart
```
First line is to restart SSH daemon on a system with System V Init.
Second line should only work on systems using Systemd.


Now, if you are logged in as root on your backup server, you should be able to login as root
on your host without having to enter a password.
Preconditions:
- You are logged in as user "root" in a terminal of your backup server.
Enter:
```bash
ssh root@<HOST>
```
Replace <HOST> with the host name or the IP address of the host you want to backup.
You should see no password prompt and instantaneously become root on <HOST>.
