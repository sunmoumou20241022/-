# VRF（VPN Instance）详解

## 1. 什么是VRF（VPN Instance）？

虚拟路由转发（VRF, Virtual Routing and Forwarding），在华为设备中被称为 VPN 实例（VPN Instance）。

### 传统局域网的局限：
- 一台物理交换机只有一张全局路由表
- 如果出现相同的 IP 网段，路由表会直接冲突
- 导致后配置的接口报错或路由彻底瘫痪

### VRF 的平行宇宙效应：
VRF 技术可以将一台物理交换机在逻辑上切分为多台相互独立的"虚拟路由器"。每个 VPN 实例都拥有：
- 完全独立的路由表（RIB）
- 转发表（FIB）
- ARP 缓存表
- 接口归属

由此实现了在同一台设备上，相同 IP 地址空间的完美共存与彻底隔离。

## 2. 核心Access 端口入向打标（Ingress Tagging）机制

这也是你发现的"不需要配置LSW1和LSW2也能通"的底层秘密：

**数据流向：**
```
PC1（发送不带VLAN Tag的原始帧）
↓
LSW1（默认VLAN 1，透明转发）
↓
Core1 GE0/0/1（Access PVID=10，入向强行打上VLAN 10标签）
↓
Vlanif10（接收，剥离标签，扣入实例A路由表）
↓
路由转发至Vlanif100
↓
Server1
```

### 详细说明：
1. 当 PC1 发送不带任何 VLAN Tag 的原始以太网帧时，傻瓜交换机 LSW1 仅仅将其作为默认 VLAN 1 流量在本地进行无感透明转发。

2. 当这个不带标签的包抵达核心交换机 core1 的 GE0/0/1（配置为 Access pvid 10）时，核心层接口启动强行接管逻辑：只要入向报文没有标签，就强行塞给它一个 VLAN 10 的 Tag。

3. 带有 VLAN 10 标签的报文在交换机内部自然精准命中了 Vlanif10，而 Vlanif10 已经被我们划归给了 vpn-instance A。整个过程有条不紊。

## 3. VRP 系统接口抹除致命规律

### 系统行为：
- 接口绑定VPN 实例的命令会重置接口的三层网络属性

### 现网防坑金句：
> **先绑后配，IP 不退；先配后绑，全是白忙。**

必须严格遵循先 `ip binding vpn-instance`，后 `ip address` 的操作顺序。

## 4. 二三层拓扑与数据流向主视图

```mermaid
graph TD
    subgraph "CORE1 (核心交换机 LSW3)"
        subgraph "【平行宇宙: 实例 A】"
            Vlanif10["Vlanif10: 192.168.1.1/24<br>(网关)"]
            Vlanif100["Vlanif100: 192.168.2.1/24"]
        end
        subgraph "【平行宇宙: 实例 b】"
            Vlanif20["Vlanif20: 192.168.1.1/24"]
            Vlanif200["Vlanif200: 192.168.3.1/24"]
        end
        
        Core1_Core["<br>+-----------------------------------------+<br>|                                  |<br>+-----------------------------------------+"]
    end
    
    GE0001["GE0/0/1<br>(Access PVID=10)<br>入向强行打上VLAN 10标签"]
    GE0002["GE0/0/2<br>(Access PVID=20)<br>入向强行打上VLAN 20标签"]
    
    LSW1("[LSW1 傻瓜交换机]<br>(默认VLAN 1透明透传)"]
    LSW2("[LSW2 傻瓜交换机]<br>(默认VLAN 1透明透传)")
    
    PC1("[PC1 客户端]<br>IP: 192.168.1.100<br>网关: 192.168.1.1")
    PC3("[PC3 客户端]<br>IP: 192.168.1.100<br>网关: 192.168.1.1")
    
    Vlanif10 --> LSW1
    GE0001 --> LSW1
    LSW1 --> PC1
    
    Vlanif20 --> LSW2
    GE0002 --> LSW2
    LSW2 --> PC3
    
    style Vlanif10 fill:#f9f,stroke:#333,stroke-width:4px
    style Vlanif100 fill:#f9f,stroke:#333,stroke-width:4px
    style Vlanif20 fill:#f9f,stroke:#333,stroke-width:4px
    style Vlanif200 fill:#f9f,stroke:#333,stroke-width:4px
```

