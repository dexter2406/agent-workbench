---
name: wechat-miniprogram-performance-expert
description: 微信小程序性能优化专家知识库，涵盖启动、渲染、setData、内存和网络优化。Use when optimizing performance in the lovey-record mini program.
---

# 微信小程序性能优化专家知识库

## 性能指标目标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 首屏渲染时间 | < 1500ms | 从打开到首屏内容展示 |
| setData 调用数据量 | < 256KB/次 | 超出会有性能告警 |
| setData 调用频率 | < 20次/秒 | 高频 setData 导致卡顿 |
| 代码包大小 | < 1.5MB（主包） | 超出无法预览/发布 |
| 图片单张 | < 1MB | 建议使用 CDN + 压缩 |
| 内存占用 | < 200MB | 超出会被系统回收 |

---

## 启动性能优化

### 1. 代码包瘦身

```bash
# 检查代码包内容
# 微信开发者工具 → 工具 → 代码质量 → 代码依赖分析
```

- 删除未使用的组件和页面
- 图片文件不要放在代码包里，用 CDN
- 避免引入大型 npm 库（如 moment → dayjs，lodash 按需引入）
- JSON 配置文件精简 `usingComponents`，只引入实际用到的组件

### 2. 分包加载

```json
// app.json
{
  "pages": ["pages/index/index"],  // 主包页面
  "subpackages": [
    {
      "root": "pages/menstrual",
      "name": "menstrual",
      "pages": ["home/index", "detail/index"]
    }
  ],
  "preloadRule": {
    "pages/index/index": {
      "network": "all",
      "packages": ["menstrual"]  // 在首页预加载分包
    }
  }
}
```

### 3. 按需注入（按需加载组件逻辑）

```json
// app.json
{
  "lazyCodeLoading": "requiredComponents"
}
```

---

## setData 优化（最重要）

### 问题：全量更新大对象

```js
// ❌ 错误：每次更新都传递整个列表
this.setData({ list: this.data.list })

// ✅ 正确：只更新变化的字段，用路径索引
this.setData({ [`list[${index}].selected`]: true })
```

### 问题：频繁 setData

```js
// ❌ 错误：循环内多次 setData
for (let i = 0; i < items.length; i++) {
  this.setData({ [`items[${i}].done`]: true }) // 触发多次渲染
}

// ✅ 正确：合并成一次 setData
const updates = {}
for (let i = 0; i < items.length; i++) {
  updates[`items[${i}].done`] = true
}
this.setData(updates)
```

### 问题：在 scroll 事件中 setData

```js
// ❌ 错误：scroll 频繁触发 setData
onScroll(e) {
  this.setData({ scrollTop: e.detail.scrollTop })
}

// ✅ 正确：节流
onScroll: throttle(function(e) {
  this.setData({ scrollTop: e.detail.scrollTop })
}, 100)
```

### 非渲染数据不放 data

```js
// ❌ 错误：把不用于渲染的数据放 data（会触发 diff）
this.setData({ internalTimer: null })

// ✅ 正确：直接挂在 this 上
this._timer = null
```

---

## 渲染优化

### 长列表虚拟化

对于超过 50 条的列表使用 `<recycle-view>`（官方组件）或懒加载分段：

```js
// 分批加载策略
loadNextBatch() {
  const nextItems = this.allItems.slice(this.loadedCount, this.loadedCount + 20)
  this.setData({
    [`items[${this.loadedCount}]`]: nextItems[0],
    // ... 或用 concat 更新，配合 scroll-view 的 lower-threshold
  })
  this.loadedCount += 20
}
```

### WXML 优化

```html
<!-- ❌ 避免：深层嵌套 -->
<view><view><view><view>content</view></view></view></view>

<!-- ✅ 使用 wx:key 加速列表渲染 -->
<view wx:for="{{list}}" wx:key="id">{{item.name}}</view>

<!-- ✅ 用 hidden 替代 wx:if（已渲染的元素频繁切换） -->
<view hidden="{{!show}}">频繁切换的内容</view>
<!-- wx:if 适合初始化时条件渲染，hidden 适合运行时切换 -->
```

---

## 网络请求优化

### 并发请求合并

```js
// ❌ 串行请求
const user = await getUser()
const records = await getRecords()

// ✅ 并行请求
const [user, records] = await Promise.all([getUser(), getRecords()])
```

### 缓存策略

```js
async function getCachedData(key, fetcher, ttlMs = 5 * 60 * 1000) {
  const cached = wx.getStorageSync(key)
  if (cached && Date.now() - cached.timestamp < ttlMs) {
    return cached.data
  }
  const data = await fetcher()
  wx.setStorageSync(key, { data, timestamp: Date.now() })
  return data
}
```

### 图片优化

- 使用 CDN 并指定尺寸参数（如 `?imageMogr2/thumbnail/200x200`）
- `<image>` 组件加 `lazy-load` 属性
- 避免 base64 大图（直接用临时文件路径或云文件 ID）

```html
<image src="{{url}}" lazy-load mode="aspectFill" />
```

---

## 内存管理

### 页面销毁时清理

```js
onUnload() {
  // 清除定时器
  clearInterval(this._timer)
  // 取消长连接/监听
  this._socketTask && this._socketTask.close()
  // 解除全局事件监听
  getApp().globalBus.off('event', this._handler)
}
```

### 避免闭包持有大对象

```js
// ❌ 闭包持有整个 data
const snapshot = this.data
setTimeout(() => { console.log(snapshot.bigList) }, 1000)

// ✅ 只持有需要的值
const id = this.data.id
setTimeout(() => { console.log(id) }, 1000)
```

---

## 分析工具

- **微信开发者工具 → Audits**：自动检测性能问题，给出体验评分
- **微信开发者工具 → Performance**：录制帧率、setData 耗时
- **微信开发者工具 → Wxml**：查看节点树层级
- **`wx.reportPerformance(id, value)`**：上报自定义性能指标到微信后台

---

## 常见陷阱

- `wx:for` 不加 `wx:key` 导致全量重排
- 在 `onShow` 里做大量数据计算（每次切回页面都执行）
- 全局 `app.globalData` 放过大的数据对象（整个 App 生命周期不释放）
- `setData` 传递 `undefined` 值会报错，传前过滤
- 图片使用 `mode="widthFix"` 在未知宽高时会导致布局抖动
