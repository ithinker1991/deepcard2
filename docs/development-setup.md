# DeepCard 开发环境搭建指南

## 🚀 一键启动 (推荐)

### 前置要求
- Python 3.8+
- 已创建虚拟环境: `cd backend && python -m venv .venv`
- 已安装依赖: `cd backend && source .venv/bin/activate && pip install -r requirements.txt`

### 启动步骤

1. **配置环境变量** (可选)
```bash
# 复制配置模板
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

2. **一键启动**
```bash
./start_dev.sh
```

3. **访问应用**
- 前端: http://localhost:3000
- 后端API: http://localhost:8004
- API文档: http://localhost:8004/docs

4. **停止服务**
```bash
./stop_dev.sh
# 或
./stop_dev.sh --clean-logs  # 同时清理日志
```

## 🔧 手动启动 (调试用)

### 启动后端
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

### 启动前端
```bash
cd frontend
python -m http.server 3000
# 然后在浏览器打开 frontend/index.html
```

## 🛠️ 端口管理

### 固定端口配置
- **后端**: 8004 (固定)
- **前端**: 3000 (固定)
- **避免冲突**: 启动脚本会自动清理占用端口的进程

### 端口使用规范
- 开发环境使用固定端口，避免混乱
- 生产环境可通过环境变量调整
- 脚本会自动检测端口占用情况

## 🔒 CORS配置

### 已解决的跨域问题
后端配置支持以下来源:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:8004`
- `http://127.0.0.1:8004`
- `file://` (直接打开HTML文件)
- `null` (某些浏览器特殊场景)

### 新增端口支持
如需添加其他端口，修改 `backend/app/shared/config.py`:
```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:你的新端口",
    # 添加其他需要的端口
]
```

## 📝 联调自动化解决方案

### 1. 一键启动脚本
- ✅ 自动清理进程冲突
- ✅ 健康检查后端服务
- ✅ 自动配置前端后端地址
- ✅ 自动打开浏览器
- ✅ 完整的错误处理

### 2. 配置管理
- ✅ 环境变量模板
- ✅ CORS自动配置
- ✅ 日志文件管理
- ✅ 调试信息输出

### 3. 开发体验优化
- ✅ 进程PID管理
- ✅ 实时日志查看
- ✅ 优雅停止机制
- ✅ 自动重载支持
- ✅ 前端环境配置系统

## 🐛 常见问题排查

### 1. 端口被占用
```bash
# 查看端口占用
lsof -i :8004
lsof -i :3000

# 强制停止
./stop_dev.sh
```

### 2. CORS错误
确认后端配置文件包含你的前端URL:
```python
# backend/app/shared/config.py
ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
```

### 3. API密钥错误
创建 `.env` 文件并配置正确的API密钥:
```bash
cp .env.example .env
# 编辑 .env 文件
```

### 4. 虚拟环境问题
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. 前端无法访问后端
检查:
- 后端是否正常启动: 访问 http://localhost:8004/health
- CORS配置是否正确
- 前端JavaScript中的API地址是否正确

## 📊 开发工具集成

### VSCode调试配置
已创建 `.vscode/launch.json` 和 `.vscode/settings.json`，支持:
- Python调试
- 前端调试
- 断点设置
- 自动格式化

### 日志管理
- 后端日志: `logs/backend.log`
- 前端日志: `logs/frontend.log`
- 控制台输出: 实时显示

### 测试运行
```bash
# Happy Path测试
cd backend
source .venv/bin/activate
TEST_MODE=local ENABLE_DATABASE_TESTS=true python -m pytest tests/test_milestone2.py -v
```

## 🎯 开发最佳实践

1. **使用一键启动脚本**: 避免手动配置错误
2. **查看日志**: 遇到问题时先查看日志文件
3. **API文档**: 后端启动后访问 /docs 查看API文档
4. **健康检查**: 定期检查 /health 确认服务状态
5. **优雅停止**: 使用停止脚本而非强制杀死进程

## 📋 快速检查清单

启动前检查:
- [ ] 虚拟环境已创建
- [ ] 依赖已安装
- [ ] API密钥已配置 (如需LLM功能)
- [ ] 端口8004和3000未被占用

启动后检查:
- [ ] 后端健康检查通过: http://localhost:8004/health
- [ ] 前端可访问: http://localhost:3000
- [ ] API文档可访问: http://localhost:8004/docs
- [ ] 浏览器控制台无CORS错误

---

**通过以上配置，您应该能够顺利启动和开发DeepCard应用！** 🎉