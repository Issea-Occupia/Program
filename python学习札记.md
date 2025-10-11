<div style="text-align : center;font-size : 40px;font-weight : 700">python学习札记(=ↀωↀ=)✧</div>

<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/2c077d928bca20e80a746ded59918443.jpg" style="width:300px; border-radius:20px;">

## 1 sys.argv的应用。

<div style = "font-size : 25px;font-weight : 700">以下官方文档的解释：</div>

>The list of command line arguments passed to a Python script. `argv[0]` is the script name (it is operating system dependent whether this is a full pathname or not). If the command was executed using the [`-c`](https://docs.python.org/3/using/cmdline.html#cmdoption-c) command line option to the interpreter, `argv[0]` is set to the string `-c`. If no script name was passed to the Python interpreter, `argv[0]` is the empty string.
>
>翻译如下：
>
>传递给Python脚本的命令列表。`argv[0]`即脚本名称（是否为全名依赖操作系统）。如果命令是通过向解释器传递 `-c` 命令行选项来执行的，那么 `argv[0]` 会被设置为字符串 `-c`。如果没有向 Python 解释器传递脚本名称，那么 `argv[0]` 就是一个空字符串。

听起来完全不是人话对不对？不过理解起来不难。我们来看一小段程序：

```python
def quadratic():
    a = float(input("What is a? "))
    b = float(input("What is b? "))
    c = float(input("What is c? "))
        
    s1 = (-b + (b**2 - 4*a*c)**0.5)/(2*a)
    s2 = (-b - (b**2 - 4*a*c)**0.5)/(2*a)

    print("Your solutions are ", s1, "and", s2)
```

这是一个一元二次方程求解函数，运用到了求根公式。我们运行这个程序时是通过和程序交互实现的。但是看看下面的程序：

```python
import sys

def quadratic():
    args = sys.argv

    a = float(args[1])
    b = float(args[2])
    c = float(args[3])

    s1 = (-b + (b**2 - 4*a*c)**0.5)/(2*a) 
    s2 = (-b - (b**2 - 4*a*c)**0.5)/(2*a) 

    print("Your solutions are ", s1, "and", s2)

quadratic()
```

各位发现什么端倪了吗？为什么没有使用 `input()` 反而使用了一个 `args列表` ？别急，让我们继续向下看。当我们正常运行这个程序，程序报错了。为什么，我们来看看`Windows11-Python 3.13.6`环境下的报错：

```
Traceback (most recent call last):
  File "d:\Program\python\others\tobase64.py", line 14, in <module>
    quadratic()
    ~~~~~~~~~^^
  File "d:\Program\python\others\tobase64.py", line 5, in quadratic
    a = float(args[1])
              ~~~~^^^
IndexError: list index out of range
```

程序告诉我们数组超出范围了。为什么，其实是因为我们没有给数组传递数据。欸，那怎么传递啊？我的数组来自于sys啊？接着看。

```
PS D:\Program> & "C:/Users/Issea Occupia/AppData/Local/Programs/Python/Python313/python.exe" d:/Program/python/others/tobase64.py 11 65 87
Your solutions are  -2.048870052492215 and -3.860220856598694
```

欸？这下怎么正常了？

不知道你有没有看出我们的区别。第一次运行时，我们只是执行`python filename.py` 这个指令，所以 `sys.argv` 里只有脚本名，没有额外参数，访问 `args[1]` 就报错了。而第二次，我们执行了`python filename.py 11 65 87` 这个指令。关键就在后面的`11 65 87` 。这些数字就是我们传递给脚本的命令行参数，它们依次存储在 `sys.argv` 中，从 `argv[1]` 开始。当环境读取到命令，他就会将这些参数传递到`sys.argv` ,我们通过读取这个列表最终实现了整个程序的运行。

<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/feda35443df77a09dfd874216740aa00.jpg" style="width:350px; border-radius:20px;">

## 2  self.变量

我在学习python初期一切都人畜无害。语法糖快给我喂出糖尿病了（bushi）。然而，当真正上手某些库时，我便被一个问题一直缠绕：

>我想知道为什么使用`__init__`方法声明的变量需要添加`self.`，换句话说，我怎么判断一个变量需要绑定到`self`上？如果不从外界显式接受，没必要将`__init__`形参没有标识的变量和`self`强绑定吧？

这个问题一直到我后期接触了很多项目才逐渐有了头绪。一句话解释

<div style="font-size:25px; font-weight : 700">
为了让一个变量在类的所有方法里都能自由使用，我们需要把它绑定到 self 上，给它“升格”为实例属性。
</div>

下面，我们通过一个小案例一起看看这是什么意思，顺便理解一下方法。

```python
class Dog():
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.fullness = "hungry"
    
    def describe(self):
        print(f"this is my dog,named {self.name},aged {self.age},she's {self.fullness}")

    def feed(self):
        self.fullness = "full"
        print("now you feed the dog ,he's full!")

ceobe = Dog("ceobe",3)
ceobe.describe()
ceobe.feed()
ceobe.describe()
```


```python
class Dog():
    def __init__(self,name,age):
        self.name = name
        self.age = age
        fullness = "hungry"
    
    def describe(self):
        print(f"this is my dog,named {self.name},aged {self.age},she's {fullness}")

    def feed(self):
        fullness = "full"
        print("now you feed the dog ,he's full!")

ceobe = Dog("ceobe",3)
ceobe.describe()
ceobe.feed()
ceobe.describe()
```

<div style = "font-size : 25px;text-align : center;font-weight : 700">你要不自己看吧。。。过了。真的，千言万语不如你自己运行一下。溜了~~~</div>

<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/d5a7572fb4d453c272333ed89c9d40da.jpg" style="width:300px; border-radius:20px;">

## 3 Python 与栈（待完工）

>我编写了一个无穷递归的python小程序，想看到程序逐渐卡死。
>
>```python
>from PyQt6.QtWidgets import *
>import sys
>from random import randint
>class MainWindow(QMainWindow):
>def __init__(self):
>   super().__init__()
>   self.windowTitleChanged.connect(self.titlechanged)
>   self.setWindowTitle("Start!!!")
>
>def titlechanged(self,title):
>   self.setWindowTitle(str(randint(1,1000000)))
>   print(f"changed to {title}")
>
>app = QApplication(sys.argv)
>w = MainWindow()
>w.show()
>app.exec()
>```
>
>但是事与愿违，程序反手抛了一个错误，直接歇菜，狠狠打了我的脸：
>
>```
>Traceback (most recent call last):
>File "d:\Program\python\PyQt6_learning\pyqt_learning_ch1-crash-version.py", line 11, in titlechanged
>self.setWindowTitle(str(randint(1,1000000)))
>File "C:\Users\Issea Occupia\AppData\Local\Programs\Python\Python313\Lib\random.py", line 340, in randint
>return self.randrange(a, b+1)
>File "C:\Users\Issea Occupia\AppData\Local\Programs\Python\Python313\Lib\random.py", line 322, in randrange
>return istart + self._randbelow(width)
>RecursionError: maximum recursion depth exceeded
>```
>
>python是怎么区分无限栈和有限超大栈？比如我曾经用递归写法用c实现了斐波那契数列求解，理论上，我给定的数字是不可能在一小时内算完，但是系统也没有崩溃，那为什么python歇菜了？python不是解释性语言吗？解释一行运行一行？我写过一个使用while true运行的循环程序，这个程序连着跑两个小时不崩溃，为什么？这个（一大堆）问题可不好回答，让我们来一起看看。

<p style = "font-size : 25px ; font-weight : 700">(1).解释型语言</p>

首先必须澄清，目前许多关于这个知识点的资料存在严重的错误，如下：

>解释型语言：是一种使用解释器一行一行地将源代码翻译成二进制机器码，进行解释执行的语言。

乍一听，这个逻辑简直对得不能再对了。解释嘛，一行一行地，不和咱人脑编译一样的嘛？但如果我们从上面的解释出发，似乎有一些问题：

>为什么我的python代码会出现递归问题？一行一行的耶？！

好了好了，我们先解决第一个问题，什么是解释型语言。

<p style = "font-size : 25px ; font-weight : 700">(2).栈与递归</p>



<p style = "font-size : 25px ; font-weight : 700">(3).栈深度，堆，内存与调用次数</p>



<p style = "font-size : 25px ; font-weight : 700">(4).两种异常</p>



<p style = "text-align : center; font-size : 25px ; font-weight : 700">嘻嘻~~</p>

<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/GPwCPB9akAEQsSr.jpg" style="width:500px; border-radius:20px;">

## 4 QLable()的一点小问题

问题起源于我的一次尝试。

>```python
>from PyQt6.QtWidgets import *
>import sys
>class MainWindow(QMainWindow):
>def __init__(self):
>   super().__init__()
>   self.setWindowTitle("My App")
>   self.input = QLineEdit()
>   self.setCentralWidget(self.input)
>
>app = QApplication(sys.argv)
>window = MainWindow()
>window.show()
>app.exec()
>```

我尝试创建一个包含输入框的窗口，然而结果不是那么喜人。。。

<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/ecd69e50953cb3913f85c5388ada3001.png" style = "height : 300px ; border-radius:20px;">

输入框呢！！我的输入框呢！！

随后，我又“灵机一动”。

>```python
>from PyQt6.QtWidgets import *
>import sys
>class MainWindow(QMainWindow):
>def __init__(self):
>   super().__init__()
>   self.setWindowTitle("My App")
>   self.input = QLineEdit()
>   layout = QHBoxLayout()
>   layout.addWidget(self.input)
>   contioner = QWidget()
>   contioner.setLayout(layout)
>   self.setCentralWidget(contioner)
>
>app = QApplication(sys.argv)
>window = MainWindow()
>window.show()
>app.exec()
>```

<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/99f133a43bbacfd209cd2bf4c479baa8.png" style = "height : 300px ; border-radius:20px;">

这下好了。可为什么呢？

细心的你应该发现：上下两个界面“背景色”不一样。没错。对于前者，由于某些原因，这个输入框被撑大了，而当我们使用嵌套结构将这个输入框放置在容器中，输入框就会恢复默认大小。而想把它变大变小也不难：

>```python
>from PyQt6.QtCore import *
>......
>self.input.setFixedHeight(self.input.sizeHint().height() + i)//i可以根据实际自行调整，谨记i为整型！ 
>self.setCentralWidget(edit)
>......
>```

如上即可。



<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/4030e381d75bb919a81cad799cc7e7f1.gif" style="width:450px; border-radius:20px;">

## 5  python中的`__name__`与模块机制

>想必各位一定对下面这行代码非常熟悉又陌生：
>
>```python
>if __name__ == "__main__" :
>```
>
>可这是什么呢？我们来一起看看

### （1）模块

首先必须澄清：对python而言，任何一个 `.py`文件都是`模块(module)` 。所以，我们先来探讨一下被大部分人忽略的“模块”

例如，我们假定有一个名叫`test.py` 的文件，以下写法可行

```python
def main():
    print("main()被加载")
    print(__name__)

import test

if __name__ == "__main__":
    test.main()
    main()
```

以下是运行结果：

```
main()被加载
test
main()被加载
__main__
```

我们来看看。我们编写了一个函数，函数可以告诉我们该函数被调用，同时也可以展示调用环境的`__name__`变量名。

python的运行逻辑比较奇特，当解释器直接执行一个 `.py` 文件时，会将其当作模块加载，并将 `__name__` 变量设置为 `"__main__"`；而当该文件被其他模块通过 `import` 导入时，它的 `__name__` 就会是它自己的模块名。当然了，由于这个变量是运行前赋值，我们可以显式更改这个变量，但是我们不推荐这样做。

试想一下，我们编写了一个模块，但如果将代码逻辑外显，会怎么样？我们编写了两个文件`test.py` `test2.py`请看：

```python
def main():
    print("main()被加载")
    print(__name__)
    print("内显的逻辑，来自test.py")

print("外显的逻辑，来自test.py")
```

```python
import test
print("外显的逻辑，来自test2.py")
```

当我们运行的时候，`test.py` 封装好的`main()`没有被调用，但是外显的逻辑却被调用。

### （2）sys.modules

上面提到任何一个文件被运行的时候都是被视为模块的，可是，我怎么知道呢？下面，隆重有请`sys`家族又一成员：`sys.modules` !

请看官方文档对该模块的介绍，我们稍后讨论这玩意背后的槽点（可多了！！！）

> This is a dictionary that maps module names to modules which have already been loaded. This can be manipulated to force reloading of modules and other tricks. However, replacing the dictionary will not necessarily work as expected and deleting essential items from the dictionary may cause Python to fail. If you want to iterate over this global dictionary always use `sys.modules.copy()` or `tuple(sys.modules)` to avoid exceptions as its size may change during iteration as a side effect of code or activity in other threads.

首先，根据描述，这个模块的作用是记录的加载的模块，我们可以简单验证。

```python
import sys

print("已启动！")
before = set(sys.modules.keys())
print("已导入模块",before)

import random                  

after = set(sys.modules.keys())   

added = after - before             
print("本次导入新增模块数量:", len(added))
print("新增模块如下:")
for name in sorted(added):
    print("   ", name)
```

以下是运行结果：

```
已启动！
已导入模块 {'_distutils_hack', 'marshal', 'pywin32_bootstrap', 'encodings', 'os.path', '_codecs', '_frozen_importlib_external', '_thread', 'sys', 'nt', 'zipimport', 'encodings.aliases', '_abc', 'ntpath', '_imp', '_weakref', 'encodings.utf_8_sig', '_stat', 'genericpath', 'encodings.cp1252', '_signal', 'encodings.utf_8', 'io', '__main__', '_collections_abc', '_io', 'pywin32_system32', '_winapi', 'codecs', 'errno', 'abc', 'winreg', 'stat', 'os', '_sitebuiltins', 'time', '_frozen_importlib', 'site', '_warnings', 'builtins'}
本次导入新增模块数量: 8
新增模块如下:
    _bisect
    _operator
    _random
    bisect
    itertools
    math
    operator
    random
```

所以，我们可以初步知道任何一个被导入的模块都会被记录到`sys.modules`这个字典里。

但是，你有有没有发现一个问题：为什么好多模块存在于`sys.modules`，那我能不能用呢？

```
>>> "os" in sys.modules
True
>>> os
Traceback (most recent call last):
  File "<python-input-9>", line 1, in <module>
    os
NameError: name 'os' is not defined. Did you forget to import 'os'?
```

啧，答案是不行。那为啥？？？

原因存在于python的模块系统。我们来看看。

Python 的模块系统其实在运行时分成 三个层面：

| 层级             | 代表对象               | 说明                                       | 举例                                    |
| ---------------- | ---------------------- | ------------------------------------------ | --------------------------------------- |
| (1) 名字绑定层   | 变量名 → 模块对象      | 发生在 import 时，在当前命名空间创建变量名 | `import math` → 创建变量 `math`         |
| (2) 模块对象层   | 模块实例（真正的对象） | 模块的 `__dict__` 存放函数、类、常量等     | `<module 'math' (built-in)>`            |
| (3) 模块注册表层 | `sys.modules`          | 全局字典，记录所有“已经加载”的模块对象     | `sys.modules['math'] = <module 'math'>` |

之所以将三个层面分开，其中一个原因是减小开销。我们来做一个小实验。

```
import time
import sys
def importre():
    print("requests" in sys.modules)
    a = time.time()
    import requests
    b = time.time()
    print("本次导入requests耗时：",b - a)

importre()
importre() 
```

以下是结果：

```
False
本次导入requests耗时： 1.0038518905639648
True
本次导入requests耗时： 1.430511474609375e-06
```

可以发现，第一次导入时，`requests`没有被写入缓存，此时导入花费了一秒的时间，而第二次，写入了缓存的`requests`使导入过程瞬间完成，事实上，我们论证了python的模块注册机制，当导入之后，会先检查是否存在导入模块是否存在于`sys.modules`随后再决定是注册还是绑定。

继续来看。

```python
import time, importlib

def import_normal():
    t1 = time.perf_counter()
    importlib.import_module("json")
    t2 = time.perf_counter()
    print("正常导入耗时：", t2 - t1)

import_normal()
```

```python
import sys, time, importlib, types
if "json" in sys.modules:
    del sys.modules["json"]
sys.modules["json"] = types.ModuleType("json")
sys.modules["json"].__dict__["preloaded"] = True  
def import_preloaded():
    t1 = time.perf_counter()
    importlib.import_module("json")
    t2 = time.perf_counter()
    print("预写入缓存导入耗时：", t2 - t1)
import_preloaded()
```

以下是运行结果：

```
正常导入耗时： 0.01141269993968308

预写入缓存导入耗时： 2.600019797682762e-06
```

我们可以看出，预写入可以优化导入速度。

最后一个问题，python是怎么决定哪些模块要被预写入，哪些不需要？这个问题比较复杂，我们简单来说。

对于程序底层把必须的模块，python会写入，对于内建的，python也会导入。而那些不是很必要的普通模块，python则会按需导入。

## （3）结语

到这里，我们其实已经串起了 Python 模块系统的整个逻辑链条：
从 `__name__ == "__main__"` 的执行入口，到 `sys.modules` 的注册缓存，再到解释器如何在启动阶段预写入内建模块。
可以看到，**Python 的模块系统并不是“简单的导入机制”**，而是一套有记忆、有层次、有策略的运行体系。第一次导入时，它要做很多事：解析路径、创建模块对象、执行顶层代码，并登记到缓存。
但从第二次开始，Python 就会像“记住”了一样，直接从 `sys.modules` 中取出模块对象。
这种**“惰性初始化 + 全局缓存”**的设计，让 Python 在灵活与效率之间找到了平衡点——既保留了解释型语言的动态性，又最大限度地减少了重复开销。而在更底层，解释器在启动时就会**预写入一批生存必须的模块**：
 `sys`、`builtins`、`_io`、`encodings`……
 这些模块支撑了整个语言的最小可运行环境。
 至于那些非核心模块（例如 `json`、`re`、`requests`），就会被延迟加载，只有在真正 `import` 时才被写入缓存。最终，Python 形成了一种很有意思的层级关系：

> 模块不是一次性“拿来用”的资源，而是可以在运行中不断“注册—复用—替换”的对象。

这也是为什么我们能在 `sys.modules` 里“看到过去”，也能通过修改它来“影响未来”。



<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/bc06c414c69dd5bb46210a43be493e2e.jpg" style="width:300px; border-radius:20px;">



## 6  **isinstance**(*object*, *classinfo*, */*)函数

函数原型中的object是要检查的对象（已经实例化的），classinfo则是类或类的元组（用于检查的类型）。

简单来说，这个函数会返回布尔值，当接受的对象是接受的类或继承该类的类的实例化时返回`True`,反之则为`False`。如下：

```python
>>> a = {'a':'1'}
>>> isinstance(a,dict)
True
>>> isinstance(a,list)
False
>>> isinstance(a,(list,str,dict))
True
>>> isinstance(a,[list,str,dict])
Traceback (most recent call last):
  File "<python-input-8>", line 1, in <module>
    isinstance(a,[list,str,dict])
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union
```

也应该注意区分该函数与`type()`区别。如下：

```
>>> class A:pass
>>> class B(A):pass
>>> a = A()
>>> b = B()
>>> isinstance(b,A)
True
>>> type(a)
<class '__main__.A'>
>>> type(b)
<class '__main__.B'>
>>> type(b) is A
False
```

可以看出,`type()`属于强类型检测。

<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/%E4%BD%A9%E4%BD%A9.png" style="width:300px; border-radius:20px;">
