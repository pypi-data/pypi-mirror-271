# sz

## PyPi

```bash
# 安装打包工具
pip install twine setuptools wheel

# 构建包 
# 修改 setup.py 中的 version
rm -rf dist build *egg-info
python setup.py sdist bdist_wheel

# 上传包 
# 设置 $HOME/.pypirc  token
twine upload dist/*

# 导入
from sz1 import sz_utils

```
