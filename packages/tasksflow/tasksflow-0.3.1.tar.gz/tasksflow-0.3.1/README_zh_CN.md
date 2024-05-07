# tasksflow

> 通过 tasks 处理复杂流程

[English](./README.md) | 简体中文

在处理复杂流程时，我们通常需要将流程分解为多个任务，然后将这些任务组合在一起。这个库提供了一种简单的方法来定义和执行这些任务。

## 快速开始

安装 tasksflow

```bash
pip install tasksflow
```

创建一些简单的任务

```python
import tasksflow.pool
import tasksflow.task
import tasksflow.cache
import tasksflow.executer
from pathlib import Path

class Task1(tasksflow.task.Task):
    def run(self):
        return {"a": 1, "b": 2}


class Task2(tasksflow.task.Task):
    def run(self, a: int, b: int):
        return {"c": a + b}

tasks = [Task1(), Task2()]
p = tasksflow.pool.Pool(tasks)
result = p.run() # run tasks in pool
print(result) # {"a": 1, "b": 2, "c": 3}
```
## 使用

### Task

每个任务都具有多个输入参数和多个输出参数。以 Task2 为例

```python
class Task2(tasksflow.task.Task):
    def run(self, a: int, b: int):
        return {"c": a + b}
```

Task2 的输入参数为 `a` 和 `b`，输出参数为 `c`。

每个任务需要继承 `tasksflow.task.Task`，并重写 `run` 方法。`run` 方法的参数即为此任务需要的输入，返回值应为 None 或 参数->值 的 dict，并请确保每个任务返回的参数不重复。

不需要显式定义任务之间的依赖关系。前序任务返回参数对应的值以后，会自动使用此值调用依赖这些参数的后置任务。

### Pool

`tasksflow.pool.Pool` 是任务池，用于一系列任务的运行。常见用法为

```python
tasks = [Task1(), Task2()]
p = tasksflow.pool.Pool(tasks)
result = p.run() # run tasks in pool
```

使用 `tasksflow.pool.Pool(tasks)` 初始化交易池，通过 `result = p.run()` 执行任务列表并获取结果，结果的类型为所有任务 参数->值 的 dict。

## 高级

### cache

对于大多数任务来说，只要输入参数和任务代码相同，最后的输出结果也是相同的。默认情况下，`tasksflow` 会对任务的代码和输入、输出进行缓存，当再次运行任务且命中缓存时，会跳过执行过程并直接使用输出。缓存功能可以有效提升开发效率，当开发者进行后续任务开发时，不再需要实际运行前置任务。

#### 禁用任务缓存

部分任务依赖网络、时间等外部因素，即使输入参数和任务代码相同也会输出不同的结果，此时可能需要禁用缓存，强制执行任务。可以在任务初始化时声明禁用缓存。

```python
tasks = [Task1(), Task2(enable_cache = False)]
```

其中 Task2 传入了 `enable_cache = False`，将不再自动进行缓存。

#### 缓存实现

`pool` 默认会在 `cache.db` 创建 Sqlite 数据库并缓存任务代码和输入。如果要自定义储存路径，可以

```python
from pathlib import Path
p = tasksflow.pool.Pool(tasks, cache_provider=tasksflow.cache.SqliteCacheProvider(Path("mycache.db")))
```

也可以使用 `MemoryCacheProvider` 代替 `SqliteCacheProvider`，将缓存保存在内存中，常用于测试。

```python
p = tasksflow.pool.Pool(tasks, cache_provider=tasksflow.cache.MemoryCacheProvider())
```

或者自定义 `CacheProvider`，继承 `tasksflow.cache.CacheProvider` 并实现 `get` 和 `set` 方法。然后将自定义的 `CacheProvider` 传入 `Pool`。

### executer

`pool` 默认使用 `tasksflow.executer.MultiprocessExecuter`，即为每个任务创建单独的进程。当一个任务被完成后，会根据此任务的输出，自动调用依赖此任务的后置任务。

也可以使用 `tasksflow.executer.SerialExecuter`，按照 tasks 的顺序依次执行任务。

```python
p = tasksflow.pool.Pool(tasks, executer=tasksflow.executer.SerialExecuter())
```

也可以自定义执行器

```python
from typing import Any
class MyExecuter(Executer):
    def run(tasks: list[tasksflow.task.Task]) -> dict[str, Any]:
        pass
p = tasksflow.pool.Pool(tasks, executer=MyExecuter())
```

### 日志

`tasksflow` 使用 `loguru` 模块打印日志，可以通过以下代码设置是否打印 `tasksflow` 的日志。默认情况下，`tasksflow` 的日志是关闭的。

```python
# install loguru by `pip install loguru`

from loguru import logger
logger.enable("tasksflow")
```

## 更真实的例子

爬取 <https://webscraper.io/test-sites> 网站的标题。使用 `tasksflow` 将爬取任务分解为 2 个子任务：网页请求、网页解析，从而实现开发 网页解析 子任务时，利用缓存避免了再次请求网页。

安装依赖

```sh
pip install tasksflow requests lxml
```

编写代码

```python
import tasksflow.pool
import tasksflow.task
from lxml import etree
import requests


class TaskRequest(tasksflow.task.Task):
    def run(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        url = "https://webscraper.io/test-sites"
        resp = requests.get(url, headers=headers).text
        return {"resp": resp}


class TaskParse(tasksflow.task.Task):
    def run(self, resp: str):
        html = etree.HTML(resp, etree.HTMLParser())
        title_elements = html.xpath("/html/body/div[1]/div[3]/div[*]/div[1]/h2/a")
        titles = [title.text.strip() for title in title_elements]
        return {"titles": titles}


def main():
    tasks = [TaskRequest(), TaskParse()]
    p = tasksflow.pool.Pool(tasks)
    result = p.run()
    print(f"titles: {result['titles']}")
    # titles: ['E-commerce site', 'E-commerce site with pagination links', 'E-commerce site with AJAX pagination links', 'E-commerce site with "Load more" buttons', 'E-commerce site that loads items while scrolling', 'Table playground']


if __name__ == "__main__":
    main()
```

## 开发

见 [dev_zh_CN.md](./docs/dev_zh_CN.md)
