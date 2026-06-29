# A1: Attention Is All You Need（Transformer 原始论文）

> **论文**：*Attention Is All You Need*
> **作者**：Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin
> **机构**：Google Brain, Google Research, University of Toronto
> **发表**：NeurIPS 2017 | arXiv:1706.03762
> **代码**：tensorflow/tensor2tensor

---

## 摘要

此前主流的序列转换模型基于复杂的 RNN 或 CNN 编码器-解码器架构，表现最好的模型还通过注意力机制连接编码器和解码器。本文提出了一种新的简单网络架构 **Transformer**，完全基于注意力机制，**摒弃了循环和卷积**。在两个机器翻译任务上的实验表明，这些模型在质量上更优，同时**并行化程度更高，训练时间显著缩短**。

- WMT 2014 英→德翻译：**28.4 BLEU**，比之前最佳集成结果高 2+ BLEU
- WMT 2014 英→法翻译：**41.8 BLEU**，8 块 GPU 训练 3.5 天，仅为文献最佳模型训练成本的一小部分
- 成功泛化到英语成分句法分析任务

---

## 1. 引言

**RNN 的问题**：
- LSTM 和 GRU 在序列建模中是 SOTA，但**固有的顺序性**阻碍了训练中的并行化
- 长序列中的信息传递受限于顺序计算，限制了长距离依赖的建模

**Transformer 的思路**：
- 不再依赖 RNN，完全用**注意力机制**来捕捉输入和输出之间的全局依赖关系
- 允许更高的并行化，在 8 块 P100 GPU 上仅需 **12 小时**即可达到 SOTA

---

## 2. 背景

此前减少顺序计算的工作：

| 模型 | 方法 | 长距离依赖路径长度 |
|------|------|------------------|
| Extended Neural GPU | 并行计算 | — |
| ByteNet | 扩张卷积 | O(log_k(n)) |
| ConvS2S | 卷积编码器-解码器 | O(n) |

**Transformer 的改进**：
- 将任意两个位置之间的操作数降到 **O(1)**（常数），代价是降低了有效分辨率
- 通过 **Multi-Head Attention** 来弥补分辨率下降

**Self-Attention 的先例**：
- 此前已在阅读理解、摘要生成、文本蕴含中使用
- 但 Transformer 是**第一个完全依赖自注意力**、不使用 RNN 或 CNN 的转换模型

---

## 3. 模型架构

### 3.1 整体结构：Encoder-Decoder

```
输入 (x₁,...,xₙ) → [Encoder] → 连续表示 z = (z₁,...,zₙ)
                                            ↓
输出 (y₁,...,yₘ) ← [Decoder] ← 自回归生成，每步消费前一步输出
```

### 3.2 Encoder Stack

- **N = 6 层**，每层结构相同
- 每层 **2 个子层**：
  1. Multi-Head Self-Attention
  2. Position-wise Feed-Forward Network
- 每个子层使用 **残差连接 + Layer Normalization**：
  ```
  output = LayerNorm(x + Sublayer(x))
  ```
- 所有子层和嵌入层输出维度：**d_model = 512**

### 3.3 Decoder Stack

- **N = 6 层**，每层结构相同
- 每层 **3 个子层**：
  1. **Masked** Multi-Head Self-Attention（掩码防止看到未来位置）
  2. Multi-Head Attention over Encoder Output（编码器-解码器注意力）
  3. Position-wise Feed-Forward Network
- 同样使用残差连接 + LayerNorm
- **Masked 的作用**：保证位置 i 的预测只依赖 i 之前的已知输出，保持自回归特性

---

### 3.4 Attention 机制

#### 3.4.1 Scaled Dot-Product Attention

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

| 符号 | 含义 | 维度 |
|------|------|------|
| Q (Query) | "我在找什么" | n × d_k |
| K (Key) | "别人有什么" | m × d_k |
| V (Value) | "别人的内容" | m × d_v |
| QK^T | 查询-键相似度矩阵 | n × m |
| √d_k | 缩放因子 | 标量 |

**为什么需要缩放？**

