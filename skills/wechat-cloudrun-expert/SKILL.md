---
name: wechat-cloudrun-expert
description: 微信云托管（WeChatCloudRun）专家知识库，涵盖部署、容器调用、联调、环境变量和常见问题。Use when working with WeChat CloudRun services in the lovey-record mini program.
---

# 微信云托管（WeChatCloudRun）专家知识库

## 核心概念

微信云托管是腾讯云的容器托管服务，深度集成于微信生态：
- **服务**：一个 Docker 容器服务，有独立的 HTTP 入口
- **版本**：每次部署生成新版本，支持流量灰度
- **环境**：对应云开发环境（env），一个环境可有多个服务
- **wx.cloud.callContainer**：小程序直接调用云托管服务，自动附带微信鉴权

---

## 小程序端调用

### 初始化（app.js / main.js）

```js
wx.cloud.init({
  env: 'your-env-id',  // 云开发环境 ID
  traceUser: true
})
```

### callContainer 调用

```js
wx.cloud.callContainer({
  config: { env: 'your-env-id' },
  path: '/api/endpoint',           // 服务内的路径
  method: 'POST',
  header: {
    'content-type': 'application/json',
    'X-WX-SERVICE': 'service-name'  // 服务名称（必填）
  },
  data: { key: 'value' },
  success(res) {
    // res.data 是响应体
    // res.statusCode 是 HTTP 状态码
  },
  fail(err) {
    // err.errMsg
  }
})
```

**Promise 化：**

```js
const res = await wx.cloud.callContainer({
  config: { env: ENV_ID },
  path: '/api/records',
  method: 'GET',
  header: { 'X-WX-SERVICE': 'lovey-backend' }
})
```

### X-WX-SERVICE Header

`X-WX-SERVICE` 决定请求路由到哪个云托管服务，**必须和微信云托管控制台中的服务名一致**。

---

## 服务端接收微信鉴权信息

调用 `callContainer` 时，微信会自动注入以下 Header：

| Header | 内容 |
|--------|------|
| `x-wx-openid` | 调用用户的 openid |
| `x-wx-unionid` | 用户的 unionid（如已绑定开放平台） |
| `x-wx-appid` | 小程序的 AppID |
| `x-wx-from-openid` | 来源 openid（同 openid） |

服务端直接读取 Header，无需自己验签：

```js
// Node.js Express 示例
app.post('/api/records', (req, res) => {
  const openid = req.headers['x-wx-openid']
  if (!openid) return res.status(401).json({ error: 'unauthorized' })
  // 用 openid 查数据库...
})
```

---

## 环境变量配置

在微信云托管控制台 → 服务 → 版本配置 → 环境变量 中设置。

服务端代码读取：

```js
const DB_URL = process.env.DB_URL
const ENV = process.env.NODE_ENV || 'production'
```

**注意**：环境变量修改后需要重新部署（发布新版本）才生效。

---

## 本地开发与联调

### 方式一：云托管本地调试（HTTP 直连）

开发时 `wx.cloud.callContainer` 无法直接访问本地服务。可以：

1. 在小程序端根据环境切换请求方式：

```js
// cloud-request.js 中的模式切换
const IS_DEV = true  // 开发时手动切换

function request(path, options) {
  if (IS_DEV) {
    return uni.request({
      url: `http://192.168.x.x:3000${path}`,  // 本地服务地址
      ...options
    })
  } else {
    return wx.cloud.callContainer({
      config: { env: ENV_ID },
      path,
      header: { 'X-WX-SERVICE': 'lovey-backend' },
      ...options
    })
  }
}
```

2. 微信开发者工具 → 详情 → 本地设置 → 勾选**不校验合法域名**

### 方式二：云托管内网访问

同一环境下的云托管服务可通过内网互访：`http://服务名/path`（无需鉴权）

---

## 部署流程

### 方式一：微信云托管控制台手动部署

1. 打包代码为 Docker 镜像，或直接上传源码（需有 Dockerfile）
2. 控制台 → 服务 → 新建版本 → 上传代码包
3. 配置实例规格、环境变量、端口
4. 流量切换到新版本

### 方式二：CI/CD（GitHub Actions）

```yaml
# .github/workflows/deploy.yml
- name: Deploy to WeChat CloudRun
  run: |
    # 使用腾讯云 CLI 或微信云托管 CLI
    tcb framework:deploy
```

### Dockerfile 建议

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

---

## 服务配置参考

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| 最小实例数 | 0（开发）/ 1（生产） | 0 允许缩容到 0，冷启动约 3-10s |
| 最大实例数 | 5-10 | 根据并发量设置 |
| CPU | 0.25-1 核 | 一般业务 0.5 核够用 |
| 内存 | 512MB-1GB | Node.js 服务 512MB 够用 |
| 超时时间 | 60s | callContainer 默认超时 |
| 端口 | 3000/8080 | 服务监听端口 |

---

## 常见陷阱

### 冷启动延迟
最小实例为 0 时，无流量的服务冷启动需要 3-10 秒。方案：
- 设置最小实例 ≥ 1（增加费用）
- 客户端做加载态，容忍首次慢响应

### callContainer 调试
`callContainer` 失败时 `err.errMsg` 可能不够详细，检查：
1. 微信云托管控制台 → 服务 → 日志
2. `X-WX-SERVICE` 是否填写正确
3. 服务是否正在运行（版本状态）

### HTTP Header 大小写
微信注入的 openid 等 Header 是**全小写**（`x-wx-openid`），服务端读取时注意框架可能转换为驼峰。

### 跨服务调用
同环境内服务互调不走公网，但仍需服务在**运行**状态（不能访问已停止版本）。

### 文件上传
云托管服务不适合直接存文件（容器无状态）。用 `wx.cloud.uploadFile` 存云存储，服务端通过 `fileID` 读取。

---

## 费用相关

- 计费维度：请求次数 + 实例运行时长 + 流量
- 最小实例 = 0 时，无请求不计费（但有冷启动）
- 开发/测试环境建议最小实例 = 0
