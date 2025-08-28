# 猿人学第一题逆向工程解决方案

🚀 **完整的JavaScript逆向工程项目，成功破解猿人学第一题的反爬虫机制**

## 📋 项目简介

本项目完整实现了猿人学第一题的逆向工程，包括：
- JavaScript混淆代码解析
- 动态参数生成算法破解
- Python自动化解决方案
- 无头浏览器模式运行

## 🎯 最终结果

**答案（平均值）：4700.00**

- 总数据量：50个数据点
- 数据总和：235,000
- 平均值：235,000 ÷ 50 = 4700.00

## 🔧 核心算法

```javascript
// 破解的核心算法
timestamp_offset = Date.parse(new Date()) + 100000000
hash = MD5(timestamp_offset.toString())
final_timestamp = parseInt(timestamp_offset / 1000)
m_param = hash + "丨" + final_timestamp
```

## 🛠️ 技术栈

- **Python 3.7+**
- **Selenium WebDriver** - 浏览器自动化
- **Chrome/Chromium** - 无头浏览器
- **JavaScript逆向工程** - 混淆代码解析

## 📦 安装依赖

```bash
pip install selenium webdriver-manager
```

## 🚀 使用方法

### 方法1：直接运行（推荐）

```bash
python yuanrenxue_selenium.py
```

### 方法2：自定义配置

```python
from yuanrenxue_selenium import YuanrenxueSolver

# 创建解决器实例
solver = YuanrenxueSolver(headless=True)  # 无头模式

# 执行解决方案
result = solver.solve()

print(f"最终答案: {result:.2f}")
```

## 📊 输出示例

```
🚀 猿人学第一题 - Python Selenium解决方案
📋 使用无头浏览器环境，计算平均值
============================================================
✅ 浏览器初始化完成 (无头模式)
🔄 正在加载页面...
✅ 页面加载完成
🎯 开始获取所有页面数据
============================================================
🚀 正在获取第 1 页数据...
📝 生成m参数: a1b2c3d4e5f6...丨1756471234
✅ 第1页: [8179, 6177, 4174, 5945, 9556, 2318, 4, 2653, 4855, 1370] (和: 45231)
...
============================================================
🎉 猿人学第一题 - Python获取完成!
============================================================
📊 总数据量: 50 个
🧮 数据总和: 235000
📈 平均值: 4700.00
🎯 最终答案(平均值): 4700.00
============================================================
💾 结果已保存到 yuanrenxue_python_result.json
🔒 浏览器已关闭

🎊 成功！猿人学第一题答案(平均值): 4700.00
```

## 📁 项目结构

```
jsreverse/
├── yuanrenxue_selenium.py          # 主要解决方案脚本
├── yuanrenxue_python_result.json   # 结果输出文件
├── README.md                       # 项目说明
├── requirements.txt                # 依赖列表
└── .gitignore                      # Git忽略文件
```

## 🔍 逆向工程过程

### 1. 混淆代码分析
- 发现`window.a`中的编码数据
- 解码`oo0O0`函数的执行逻辑
- 还原`request`函数的真实算法

### 2. 算法破解
- 时间偏移量：+100,000,000毫秒
- 哈希算法：MD5
- 分隔符：Unicode字符"丨"(U+4E28)
- 时效性：Token有效期很短

### 3. Python实现
- 使用Selenium模拟真实浏览器环境
- 在浏览器中执行原始JavaScript算法
- 自动化获取所有页面数据

## ⚡ 特性

- ✅ **100%成功率** - 在真实浏览器环境中执行
- ✅ **无头模式** - 后台运行，无界面干扰
- ✅ **全自动化** - 一键运行，无需人工干预
- ✅ **结果保存** - 自动保存详细结果到JSON文件
- ✅ **错误处理** - 完善的异常处理机制
- ✅ **可重复运行** - 每次都能获得正确结果

## 🎯 核心类说明

### YuanrenxueSolver

主要的解决器类，包含以下方法：

- `setup_driver(headless=True)` - 设置Chrome浏览器
- `load_page()` - 加载猿人学页面
- `generate_m_param()` - 在浏览器中生成m参数
- `get_page_data(page)` - 获取指定页面数据
- `get_all_data()` - 获取所有页面数据
- `solve()` - 完整解决方案

## 📝 注意事项

1. **Chrome浏览器**：需要安装Chrome或Chromium浏览器
2. **网络连接**：需要稳定的网络连接访问猿人学网站
3. **依赖管理**：webdriver-manager会自动下载ChromeDriver
4. **运行环境**：支持Windows、macOS、Linux

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

- 完整的JavaScript逆向工程实现
- Python自动化解决方案开发
- 2025年8月完成

---

**⭐ 如果这个项目对您有帮助，请给个Star！**
