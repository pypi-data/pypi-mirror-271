# supabase-utils

A collection of framework specific utilities for working with Supabase.

## Installation

```sh
pip supabase-utils
```

## Usage

```python
from sb_utils import sb_table


accounts = sb_table("accounts").select("id, title, created_by(username)", count="exact")

for account in accounts.data:
  print(account.get("title"))
```


```python
from pydantic import BaseModel
from sb_utils import BaseService


class User(BaseModel):
    __tablename__ = "users"

    id: Optional[str] = Field(default=None, primary_key=True)
    username: str


class Account(BaseModel):
    __tablename__ = "accounts"

    id: Optional[str] = Field(default=None, primary_key=True)
    title: str
    created_by: User = Field(related_name="username")


class AccountService(BaseService):
    model = Account


accounts = AccountService.all()

for account in accounts:
  print(account.title)
```




## Documentation


## Community


## License


