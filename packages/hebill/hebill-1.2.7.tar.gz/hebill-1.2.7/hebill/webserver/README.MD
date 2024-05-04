# hebill.webserver

## 应用
快速布置服务器

## 示例
```python
# 你的处理类 
import hebill


class MyHandle(hebill.webserver.Handle):
    def response(self) -> str:
        doc = hebill.html.Document()

        def output_parameters(parameters: dict):
            table = doc.html.body.create.component.table()
            if len(parameters) > 0:
                for ki, vi in parameters.items():
                    row = table.body.add_row()
                    row.add_cell(ki)
                    row.add_cell(vi)

        output_parameters(self.requests.cookies)
        output_parameters(self.requests.gets)
        output_parameters(self.requests.posts)
        output_parameters(self.requests.headers)
        return doc.output()


```
```python
# 开始运行服务器 
import hebill


if __name__ == '__main__':
    app = hebill.webserver.WebServer('', 1080, MyHandle)
    app.start()
```
## 示例获取当前客户端连接参数
```python
# 开始运行服务器 
import hebill


if __name__ == '__main__':
    app = hebill.webserver.WebServer('', 1080, hebill.webserver.HandleInfo)
    app.start()
```