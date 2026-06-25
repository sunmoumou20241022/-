# ACL 访问控制列表实验

> **知识关联**：前置 → [[配置IP地址]] | 安全双盾 → [[📝 eNSP 网络设备 AAA 认证实]] | 二层基础 → [[VLAN 跨交换机通信]] [[STP生成树]]

![[ACL_img_1.png]]

## 1. 这个实验到底要干什么？（核心目标）

在企业网络中，网络里的任何一台电脑（普通员工、外来访客、IT系统管理员）如果都能通过网络远程登录（Telnet）到核心服务器或核心路由器上敲命令，是非常危险的。

**我们的最终目标：** 利用 **ACL（Access Control List，访问控制列表）** 技术充当"数字安检门"，实现精细化控制——**只允许管理员（R1的LoopBack 1）登录核心服务器（R3），而坚决拦截并丢弃普通用户（R1的LoopBack 0）的登录请求**。

## 2. 实验网络拓扑与流量方向 (ASCII Diagram)

在配置任何命令前，你的脑海里必须先建立起清晰的设备连线、接口、IP地址以及流量的走向图。

```
                OSPF Area 0 动态路由骨干域 (全网互通基础)

  [ R1 客户端 ]
  +---------------------------------------+
  | LoopBack 0: 10.1.1.1/24 (普通用户 A)   |
  | LoopBack 1: 10.1.4.1/24 (IT管理员 B)   |
  +-------------------+-------------------+
                      |
                (GE0/0/3) 10.1.2.1/24
                      |
                      | ======> [流量发起方向：R1 客户端 向 R3 发起远程请求]
                      v
                      |
                (GE0/0/3) 10.1.2.2/24
  [ R2 中转路由器 ]
  +---------------------------------------+
  | * 方式二：在此物理接口入方向挂安检门   |
  +-------------------+-------------------+
                      |
                (GE0/0/4) 10.1.3.2/24
                      |
                      v
                      |
                (GE0/0/3) 10.1.3.1/24
  [ R3 Telnet 服务器 ]
  +---------------------------------------+
  | 服务器目的管理IP: 10.1.3.1            |
  | * 方式一：在此设备的虚拟管理通道挂安检门|
  +---------------------------------------+
```

## 3. 实验全过程端到端深度剖析

### 阶段一：打通马路（手册中的步骤1与步骤2：IP地址与OSPF路由）

**网络逻辑与故障域分析 (Root Cause / Logical Domain)**：上层安全控制（ACL）必须建立在**网络层（Layer 3）路由可达**的基础之上。如果设备之间连路都不认识，数据包在中途就丢了，安检门就没有任何意义。因此，第一步必须通过 OSPF 动态路由协议，让全网所有的 IP 地址（包括 R1 的两个环回口逻辑地址）都互相认识。

**FACT（协议事实）**：在华为 VRP 操作系统中，配置完接口 IP 并将网段通过 `network` 命令宣告进 OSPF 区域后，路由器会通过发送 Hello 报文建立邻居，并在全网计算出最优的路由表项。

**基础打通命令：**

```text
# ===== R1 基础配置 =====
[R1] interface GigabitEthernet0/0/3
[R1-GigabitEthernet0/0/3] ip address 10.1.2.1 24
[R1-GigabitEthernet0/0/3] quit
[R1] interface LoopBack 0
[R1-LoopBack0] ip address 10.1.1.1 24
[R1-LoopBack0] quit
[R1] interface LoopBack 1
[R1-LoopBack1] ip address 10.1.4.1 24
[R1-LoopBack1] quit
[R1] ospf 1
[R1-ospf-1] area 0
[R1-ospf-1-area-0.0.0.0] network 10.1.1.1 0.0.0.0
[R1-ospf-1-area-0.0.0.0] network 10.1.2.1 0.0.0.0
[R1-ospf-1-area-0.0.0.0] network 10.1.4.1 0.0.0.0

# ===== R2 基础配置 =====
[R2] interface GigabitEthernet0/0/3
[R2-GigabitEthernet0/0/3] ip address 10.1.2.2 24
[R2-GigabitEthernet0/0/3] quit
[R2] interface GigabitEthernet0/0/4
[R2-GigabitEthernet0/0/4] ip address 10.1.3.2 24
[R2-GigabitEthernet0/0/4] quit
[R2] ospf 1
[R2-ospf-1] area 0
[R2-ospf-1-area-0.0.0.0] network 10.1.2.2 0.0.0.0
[R2-ospf-1-area-0.0.0.0] network 10.1.3.2 0.0.0.0

# ===== R3 基础配置 =====
[R3] interface GigabitEthernet0/0/3
[R3-GigabitEthernet0/0/3] ip address 10.1.3.1 24
[R3-GigabitEthernet0/0/3] quit
[R3] ospf 1
[R3-ospf-1] area 0
[R3-ospf-1-area-0.0.0.0] network 10.1.3.1 0.0.0.0
```

