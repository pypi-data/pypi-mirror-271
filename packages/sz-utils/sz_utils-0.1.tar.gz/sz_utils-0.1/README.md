# sz

## PyPi

```bash
# 安装打包工具
pip install twine setuptools wheel

# 构建包
rm -rf dist build
python setup.py sdist bdist_wheel

# 上传包 
# 设置 $HOME/.pypirc  token
twine upload dist/*


```
