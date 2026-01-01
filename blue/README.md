# blue

Run the playbook:

```bash
ansible-playbook -i inventories/localhost.ini playbooks/pi-trixie.yml
```

Cloudflare API token (Ansible Vault):
1) Create the vault file:
```bash
ansible-vault create inventories/group_vars/all/vault.yml
```
2) Add:
```yaml
caddy_cloudflare_api_token: "YOUR_TOKEN"
```
3) Run with:
```bash
ansible-playbook -i inventories/localhost.ini playbooks/pi-trixie.yml --ask-vault-pass
```