*（注：`0.0.0.0` 在 OSPF 的 network 命令中是反掩码，表示精确宣告某一个单 IP 地址。）*

**当前数据包的端到端流量路径 (Traffic Path)**： 配置完 OSPF 后，如果管理员从 R1 发起对 R3 的测试：

1. 报文从 R1 的 LoopBack 1 出发，查路由表：下一跳是 R2（`10.1.2.2`）。
2. 报文到达 R2 的 GE0/0/3 接口，R2 拆开网络层报文头，查路由表：去往 `10.1.3.1` 的最优路径是从 GE0/0/4 口直连丢给 R3。
3. 报文顺利到达 R3。由于目前还没有设防，任何人都能给 R3 发包。

### 阶段二：给服务器安上大门锁（手册中的步骤3：配置R3为Telnet服务器）

**原理解析**：远程登录（Telnet）工作在**应用层（Layer 7）**，其底层使用的是传输层 **TCP 协议的 23 号端口**。网络设备为了让别人能登进来，会在系统内部开辟一组专门接收管理流量的虚拟通道，技术上叫 **VTY（Virtual Type Terminal）用户界面**。

手册里的步骤3，就是让 R3 扮演服务器的角色，打开这扇网络管理的大门，并配上钥匙（密码 `Huawei@123`）。

**大门开启命令（在R3上配置）：**

```text
[R3] telnet server enable
[R3] user-interface vty 0 4
[R3-ui-vty0-4] user privilege level 3
[R3-ui-vty0-4] set authentication password cipher Huawei@123
[R3-ui-vty0-4] quit
```

*（注：`vty 0 4` 代表打开 0,1,2,3,4 这 5个虚拟远程通道，允许最多 5 个人同时登录到这台路由器上。）*

### 阶段三：配置安检过滤器（手册中的步骤4：ACL 流量过滤）

现在全网通了，R3 登录服务也开好了。此时，普通用户和管理员都能登录。为了实现隔离，手册在步骤4给出了**两种挂载安检过滤器的方案**。我们分别来看它们的运行逻辑：

#### 方案一：在服务器 R3 的家门口安检（联动 VTY 虚拟通道）

这种方案的逻辑是：让所有人一路上绿灯，把报文欢天喜地地送到 R3 路由器大门口（VTY 接口）。但在进入密码认证前，R3 检查高级 ACL 3000。如果发现不是管理员的 IP，就地在 R3 协议栈内销毁报文。

**方案一配置命令（在 R3 上执行）：**

```text
[R3] acl 3000
[R3-acl-adv-3000] rule 5 permit tcp source 10.1.4.1 0.0.0.0 destination 10.1.3.1 0.0.0.0 destination-port eq 23
[R3-acl-adv-3000] rule 10 deny tcp source any
[R3-acl-adv-3000] quit

[R3] user-interface vty 0 4
[R3-ui-vty0-4] acl 3000 inbound
[R3-ui-vty0-4] quit
```

#### 方案二：在中途马路边上拦截（在干线路由器 R2 的物理接口过滤）

这种方案的逻辑更先进：将拦截点前移。普通用户（`10.1.1.1`）刚尝试发包通过 R2 的 GE0/0/3 接收物理口时，R2 通过硬件芯片直接读取报文，命中 `rule 10 deny`，**当场在中途把报文丢弃**。这样做的好处是不会浪费后续的网络带宽，也完全不占用核心服务器 R3 的 CPU 算力。

**方案二配置命令（在 R2 上执行）：**

