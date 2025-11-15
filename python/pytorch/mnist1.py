# mnist_start.py
# ========================
# 🚀 MNIST 手写数字识别入门程序
# 作者: ChatGPT & Issea Occupia
# 功能: 训练一个简单的全连接神经网络识别手写数字 (0~9)
# ========================

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms

# ========================
# 一、环境与数据准备
# ========================

# 自动选择设备 (GPU 优先)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"💻 Using device: {device}")

# 数据预处理: 转换为Tensor + 归一化到(-1, 1)
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# 下载并加载 MNIST 数据集
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_data = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = torch.utils.data.DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=64, shuffle=False)

# ========================
# 二、定义网络结构
# ========================

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128)  # 输入层 -> 隐藏层1
        self.fc2 = nn.Linear(128, 64)       # 隐藏层1 -> 隐藏层2
        self.fc3 = nn.Linear(64, 10)        # 隐藏层2 -> 输出层

    def forward(self, x):
        x = x.view(-1, 28 * 28)  # 展平图片
        x = F.relu(self.fc1(x))  # 激活函数 ReLU
        x = F.relu(self.fc2(x))
        x = self.fc3(x)          # 输出层（不加Softmax）
        return x

# ========================
# 三、训练准备
# ========================

model = SimpleNet().to(device)
criterion = nn.CrossEntropyLoss()               # 交叉熵损失函数
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# ========================
# 四、训练模型
# ========================

epochs = 50
for epoch in range(epochs):
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f"Epoch [{epoch+1}/{epochs}] | Loss: {running_loss/len(train_loader):.4f}")

print("✅ 训练完成！")

# ========================
# 五、模型测试
# ========================

correct, total = 0, 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"🎯 测试集准确率: {accuracy:.2f}%")

# ========================
# 六、保存模型
# ========================

torch.save(model.state_dict(), "mnist_simple.pth")
print("💾 模型已保存为 mnist_simple.pth")

# ========================
# 七、结语
# ========================
# 下一步建议：
# 1️⃣ 理解 tensor、反向传播机制；
# 2️⃣ 尝试添加卷积层（CNN）；
# 3️⃣ 使用 matplotlib 可视化预测结果。
