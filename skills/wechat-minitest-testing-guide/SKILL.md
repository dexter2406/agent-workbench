---
name: wechat-minitest-testing-guide
description: 微信小程序 Minium 自动化测试指南，涵盖环境配置、用例编写、元素操作、Mock 和 CI 集成。Use when writing or debugging automated tests for the lovey-record mini program.
---

# 微信小程序 Minium 自动化测试指南

文档来源：https://minitest.weixin.qq.com

## 快速开始

### 安装

```bash
pip install minium
# 验证安装
minitest --help
```

**依赖要求：**
- Python 3.7+
- 微信开发者工具（需开启服务端口）
- 开发者工具 → 设置 → 安全设置 → 开启**服务端口**

### 最小配置文件

```json
// minitest.json（项目根目录）
{
  "project_path": "D:/CodeSpace/hbuilder-projects/lovey-record/dist/dev/mp-weixin",
  "dev_tool_path": "C:/Program Files (x86)/Tencent/微信web开发者工具/cli.bat",
  "test_port": 9420,
  "assert_capture": true
}
```

### 运行测试

```bash
# 运行单个测试文件
minitest -m test_home.py

# 运行测试套件（suite.json）
minitest -s suite.json

# 运行所有测试
minitest -d tests/
```

---

## 测试用例结构

```python
import minium

class HomePageTest(minium.MiniTest):
    
    def setUp(self):
        # 每个测试方法前运行
        self.app.navigate_to('/pages/index/index')
    
    def tearDown(self):
        # 每个测试方法后运行
        pass
    
    def test_page_loads(self):
        """首页正常加载"""
        page = self.app.get_current_page()
        self.assertPageExist('/pages/index/index')
    
    def test_click_button(self):
        """点击按钮跳转"""
        btn = self.page.get_element('.my-button')
        btn.tap()
        self.assertPageExist('/pages/detail/index')
```

**MiniTest 核心属性：**

| 属性 | 说明 |
|------|------|
| `self.mini` | Minium 实例，管理整个小程序 |
| `self.app` | App 对象，跨页面操作 |
| `self.page` | 当前页面对象 |
| `self.native` | 原生控件操作（系统弹窗、授权框等） |

---

## App 对象（跨页面导航）

```python
# 跳转页面
self.app.navigate_to('/pages/menstrual/home/index')
self.app.redirect_to('/pages/index/index')
self.app.relaunch('/pages/index/index')
self.app.switch_tab('/pages/profile/index')
self.app.navigate_back()  # 返回上一页

# 获取当前页面
page = self.app.get_current_page()
print(page.path)  # '/pages/index/index'

# 在页面中执行 JS
result = self.app.evaluate('App.globalData.userId')

# 调用小程序 wx API
self.app.call_wx_method('showToast', {'title': '测试'})
```

---

## Page 对象（页面内操作）

```python
# 获取元素（返回第一个匹配）
element = self.page.get_element('.card-item')
element = self.page.get_element('#submit-btn')

# 获取多个元素
elements = self.page.get_elements('.list-item')
print(len(elements))

# 检查元素是否存在
exists = self.page.element_is_exists('.error-msg')

# 读取页面 data
data = self.page.data
print(data['title'])

# 直接修改页面 data（用于设置测试状态）
self.page.data = {'loading': False, 'list': []}

# 调用页面方法
self.page.call_method('onRefresh')
```

---

## Element 对象（元素操作）

```python
element = self.page.get_element('.my-element')

# 点击
element.tap()
element.click()        # 等同于 tap
element.long_press()   # 长按

# 获取属性
text = element.inner_text
value = element.attribute('data-id')
style = element.style('color')

# 获取子元素
child = element.get_element('.child-class')

# 表单元素操作（FormElement）
input_el = self.page.get_element('input')
input_el.input('hello world')    # 输入文字

switch_el = self.page.get_element('switch')
switch_el.switch()               # 切换开关

slider_el = self.page.get_element('slider')
slider_el.slide_to(80)           # 滑动到 80%

picker_el = self.page.get_element('picker')
picker_el.pick({'value': 1})     # 选择选项
```

---

## 选择器

Minium 支持 CSS 选择器和 XPath：

