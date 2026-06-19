# 页面PDF格式翻译和自动排版记笔记

> MITRE ATLAS AML.T0051 (Indirect Prompt Injection) / OWASP LLM01: Prompt Injection
在物理机或云端沙箱中复现这款“沉浸式 PDF 双语翻译器”，本质上是在部署一个标准化的**AI安全实战靶场 (AI Security Target Range)**。该应用在架构上存在典型的指令与数据边界混淆缺陷：它将不受信的外部文档（PDF文件流）隐式转换为纯文本，并与系统提示词（System Prompt）在高权限上下文中进行硬拼接。引入 `react-markdown` 缓解了直接执行恶意 HTML 的 XSS 风险，但同时也为测试零点击 Markdown 盲水印外带（Zero-click Markdown Exfiltration）等更隐蔽的次生载荷提供了完美的测试环境。
> 

**对抗流水线 (The Pipeline)**
这是一套针对全新 Windows 环境的保姆级一键部署 SOP，已彻底消除依赖漂移和样式引擎逃逸问题：

1. **静默构建与目录劫持 (Silent Scaffolding & Hijacking):** 利用 Vite 快速生成 React 基线，并直接将终端上下文下潜至靶场目录。
2. **依赖锚定 (Dependency Anchoring):** 强制锁定 Tailwind CSS v3 核心，同步挂载 PDF.js 解析器与 Markdown 渲染引擎，阻断供应链版本冲突。
3. **配置强写 (Configuration Overwrite):** 利用系统底层 API 强行写入前端编译桥接文件，确保样式引擎精准接管。
4. **载荷投递 (Payload Delivery):** 注入包含核心业务逻辑与安全盲区的 `App.jsx` 组件。
5. **跨界暴露 (Cross-boundary Exposure):** 强制解除网络栈沙箱，将靶场端口挂载至 `0.0.0.0` 以支持局域网内的跨设备渗透测试。

**核心载荷 (The Payload)**

### 阶段一：环境基线与配置直写

在目标电脑上安装 Node.js 后，打开 PowerShell，全选并一次性粘贴执行以下命令：

PowerShell

