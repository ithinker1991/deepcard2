# 里程碑1验收手册

## 🎯 验收目标

验证基础架构和LLM集成核心功能是否正常工作，确保为后续开发奠定坚实基础。

## 📋 验收前准备

### 必要准备事项

**你需要准备以下事项：**

1. **OpenAI API Key** (可选，用于完整功能测试)
   - 访问 https://platform.openai.com/api-keys
   - 创建新的API密钥
   - 充值少量金额用于测试

2. **DeepSeek API Key** (可选，用于多厂商测试)
   - 访问 https://platform.deepseek.com/
   - 注册并获取API密钥

3. **开发环境检查**
   - Python 3.11+ 已安装
   - Git已配置
   - VSCode已安装（推荐）

### 环境配置步骤

```bash
# 1. 进入项目目录
cd deepcard2/backend

# 2. 激活虚拟环境
source .venv/bin/activate

# 3. 配置环境变量（如果有API Key）
cp .env.example .env
# 编辑 .env 文件，添加你的API Key:
# OPENAI_API_KEY="your-actual-openai-key"
# DEEPSEEK_API_KEY="your-actual-deepseek-key"
```

---

## 🧪 验收测试步骤

### 测试1: 基础架构验证

**目标**: 验证FastAPI应用可以正常启动

**自动化状态**: 🔧 手动测试 (需要启动服务器)

**步骤**:
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**预期结果**:
- 服务器在 http://localhost:8000 启动
- 无错误信息
- 显示 "Uvicorn running on http://0.0.0.0:8000"

**验收标准**: ✅ 服务器成功启动

**自动化测试替代**:
```bash
source .venv/bin/activate && python -c "from app.main import app; print('✅ FastAPI app loaded successfully')"
```

---

### 测试2: 健康检查API

**目标**: 验证基础API端点正常工作

**自动化状态**: ✅ 可自动化测试

**步骤**:
```bash
# 在新终端中执行
curl -X GET "http://localhost:8000/health"
```

**预期结果**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "app": "DeepCard API"
}
```

**验收标准**: ✅ 返回正确的健康状态信息

**自动化测试命令**:
```bash
source .venv/bin/activate && python -m pytest tests/test_happy_path.py::TestHappyPath::test_health_check_happy_path -v
```

---

### 测试3: API文档验证

**目标**: 验证API文档可访问

**自动化状态**: ✅ 可自动化测试

**步骤**:
```bash
curl -X GET "http://localhost:8000/docs"
```

**预期结果**: HTML页面，显示Swagger UI界面

**验收标准**: ✅ API文档页面正常显示

**自动化测试命令**:
```bash
source .venv/bin/activate && python -m pytest tests/test_happy_path.py::TestHappyPath::test_api_docs_happy_path -v
```

---

### 测试4: LLM提供商列表

**目标**: 验证LLM抽象层正常工作

**自动化状态**: ✅ 可自动化测试

**步骤**:
```bash
curl -X GET "http://localhost:8000/api/v1/llm/providers"
```

**预期结果**:
```json
{
  "providers": ["openai", "deepseek", "siliconflow"],
  "details": {
    "openai": {
      "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
      "default": "gpt-3.5-turbo",
      "description": "OpenAI GPT models"
    },
    "deepseek": {
      "models": ["deepseek-chat", "deepseek-coder"],
      "default": "deepseek-chat",
      "description": "DeepSeek AI models"
    },
    "siliconflow": {
      "models": ["deepseek-ai/DeepSeek-V3", "Qwen/Qwen2.5-7B-Instruct", "meta-llama/Llama-3.1-8B-Instruct"],
      "default": "deepseek-ai/DeepSeek-V3",
      "description": "SiliconFlow hosted models"
    }
  },
  "default_provider": "openai"
}
```

**验收标准**: ✅ 返回支持的LLM厂商列表（包含SiliconFlow）

**自动化测试命令**:
```bash
source .venv/bin/activate && python -m pytest tests/test_happy_path.py::TestHappyPath::test_get_llm_providers_happy_path -v
```

---

### 测试5: LLM连通性测试（无真实API Key）

**目标**: 验证LLM连接测试API的错误处理

**自动化状态**: 🔧 手动测试 (依赖外部API响应)

**步骤**:
```bash
curl -X POST "http://localhost:8000/api/v1/llm/test" \
-H "Content-Type: application/json" \
-d '{"provider": "openai", "api_key": "test-key"}'
```

**预期结果**:
```json
{
  "status": "error",
  "provider": "openai",
  "model": null,
  "error": "Invalid API key for OpenAI: Client error '401 Unauthorized'...",
  "message": "Connection failed"
}
```

**验收标准**: ✅ 正确处理无效API密钥的情况

**说明**: 此测试依赖外部API响应，无法完全自动化。可验证错误处理逻辑是否正常工作。

---

### 测试6: 文本生成测试（无真实API Key）

**目标**: 验证文本生成API的错误处理

**自动化状态**: 🔧 手动测试 (依赖外部API响应)

**步骤**:
```bash
curl -X POST "http://localhost:8000/api/v1/llm/generate" \
-H "Content-Type: application/json" \
-d '{
  "provider": "openai",
  "prompt": "What is machine learning?",
  "max_tokens": 100
}'
```

**预期结果**: 返回401错误，因为没有有效的API密钥

**验收标准**: ✅ 正确处理缺少API密钥的情况

**说明**: 此测试依赖外部API响应，无法完全自动化。主要验证API参数验证和错误处理逻辑。

---

### 测试7: 自动化测试验证

**目标**: 验证所有Happy Path测试通过

**自动化状态**: ✅ 完全自动化测试

**步骤**:
```bash
cd backend
source .venv/bin/activate
python -m pytest tests/test_happy_path.py -v
```

**预期结果**:
```
============================= test session starts ==============================
collected 8 items