当 d_k 较大时，点积的方差也随之增大（均值为 0，方差为 d_k），导致 softmax 进入**梯度极小区域**。除以 √d_k 将方差归一化回 1。

#### 3.4.2 Multi-Head Attention

**动机**：单一注意力函数只能学习一种关联模式。多头允许模型同时关注不同位置的不同表示子空间。

**公式**：

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O$$

$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

**参数**：

| 参数 | 值 |
|------|-----|
| h（头数） | 8 |
| d_k = d_v | d_model / h = 64 |
| W_i^Q | d_model × d_k |
| W_i^K | d_model × d_k |
| W_i^V | d_model × d_v |
| W^O | hd_v × d_model |

**计算成本**：多头注意力的总计算成本与单头全维度注意力相近，因为每个头的维度降低了。

#### 3.4.3 Attention 的三种应用

| 应用 | Q 来源 | K,V 来源 | 说明 |
|------|--------|---------|------|
| Encoder Self-Attention | 上一层编码器输出 | 上一层编码器输出 | 每个位置关注输入序列的所有位置 |
| Decoder Self-Attention | 上一层解码器输出 | 上一层解码器输出（masked） | 每个位置只能关注之前的位置 |
| Encoder-Decoder Attention | 上一层解码器输出 | 编码器输出 | 解码器查询编码器的信息 |

---

### 3.5 Position-wise Feed-Forward Network

$$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$$

- 两层线性变换，中间是 ReLU 激活
- 对每个位置**独立且相同**地应用
- 输入/输出维度：d_model = 512
- 隐藏层维度：d_ff = 2048（扩展 4 倍）

**理解**：等价于两个 1×1 卷积核，对每个 token 做一次特征变换。

---

### 3.6 Embeddings 和 Softmax

- 学习的嵌入将 token 转为 d_model 维向量
- 编码器输入嵌入、解码器输入嵌入、Softmax 前线性层**共享同一权重矩阵**
- 嵌入层权重乘以 √d_model（因为嵌入值较小，乘以 √d_model 使其与位置编码量级匹配）

---

### 3.7 Positional Encoding

**问题**：Transformer 没有循环和卷积，无法感知序列顺序。

**方案**：在输入嵌入上叠加位置编码。

**Sinusoidal 公式**：

$$PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d_{\text{model}}})$$

$$PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d_{\text{model}}})$$

**特点**：
- 波长从 2π 到 10000·2π，形成几何级数
- **关键性质**：对于固定偏移 k，PE_{pos+k} 可以表示为 PE_pos 的线性函数 → 模型可以学习相对位置关系
- 实验显示，学习的位置编码与 sinusoidal 编码效果几乎相同（25.7 vs 25.8 BLEU）

---

## 4. 为什么选择 Self-Attention？

三种标准的比较：

| 层类型 | 每层复杂度 | 顺序操作数 | 最大路径长度 |
|--------|-----------|-----------|-------------|
| Self-Attention | O(n²·d) | O(1) | O(1) |
| Recurrent | O(n·d²) | O(n) | O(n) |
| Convolutional | O(k·n·d²) | O(1) | O(log_k(n)) |
| Restricted Self-Attention | O(r·n·d) | O(1) | O(n/r) |

**关键结论**：

1. **当 n < d 时**（大多数翻译句子满足此条件），Self-Attention 比 Recurrent **更快**
2. Self-Attention 的最大路径长度为 **O(1)**，远优于 Recurrent 的 O(n)
3. 注意力分布可解释性更强：不同的头学到不同的语法/语义任务

---

## 5. 训练

### 5.1 训练数据

| 任务 | 数据规模 | 分词方式 | 词表大小 |
|------|---------|---------|---------|
| EN→DE | ~4.5M 句对 | Byte-Pair Encoding | ~37K tokens |
| EN→FR | 36M 句子 | Word-Piece | 32K |

每个 batch 约 25K 源语言 + 25K 目标语言 token。

### 5.2 硬件与训练时间

| 模型 | 步数 | 每步耗时 | 总时间 |
|------|------|---------|--------|
| Base Model | 100K | ~0.4s | **12 小时** |
| Big Model | 300K | ~1.0s | **3.5 天** |