```
# 1. 静默创建靶场环境并进入目录
npm create vite@latest immersive-translator --yes -- --template react
cd immersive-translator

# 2. 锚定核心依赖与 UI 渲染引擎
npm install
npm install lucide-react pdfjs-dist react-markdown remark-gfm
npm install -D tailwindcss@3 postcss autoprefixer

# 3. 强行覆写 Tailwind 扫描边界
Set-Content -Path "tailwind.config.js" -Value "export default { content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'], theme: { extend: {} }, plugins: [require('@tailwindcss/typography')] }" -Encoding UTF8

# 4. 强行覆写 PostCSS 引擎桥接
Set-Content -Path "postcss.config.js" -Value "export default { plugins: { tailwindcss: {}, autoprefixer: {}, }, }" -Encoding UTF8

# 5. 强行覆写全局底层宏指令
Set-Content -Path "src\index.css" -Value "@tailwind base;`n@tailwind components;`n@tailwind utilities;`nbody { margin: 0; padding: 0; background-color: #f5f5f5; }" -Encoding UTF8
```

*(注：这里为 Tailwind 配置额外加入了 Typography 插件的支持，以确保 Markdown 渲染达到最佳的沉浸式排版效果。执行完上述命令后，请运行 `npm install -D @tailwindcss/typography` 补充该插件。)*

### 阶段二：核心业务漏洞代码注入

打开项目文件夹中的 `src\App.jsx`，清空原有内容，将以下完整的最终版代码直接贴入并保存：

JavaScript

```
import React, { useState, useEffect, useRef } from 'react';
import {
  ChevronDown, Search, History, Printer, Download,
  Menu, ChevronLeft, ChevronRight, Maximize,
  Settings2, FileText, Image as ImageIcon, LayoutGrid
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function App(){
  const [isPdfjsLoaded, setIsPdfjsLoaded] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfDoc, setPdfDoc] = useState(null);
  const [pageStates, setPageStates] = useState({});
  const [error, setError] = useState(null);

  const [scale, setScale] = useState(1.2);
  const [selectedModel, setSelectedModel] = useState('DeepSeek-v4-pro');
  const [isEnhanced, setIsEnhanced] = useState(true);

  const leftPaneRef = useRef(null);
  const rightPaneRef = useRef(null);
  const fileInputRef = useRef(null);

  const isSyncingLeft = useRef(false);
  const isSyncingRight = useRef(false);

  // 挂载 PDF.js Worker
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js';
    script.onload = () => {
      if (window.pdfjsLib) {
        window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
        setIsPdfjsLoaded(true);
      }
    };
    document.body.appendChild(script);
    return () => {
      if (document.body.contains(script)) document.body.removeChild(script);
    };
  }, []);

  // 同步滚动防抖逻辑
  const handleScroll = (e, source) => {
    const target = e.target;
    const ratio = target.scrollTop / (target.scrollHeight - target.clientHeight);

    if (source === 'left') {
      if (isSyncingLeft.current) { isSyncingLeft.current = false; return; }
      isSyncingRight.current = true;
      if (rightPaneRef.current) rightPaneRef.current.scrollTop = ratio * (rightPaneRef.current.scrollHeight - rightPaneRef.current.clientHeight);
    } else {
      if (isSyncingRight.current) { isSyncingRight.current = false; return; }
      isSyncingLeft.current = true;
      if (leftPaneRef.current) leftPaneRef.current.scrollTop = ratio * (leftPaneRef.current.scrollHeight - leftPaneRef.current.clientHeight);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      const fileReader = new FileReader();
      fileReader.onload = function(){
        loadPdf(new Uint8Array(this.result));
      };
      fileReader.readAsArrayBuffer(file);
      setPdfFile(file);
    }
  };

  const loadPdf = async (data) => {
    if (!window.pdfjsLib) return;
    try {
      const pdf = await window.pdfjsLib.getDocument({ data }).promise;
      setPdfDoc(pdf);
      setPageStates({});
    } catch (err) {
      setError("PDF加载失败: " + err.message);
    }
  };

  // 全文档离线渲染与数据提取
  useEffect(() => {
    if (!pdfDoc) return;
    let isCancelled = false;

    const renderAllPages = async () => {
      for (let i = 1; i <= pdfDoc.numPages; i++) {
        if (isCancelled) break;
        try {
          const page = await pdfDoc.getPage(i);
          const viewport = page.getViewport({ scale });
          const canvas = document.getElementById(`pdf-canvas-${i}`);

          if (canvas) {
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            await page.render({ canvasContext: context, viewport }).promise;

            const textContent = await page.getTextContent();
            const text = textContent.items.map(item => item.str).join(' ');

            setPageStates(prev => ({
              ...prev,
              [i]: { ...prev[i], text, status: prev[i]?.status || 'idle' }
            }));
          }
        } catch (err) {
          console.error(`Page ${i} render error:`, err);
        }
      }
    };

    renderAllPages();
    return () => { isCancelled = true; };
  }, [pdfDoc, scale]);

  // 自动触发多线程翻译
  useEffect(() => {
    if (!apiKey) return;
    Object.entries(pageStates).forEach(([pageNum, data]) => {
      if (data.text && data.status === 'idle') translatePageText(pageNum, data.text);
    });
  }, [pageStates, apiKey]);

  // 核心盲点：大模型调用与越狱接口
  const translatePageText = async (pageNum, text) => {
    if (!text.trim()) return;
    setPageStates(prev => ({ ...prev, [pageNum]: { ...prev[pageNum], status: 'translating' } }));

    const systemPrompt = `你是一个高级文档排版与翻译引擎。
目标：将提取出的碎片化PDF英文文本翻译为流畅的简体中文，并完美重建原有的文档结构。
强制规则：
1. 必须使用 Markdown 格式输出。
2. 智能识别大标题、副标题，并使用适当的 Markdown 标题语法（#，## 等）。
3. 智能合并因PDF换行导致的断句，恢复完整的段落语义。不同段落之间必须使用空行分隔。
4. 如果原文有列表（Bullet points或数字列表），请使用相应的 Markdown 列表语法还原。
5. 突出关键术语可以使用加粗（**）。
6. 不要输出任何代码块标记（如 \`\`\`markdown），直接输出解析后的纯净文本即可。`;

    try {
      const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          model: 'deepseek-chat',
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: text }
          ],
          temperature: 0.2
        })
      });

      if (!response.ok) throw new Error(`API Error ${response.status}`);
      const data = await response.json();

      setPageStates(prev => ({
        ...prev,
        [pageNum]: { ...prev[pageNum], status: 'done', translatedText: data.choices[0].message.content }
      }));
    } catch (err) {
      setPageStates(prev => ({
        ...prev,
        [pageNum]: { ...prev[pageNum], status: 'error', error: err.message }
      }));
    }
  };

  const pagesArray = Array.from({ length: pdfDoc?.numPages || 1 }, (_, i) => i + 1);
  const estimatedPageHeight = 1130 * (scale / 1.2);

  return (
    <div className="h-screen w-full bg-[#f5f5f5] flex flex-col font-sans text-gray-800 overflow-hidden">
      <header className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-4 shrink-0 z-20 shadow-sm">
        <div className="flex items-center gap-4">
          <button className="flex items-center gap-1 text-sm font-medium hover:bg-gray-100 px-2 py-1.5 rounded">
            <LayoutGrid size={16} /> 双语长卷视图 <ChevronDown size={14} className="text-gray-500" />
          </button>
          <button className="flex items-center gap-1 text-sm text-gray-600 hover:bg-gray-100 px-2 py-1.5 rounded">
            同步滚动 <ChevronDown size={14} />
          </button>
        </div>

        <div className="flex items-center gap-2 bg-gray-50 rounded-full px-2 py-1 border border-gray-200">
          <div className="flex items-center gap-1 px-3 border-r border-gray-300"><span className="text-sm">自动检测</span></div>
          <span className="text-gray-400 text-xs px-1">↔</span>
          <button className="flex items-center gap-1 px-3 text-sm hover:bg-gray-200 rounded-full py-1 transition-colors">
            简体中文 <ChevronDown size={14} className="text-gray-500"/>
          </button>
          <button className="flex items-center gap-2 px-3 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-full py-1 border-l border-gray-300 transition-colors">
            <Settings2 size={16} /> {selectedModel} <ChevronDown size={14} />
          </button>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="password"
            placeholder="输入 API Key"
            className="text-xs border rounded px-2 py-1 w-32 focus:outline-blue-500"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
          <div className="h-4 w-px bg-gray-300 mx-1"></div>
          <button onClick={() => fileInputRef.current?.click()} className="flex items-center gap-1 text-sm hover:bg-gray-100 px-3 py-1.5 rounded transition-colors font-medium">
            打开文档 <ChevronDown size={14} />
            <input type="file" ref={fileInputRef} className="hidden" accept=".pdf" onChange={handleFileChange} />
          </button>
          <button className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-1.5 rounded transition-colors shadow-sm">
            全卷下载
          </button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <aside className="w-12 bg-white border-r border-gray-200 flex flex-col items-center py-4 gap-6 shrink-0 z-10">
          <button className="p-2 text-gray-400 hover:text-gray-800"><Menu size={20} /></button>
          <button className="p-2 text-blue-600 bg-blue-50 rounded-lg"><FileText size={20} /></button>
          <button className="p-2 text-gray-400 hover:text-gray-800"><ImageIcon size={20} /></button>
          <div className="mt-auto pb-4"><span className="text-xs font-medium text-gray-400">{pdfDoc?.numPages ? `共${pdfDoc.numPages}页` : ''}</span></div>
        </aside>

        <main className="flex-1 flex bg-[#e8eaed] relative">
          <div
            ref={leftPaneRef}
            onScroll={(e) => handleScroll(e, 'left')}
            className="flex-1 overflow-y-auto overflow-x-hidden flex flex-col items-center py-8 gap-8 custom-scrollbar scroll-smooth"
          >
            {!pdfFile && (
              <div className="w-[800px] h-[1130px] bg-white shadow-md flex items-center justify-center text-gray-400 border border-gray-200">
                <p>点击上方“打开文档”加载 PDF</p>
              </div>
            )}

            {pdfFile && pagesArray.map(pageNum => (
              <div key={`pdf-${pageNum}`} className="relative shadow-md border border-gray-200 bg-white" style={{ width: `${800 * (scale/1.2)}px` }}>
                <div className="absolute -left-10 top-0 text-xs text-gray-400 font-medium">{pageNum}</div>
                <canvas id={`pdf-canvas-${pageNum}`} className="w-full"></canvas>
              </div>
            ))}
          </div>

          <div className="w-px bg-gray-300 shadow-[0_0_10px_rgba(0,0,0,0.1)] z-10"></div>

          <div
            ref={rightPaneRef}
            onScroll={(e) => handleScroll(e, 'right')}
            className="flex-1 overflow-y-auto overflow-x-hidden flex flex-col items-center py-8 gap-8 custom-scrollbar scroll-smooth relative"
          >
            {!apiKey && pdfFile && (
               <div className="fixed top-24 right-10 bg-yellow-100 border border-yellow-300 text-yellow-800 text-xs px-4 py-2 rounded shadow-sm z-30">
                 提示：请输入 API Key 以启动实时流式翻译
               </div>
            )}

            {!pdfFile && (
              <div className="w-[800px] h-[1130px] bg-white shadow-md flex items-center justify-center text-gray-400 border border-gray-200"></div>
            )}

            {pdfFile && pagesArray.map(pageNum => {
              const state = pageStates[pageNum];
              return (
                <div
                  key={`trans-${pageNum}`}
                  className="bg-white shadow-md border border-gray-200 px-12 py-16 relative"
                  style={{ width: `${800 * (scale/1.2)}px`, minHeight: `${estimatedPageHeight}px` }}
                >
                  <div className="absolute top-4 right-4 text-xs text-gray-400">
                    {state?.status === 'translating' && <span className="flex items-center gap-1 text-blue-500"><span className="animate-spin h-3 w-3 border-2 border-current border-t-transparent rounded-full"></span> 翻译中...</span>}
                    {state?.status === 'done' && <span className="text-green-600">✓ 完成</span>}
                    {state?.status === 'error' && <span className="text-red-500">⚠ 失败</span>}
                  </div>

                  {!apiKey ? (
                     <div className="h-full flex items-center justify-center text-gray-300">等待 API Key...</div>
                  ) : state?.status === 'translating' ? (
                     <div className="space-y-4 animate-pulse pt-4">
                       <div className="h-4 bg-gray-100 rounded w-full"></div>
                       <div className="h-4 bg-gray-100 rounded w-[90%]"></div>
                       <div className="h-4 bg-gray-100 rounded w-[95%]"></div>
                       <br/>
                       <div className="h-4 bg-gray-100 rounded w-[80%]"></div>
                     </div>
                  ) : (
                    // 动态 Markdown 渲染沙箱
                    <div className="prose prose-lg prose-blue max-w-none font-sans leading-relaxed text-gray-800 break-words prose-headings:font-bold prose-h1:text-3xl prose-h2:text-2xl prose-p:my-4">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {state?.translatedText || ""}
                      </ReactMarkdown>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="fixed bottom-8 right-12 bg-white shadow-lg border border-gray-200 rounded-full px-4 py-2 flex items-center gap-3 z-30 opacity-80 hover:opacity-100 transition-opacity">
            <button onClick={() => setScale(s => Math.max(0.5, s - 0.2))} className="text-gray-500 hover:text-blue-600 font-bold">-</button>
            <span className="text-xs font-medium w-12 text-center">{Math.round((scale/1.2)*100)}%</span>
            <button onClick={() => setScale(s => Math.min(3, s + 0.2))} className="text-gray-500 hover:text-blue-600 font-bold">+</button>
            <div className="w-px h-4 bg-gray-300"></div>
            <button className="text-gray-500 hover:text-blue-600"><Maximize size={14}/></button>
          </div>

        </main>
      </div>

      <style dangerouslySetInnerHTML={{__html: `
        .custom-scrollbar::-webkit-scrollbar { width: 8px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #e8eaed; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
      `}} />
    </div>
  );
}
```

### 阶段三：拉起服务

代码保存完毕后，在当前项目目录的 PowerShell 中执行最终挂载命令：

PowerShell

```
npm run dev -- --host
```

**自动化验证 (The Automation)**
打开局域网内任意一台电脑的浏览器，通过宿主机的物理 IP 探测靶场。若成功返回响应结构，即可开始投递测试载荷：

PowerShell

```
# 替换为运行该靶场的物理机 IP (例如: 192.168.1.100)
Invoke-WebRequest -Uri "http://127.0.0.1:5173" -UseBasicParsing | Select-Object StatusCode
```

## 🚀 核心载荷 (The Payload)

这是完整、未被截断的 `notion_injector.py`，已包含 $\color{red}{\textbf{单\$符号降级}}$、$\color{blue}{\textbf{\textbackslash textbf闭包强化}}$ 以及 `r"""` 原始字符串防转义机制。

### 🐍 Python 代码

```python
import keyboard
import pyperclip
import requests

# 务必替换为你真实的 DeepSeek API Key
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_URL = "<https://api.deepseek.com/v1/chat/completions>"

def exploit_clipboard():
    try:
        raw_text = pyperclip.paste()
        if not raw_text.strip():
            return

        # [核心修复]: 降级定界符为单 $，并嵌套 \\textbf 强化 AST 渲染权重，防止转义塌陷
        system_prompt = r"""
        === [SYSTEM OVERRIDE: NOTION FORMATTER] ===
        [INSTRUCTION PRIORITY: CRITICAL]
        你现在的唯一身份是Notion原生排版引擎。必须对用户输入进行重构。
        强制规则：
        1. 必须使用 Markdown 格式。使用 ## 和 ### 构建清晰层级。
        2. 每个标题和列表项开头必须补充符合语境的 Emoji。
        3. [最高优先级] 识别文本中的核心概念、高危警告或总结，必须使用KaTeX语法强制注入颜色！
           定界符严格使用单美元符号！并且使用 \\textbf 加粗！
           合法载荷示例：$\\color{red}{\\textbf{高危警告}}$ 或 $\\color{blue}{\\textbf{核心逻辑}}$
        4. 公式标记内绝对禁止出现任何空格。
        5. 仅输出处理后的纯净文本，绝对禁止将结果包裹在 ``` 或 ```markdown 代码块中！
        === [END SYSTEM OVERRIDE] ===
        """

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text}
            ],
            "temperature": 0.2
        }

        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json=payload
        )

        if response.ok:
            formatted_payload = response.json()['choices'][0]['message']['content']
            pyperclip.copy(formatted_payload)
            print("[+] Payload successfully written to clipboard.")
        else:
            print(f"[-] API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Execution failed: {e}")

# 注册全局键盘钩子，监听触发信号
keyboard.add_hotkey('ctrl+alt+n', exploit_clipboard)
print("[*] Notion Injector is listening in the background... (Press Ctrl+Alt+N to trigger)")
keyboard.wait()
```

## ⚡ 自动化验证 (The Automation)

在终端中执行以下链式命令。第一部分将强行清理任何残留的 Python 挂起进程（$\color{red}{\textbf{防止快捷键冲突}}$），第二部分重新拉起监听器：

### 💻 PowerShell 命令

```powershell
taskkill /F /IM python.exe 2>$null ; python notion_injector.py
```

### 📋 操作流程

1. ⏳ 等待终端输出 `[*] Notion Injector is listening...`
2. 📝 复制任意文本到剪贴板
3. ⌨️ 按下 `Ctrl+Alt+N`
4. ✅ 看到 `[+] Payload successfully written` 提示
5. 📌 直接去 Notion 按 `Ctrl+V` 测试排版效果

$\color{blue}{\textbf{核心逻辑}}$：通过系统提示词强制 DeepSeek API 输出符合 Notion 原生 KaTeX 渲染规范的 Markdown 格式文本，实现一键格式化粘贴。