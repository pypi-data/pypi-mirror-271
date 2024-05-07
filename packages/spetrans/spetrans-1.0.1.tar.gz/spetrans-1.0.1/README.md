# Spetrans

Spetrans 是一个使用 LLM 以识别植物标本图像中的标签信息，并返回 DWC 标准数据的库。

## 安装

```bash
pip install spetrans
```

## 使用方法

```python
from spetrans import Spetrans

spetrans = Spetrans()
spetrans.set_api_key("your api key")
spetrans.set_base_url("your base url")
label_data = spetrans.get_label_data("./test_images/02432001.jpg")
print(label_data)
```

## 许可证

[MIT License](https://opensource.org/licenses/MIT)
