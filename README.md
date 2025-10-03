<div style="text-align : center;font-size : 40px;font-weight : 700">python学习札记(=ↀωↀ=)✧</div>

<img src = "https://raw.githubusercontent.com/Issea-Occupia/Program/refs/heads/main/photos/2c077d928bca20e80a746ded59918443.jpg" style="width:300px; border-radius:20px;">

## 1 <strong>sys.argv</strong>的应用。

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

## 2  <strong>self.变量</strong>

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
