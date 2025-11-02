# 开发指南

## 项目概述

DeepCard 是一个基于LLM的智能闪卡应用，支持从多种内容源自动生成学习卡片，并提供科学的记忆复习系统。

## 技术栈

### 后端
- **Python 3.11+** + **FastAPI**
- **SQLite** (开发) / **PostgreSQL** (生产)
- **Redis** (缓存)
- **SQLAlchemy** (ORM)
- **Pydantic** (数据验证)

### 前端
- **React 18** + **Next.js 14**
- **TypeScript**
- **Tailwind CSS**
- **Zustand** (状态管理)

## 快速开始

### 1. 环境要求

- Docker & Docker Compose
- Python 3.11+ (本地开发)
- Node.js 18+ (本地开发)

### 2. 使用Docker启动 (推荐)

```bash
# 克隆项目
git clone <repository-url>
cd deepcard2

# 启动开发环境
./start-dev.sh
```

### 3. 本地开发

#### 后端设置

```bash
cd backend

# 安装Poetry (如果还没有)
pip install poetry

# 安装依赖
poetry install

# 复制环境配置
cp .env.example .env
# 编辑 .env 文件，填入必要配置

# 启动开发服务器
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 复制环境配置
cp ../frontend/.env.local.example .env.local

# 启动开发服务器
npm run dev
```

## 项目结构

```
deepcard2/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── domains/        # 领域层 (DDD)
│   │   │   ├── card/       # 卡片领域
│   │   │   ├── resource/   # 资源领域
│   │   │   ├── learning/   # 学习领域
│   │   │   └── generation/ # 生成领域
│   │   ├── infrastructure/ # 基础设施层
│   │   ├── application/    # 应用层
│   │   ├── interfaces/     # 接口层 (API)
│   │   └── shared/         # 共享模块
│   └── tests/              # 测试代码
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   ├── components/    # 共享组件
│   │   ├── features/      # 功能模块
│   │   ├── hooks/         # 自定义钩子
│   │   ├── services/      # API服务
│   │   ├── store/         # 状态管理
│   │   └── types/         # 类型定义
├── docs/                  # 项目文档
└── docker-compose.yml     # Docker配置
```

## 开发流程

### 1. 创建新功能

#### 后端

1. 在 `domains/` 下创建或修改领域模型
2. 在 `application/services/` 创建应用服务
3. 在 `interfaces/api/` 创建API端点
4. 在 `tests/` 编写测试

#### 前端

1. 在 `features/` 下创建功能模块
2. 创建组件、钩子和服务
3. 更新状态管理
4. 添加路由

### 2. 数据库迁移

```bash
cd backend

# 创建迁移文件
poetry run alembic revision --autogenerate -m "描述"

# 应用迁移
poetry run alembic upgrade head
```

### 3. 测试

```bash
# 后端测试
cd backend
poetry run pytest

# 前端测试
cd frontend
npm test
```

## 核心概念

### 领域驱动设计 (DDD)

项目采用DDD架构，主要领域包括：

1. **卡片领域**: 卡片的创建、编辑、删除
2. **资源领域**: 原始资源管理和内容提取
3. **学习领域**: 记忆算法和学习进度
4. **生成领域**: LLM集成和卡片生成

### API设计原则

- RESTful API设计
- 统一的错误处理
- 请求/响应验证
- 适当的HTTP状态码

### 前端架构

- 组件化设计
- 特性模块化
- 状态管理 (Zustand)
- 类型安全 (TypeScript)

## 开发规范

### 代码风格

- **后端**: 使用 `black` 和 `isort` 格式化代码
- **前端**: 使用 `prettier` 格式化代码
- 所有代码需要通过类型检查

### 提交规范

使用约定式提交格式:

```
type(scope): description

[optional body]

[optional footer]
```

类型包括:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建或辅助工具变动

### 分支策略

- `main`: 主分支，生产环境代码
- `develop`: 开发分支，集成最新功能
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复分支

## 调试指南

### 后端调试

1. 查看日志: `docker-compose logs -f backend`
2. API文档: http://localhost:8000/docs
3. 数据库: 使用SQLite浏览器或PostgreSQL客户端

### 前端调试

1. 使用浏览器开发者工具
2. React DevTools
3. 网络请求检查

## 部署

### 开发环境

```bash
docker-compose up -d
```

### 生产环境

参考 `docker-compose.prod.yml` (待创建)

## 常见问题

### 1. 数据库连接问题

确保数据库配置正确，检查 `DATABASE_URL` 环境变量。

### 2. LLM API问题

确保正确配置了OpenAI API密钥，检查网络连接。

### 3. 前后端通信问题

检查CORS配置和API端点URL。

## 项目特殊要求

### Happy Path优先原则
- **核心思想**: 先实现主要功能，后续完善边界情况
- **验收标准**: 每个里程碑的完成标准是Happy Path测试通过
- **防御式编程**: 避免过度防御，专注于核心用户流程
- **用户操作**: 不绕过用户必须配置的部分（如API密钥设置）

### 里程碑驱动开发
- **渐进式迭代**: 每个里程碑都有可演示的功能
- **验收流程**: 每个里程碑完成后进行实际操作验收
- **文档同步**: 开发要求和原则需要及时更新到文档中
- **验收手册**: 每个里程碑都有对应的验收手册

### 简单适用演进原则
- **技术选择**: 优先选择成熟稳定的技术栈
- **架构设计**: 适度抽象，避免过度设计
- **功能优先**: 以用户价值为导向，不过度优化
- **持续演进**: 支持功能的逐步完善和扩展

### 验收要求
- **自动化测试**: 每个里程碑必须有通过的Happy Path测试
- **实际操作**: 开发者必须能够实际操作验证功能
- **必要配置**: 不绕过用户必须完成的配置步骤
- **文档完整**: 验收手册和开发要求保持同步

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request
5. 代码审查和合并

## 联系方式

如有问题，请通过以下方式联系:
- 创建Issue
- 发送邮件
- 项目讨论群