```text
[R2] acl 3001
[R2-acl-adv-3001] rule 5 permit tcp source 10.1.4.1 0.0.0.0 destination 10.1.3.1 0.0.0.0 destination-port eq 23
[R2-acl-adv-3001] rule 10 deny tcp source any
[R2-acl-adv-3001] quit

[R2] interface GigabitEthernet 0/0/3
[R2-GigabitEthernet0/0/3] traffic-filter inbound acl 3001
[R2-GigabitEthernet0/0/3] quit
```

## 4. 预期成功现象与失败症状诊断 (Outputs & Symptoms)

### VERIFIED RESULT：关键的成功验证

当管理员（`10.1.4.1`）在 R1 上执行登录时，由于完全命中了 `rule 5 permit` 放行规则，能够顺利建立连接。

在 R3（方案一）或 R2（方案二）上输入查看命令，**这是网络大赛和工程中评判分数的绝对核心关键步（Scoring-Critical Step）**：

```text
<R2> display acl 3001
Advanced ACL 3001, 2 rules
Acl's step is 5
 rule 5 permit tcp source 10.1.4.1 0 destination 10.1.3.1 0 destination-port eq telnet (21 matches)
 rule 10 deny tcp (1 matches)
```

**回显解读**：如果你看到规则5末尾带有 `(21 matches)` 的回显，代表你的规则完全写对了，并且硬件策略已经精准捕获并放行了 21 个来自管理员的合法数据包。

### FAILURE SYMPTOM：失败症状回显

当普通用户（`10.1.1.1`）在 R1 上尝试违规远程登录 R3 时：

```text
<R1> telnet -a 10.1.1.1 10.1.3.1
Press CTRL] to quit telnet mode
Trying 10.1.3.1 ...
Error: Can't connect to the remote host
```

**失败现象解读**：回显提示 `Error: Can't connect to the remote host`。

**背后的网络底层本质**：由于普通用户的数据包触发了安全过滤器中的 `rule 10 deny tcp`，路由器直接在入方向剥离并静默丢弃（Drop）了该 TCP 同步报文（SYN）。普通用户的电脑在规定时间内没有得到任何来自服务器的应答，导致传输层三次握手根本无法建立，从而直接报错断开。

## 5. 事实与推论归类证明

**FACT（确认事实）**：华为高级 ACL（3000-3999）匹配顺序是**自上而下、一命中即停止**的。如果一个报文已经命中了前面的允许（permit）规则，后续的拒绝（deny）规则对它将完全失效。

**ASSUMPTION（工程推论）**：在本实验中，由于我们没有真实的外界物理电脑主机，因此在 R1 上使用 `LoopBack 0` 和 `LoopBack 1` 接口来**模拟**两个完全独立不同的业务网段客户端，这是极其高效且合理的硬件仿真手段。

**HYPOTHESIS（故障假设）**：如果在测试时发现普通员工和管理员都无法登录成功，可能存在的假设是：调用 ACL 过滤时的流量方向挂反了（比如把 `inbound` 误写成了 `outbound`），导致服务器发出来的回包被安全策略误杀。

## 6. 核心精简总结

**实验本质**：利用高级 ACL 精准识别网络层 IP 头部和传输层 TCP 端口号，实现网络管理权限的精细化、差异化控制。

**避坑关键得分点：**

1. 精确匹配单 IP 时，反掩码必须写成 `0.0.0.0`（代表 32 位全匹配）。
2. 在接口下挂载流量过滤时，必须是流量流入的系统方向，即 **inbound**。
3. 实验配置后，务必使用 `display acl [编号]` 观察是否有增加的匹配计数（`matches`），这是工业运维验收的最高标准。

---


![[Pasted image 20260623165629.png]]


# ACL 进阶实验（4.1：多业务精细化控制与终极拦截防线）

上面的基础实验只区分了"管理员放行 vs 所有人拒绝"两种极简情况。但在真实企业网中，**不同角色、不同业务需要不同的访问权限**——管理员可以 Telnet 远程管设备，普通员工只能 FTP 传文件，而一切未授权的流量必须全部击杀。这就是 4.1 进阶实验要解决的核心命题。

## 1. 协议层级别与控制域本质 (Root Cause & Logical Domain)

