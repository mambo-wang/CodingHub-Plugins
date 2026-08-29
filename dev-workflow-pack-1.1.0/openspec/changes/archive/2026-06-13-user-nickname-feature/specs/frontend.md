# Frontend - Nickname Display

## ADDED Requirements

### Scenario 1: 注册页面显示昵称输入框

- GIVEN: 用户访问注册页面 /register
- WHEN: 页面加载
- THEN: 表单包含 username（账号）、nickname（昵称）、password（密码）三个输入框

### Scenario 2: 右上角显示昵称

- GIVEN: 用户已登录，用户信息为 username="wangbao", nickname="王宝"
- WHEN: 页面右上角渲染用户信息
- THEN: 显示"王宝"（昵称），而非"wangbao"（账号）

### Scenario 3: 右上角未设置昵称时显示账号

- GIVEN: 用户已登录，用户信息为 username="olduser", nickname=null
- WHEN: 页面右上角渲染用户信息
- THEN: 显示"olduser"（账号）

### Scenario 4: 工具详情页作者信息展示

- GIVEN: 工具详情页，工具作者信息为 username="wangbao", nickname="王宝"
- WHEN: 页面渲染作者信息区域
- THEN: 显示"王宝(wangbao)"格式
- AND: Hover 时显示完整信息 tooltip

### Scenario 5: 帖子详情页作者信息展示

- GIVEN: 帖子详情页，帖子作者信息为 username="wangbao", nickname="王宝"
- WHEN: 页面渲染作者信息区域
- THEN: 显示"王宝(wangbao)"格式
- AND: Hover 时显示完整信息 tooltip

### Scenario 6: 帖子列表作者信息展示

- GIVEN: 帖子列表页，帖子作者信息为 username="wangbao", nickname="王宝"
- WHEN: 页面渲染帖子列表
- THEN: 每条帖子的作者显示"王宝(wangbao)"格式

### Scenario 7: 工具列表作者信息展示

- GIVEN: 工具广场列表页，工具作者信息为 username="wangbao", nickname="王宝"
- WHEN: 页面渲染工具卡片
- THEN: 作者信息显示"王宝(wangbao)"格式