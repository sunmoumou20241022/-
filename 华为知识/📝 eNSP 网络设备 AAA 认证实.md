# 📝 eNSP 网络设备 AAA 认证实

### 1. 实验目标

实现 AR1 能够通过 Telnet 协议访问 AR2，并使用指定的本地账号（AAA 模式）进行登录验证。

### 2. 关键配置步骤 (以服务端 AR2 为主)

### A. 基础网络连通

确保双方接口 IP 处于同一网段，且能互相 Ping 通。

- **AR1:** `172.168.10.1/24`
- **AR2:** `172.168.10.2/24`

### B. 配置 AAA 认证 (AR2)

代码段

`[AR2] aaa
[AR2-aaa] local-user hw password cipher 123      // 创建用户并加密密码
[AR2-aaa] local-user hw privilege level 3        // 设置管理权限(最高15)
[AR2-aaa] local-user hw service-type telnet      // 明确授权Telnet服务`

### C. 开启远程访问权限 (AR2)

代码段

`[AR2] user-interface vty 0 4                     // 进入虚拟终端线路
[AR2-ui-vty0-4] authentication-mode aaa          // 调用AAA认证数据库`

---

### 3. 命令避坑指南

- **视图切换**：执行 `telnet` 或 `save` 命令时，必须在 **用户视图** `< >` 下；配置命令则在 **系统视图** `[ ]` 下。
- **输入隐形**：在 Telnet 登录时，输入密码是不显示任何字符或星号的，输完直接回车即可。
- **权限问题**：若登录后无法进入系统视图，检查 `privilege level` 是否配置（通常管理级设为 3）。

---

### 4. 保存与备份

- **常规保存**：在 `< >` 视图执行 `save`，按 `y` 确认。
- **另存为**：`save filename.cfg` 可保存为特定名称文件。
- **设置启动项**：若更换了文件名，需执行 `startup saved-configuration filename.cfg` 指定下次读取该文件。
- **外部导出**：eNSP 中右键点击设备图标 -> **导出配置**，可直接存到电脑本地。

## 🔒 SSH (Stelnet) 配置核心步骤

我们还是以 **AR1 访问 AR2** 为例，在 **AR2** 上进行配置：

### 1. 开启 SSH 服务与生成密钥

SSH 必须有一对“钥匙”来加密数据。

代码段

`[AR2] rsa local-key-pair create
// 执行后直接回车，通常选择默认的 2048 位长度
[AR2] stelnet server enable`

### 2. 配置 AAA 用户 (SSH版)

用户配置与 Telnet 类似，但 `service-type` 要改。

代码段

`[AR2] aaa
[AR2-aaa] local-user hw password cipher 123
[AR2-aaa] local-user hw privilege level 3
[AR2-aaa] local-user hw service-type ssh    // 这里一定要改为ssh
[AR2-aaa] quit`

### 3. 配置 VTY 界面

这一步是很多新手容易漏掉的，你需要告诉 VTY 线路：**只允许 SSH 登录，拒绝 Telnet**。

代码段

`[AR2] user-interface vty 0 4
[AR2-ui-vty0-4] authentication-mode aaa
[AR2-ui-vty0-4] protocol inbound ssh       // 关键！只允许ssh流量进入
[AR2-ui-vty0-4] quit`

### 4. 必须配置 SSH 用户认证方式

华为设备要求显式定义 SSH 用户的认证模式（常用的是 password 认证）。

代码段

`[AR2] ssh user hw authentication-type password`

---

## 🚀 在 AR1 上如何连接？

在 AR1 上，你不能再敲 `telnet` 了，要使用 `stelnet` 命令。

**第一次连接时的“坑”：**

华为设备默认开启了“中间人攻击检测”，如果 AR1 不信任 AR2，连接会失败。

1. **方法一（正式）**：在 AR1 上开启首次认证：
    
    `[AR1] ssh client first-time enable`
    
2. **方法二（登录）**：回到用户视图访问：
    
    `<AR1> stelnet 172.168.10.2`
    

---

## 📊 SSH vs Telnet 对比总结

| **特性** | **Telnet** | **SSH (Stelnet)** |
| --- | --- | --- |
| **安全性** | 明文传输（不安全） | 加密传输（安全） |
| **默认端口** | 23 | 22 |
| **复杂度** | 配置简单 | 较复杂（需生成RSA密钥） |
| **推荐场景** | 内部实验、受信任局域网 | **所有生产环境** |