**协议层级别**：网络层（Layer 3 - IP 头部审查）与传输层（Layer 4 - TCP 端口精准卡控）。

**控制域核心本质（FACT）**：高级访问控制列表（ACL 3001）部署在网络区域的交界处（中转路由器 R2），充当网络的"硬件安检门"。它通过精细化识别流量的"源 IP、目的 IP、协议类型、目标端口"四个维度，人为将全网互通的动态路由域，划分为**允许管理域**、**允许业务域**、以及**拒绝未授权域**，实现最小特权原则的安全闭环。

## 2. 实验最终控制拓扑与流量路径 (ASCII Diagram & Traffic Path)

```
  [ R1 客户端多业务模拟 ]
  +-------------------------------+
  | Lo0 (员工网段): 10.1.1.1/24    | ----> 发起 FTP 访问 (TCP 20/21) --+
  | Lo1 (管理员网段): 10.1.2.1/24  | ----> 发起 Telnet 访问 (TCP 23) --+
  +---------------+---------------+                                    |
                  |                                                    |
            (物理口流入)                                                |
                  v                                                    v [流量方向]
            (GE0/0/3) 10.1.2.2/24                                      |
  [ R2 中转安全网关 ] =====================================================+
  | 接口入方向捆绑 ACL 3001 硬件流水线：                                   |
  |  - 关卡 1 (rule 5):  比对管理员的 Telnet 23 端口，符合则放行         |
  |  - 关卡 2 (rule 10): 比对员工的 FTP 20/21 端口，符合则放行           |
  |  - 关卡 3 (rule 15): 终极拦截所有其余未知 TCP 流量，直接击杀            |
  +---------------+----------------------------------------------------+
                  | (过滤后干净的合法流量)
                  v
            (GE0/0/3) 10.1.3.1/24
  [ R3 核心服务器 ] (提供 Telnet 与 FTP 响应)
```

### 端到端流量路径审查逻辑 (Traffic Path)

- **管理员流量**：源 `10.1.2.1`，目的端口 `23` → 撞击 R2 接口 → 命中 `rule 5` → 执行 `permit` 放行 → 顺利直达 R3。
- **普通员工流量**：源 `10.1.1.1`，目的端口 `21/20` → 撞击 R2 接口 → 错过 `rule 5` → 命中 `rule 10` → 执行 `permit` 放行 → 顺利直达 R3。
- **非法/未知流量**：任意源 IP，非允许的端口 → 撞击 R2 接口 → 连续错过 `rule 5` 和 `rule 10` → 命中末尾的 `rule 15` 终极拦截 → 执行 `deny` → 报文在 R2 缓冲区被硬件直接丢弃（Drop），无法到达 R3。

## 3. 终极完整配置命令行 (Configuration)

在中转路由器 R2 的物理边界接口入方向，部署完整的、带有步长预留和终极拦截策略的高级 ACL：

```text
[R2] acl 3001
[R2-acl-adv-3001] rule 5 permit tcp source 10.1.2.1 0.0.0.0 destination 10.1.3.1 0.0.0.0 destination-port eq 23
[R2-acl-adv-3001] rule 10 permit tcp source 10.1.1.1 0.0.0.0 destination 10.1.3.1 0.0.0.0 destination-port range 20 21
[R2-acl-adv-3001] rule 15 deny tcp source any
[R2-acl-adv-3001] quit

[R2] interface GigabitEthernet 0/0/3
[R2-GigabitEthernet0/0/3] traffic-filter inbound acl 3001
[R2-GigabitEthernet0/0/3] quit
```


#### 步骤一：在 R3 上把 FTP 的房间盖起来（开启应用服务与数据库）

代码段

```
[R3] ftp server enable                                     // 开启应用层 FTP 守护进程（打开 TCP 21端口）
[R3] aaa                                                   // 进入本地安全认证平面
[R3-aaa] local-user admin password cipher Huawei@123       // 创建员工专属登录账号和密码
[R3-aaa] local-user admin privilege level 15               // 关键步：赋予高级别权限，否则系统会报无权浏览
[R3-aaa] local-user admin service-type ftp                // 限定该本地账户的服务类型为 FTP
[R3-aaa] local-user admin ftp-directory flash:/           // 核心步：绑定员工登录进服务器后的文件根目录
[R3-aaa] quit
```