tests/test_happy_path.py::TestHappyPath::test_health_check_happy_path PASSED [ 12%]
tests/test_happy_path.py::TestHappyPath::test_get_llm_providers_happy_path PASSED [ 25%]
tests/test_happy_path.py::TestHappyPath::test_llm_factory_happy_path PASSED [ 37%]
tests/test_happy_path.py::TestHappyPath::test_llm_provider_initialization_happy_path PASSED [ 50%]
tests/test_happy_path.py::TestHappyPath::test_llm_provider_config_happy_path PASSED [ 62%]
tests/test_happy_path.py::TestHappyPath::test_api_docs_happy_path PASSED [ 75%]
tests/test_happy_path.py::TestHappyPath::test_openapi_schema_happy_path PASSED [ 87%]
tests/test_happy_path.py::TestHappyPath::test_root_endpoint_happy_path PASSED [100%]

============================== 8 passed in 0.03s ===============================
```

**验收标准**: ✅ 所有8个测试通过

**说明**: 这是核心的自动化测试套件，覆盖所有Happy Path功能。

---

## 🎯 完整功能测试（可选）

如果你有真实的API密钥，可以进行以下完整功能测试：

### 完整LLM连通性测试

**步骤**:
```bash
curl -X POST "http://localhost:8000/api/v1/llm/test" \
-H "Content-Type: application/json" \
-d '{"provider": "openai", "api_key": "your-actual-openai-key"}'
```

**预期结果**:
```json
{
  "status": "success",
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "test_response": "Hello, OpenAI!",
  "message": "Connection successful"
}
```

### 完整文本生成测试

**步骤**:
```bash
curl -X POST "http://localhost:8000/api/v1/llm/generate" \
-H "Content-Type: application/json" \
-d '{
  "provider": "openai",
  "prompt": "What is machine learning?",
  "max_tokens": 100
}'
```

**预期结果**: 返回实际生成的文本内容

---

## ⚡ 快速自动化验收

**一键运行所有自动化测试**:
```bash
cd backend
source .venv/bin/activate

# 运行所有Happy Path测��
python -m pytest tests/test_happy_path.py -v

# 验证LLM工厂功能
python -c "
from app.infrastructure.llm import LLMFactory
print('✅ LLM Providers:', LLMFactory.get_supported_providers())
print('✅ SiliconFlow Models:', LLMFactory.get_provider_models('siliconflow')['models'])
"

# 验证应用加载
python -c "from app.main import app; print('✅ FastAPI app loaded successfully')"
```

**预期结果**: 所有命令都显示成功信息，无错误

## ✅ 验收清单

请逐项确认以下功能：

### 🤖 自动化测试 (必须通过)
- [ ] **自动化测试套件**: 运行 `python -m pytest tests/test_happy_path.py -v`
- [ ] **LLM工厂测试**: 验证提供商和模型列表
- [ ] **应用加载测试**: 验证FastAPI应用正常加载

### 🔧 手动测试 (建议验证)
- [ ] **基础架构**: FastAPI应用正常启动
- [ ] **健康检查**: `/health` 端点返回正确信息
- [ ] **API文档**: `/docs` 页面可访问
- [ ] **LLM提供商**: `/api/v1/llm/providers` 返回厂商列表（包含SiliconFlow）
- [ ] **错误处理**: 无效API密钥时正确返回错误
- [ ] **可选**: 有API密钥时可进行完整功能测试

## 📊 测试自动化状态总览

| 测试项目 | 自动化状态 | 测试命令 | 验收重点 |
|---------|-----------|---------|---------|
| 基础架构验证 | 🔧 手动 | 启动服务器 | 应用启动 |
| 健康检查API | ✅ 自动化 | pytest test_health_check | API响应 |
| API文档验证 | ✅ 自动化 | pytest test_api_docs | 文档访问 |
| LLM提供商列表 | ✅ 自动化 | pytest test_get_llm_providers | 提供商支持 |
| LLM连通性测试 | 🔧 手动 | curl POST /test | 错误处理 |
| 文本生成测试 | 🔧 手动 | curl POST /generate | API验证 |
| 自动化测试套件 | ✅ 自动化 | pytest test_happy_path | 综合功能 |

**自动化图标说明**:
- ✅ **完全自动化**: 可通过pytest自动验证
- 🔧 **手动测试**: 需要手动操作或依赖外部服务

## 🚨 注意事项

1. **不要绕过必要配置**: 如果你没有API密钥，跳过完整功能测试即可
2. **专注Happy Path**: 不要测试边界情况和错误路径
3. **记录问题**: 如果任何测试失败，记录具体错误信息
4. **环境清理**: 测试完成后停止服务器
5. **自动化优先**: 优先运行自动化测试，手动测试作为补充

## 📞 遇到问题？

如果验收过程中遇到任何问题：
1. 检查环境配置是否正确
2. 确认虚拟环境已激活
3. 查看服务器启动日志
4. 联系开发团队获取支持

---

**准备好开始验收了吗？** 请按照上述步骤逐一验证每个功能点。