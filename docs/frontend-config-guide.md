# DeepCard 前端配置系统使用指南

## 🎯 概述

DeepCard前端配置系统允许您灵活切换不同的后端环境，支持开发、测试、生产和自定义环境。无需修改代码，通过UI界面即可完成环境切换。

## 🔧 配置功能

### 1. 环境切换
- **开发环境**: 默认连接 `http://localhost:8004`
- **测试环境**: 连接 `http://localhost:8005` (用于测试服务器)
- **自定义环境**: 连接任意您指定的后端地址

### 2. 自动配置管理
- 配置自动保存到浏览器本地存储
- 页面刷新后保持环境设置
- 实时显示当前环境状态

### 3. 健康检查
- 每30秒自动检查后端健康状态
- 连接失败时自动提醒
- 控制台详细日志输出

## 📱 使用方法

### 基本环境切换

1. **打开前端界面** (http://localhost:3000)
2. **在顶部控制区域找到"后端环境"下拉菜单**
3. **选择目标环境**:
   - 开发环境 (8004): 用于本地开发
   - 测试环境 (8005): 用于测试服务器
   - 自定义环境: 连接到任意后端

### 自定义后端配置

1. **选择"自定义环境"**
2. **在出现的输入框中填写后端地址**:
   ```
   http://localhost:8004
   http://192.168.1.100:8004
   https://your-api-server.com
   ```
3. **点击"保存"按钮**
4. **系统自动切换到新的后端**

### 环境状态查看

配置界面会显示当前环境信息:
```
当前环境: 开发环境 | 后端地址: http://localhost:8004 | 调试模式: 开启
```

## 🌐 URL参数支持

您可以通过URL参数直接指定环境:

```bash
# 直接打开开发环境
http://localhost:3000?env=development

# 直接打开测试环境
http://localhost:3000?env=testing

# 直接打开自定义环境
http://localhost:3000?env=custom
```

## ⚙️ 配置文件结构

前端配置系统基于 `frontend/config.js` 文件:

```javascript
const Config = {
    environments: {
        development: {
            name: '开发环境',
            apiBaseUrl: 'http://localhost:8004',
            debug: true
        },
        testing: {
            name: '测试环境',
            apiBaseUrl: 'http://localhost:8005',
            debug: true
        },
        custom: {
            name: '自定义环境',
            apiBaseUrl: '从localStorage读取',
            debug: true
        }
    }
};
```

## 🔧 高级配置

### 修改默认环境

编辑 `frontend/config.js` 文件:

```javascript
// 修改默认环境
current: 'development', // 改为 'testing' 或 'custom'

// 修改默认端口
development: {
    apiBaseUrl: 'http://localhost:9000', // 修改为您的端口
}
```

### 添加新环境

```javascript
environments: {
    // 添加生产环境
    production: {
        name: '生产环境',
        apiBaseUrl: 'https://api.deepcard.app',
        debug: false,
        timeout: 20000
    },

    // 添加团队环境
    team: {
        name: '团队环境',
        apiBaseUrl: 'http://team-server.local:8004',
        debug: true
    }
}
```

## 🚀 开发工作流

### 本地开发
1. 启动后端: `./start_dev.sh`
2. 打开前端: http://localhost:3000
3. 确认选择"开发环境"
4. 开始开发调试

### 连接远程后端
1. 确保远程后端已启动并配置了正确的CORS
2. 打开前端界面
3. 选择"自定义环境"
4. 输入远程后端地址 (如: `http://192.168.1.100:8004`)
5. 点击保存

### 团队协作
1. 团队成员启动本地后端在不同端口
2. 其他成员通过"自定义环境"连接
3. 实时测试和调试

## 🔍 故障排查

### 1. 连接失败
- **检查后端是否启动**: 访问 `http://后端地址/health`
- **检查CORS配置**: 确认后端允许您的前端域名
- **检查网络连接**: 确认可以访问后端地址

### 2. 配置不生效
- **清除浏览器缓存**: 刷新页面时按 Ctrl+F5
- **检查localStorage**: 在控制台运行 `localStorage.clear()`
- **查看控制台日志**: 检查是否有JavaScript错误

### 3. 跨域问题
如果遇到CORS错误，确认后端配置包含您的前端地址:

```python
# backend/app/shared/config.py
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # 添加您的自定义地址
    "http://your-domain:3000"
]
```

## 📱 移动端支持

配置系统完全支持移动端:
- 响应式设计，适配手机屏幕
- 触摸友好的控件
- 移动端浏览器兼容

## 🔒 安全注意事项

1. **自定义后端**: 只连接您信任的后端服务
2. **HTTPS**: 生产环境建议使用HTTPS
3. **调试模式**: 生产环境建议关闭调试模式
4. **API密钥**: 确保后端API密钥安全

## 🎯 最佳实践

1. **开发环境**: 本地开发使用默认配置
2. **测试环境**: 团队测试使用专用测试服务器
3. **生产环境**: 使用正式的生产服务器
4. **自定义环境**: 临时调试或特殊场景使用

---

**通过这个配置系统，您可以轻松管理多个后端环境，提高开发和测试效率！** 🚀