#### 步骤二：在 R1 客户端上发起正式的 FTP 联调登录

根据你写的 OSPF 规划 ，为了精准触发 R2 接口上针对普通员工 `10.1.1.1` 的安全规则 ，你在 R1 上敲击连接命令时，**必须带上 `-a` 参数来强制绑定你发送报文的源 IP 地址**：

代码段

```
<R1> ftp -a 10.1.1.1 10.1.3.1
```

### 4. 预期完全成功状态与回显查看 (Expected Output)

当你把剩下的这一半服务器命令补齐后，在 R1 上执行登录，就会看到以下健康的、全业务交付的成功提示：

代码段

```
<R1> ftp -a 10.1.1.1 10.1.3.1
Trying 10.1.3.1 ...
Connected to 10.1.3.1.
220 FTP service ready.                                     // 证明 R3 的 FTP 应用层大门已经彻底打开！
User(10.1.3.1:(none)): admin                               // 输入你在 R3 上创建的本地用户名
331 Password required for admin.
Enter password:                                            // 输入密码 Huawei@123 (隐式不回显)
230 User logged in.                                        // 【全业务通车指标A：提示登录完全成功！】

ftp> ls                                                    // 【全业务通车指标B：测试数据通道 20 端口】
200 PORT command successful.
150 Opening ASCII mode data connection for directory list.
drwxrwxrwx   1 no_user  no_group            0 Jun 23 2026  flash:/
226 Transfer complete.                                     // 双通道全部放行，成功读取并下载文件！
ftp> quit
```

#### VERIFIED RESULT：在 R2 上审计全状态计数器

此时，来到负责边界安检的 **R2** 上输入审计命令（**这是判定实验100%全通的终极得分依据**）：

代码段

```
<R2> display acl 3000
Advanced ACL 3000, 2 rules
Acl's step is 5
 rule 5 permit tcp source 10.1.2.1 0 destination 10.1.3.1 0 destination-port eq telnet (15 matches)
 rule 10 permit tcp source 10.1.1.1 0 destination 10.1.3.1 0 destination-port range ftp-data ftp (36 matches)
```

- **回显解读**：如果你看到 `rule 5` 有匹配计数（代表昨天的 Telnet 通了），同时看到 `rule 10` 的末尾也跳出了 **`(36 matches)`**（代表今天的 FTP 也通了），这才叫**真正的全网全业务 100% 完工**。
    

### 5. 现阶段不补齐引发的失败症状 (Failure Symptoms)

如果你现在不补齐 R3 的另外一半配置，直接在 R1 上盲目敲击 FTP 登录，会遭遇以下典型的应用层断头报错：

代码段

```
<R1> ftp -a 10.1.1.1 10.1.3.1
Trying 10.1.3.1 ...
Error: Remote host refused the connection.                 // <=== 典型的“业务未开启”报错现象
```

- **故障底层诊断**：回显提示 `Remote host refused the connection`（远端主机拒绝连接）。这用工程事实证明了网络的 Layer 3（路由）和 Layer 4（中途放行）全部通畅 ；数据包已经安全送达终点，但正因为 R3 的 **Layer 7（没有开启 FTP 进程）** ，才导致了业务彻底卡死在一半的位置。

- `rule 5`：管理员 `10.1.2.1` 只允许远程管理（Telnet TCP 23），精确到单个端口，最小权限。
- `rule 10`：员工 `10.1.1.1` 只允许文件传输（FTP TCP 20/21），**必须用 `range 20 21` 同时开放控制通道和数据通道**（详见下方 FTP 双通道铁律）。
- `rule 15`：**终极拦截防线（兜底 deny）**——所有既不是管理员 Telnet、也不是员工 FTP 的 TCP 流量，全部击杀。这行是安全闭环的底线。
- 步长（Step）为 5，所以三条规则的编号是 5、10、15，中间留出的空档（6-9、11-14）用于未来随时精准插入新的补丁策略，而不破坏原有配置。

## 4. 预期成功现象与查看回显 (Outputs & Verified Result)

### VERIFIED RESULT：核心验证命令查看

当网络正常通信后，在 R2 上输入查看命令。在职业技能大赛与真实企业工程中，这是评判策略是否正确交付的唯一得分判定步（Scoring-Critical Step）：

