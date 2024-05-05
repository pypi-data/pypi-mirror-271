# mmo_tools
©dinhlam
Đây là một thư viện Python chứa các hàm tiện ích để chuyển đổi dữ liệu và cấu hình proxy .

## func

### `convert_data(file)`
- Chuyển đổi dữ liệu từ tệp đầu vào thành danh sách các đối tượng từ điển.
- **input**: path file input (str).
- **result**: dict (`[{},{}`]).

#### example
```python
import os , sys
from lam_tools import convert_data

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
# Giả sử file_path là đường dẫn tới tệp dữ liệu
file_path = 'data/mmo_tools.txt'

# Chuyển đổi dữ liệu từ tệp
data = convert_data(file_path)

print(data)  # [{'key': 'value'}, {'key2': 'value2'}]

```
## install
```bash
pip install mmo_tools

```
# contact
-  Youtube : [ilam](https://www.youtube.com/@iam_dlam)
- Facebbok : [Le Dinh Lam](https://www.facebook.com/IT.Admin.InF/)
- Telegram : [Lam](https://t.me/im_dlam)