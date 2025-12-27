# red

Run the playbook:

```bash
ansible-playbook -i inventories/localhost.ini playbooks/pi-trixie.yml
```

SMB password (Ansible Vault):
1) Create the vault file:
```bash
ansible-vault create inventories/group_vars/all/vault.yml
```
2) Add:
```yaml
smb_password: "YOUR_PASSWORD"
```
3) Run with:
```bash
ansible-playbook -i inventories/localhost.ini playbooks/pi-trixie.yml --ask-vault-pass
```
