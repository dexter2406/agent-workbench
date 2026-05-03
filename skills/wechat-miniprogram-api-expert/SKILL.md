---
name: wechat-miniprogram-api-expert
description: 微信小程序 API 专家知识库，涵盖路由导航、网络请求、存储、UI 交互和 JS 运行时限制。Use when implementing WeChat Mini Program features in lovey-record.
---

# 微信小程序 API 专家知识库

## ⚠️ 运行时限制与兼容性（重要）

微信小程序 JS 运行时 **不是** 浏览器环境，以下 Web API **不可用**：

| 不可用 API | 替代方案 |
|-----------|--------|
| `URLSearchParams` | 手动字符串拼接 + `encodeURIComponent` |
| `URL` 构造函数 | 字符串操作 |
| `localStorage` / `sessionStorage` | `wx.setStorageSync` / `wx.getStorageSync` |
| `document` / `window` | 不适用，用小程序生命周期 |
| `fetch` | `wx.request` / `uni.request` |
| `XMLHttpRequest` | 同上 |

**Object.entries 编译陷阱**：HBuilderX/Babel 会把 `Object.entries()` 编译成 `require('@babel/runtime/helpers/Objectentries')`，该 helper 不存在于小程序 bundle 中。用 `Object.keys(obj).map(k => [k, obj[k]])` 替代。

**URL 参数不自动 decode**：通过 `wx.navigateTo` 或 `<navigator>` 跳转时，`onLoad(options)` 收到的参数是**原始编码字符串**，不会自动 `decodeURIComponent`。

```js
// onLoad 里必须手动 decode
onLoad(options) {
  const d = v => v ? decodeURIComponent(v) : v;
  this.apiBaseUrl = d(options.apiBaseUrl);
}
```

---

## 路由导航

```js
// 跳转新页面（可返回）
wx.navigateTo({ url: '/pages/foo/index?id=123' })

// 跳转并关闭当前页
wx.redirectTo({ url: '/pages/foo/index' })

// 关闭所有页面，跳转到应用首页
wx.reLaunch({ url: '/pages/index/index' })

// 返回上一页
wx.navigateBack({ delta: 1 })

// 切换 tabBar 页面
wx.switchTab({ url: '/pages/index/index' })
```

**传递复杂数据用 EventChannel（避免 URL encode 限制）：**

```js
// 发起方
wx.navigateTo({
  url: '/pages/detail/index',
  events: {
    acceptData: (data) => { console.log(data) }
  },
  success(res) {
    res.eventChannel.emit('sendData', { payload: complexObj })
  }
})

// 目标页面 onLoad
onLoad() {
  const channel = this.getOpenerEventChannel()
  channel.on('sendData', (data) => { this.payload = data.payload })
}
```

---

## 网络请求

项目使用 `cloud-request.js` 封装了两种模式：

**开发模式（uni.request）：**

```js
uni.request({
  url: `${apiBaseUrl}/api/endpoint`,
  method: 'POST',
  data: { key: 'value' },
  header: { 'content-type': 'application/json' },
  success(res) { /* res.data */ },
  fail(err) { /* err.errMsg */ }
})
```

**生产模式（wx.cloud.callContainer）：**

```js
wx.cloud.callContainer({
  config: { env: 'your-env-id' },
  path: '/api/endpoint',
  method: 'POST',
  header: { 'content-type': 'application/json', 'X-WX-SERVICE': 'service-name' },
  data: { key: 'value' },
  success(res) { /* res.data */ },
  fail(err) { }
})
```

---

## 本地存储

```js
// 同步（推荐用于简单场景）
wx.setStorageSync('key', value)        // value 可以是对象
const val = wx.getStorageSync('key')   // 不存在返回 ''
wx.removeStorageSync('key')

// 异步
wx.setStorage({ key: 'key', data: value, success() {}, fail() {} })
wx.getStorage({ key: 'key', success(res) { res.data }, fail() {} })
wx.clearStorage()
```

