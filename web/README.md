# 教程
https://blog.csdn.net/u011054333/article/details/70151857
# 使用
- 安装falsk： pip install flask
- 将静态文件放到static目录
- 启动：执行app.py文件即可
```python
 python app.py
```
- 访问：
    - 静态文件:localhost:8000/static/index.html
    - 数据接口:localhost:8000/{PATH} (see @app.route('{PATH}')) 
        - 例如：http://localhost:5000/calEnergy?jindu=1&weidu=2