```text
<R2> display acl 3001
Advanced ACL 3001, 3 rules
Acl's step is 5
 rule 5 permit tcp source 10.1.2.1 0 destination 10.1.3.1 0 destination-port eq telnet (12 matches)
 rule 10 permit tcp source 10.1.1.1 0 destination 10.1.3.1 0 destination-port range ftp-data ftp (48 matches)
 rule 15 deny tcp (235 matches)
```

**成功回显解读**：

1. 系统自动将 `range 20 21` 翻译为 `range ftp-data ftp`，证明双通道语法完全生效。
2. `rule 15` 末尾跳出 `(235 matches)`，用铁的事实证明终极拦截策略正在高效工作，成功在边界击杀了 235 个意图不轨或计划外的非法数据包。

## 5. 故障失败症状现象解析 (Failure Symptoms)

### 症状一：FTP 业务出现"能登录、敲命令卡死超时"的半死不活现象

**故障根源（HYPOTHESIS）**：在编写 `rule 10` 时，漏掉了 20 端口，误写成了 `eq 21`。

**临床报错回显（FAILURE SYMPTOM）**：

```text
ftp> user admin
230 User admin logged in.   <=== 控制通道(21)正常，登录成功！
ftp> ls
200 PORT command successful.
Error: Connection timed out. <=== 数据通道(20)被末尾的 rule 15 误杀，传输卡死超时！
```

**底层本质**：FTP 是双通道协议——21 号端口只管命令交互（控制通道），20 号端口才管真正的数据搬运（数据通道）。如果只放行了 21 而漏掉了 20，用户能登录成功但永远无法获取文件列表或传输数据，因为数据包被 `rule 15` 的兜底 deny 给击杀了。

### 症状二：全网所有合法的 Telnet 和 FTP 业务瞬间全部瘫痪

**故障根源（HYPOTHESIS）**：误将终极拦截策略（deny）排在了流水线的最前排（例如错编成了 `rule 3`）。

**临床报错回显（FAILURE SYMPTOM）**：所有人一进门就直接撞在 deny 上被硬件抹除，后面的放行代码彻底沦为读不到的"死代码"，客户端无一例外全部弹窗：`Error: Can't connect to the remote host`。

## 6. 进阶实验核心总结 (Short Bullet Summary)

**四大核心机制**：

1. **一命中即停止（FACT）**：数据包自上而下比对规则，一旦在某个关卡匹配成功（不论 permit 还是 deny），立刻带着结果离场，后续规则直接锁定。
2. **步长预留机制（FACT）**：华为默认步长（Step）为 5。留出的数字空档（如 6, 7, 12）用于在不破坏原有配置的情况下，随时精准插入新的补丁策略。
3. **FTP 双通道铁律（FACT）**：FTP 是特殊协议，21 号管命令控制，20 号管数据搬运。放行 FTP 必须使用 `range 20 21` 同时开放这两个端口，否则业务必然卡死超时。
4. **终极拦截防线（FACT）**：华为物理接口挂载过滤时，隐式动作为默认放行。必须在 ACL 的最末尾（如 rule 15）手动补齐 `deny tcp source any` 进行兜底，才能真正关上网络的安全大门。






# ==OSPF和"area 0“和”network“==
OSPF 是”动态路由“
在 OSPF 协议的设计标准中，`Area 0` 被定义为唯一的核心骨干区域
### Root Cause (协议层与逻辑路由域分析)

- **协议层级别**：网络层（Layer 3 - 动态路由控制平面）。
    
- **为什么需要 OSPF（FACT）**：在没有配置这三行命令前，R1 只知道自己直连的接口，完全不知道远端 R3（`10.1.3.1`）在哪里。如果使用静态路由，网络规模变大时需要人工手写成百上千条命令。而 **OSPF（Open Shortest Path First，开放最短路径优先）** 是一种动态路由协议，它让路由器之间自动发送报文、互相拜访、交换各自知道的网段信息，最终在每台设备的系统内部自动算出一张全网互通的最优路由表。
    

### 2. OSPF 骨干域网络拓扑与控制流 (ASCII Diagram & Traffic Path)