---

## UI 交互

**Toast：**

```js
wx.showToast({ title: '操作成功', icon: 'success', duration: 2000 })
wx.showToast({ title: '加载中', icon: 'loading', mask: true })
wx.hideToast()
```

**Modal（项目中 Promise 化封装）：**

```js
// 项目内封装模式（来自 home.vue）
const showModal = (title, content) => new Promise((resolve, reject) => {
  wx.showModal({
    title,
    content,
    success(res) { res.confirm ? resolve() : reject() },
    fail: reject
  })
})
```

**Loading：**

```js
wx.showLoading({ title: '加载中', mask: true })
wx.hideLoading()
```

**ActionSheet：**

```js
wx.showActionSheet({
  itemList: ['选项1', '选项2'],
  success(res) { console.log(res.tapIndex) },
  fail(res) { /* 取消时 errMsg: 'showActionSheet:fail cancel' */ }
})
```

---

## 剪贴板

```js
// Promise 化模式（来自 home.vue）
const copyToClipboard = (text) => new Promise((resolve, reject) => {
  wx.setClipboardData({
    data: text,
    success: resolve,
    fail: reject
  })
})

wx.getClipboardData({ success(res) { res.data } })
```

---

## SelectorQuery（获取节点信息）

```js
// 必须用 .in(this) 才能在组件内正确查询
const query = wx.createSelectorQuery().in(this)
query.select('#my-element').boundingClientRect(rect => {
  console.log(rect.height, rect.top)
}).exec()

// 获取滚动位置
query.selectViewport().scrollOffset(res => {
  console.log(res.scrollTop)
}).exec()
```

---

## 用户信息

```js
// 获取登录凭证（code → 后端换 openid）
wx.login({
  success(res) {
    // res.code 传给后端，后端调用 jscode2session 获取 openid
    callBackend('/auth/login', { code: res.code })
  }
})

// 获取用户信息（需要用户点击授权按钮触发）
// 注意：wx.getUserInfo 已废弃，使用 button open-type="getUserInfo"
// <button open-type="getUserInfo" @getuserinfo="onGetUserInfo">授权</button>
onGetUserInfo(e) {
  const { nickName, avatarUrl } = e.detail.userInfo
}
```

---

## 图片

```js
// 选择图片
wx.chooseMedia({
  count: 1,
  mediaType: ['image'],
  sourceType: ['album', 'camera'],
  success(res) {
    const tempFilePath = res.tempFiles[0].tempFilePath
  }
})

// 上传到云存储
wx.cloud.uploadFile({
  cloudPath: `images/${Date.now()}.jpg`,
  filePath: tempFilePath,
  success(res) { res.fileID }
})

// 预览图片
wx.previewImage({ urls: [imageUrl], current: imageUrl })
```

---

## Promise 化工具

uni-app 中大部分 wx API 都有 Promise 版本（`uni.xxx` 返回 Promise）：

```js
// uni-app 封装的 Promise 化版本
const [err, res] = await uni.request({ url: '...', method: 'GET' })
const [err, res] = await uni.getStorage({ key: 'userInfo' })
```

原生 wx API 手动 promisify：

```js
const promisify = (fn) => (options = {}) => new Promise((resolve, reject) => {
  fn({ ...options, success: resolve, fail: reject })
})
const wxLogin = promisify(wx.login)
const { code } = await wxLogin()
```

---

## 常见陷阱

- `wx.navigateTo` 最多 10 层页面栈，超出会失败 → 考虑用 `redirectTo`
- `setStorageSync` 单个 key 限制 1MB，总存储 10MB
- `wx.request` 域名必须在微信公众平台白名单中（开发时可关闭校验）
- `wx.cloud.callContainer` 需要先调用 `wx.cloud.init`
- `showToast` 和 `showLoading` 会互相覆盖，不能同时显示
