# Claude Code 配置

本项目使用 Claude Code 进行开发，以下是配置和最佳实践指南。

## 📋 项目概况

**项目类型**: 全栈Web应用 (AI-powered Flashcard Application)
**技术栈**:
- 后端: Python + FastAPI + SQLite + Redis
- 前端: React + Next.js + TypeScript + Tailwind CSS
- AI: 多LLM支持 (OpenAI, DeepSeek, SiliconFlow)
- 架构: DDD领域驱动设计

**项目规模**: 中小型项目，1个主要开发者
**开发阶段**: 里程碑驱动开发

## 🛠️ 配置

### 权限管理
项目已配置完整的权限设置，支持所有必要的操作：
- ✅ 文件编辑和创建
- ✅ Git版本控制操作
- ✅ 测试运行
- ✅ 文件系统操作

### 快速启动
```bash
# 一键启动开发环境
./start-dev.sh

# 后端服务
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload

# 前端服务
cd frontend && npm run dev

# 数据库迁移 (如需要)
cd backend && alembic upgrade head
```

### 测试策略 (TDD推荐)
```bash
# 运行所有测试
cd backend && python -m pytest tests/ -v

# 运行特定测试套件
python -m pytest tests/test_happy_path.py -v  # 基础功能测试
python -m pytest tests/test_llm_providers.py -v  # LLM提供商测试

# 单个测试文件
python -m pytest tests/test_main.py::test_health_check -v

# 性能优化测试
python -m pytest -v --benchmark-only tests/benchmarks/
```

### 代码质量检查
```bash
# 后端代码质量
cd backend
black .                    # 代码格式化
isort .                   # 导入排序
mypy app/                  # 类型检查
python -m pytest --cov=app tests/  # 测试覆盖率

# 前端代码质量
cd frontend
npm run type-check         # TypeScript检查
npm run lint               # ESLint检查
npm run format             # Prettier格式化
npm run test               # 单元测试
```

## 📁 项目结构

```
deepcard2/
├── backend/                 # 后端代码
│   ├── app/                # 应用主目录
│   │   ├── domains/       # 领域层 (DDD)
│   │   ├── infrastructure/ # 基础设施层
│   │   └── shared/        # 共享模块
│   ├── tests/             # 测试代码
│   └── pyproject.toml     # Python项目配置
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   ├── components/    # 组件
│   │   └── features/      # 功能模块
│   └── package.json       # Node.js配置
├── docs/                   # 项目文档
│   ├── milestone-*/       # 里程碑文档
│   ├── *.md              # 设计文档
│   └── acceptance.md      # 验收文档
├── milestone-*/            # 里程碑开发文件
└── .vscode/               # VSCode配置
```

## 🎯 开发工作流

### 里程碑驱动开发
1. **当前里程碑**: 里程碑2 - 卡片基础 + 文本生成 ✅ **已完成**
2. **已完成**: 里程碑1 - 基础架构 + LLM集成 ✅
3. **后续计划**: 资源管理 → 高级生成 → 学习功能 → 算法优化 → 体验优化

### Git管理规范
**每个里程碑完成前必须确认**:
1. 与用户确认是否需要更新Git仓库并推送到远端
2. 提交格式: `feat(milestone-X): 完成里程碑X功能开发`
3. 包含完整的提交信息和变更说明
4. 推送前确保所有测试通过

### 技术方案对齐流程
**开始实现前必须对齐**:
1. **需求确认**: 与用户确认功能需求和技术要求
2. **方案设计**: 提出技术方案和实现思路
3. **风险评估**: 识别潜在问题和依赖关系
4. **实现计划**: 制定详细的开发步骤和验收标准
5. **文档更新**: 将决策记录到相关文档中

### 日志框架要求
**后端和前端都需要完整日志**:
- 关键API端点必须有请求/响应日志
- 数据库操作需要记录执行时间
- LLM调用需要记录请求参数和响应状态
- 错误处理需要详细的错误堆栈
- 用户操作需要记录审计日志

### TDD 开发流程 (推荐)
1. **编写测试** - 先写期望失败的测试
2. **提交测试** - 记录需求到版本控制
3. **实现功能** - 编写代码使测试通过
4. **提交实现** - 完成功能开发

### 验证流程
每个里程碑完成后：
1. 运行自动化测试验证
2. 手动验收关键功能
3. 确认文档更新
4. 推送代码到GitHub

### 任务切换技巧
```bash
# 清理上下文，开始新任务
/clear

# 查看当前状态
git status
git log --oneline -5

# 切换到特定任务
cd milestone-2/backend
```

### 文档优先原则
1. **设计先于代码**: 先理解需求和设计
2. **测试驱动**: 测试代码和实现代码并行
3. **文档同步**: 功能完成后立即更新文档
4. **验收导向**: 每个里程碑都有完整的验收文档

## 🧪 测试策略

### Happy Path优先
- 先实现核心功能测试
- 后续完善边界情况测试
- 每个里程碑都有独立的测试套件

### 自动化测试配置化
- 数据库测试开关
- LLM调用测试开关
- 外部API测试开关
- 详细配置参考: `docs/automated-testing-config.md`

### 测试运行
```bash
# 快速自动化验收
cd backend && source .venv/bin/activate
python -m pytest tests/test_happy_path.py -v

# 验证LLM功能
python -c "
from app.infrastructure.llm import LLMFactory
print('Providers:', LLMFactory.get_supported_providers())
"
```

## 🔧 常用命令

### 后端开发
```bash
# 启动后端服务器
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload

# 运行测试
python -m pytest tests/ -v

# 代码格式化
black .
isort .

# 类型检查
mypy app/
```

