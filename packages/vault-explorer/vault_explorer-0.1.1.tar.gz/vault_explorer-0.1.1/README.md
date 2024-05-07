# vault-explorer

A module to recursively retrieve values from HashiCorp Vault KV store and apply functions on them.

## Usage

```python
def main():
    vault_url = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")
    
    client = hvac.Client(
        url=vault_url,
        token=vault_token
    )
    
    client.secrets.kv.v2.configure(
        mount_point = "secrets"
    )
    
    explorer = VaultExplorer(client, flattenJson=True)
    explorer.apply("/", lambda path, secret: print(path, str(secret)))
```