```python
# CSS 选择器（推荐）
self.page.get_element('.class-name')
self.page.get_element('#element-id')
self.page.get_element('view.card > text')

# 跨组件（穿透 shadow DOM）用 >>>
self.page.get_element('.parent >>> .child-in-component')

# XPath
self.page.get_element('//view[@class="container"]')

# 通过文字内容（XPath）
self.page.get_element('//text()[contains(., "提交")]/..')
```

**调试选择器：** 在开发者工具 WXML 面板找到元素的类名和结构，再写选择器。

---

## Mock 请求与方法

### Mock 网络请求

```python
# 拦截 wx.request
self.app.mock_request(
    url='https://api.example.com/records',
    method='GET',
    response={
        'statusCode': 200,
        'data': {'records': [{'id': 1, 'title': '测试记录'}]}
    }
)

# 清除 mock
self.app.restore_request()
```

### Mock wx 方法

```python
# Mock wx.showModal 返回用户点击确认
self.app.mock_wx_method(
    'showModal',
    return_value={'confirm': True, 'cancel': False}
)

# Mock wx.chooseMedia（模拟选图）
self.app.mock_wx_method(
    'chooseMedia',
    return_value={
        'tempFiles': [{'tempFilePath': '/tmp/test.jpg', 'size': 1024}]
    }
)

# 恢复原始方法
self.app.restore_wx_method('showModal')
```

### uni-app 项目特殊处理

uni-app 编译后的小程序，`wx` 会被代理为 `wx._MINI_WX_PROXY_`，mock 时：

```python
# 使用 evaluate 直接操作
self.app.evaluate("wx._MINI_WX_PROXY_.request = function(options) { options.success({data: {}}) }")
```

---

## 断言

```python
# 页面断言
self.assertPageExist('/pages/index/index')     # 当前页面路径
self.assertPageNotExist('/pages/error/index')

# 元素断言
el = self.page.get_element('.title')
self.assertExists(el)
self.assertNotExists(self.page.get_element('.error'))

# 文字断言
self.assertEqual(el.inner_text, '预期文字')
self.assertIn('关键词', el.inner_text)

# 数据断言
data = self.page.data
self.assertEqual(data['count'], 5)
self.assertTrue(data['loaded'])

# 标准 Python unittest 断言均可用
self.assertEqual(a, b)
self.assertTrue(condition)
self.assertIsNone(value)
```

---

## 截图与调试

```python
# 截图（自动保存到 outputs/ 目录）
self.mini.capture('test_step_1')

# 获取页面截图
screenshot = self.page.screenshot()

# 打印页面 data（调试用）
import json
print(json.dumps(self.page.data, ensure_ascii=False, indent=2))
```

`assert_capture: true`（配置项）会在断言失败时自动截图。

---

## 真机测试

```json
// minitest.json（真机配置）
{
  "device_desire": {
    "platform": "Android",
    "deviceId": "设备序列号(adb devices获取)"
  },
  "test_port": 9420
}
```

```bash
# 查看已连接 Android 设备
adb devices

# iOS 需要安装 libimobiledevice
idevice_id -l
```

---

## 测试套件（suite.json）

```json
{
  "pkg_list": [
    {
      "case_list": ["test_*"],       // 通配符匹配方法名
      "pkg": "tests.test_home"       // 模块路径
    },
    {
      "case_list": ["TestRecord"],   // 精确类名
      "pkg": "tests.test_record"
    }
  ]
}
```

```bash
minitest -s suite.json -o outputs/  # -o 指定输出目录
```

---

## 常见问题

**连接失败（Connection refused）：**
1. 确认开发者工具已**开启服务端口**（设置 → 安全）
2. 检查 `test_port` 和开发者工具端口一致（默认 9420）
3. 重启开发者工具

**元素找不到：**
1. 加 `self.mini.sleep(1)` 等待页面渲染完成
2. 检查选择器：在开发者工具 WXML 面板确认类名
3. 跨组件用 `>>>` 穿透选择器
4. 注意 `wx:if` 隐藏的元素不在 DOM 中，用 `wx:hidden` 替代

**mock_request 不生效（uni-app）：**
uni-app 的网络请求走 `uni.request` 而非直接 `wx.request`，需用 `evaluate` 注入 mock 或在代码层封装请求拦截。

**测试间状态污染：**
在 `tearDown` 中清理存储：
```python
def tearDown(self):
    self.app.call_wx_method('clearStorageSync')
```