硬件：1 台机器，8 块 NVIDIA P100 GPU

### 5.3 优化器

**Adam**：β₁ = 0.9, β₂ = 0.98, ε = 10⁻⁹

**学习率调度**：

$$lrate = d_{\text{model}}^{-0.5} \cdot \min(step\_num^{-0.5},\ step\_num \cdot warmup\_steps^{-1.5})$$

- warmup_steps = 4000
- 前 4000 步：学习率线性增加
- 之后：按步数平方根反比衰减

### 5.4 正则化

| 方法 | 参数 | 效果 |
|------|------|------|
| Residual Dropout | P_drop = 0.1（Base）/ 0.3（Big） | 每个子层输出 + embedding + pos encoding 后施加 |
| Label Smoothing | ε_ls = 0.1 | 损害 perplexity，但提升 accuracy 和 BLEU |

---

## 6. 结果

### 6.1 机器翻译

| 模型 | EN→DE BLEU | EN→FR BLEU | EN→DE 训练成本 |
|------|-----------|-----------|---------------|
| Transformer (base) | 27.3 | 38.1 | 3.3×10¹⁸ FLOPs |
| **Transformer (big)** | **28.4** | **41.8** | 2.3×10¹⁹ FLOPs |
| ConvS2S Ensemble | 26.36 | 41.29 | 7.7×10¹⁹ FLOPs |

- Big model 比之前最佳集成高 **2+ BLEU**，训练成本仅为 1/3
- EN→FR 任务上，训练成本不到 ConvS2S 的 **1/4**

### 6.2 消融实验关键发现

| 变量 | 发现 |
|------|------|
| **头数** | 8 头最优；1 头下降 0.9 BLEU（25.8→24.9）；太多头也降 |
| **Key 维度** | 减小 d_k 会损害性能 → "判断兼容性并不容易" |
| **模型大小** | 更大更好；2 层仅 23.7 BLEU vs 6 层 25.8 BLEU |
| **Dropout** | P_drop=0.1 最优；去掉 dropout 降到 24.6 BLEU |
| **位置编码** | 学习式 vs Sinusoidal 几乎相同（25.7 vs 25.8 BLEU） |

### 6.3 英语成分句法分析

| 设置 | F1 |
|------|-----|
| 4 层 Transformer，仅 WSJ（~40K 句） | 91.3 |
| 4 层 Transformer，半监督（+17M 句） | 92.7 |

- 在仅用 WSJ 训练时，超过了 BerkeleyParser
- RNN 序列到序列模型在同等数据量下无法做到这一点

---

## 7. 结论

1. Transformer 是**第一个完全基于注意力**的序列转换模型
2. 训练速度比 RNN/CNN 架构**显著更快**
3. 在 WMT 2014 翻译任务上达到**新的 SOTA**
4. 泛化能力强，在句法分析任务上也表现优异

**未来方向**：
- 将注意力应用于其他模态（图像、音频、视频）
- 研究局部/受限注意力以处理大输入
- 使生成过程更少顺序化

---

## 与 LLM 安全的关系

> 本文理解 Transformer 架构是理解 LLM 安全的基础：

1. **Tokenizer → Embedding → Transformer** 是 LLM 处理文本的三层管道
2. **Self-Attention** 让每个 token 可以"看到"所有其他 token → Prompt Injection 得以在全局传播
3. **Positional Encoding** 是位置信息的唯一来源 → 攻击者可以通过位置操纵影响模型行为
4. **Multi-Head** 学到不同的关系 → 安全对齐可能只在某些头生效，其他头仍可被利用

---

## 参考信息

- 论文链接：https://arxiv.org/abs/1706.03762
- HTML 版本：https://arxiv.org/html/1706.03762v7
- 代码：tensorflow/tensor2tensor
- 发表：NeurIPS 2017

---

[[第一周第一日]] | [[论文/A4（Red-Teaming Language Models to Reduce Harms（Anthropic）.md]] | [[论文/F3（Safety Alignment Should Be Made More Than Just a Few Tokens Deep（浅层安全对齐，Qi et al.）.md]]