# mmo_tools
Đây là một thư viện Python chứa các hàm tiện ích để chuyển đổi dữ liệu và cấu hình proxy .

## funciton

### `convert_data`
- Chuyển đổi dữ liệu từ tệp đầu vào thành danh sách các đối tượng từ điển.
- **input**: path file input (str).
- **result**: dict (`[{},{}`]).
### `headers`
- return dict facebook headers 

### `checklive`
- return status account facebook uid
- **input** : user-id facebook account
- **result** : + status live : 1 
               + status die  : 0

## example
```python
import os , sys
from mmo_tools import *
# Giả sử file_path là đường dẫn tới tệp dữ liệu
file_path = 'data/mmo_tools.txt'
def func1():
    # Chuyển đổi dữ liệu từ tệp
    data = convert_data(file_path)

    print(data)  # [{'key': 'value'}, {'key2': 'value2'}]

def func2():
    headers = headers()
    print(headers) # {'user-agent':'my user-agent','accept':'*/*'...}

def funcc():
    status = checlive(506356883)
    print(status) # result : 0 

```
## install
```bash
pip install mmo_tools

```
## update new version
``` update
pip install --upgrade mmo_tools
```
# contact
-  Youtube : [ilam](https://www.youtube.com/@iam_dlam)
- Facebbok : [Le Dinh Lam](https://www.facebook.com/IT.Admin.InF/)
- Telegram : [Lam](https://t.me/im_dlam)