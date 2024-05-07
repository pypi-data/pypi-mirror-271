## 说明
快速打包上传到项目到 pypi.org。  
模块在WIN系统pyCharm中测试，不做其他环境使用。

## 设置 .pypi
在你的/~user/里面创建 .pypi，用记事本编辑以下内容并保存
```text
[pypi]
username = your pypi username
password = pypi-(Your pypi key)
```

## 步骤
1. 目录结构格式：  
    ```text
    /source_root  
     -- /myProject  
     -- /myProject/__init__.py  
     -- /myProject/constants.py  
     -- /myProject/core.py  
     -- pypi.py  
     -- README.MD  
     -- requirements.txt
    ```
2. 在constants.py中设定常量   
    ```python
    VERSION = '1.0.0'
    NAME = 'myProject'
    DESCRIPTION = 'Project Description'
    LONG_DESCRIPTION = 'README.MD'
    LONG_DESCRIPTION_TYPE = 'text/markdown'
    URL = 'http://www.project.url/'
    AUTHOR = 'Your Name'
    AUTHOR_EMAIL = 'email@project.url'
    AUTHOR_URL = 'http://www.project.url/'
    ```
   
3. 在__init__.py中加载
    ```python
    from .core import MyModule
    from .constants import *
    ```
4. 编写 pypi.py 内容
   ```python
   from hebill_pypi import Pypi
   import myProject
   
   pypi = Pypi(myProject, r'D:\SDK\Environments\myProject\Scripts\python.exe')
   pypi.pack()
   ```

5. 运行 pypi.py