### 【数据流向轨迹（以PC1为例）】：
```
PC1 (发包) 
↓
LSW1 (保持原样) 
↓
Core1 GE0/0/1 (强行盖戳 VLAN 10) 
↓
Vlanif10 接收 → 剥离标签并扣入 [实例 A 路由表] → 路由转发至 Vlanif100 → Server1
```

## 5. 完整标准配置步骤（SOP 黄金指南）

### 阶段一：初始化二层通道（创建VLAN，划分物理接口）

```bash
<Huawei> system-view
[Huawei] sysname Core1
# 1. 批量创建业务所需的 VLAN
[Core1] vlan batch 10 20 100 200
# 2. 配置物理接口为 Access 模式并绑定各自 VLAN
[Core1] interface GigabitEthernet 0/0/1
[Core1-GigabitEthernet0/0/1] port link-type access
[Core1-GigabitEthernet0/0/1] port default vlan 10
[Core1] interface GigabitEthernet 0/0/2
[Core1-GigabitEthernet0/0/2] port link-type access
[Core1-GigabitEthernet0/0/2] port default vlan 20
[Core1] interface GigabitEthernet 0/0/3
[Core1-GigabitEthernet0/0/3] port link-type access
[Core1-GigabitEthernet0/0/3] port default vlan 100
[Core1] interface GigabitEthernet 0/0/4
[Core1-GigabitEthernet0/0/4] port link-type access
[Core1-GigabitEthernet0/0/4] port default vlan 200
[Core1-GigabitEthernet0/0/4] quit
```

### 阶段二：创建VPN 实例控制平面

```bash
# 1. 配置左侧业务实例 A
[Core1] ip vpn-instance A
[Core1-vpn-instance-A] ipv4-family
[Core1-vpn-instance-A-ipv4] quit
[Core1-vpn-instance-A] quit
# 2. 配置右侧业务实例 B
[Core1] ip vpn-instance B
[Core1-vpn-instance-B] ipv4-family
[Core1-vpn-instance-B-ipv4] quit
[Core1-vpn-instance-B] quit
```

### 阶段三：三层虚拟接口映射与IP 宣告（严格执行防坑顺序！）

```bash
# 1. 激活并绑定左侧宇宙 (实例 A) 链路
[Core1] interface Vlanif 10
[Core1-Vlanif10] ip binding vpn-instance A
[Core1-Vlanif10] ip address 192.168.1.1 24
[Core1] interface Vlanif 100
[Core1-Vlanif100] ip binding vpn-instance A
[Core1-Vlanif100] ip address 192.168.2.1 24
[Core1-Vlanif100] quit
# 2. 激活并绑定右侧宇宙 (实例 B) 链路
[Core1] interface Vlanif 20
[Core1-Vlanif20] ip binding vpn-instance B
[Core1-Vlanif20] ip address 192.168.1.1 24
[Core1] interface Vlanif 200
[Core1-Vlanif200] ip binding vpn-instance B
[Core1-Vlanif200] ip address 192.168.3.1 24
[Core1-Vlanif200] quit
```

## 6. 竞赛裁判级验证与排错矩阵

| 验证/排查目标 | 执行诊断命令 | 完美成功的期望输出指标 | 异常失败的表现与含义 |
|--------------|--------------|----------------------|-------------------|
| 检查实例三层IP 状态 | `display ip interface brief vpn-instance A` | Vlanif10与Vlanif100的IP 健在，且状态为up / up | 接口IP 显示为unassigned，意味着遭遇了"先配后绑"的系统擦除陷阱 |
| 审计实例私有路由表 | `display ip routing-table vpn-instance B` | 只能看到192.168.1.0/24和192.168.3.0/24的直连路由 | 路由表为空，或者里面离奇出现了192.168.2.0/24（说明发生了严重的路由泄漏失误） |
| 自证局域网二三层对接 | `display arp vpn-instance A` | 同时存在类型为 I 的本地网关条目与类型为 D-0 的终端动态MAC 条目 | 只有I没有D-0：代表下层终端（PC）的默认网关没有填写或填错，导致交换机收不到客户端的ARP 响应 |
| 查看物理通道数据吞吐 | `display interface GigabitEthernet 0/0/3` | Input与Output的数据包（packets）计数均大于0且持续跳动 | Input: 0 packets：代表对端服务器目前处于关机、崩溃或者eNSP 底层拓扑死锁卡死状态 |