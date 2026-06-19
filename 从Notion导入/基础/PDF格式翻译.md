# PDF格式翻译

### 第一步：准备 Windows 基础环境

1. 在新电脑上，你需要先下载并安装 **Python**（建议版本在 3.11 到 3.12 之间）。
2. **关键注意：** 在安装 Python 的界面底部，务必勾选 **“Add Python to PATH”**（将 Python 添加到环境变量），否则后续在终端中会找不到命令。

### 第二步：一键安装翻译工具

打开新电脑的命令提示符（CMD）或终端（Terminal），直接输入以下命令进行安装：
`pip install pdf2zh`*(注：如果你希望安装速度更快且环境更独立，也可以先安装包管理器 uv，再运行 `uv tool install --python 3.12 pdf2zh` )*

### 第三步：启动网页图形界面 (WebUI)

为了获得类似你之前觉得好用的 AnyDoc 翻译器那样的可视化体验，并跳过复杂的 VS Code 插件配置，直接在终端中输入以下启动命令：
`pdf2zh -i`
按下回车后，你的浏览器会自动打开一个本地的图形化翻译界面。

### 第四步：配置 API（避开截图中的报错陷阱）

在打开的网页界面设置中，你需要重新配置免费的 API。结合你第三张截图里 `openrouter/owl-alpha` 无法访问和单模态不识别图片的教训，请使用以下两种免费方案之一：

**方案 A：继续使用 OpenRouter（智能免费路由）**

- **服务 (Service)**：选择 `OpenAI`
- **Base URL**：必须填入标准的 API 路径 `https://openrouter.ai/api/v1`（不要填截图1里的 rankings 网址）
- **API Key**：填入你的 OpenRouter 密钥
- **Model (模型)**：**务必填写 `openrouter/free`**。这是一个智能路由，会自动为你分配存活的免费模型，并自动避开那些不支持你当前任务（比如没有视觉能力或已下线）的模型。

**方案 B：使用国内的硅基流动（SiliconFlow）免费模型（推荐）**

- **服务 (Service)**：选择 `Silicon`
- **API Key**：填入你申请的 SiliconFlow 密钥
- **Model (模型)**：填写 `Qwen/Qwen2.5-7B-Instruct` 等免费的长文本模型。

### 第五步：开始翻译

配置完成后，回到界面的主页，直接将你那 30 页的英语论文 PDF 拖拽进网页框中。系统会在后台调用你配置的免费 API 进行逐页翻译，最后输出一份排版、公式和图表完全保留的中文 PDF 文件。

`pdf2zh "你的PDF文件路径.pdf" -o "输出目录"`

pdf2zh "C:\Users\Administrator\Desktop\pdf2zh_files\2203.02155v1.pdf" -o "C:\Users\Administrator\Desktop\pdf2zh_output"