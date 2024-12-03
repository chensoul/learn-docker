# 使用 3.9 版本的 python
FROM python:3.13

# docker 中，此项目的运行地址为 /code 
WORKDIR /code

# 拷贝本地的 requirements.txt 文件到地址：/code/requirements.txt 
COPY ./requirements.txt /code/requirements.txt

# 根据 requirements 文件安装 python 第三方包
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 拷贝 app 文件夹的内容到 /code/app
COPY ./app /code/app

# 执行命令，启用 fastapi 应用
CMD ["uvicorn", "app.feishu:app", "--host", "0.0.0.0", "--port", "3080"]


