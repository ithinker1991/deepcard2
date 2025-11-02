# DeepCard 开发指南

## 📋 项目概述

本文档记录了DeepCard项目的开发规范、技术要求和最佳实践。

## 🔧 开发环境要求

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

## 📝 日志框架要求

### 后端日志规范
**必须使用Python logging模块**:

```python
import logging

logger = logging.getLogger(__name__)

# 在关键位置添加日志
logger.info("API请求开始: method=%s, path=%s, user_id=%s", method, path, user_id)
logger.debug("数据库操作: table=%s, operation=%s, duration=%sms", table, op, duration)
logger.info("LLM调用: provider=%s, model=%s, tokens=%d", provider, model, tokens)
logger.error("API错误: status=%d, error=%s", status_code, error_msg, exc_info=True)
```

**关键日志点**:
- API请求/响应
- 数据库操作执行时间
- LLM调用参数和响应状态
- 错误处理和异常堆栈
- 用户操作审计日志

### 前端日志规范
**必须添加控制台日志**:

```javascript
// API调用日志
console.log(`API Request: ${method} ${url}`, data);
console.log(`API Response: ${status}`, response);

// 用户操作日志
console.log(`User Action: ${action}`, details);

// 错误日志
console.error('Application Error:', error, stackTrace);
```

## 🏗️ 技术架构要求

### 后端架构
- **DDD领域驱动设计**: 清晰的领域边界和聚合根
- **依赖注入**: 使用FastAPI的依赖注入系统
- **异步处理**: 所有I/O操作使用async/await
- **错误处理**: 统一的异常处理机制

### 前端架构
- **组件化**: 可复用的UI组件
- **状态管理**: 清晰的数据流
- **类型安全**: TypeScript严格模式
- **响应式设计**: 移动端适配

## 🧪 测试要求

### 测试覆盖要求
- **Happy Path测试**: 每个核心功能必须有基础测试
- **边界测试**: 错误情况和异常处理
- **集成测试**: API端到端测试
- **性能测试**: 关键操作的性能基准

### 测试配置化
```bash
# 不同环境的测试模式
TEST_MODE=offline python -m pytest tests/ -v          # 无外部依赖
TEST_MODE=local ENABLE_DATABASE_TESTS=true python -m pytest tests/ -v  # 包含数据库
TEST_MODE=integration ENABLE_LLM_TESTS=true python -m pytest tests/ -v  # 包含LLM
```

## 📊 性能要求

### API响应时间
- **健康检查**: < 10ms
- **CRUD操作**: < 50ms
- **LLM生成**: < 15秒
- **数据库查询**: < 20ms

### 数据库优化
- **索引策略**: 用户ID、卡片ID、创建时间
- **查询优化**: 避免N+1查询
- **连接池**: 合理的连接池配置

## 🔒 安全要求

### 数据隔离
- **用户数据**: 严格的user_id隔离
- **API权限**: 基于用户ID的访问控制
- **敏感信息**: API密钥和配置文件保护

### 输入验证
- **Pydantic模型**: 严格的输入验证
- **SQL注入防护**: 使用ORM参数化查询
- **XSS防护**: 前端输入转义

## 📦 依赖管理

### 后端依赖
```bash
# 核心依赖
fastapi>=0.100.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pytest>=7.0.0

# 开发依赖
black>=23.0.0
isort>=5.12.0
mypy>=1.0.0
```

### 前端依赖
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "next": "^14.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0"
  }
}
```

## 🚀 部署要求

### 环境配置
- **开发环境**: SQLite + 本地文件存储
- **测试环境**: 内存数据库 + Mock服务
- **生产环境**: PostgreSQL + Redis + 云存储

### 监控和日志
- **应用日志**: 结构化日志输出
- **性能监控**: 响应时间和错误率
- **健康检查**: 服务状态监控

## 📚 文档要求

### 必需文档
- **API文档**: OpenAPI/Swagger规范
- **数据库文档**: ER图和表结构
- **部署文档**: 环境配置和部署步骤
- **用户文档**: 功能使用说明

### 文档更新流程
1. 功能开发完成后立即更新文档
2. API变更必须更新API文档
3. 数据库结构变更更新数据库文档
4. 重大变更更新用户文档

## 🔄 代码审查要求

### 审查清单
- [ ] 代码符合项目规范
- [ ] 测试覆盖核心功能
- [ ] 日志记录完整
- [ ] 错误处理恰当
- [ ] 性能考虑合理
- [ ] 安全措施到位

### 审查重点
- **代码质量**: 可读性、可维护性
- **架构设计**: 符合DDD原则
- **测试质量**: 测试覆盖率和有效性
- **性能影响**: 资源使用和响应时间

## 🐛 问题排查流程

### 日志分析
1. 查看应用日志文件
2. 分析错误堆栈信息
3. 检查相关配置文件
4. 复现问题场景

### 调试工具
- **后端**: pdb、logging、profiler
- **前端**: Chrome DevTools、console.log
- **数据库**: 查询分析、索引检查
- **网络**: 抓包工具、API测试

## 📈 持续改进

### 代码质量指标
- **测试覆盖率**: 目标 > 80%
- **代码复杂度**: 避免过度复杂的函数
- **重复代码**: 使用抽象和重构
- **技术债务**: 定期重构和优化

### 团队协作
- **代码规范**: 统一的编码标准
- **文档维护**: 及时更新技术文档
- **知识分享**: 定期技术分享会
- **工具使用**: 高效的开发工具配置

---

**本文档随项目发展持续更新，确保团队协作和代码质量。**