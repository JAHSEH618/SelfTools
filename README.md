<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-macOS%20|%20Linux%20|%20Windows-lightgrey?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<h1 align="center">🛠️ SelfTools</h1>

<p align="center">
  <strong>个人实用工具集 —— 提升日常开发与文件处理效率</strong>
</p>

<p align="center">
  <em>一个专注于图像处理、格式转换的 Python 工具集合</em>
</p>

---

## 📖 目录

- [✨ 项目简介](#-项目简介)
- [🚀 快速开始](#-快速开始)
- [🧰 工具列表](#-工具列表)
  - [📸 HTML to PNG Exporter](#-html-to-png-exporter)
  - [🔐 Image to Base64 Converter](#-image-to-base64-converter)
- [📦 安装依赖](#-安装依赖)
- [🗂️ 项目结构](#️-项目结构)
- [📝 更新日志](#-更新日志)
- [🤝 贡献指南](#-贡献指南)
- [📄 开源许可](#-开源许可)

---

## ✨ 项目简介

**SelfTools** 是一个轻量级的个人工具集，旨在解决日常开发中常见的文件处理需求。目前主要聚焦于：

- 🖼️ **HTML 转 PNG** —— 将 HTML 文件渲染为高分辨率 PNG 图片
- 🔄 **图片转 Base64** —— 图片与 Base64 编码的双向转换

这些工具设计简洁、易于使用，支持命令行调用，可以方便地集成到各种工作流程中。

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/SelfTools.git
cd SelfTools

# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install playwright
playwright install chromium
```

---

## 🧰 工具列表

### 📸 HTML to PNG Exporter

> 将 HTML 文件转换为高清晰度 PNG 图片，基于 Playwright 浏览器引擎实现精准渲染。

#### 核心特性

| 特性 | 描述 |
|:---:|:---|
| 🎨 **高分辨率输出** | 支持 2x-4x 缩放因子，生成超清图片 |
| 📐 **自定义视口宽度** | 灵活调整渲染宽度，适配不同场景 |
| ⏱️ **渲染等待控制** | 可配置等待时间，确保动态内容完全加载 |
| 📄 **全页面捕获** | 自动计算页面高度，完整截取长页面 |
| 🔄 **向后兼容** | 同时支持命名参数和位置参数两种调用方式 |

#### 命令行参数

| 参数 | 短参数 | 类型 | 默认值 | 说明 |
|:---|:---:|:---:|:---:|:---|
| `--input` | `-i` | string | - | 输入 HTML 文件路径（必填） |
| `--output` | `-o` | string | 同名 .png | 输出 PNG 文件路径 |
| `--scale` | `-s` | int | 2 | 缩放因子（推荐 2-4） |
| `--width` | `-w` | int | 1200 | 视口宽度（像素） |
| `--wait` | - | int | 1000 | 渲染等待时间（毫秒） |

#### 使用示例

```bash
# 基础用法：使用命名参数
python html_to_png.py -i document.html -o export.png

# 高分辨率导出（4x 缩放）
python html_to_png.py --input page.html --output ./exports/page.png --scale 4

# 宽屏渲染
python html_to_png.py -i report.html -o report.png --width 1920 --scale 3

# 向后兼容模式：位置参数
python html_to_png.py document.html                     # 输出: document.png
python html_to_png.py document.html custom_output.png   # 指定输出路径
python html_to_png.py document.html output.png 3        # 指定缩放因子
```

#### 输出示例

```
📄 Input:  /path/to/document.html
🖼️  Output: /path/to/document.png
🔍 Scale:  2x | Width: 1200px

✅ Successfully exported!
   📁 File: /path/to/document.png
   📊 Size: 256.5 KB
   🎨 Resolution: 2x (2400px effective width)
```

---

### 🔐 Image to Base64 Converter

> 实现图片与 Base64 编码的双向转换，支持生成可直接嵌入 HTML/CSS 的 Data URI 格式。

#### 核心特性

| 特性 | 描述 |
|:---:|:---|
| 🔄 **双向转换** | 支持图片 → Base64 和 Base64 → 图片 |
| 🌐 **Data URI 格式** | 自动生成带 MIME 类型的 Data URI，可直接用于网页 |
| 📁 **文件保存** | 可将 Base64 编码保存到文本文件 |
| 🖼️ **多格式支持** | 支持 JPG、PNG、GIF、BMP、WebP、SVG 等常见格式 |

#### 支持的图片格式

| 格式 | 扩展名 | MIME 类型 |
|:---:|:---:|:---|
| JPEG | `.jpg` / `.jpeg` | `image/jpeg` |
| PNG | `.png` | `image/png` |
| GIF | `.gif` | `image/gif` |
| BMP | `.bmp` | `image/bmp` |
| WebP | `.webp` | `image/webp` |
| SVG | `.svg` | `image/svg+xml` |

#### API 函数说明

##### `image_to_base64(image_path)`

将图片文件转换为纯 Base64 字符串。

```python
from img2base64 import image_to_base64

base64_str = image_to_base64("./photo.png")
print(base64_str[:50])  # 输出前50个字符
```

##### `image_to_base64_with_prefix(image_path)`

生成带 Data URI 前缀的 Base64 字符串，可直接用于 HTML `<img>` 标签或 CSS `background-image`。

```python
from img2base64 import image_to_base64_with_prefix

data_uri = image_to_base64_with_prefix("./logo.png")
# 输出: data:image/png;base64,iVBORw0KGgo...
```

**HTML 使用示例：**

```html
<img src="data:image/png;base64,iVBORw0KGgo..." alt="logo" />
```

##### `save_base64_to_file(image_path, output_path)`

将图片的 Base64 编码保存到文本文件。

```python
from img2base64 import save_base64_to_file

save_base64_to_file("./image.png", "./encoded.txt")
# 输出: Base64字符串已保存到: ./encoded.txt
```

##### `base64_to_image(base64_string, output_path)`

将 Base64 字符串还原为图片文件。

```python
from img2base64 import base64_to_image

# 支持带或不带 Data URI 前缀的字符串
base64_to_image(data_uri, "./restored.png")
# 输出: 图片已保存到: ./restored.png
```

#### 命令行使用

```bash
# 直接运行查看示例输出
python img2base64.py
```

---

## 📦 安装依赖

### 系统要求

- Python 3.8+
- pip 包管理器

### 依赖安装

```bash
# HTML to PNG 工具依赖
pip install playwright
playwright install chromium

# Image to Base64 工具无需额外依赖（使用 Python 标准库）
```

### 完整依赖列表

| 依赖 | 用途 | 必需 |
|:---|:---|:---:|
| `playwright` | HTML 渲染引擎 | ✅ (html_to_png) |
| `chromium` | Playwright 浏览器内核 | ✅ (html_to_png) |
| `base64` | Base64 编解码 | ✅ (内置库) |
| `pathlib` | 路径处理 | ✅ (内置库) |

---

## 🗂️ 项目结构

```
SelfTools/
├── 📄 README.md              # 项目说明文档
├── 📄 .gitignore             # Git 忽略配置
├── 🐍 html_to_png.py         # HTML 转 PNG 工具
├── 🐍 img2base64.py          # 图片 Base64 编解码工具
├── 📁 .venv/                 # Python 虚拟环境
└── 📁 .idea/                 # IDE 配置（已忽略）
```

---

## 📝 更新日志

### v1.0.0 (2026-01-21)

#### 🎉 首次发布

- ✨ 新增 `html_to_png.py` —— HTML 转高清 PNG 工具
  - 支持命名参数 (`-i`, `-o`, `-s`, `-w`) 和位置参数
  - 可配置缩放因子、视口宽度、渲染等待时间
  - 完整的错误处理和友好的输出提示

- ✨ 新增 `img2base64.py` —— 图片与 Base64 双向转换工具
  - 支持纯 Base64 和 Data URI 格式输出
  - 支持常见图片格式（JPG/PNG/GIF/BMP/WebP/SVG）
  - 提供文件保存和图片还原功能

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源许可

本项目采用 [MIT License](LICENSE) 开源许可协议。

---

<p align="center">
  <strong>Made with ❤️ for productivity</strong>
</p>

<p align="center">
  如果这个项目对你有帮助，欢迎点个 ⭐️ Star！
</p>
