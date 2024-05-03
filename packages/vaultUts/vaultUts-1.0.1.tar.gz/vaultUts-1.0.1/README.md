# Vault Uts
#
### Installation

```sh
pip install vaultUts
```

### Usage
#
#### link
```py
from vaultUts import VaultLib

vlt = VaultLib(
    "<HOST>",
    "<TOKEN>"
    )

@vlt.link("<MyLocker>/data/<MySecret>")
class MySecret(): 
    USER    : str
    PASSWORD: str

print(MySecret.USER)
print(MySecret.PASSWORD)
```
```py
my_user_here
py_password
```
