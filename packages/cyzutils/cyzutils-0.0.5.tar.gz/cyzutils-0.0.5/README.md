### Install

```bash
pip install cyzutils
```

### Usage

Send email

```python
# mail
from cyzutils import send_mail
send_mail('subject', 'content', 'xxxxxxx@xxx.xx')
send_mail('subject', 'content') # send to myself
```

---

Run python file with cmd

Each command line parameter needs to be given as a list or a specific value

No limit on the number of command line parameters

```python
# run python cmd
from cyzutils import run_py
run_py(fail_path, arg1_name=arg1_list, arg2_name=arg2_list)
# eg.
file_path = 'test/test.py'
test1 = [1, 2]
test2 = [3, 4]
test3 = [5, 6]
run_py(file_path, arg1=test1, arg2=test2, arg3=test3)
```

### 打包上传 pypi 命令

```shell
pip install build

python -m build

pip install twine

twine check dist/*

twine upload dist/*
```

https://juejin.cn/post/7053009657371033630