### 前端开发
```bash
# 启动前端开发服务器
cd frontend && npm run dev

# 类型检查
npm run type-check

# 代码格式化
npm run format

# 代码检查
npm run lint
```

### Docker开发
```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📝 文档结构

### 核心文档
- `README.md`: 项目总体介绍
- `ROADMAP.md`: 开发路线图
- `DEVELOPMENT.md`: 开发指南
- `CLAUDE.md`: Claude Code配置 (本文件)

### 设计文档
- `docs/domain-model.md`: 领域模型设计
- `docs/database-schema.md`: 数据库设计
- `docs/automated-testing-config.md`: 测试配置需求

### 验收文档
- `docs/milestone-1-acceptance.md`: 里程碑1验收手册
- `docs/milestone-*-acceptance.md`: 各里程碑验收文档

### 任务跟踪
- `docs/development-tasks.md`: 任务跟踪系统
- `docs/regression-testing-plan.md`: 回归测试计划

## 🎯 开发规范

### 提交规范 (已配置)
```
type(scope): description

[optional body]

footer

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

### 分支策略
- `main`: 主分支，稳定代码
- `develop`: 开发分支，集成最新功能
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复分支

### 代码质量 (已配置)
- 后端: Black + isort + MyPy
- 前端: Prettier + ESLint
- 测试: 每个功能都有Happy Path测试
- 自动格式化: 保存时自动格式化代码

## 🤖 Claude Code 最佳实践

### 具体指令优于通用请求
```bash
# ❌ 不推荐
"帮我优化后端代码性能"

# ✅ 推荐
"优化cards表的数据库查询，添加必要的索引，并分析查询计划"

# ❌ 不推荐
"修复所有测试"

# ✅ 推荐
"修复test_card_crud中失败的测试用例，问题在于缺少用户权限验证"
```

### 提供视觉目标
```bash
# 提供设计参考
"根据这个设计稿实现卡片列表页面：[image: src/design/card-list.png]"
"使用这个配色方案更新主题：#007bff"

# 提供示例输出
"API应该返回这个JSON格式：{\n  \"status\": \"success\",\n  \"cards\": [...]\n}"
```

### 保持上下文清晰
```bash
# 开始新任务时
/clear

# 提供背景信息
"我正在实现里程碑2的卡片CRUD功能，已经完成了数据库模型，现在需要创建API端点"

# 提供具体位置
"在backend/app/interfaces/api/v1/endpoints/cards.py中添加创建卡片的API端点"

# 请求明确结果
"请创建一个POST /api/v1/cards端点，接收JSON请求体，返回创建的卡片对象"
```

### 使用文件引用
```bash
# ❌ 避免复制大量代码
"添加以下代码到文件中：[大量代码块]"

# ✅ 推荐引用文件位置
"请参考backend/app/infrastructure/llm/base.py中的LLMProvider基类设计，在SiliconFlowProvider中实现generate_text方法"

# 提供上下文信息
"查看backend/app/domains/card/entities.py中的Card实体，为它添加一个update_tags方法"
```

### 使用代码导航
```bash
# 查找特定模式
"搜索项目中所有使用FastAPI装饰器的文件"
"找到处理cards相关路由的文件"
"搜索所有包含'database'关键词的文件"

# 理解代码结构
"分析backend/app/domains/目录的领域结构，解释每个模块的职责"
"查看app/infrastructure/llm/目录下的所有文件，了解LLM集成架构"
```

## 🤖 Claude Code 使用技巧

### 项目导航
```bash
# 查看项目结构
find . -name "*.py" -o -name "*.ts" -o -name "*.tsx" | head -20

# 查看最近的文件修改
git log --oneline -10

# 查看文件内容统计
find . -name "*.py" | xargs wc -l | tail -1
```

### 功能开发
1. 先理解需求和设计文档
2. 查看相关领域的代码结构
3. 实现核心功能，保持简单
4. 添加对应的测试用例
5. 更新相关文档

### 问题排查
1. 查看错误日志
2. 检查配置文件
3. 运行相关测试
4. 参考文档和注释

## 📞 获取帮助

### 项目文档
- 详细开发指南: `DEVELOPMENT.md`
- 技术架构: `docs/domain-model.md`
- 测试配置: `docs/automated-testing-config.md`

### Claude Code 帮用功能
- 搜索代码: 使用 `Grep` 工具
- 文件导航: 使用 `Glob` 工具
- 代码编辑: 使用 `Edit` 工具
- 任务管理: 使用 `TodoWrite` 工具

### 代码质量
- 类型检查: 使用 `mypy` (Python) / `TypeScript` (前端)
- 代码格式化: 自动保存时运行
- 测试运行: 使用 `pytest` (Python) / `jest` (前端)

## 🎨 项目特色

### AI集成
- 支持多LLM厂商 (OpenAI, DeepSeek, SiliconFlow)
- 配置化测试，避免不必要的API调用
- 完整的错误处理和重试机制

### 架构设计
- DDD领域驱动设计
- 清晰的分层架构
- 良好的代码组织结构

### 开发体验
- 完整的开发环境配置
- 自动化测试和部署
- 详细的文档和指南

## 🚀 快速开始

1. **首次使用**:
   ```bash
   git clone git@github.com:ithinker1991/deepcard2.git
   cd deepcard2
   ./start-dev.sh
   ```

2. **开始开发**:
   - 参考 `DEVELOPMENT.md` 设置开发环境
   - 查看 `ROADMAP.md` 了解项目规划
   - 根据当前里程碑开始开发

3. **验证功能**:
   - 运行自动化测试
   - 手动验收关键功能
   - 更新相关文档

---

**Happy coding with Claude Code!** 🎉