这三行命令在你的整体网络中构建了如下的 **OSPF Area 0 骨干路由域**：

```
+-------------------------------------------------------------------------+
|                       OSPF Area 0 骨干路由区域                          |
|                                                                         |
|     [ R1 路由器 ]                   [ R2 路由器 ]               [ R3 ]  |
|  +-----------------+             +-----------------+             +----+ |
|  | Lo0: 10.1.1.1   |             |                 |             |    | |
|  |   (宣告进Area 0)|             |                 |             |    | |
|  +--------+--------+             +--------+--------+             +--+-+ |
|           | g0/0/0                        | g0/0/0                  |   |
|           | 10.1.2.1                      | 10.1.2.2                |   |
|           +============== Hello 报文 =====>+                         |   |
|           |         (建立 OSPF 邻居)       |                         |   |
|           |                                |                         |   |
|           | <====== 传递 10.1.1.1 路由 ====+= 向右继续传递 ==========>|   |
+-----------+--------------------------------+-------------------------+---+

【控制流与路径 (Traffic Path)】：
1) R1 启动 OSPF 进程 ，在骨干域 Area 0  精确捕获 LoopBack 0 接口（10.1.1.1）。
2) R1 的 g0/0/0 接口向外发送 OSPF Hello 报文，发现邻居 R2 [cite: 19]。
3) R1 把自己的地图（“我知道怎么去 10.1.1.1”）封装成 LSA（链路状态通告），通过 R2 一路传给 R3。
4) R3 自动学习到去往 10.1.1.1 的地图，路由打通。
```

### 3. 命令逐行深度拆解（是什么意思）

根据你发来的 Word 文档脚本 ，我们把这三行命令拆开来揉碎了讲：

① `[R1] ospf` （或 `ospf 1`）

- **大白话**：**“大喊一声：开启 OSPF 动态路由功能！”**
    
- **网络本质**：告诉路由器的 CPU，在系统后台启动一个 OSPF 路由协议进程。如果没有这一步，路由器就是个“哑巴”，绝不会向外发送任何路由协议报文。
    

② `[R1-ospf-1] area 0`

- **大白话**：**“划分地盘：创建并进入 0 号核心区域（骨干区域）。”**
    
- **网络本质**：OSPF 为了防止全天下路由器太多、地图太大导致 CPU 算不过来，把网络划分成不同的“房间”，技术上叫**区域（Area）**。
    
- **现网铁律（FACT）**：**`Area 0` 是 OSPF 的中心骨干区域（Backbone Area）**。全网所有的其他区域（比如 Area 1、Area 2）都必须像车轮的轮轴一样，直接物理或逻辑连接在 Area 0 上。你在所有设备上都写 `area 0`，代表让 R1、R2、R3 坐进同一个核心大房间里直接开会 。
    

③ `[R1-ospf-1-area-0.0.0.0] network 10.1.1.1 0.0.0.0`

- **大白话**：**“画出安检范围：精准把 10.1.1.1 这个接口抓进 Area 0，并向全世界广播它！”**
    
- **网络本质**：这行 `network`（宣告）命令在 OSPF 内部具有**两个同时生效**的底层核心行为：
    
    1. **点名激活接口**：路由器身上有很多接口。这行命令告诉 OSPF，去检查哪个接口的 IP 刚好是 `10.1.1.1` 。一旦找到了（比如你的 LoopBack 0） ，就让这个接口开始对外发送 OSPF Hello 报文去交朋友。
        
    2. **制作地图并广播**：把 `10.1.1.1` 这个接口的网段信息打包放进自己的地图册里，通过 OSPF 邻居关系，大声广播给全网的 R2 和 R3，让整个网络的设备都自动学会怎么走这条路由。
        
- **这里的 `0.0.0.0` 是什么鬼？**
    
    它在路由宣告里叫 **“反掩码（Wildcard Mask）”**。它的二进制规则是：**0 代表必须严格死磕、一模一样；255 代表无所谓、什么数字都行**。
    
    - 你写的是 `10.1.1.1 0.0.0.0`，四个位置全都是 0。这意味着系统在抓取接口时，必须 100% 精确匹配 `10.1.1.1` 这一个单 IP 接口 ，多一点少一点都不行（这属于**工业标准中的精确接口宣告**）。