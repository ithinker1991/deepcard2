# 自动化测试配置化需求

## 📋 需求概述

为了提高���试的灵活性和可维护性，需要实现配置化的自动化测试开关，允许在不同场景下选择性地运行测试套件。

## 🎯 核心功能

### 1. 数据库测试开关
- **功能**: 控制是否运行涉及数据库操作的自动化测试
- **用途**:
  - CI/CD环境中可能不使用真实数据库
  - 本地开发时可以选择性运行数据库测试
  - 避免测试数据库的数据污染

### 2. LLM调用测试开关
- **功能**: 控制是否运行涉及真实LLM API调用的测试
- **用途**:
  - 避免产生API调用费用
  - 防止API配额耗尽
  - 在无网络环境下运行测试
  - CI/CD环境中的成本控制

## 🔧 实现方案

### 配置文件结构

**backend/app/shared/testing_config.py**:
```python
from enum import Enum
from pydantic import BaseSettings
from app.shared.config import get_settings

class TestMode(str, Enum):
    OFFLINE = "offline"      # 无外部依赖
    LOCAL = "local"         # 包含数据库
    INTEGRATION = "integration"  # 包含所有外部依赖
    FULL = "full"           # 完整测试套件

class TestingConfig(BaseSettings):
    """测试配置管理"""

    # 测试模式
    test_mode: TestMode = TestMode.OFFLINE

    # 功能开关
    enable_database_tests: bool = False
    enable_llm_tests: bool = False
    enable_external_api_tests: bool = False

    # 数据库测试配置
    test_database_url: str = "sqlite:///./test.db"
    cleanup_test_data: bool = True

    # LLM测试配置
    llm_test_provider: str = "openai"
    llm_test_model: str = "gpt-3.5-turbo"
    max_llm_test_calls: int = 5

    # 性能测试配置
    enable_performance_tests: bool = False
    performance_test_timeout: int = 30

    @property
    def should_run_database_tests(self) -> bool:
        return self.enable_database_tests and self.test_mode in [TestMode.LOCAL, TestMode.INTEGRATION, TestMode.FULL]

    @property
    def should_run_llm_tests(self) -> bool:
        return self.enable_llm_tests and self.test_mode in [TestMode.INTEGRATION, TestMode.FULL]

def get_testing_config() -> TestingConfig:
    """获取测试配置"""
    return TestingConfig()
```

### 环境变量配置

**.env.testing**:
```bash
# 测试模式: offline, local, integration, full
TEST_MODE=offline

# 功能开关
ENABLE_DATABASE_TESTS=false
ENABLE_LLM_TESTS=false
ENABLE_EXTERNAL_API_TESTS=false

# 数据库测试
TEST_DATABASE_URL=sqlite:///./test.db
CLEANUP_TEST_DATA=true

# LLM测试
LLM_TEST_PROVIDER=openai
LLM_TEST_MODEL=gpt-3.5-turbo
MAX_LLM_TEST_CALLS=5

# 性能测试
ENABLE_PERFORMANCE_TESTS=false
PERFORMANCE_TEST_TIMEOUT=30
```

### 测试装饰器实现

**backend/tests/conftest.py 扩展**:
```python
import pytest
from app.shared.testing_config import get_testing_config

testing_config = get_testing_config()

def pytest_configure(config):
    """pytest配置钩子"""
    config.addinivalue_line(
        "markers", "database: mark test as database test"
    )
    config.addinivalue_line(
        "markers", "llm: mark test as LLM test"
    )
    config.addinivalue_line(
        "markers", "external_api: mark test as external API test"
    )

def pytest_collection_modifyitems(config, items):
    """根据配置动态跳过测试"""
    skip_database = not testing_config.should_run_database_tests
    skip_llm = not testing_config.should_run_llm_tests
    skip_external = not testing_config.enable_external_api_tests

    for item in items:
        if skip_database and "database" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="Database tests disabled"))
        if skip_llm and "llm" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="LLM tests disabled"))
        if skip_external and "external_api" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="External API tests disabled"))

# 数据库测试装饰器
def requires_database(func):
    """需要数据库的测试装饰器"""
    func = pytest.mark.database(func)
    return func

# LLM测试装饰器
def requires_llm(func):
    """需要LLM的测试装饰器"""
    func = pytest.mark.llm(func)
    return func

# 外部API测试装饰器
def requires_external_api(func):
    """需要外部API的测试装饰器"""
    func = pytest.mark.external_api(func)
    return func
```

### 测试示例

**backend/tests/test_database_operations.py**:
```python
import pytest
from tests.conftest import requires_database
from app.infrastructure.database import get_db

@requires_database
def test_card_crud_operations():
    """测试卡片的数据库操作"""
    # 数据库测试代码
    pass

@requires_database
def test_user_data_isolation():
    """测试用户数据隔离"""
    # 数据库隔离测试代码
    pass
```

**backend/tests/test_llm_integration.py**:
```python
import pytest
from tests.conftest import requires_llm
from app.infrastructure.llm import LLMFactory

@requires_llm
def test_siliconflow_text_generation():
    """测试SiliconFlow文本生成"""
    provider = LLMFactory.create_provider(
        "siliconflow",
        get_testing_config().llm_test_provider
    )
    # LLM测试代码
    pass

@requires_llm
def test_multiple_llm_providers():
    """测试多个LLM提供商"""
    # 多提供商测试代码
    pass
```

**backend/tests/test_external_apis.py**:
```python
import pytest
from tests.conftest import requires_external_api

@requires_external_api
def test_url_content_extraction():
    """测试URL内容提取"""
    # 外部API测试代码
    pass
```

## 📋 使用场景

### 1. 本地开发环境
```bash
# 运行基础测试（无外部依赖）
TEST_MODE=offline python -m pytest tests/ -v

# 运行包含数据库的测试
TEST_MODE=local ENABLE_DATABASE_TESTS=true python -m pytest tests/ -v

# 运行完整集成测试
TEST_MODE=integration ENABLE_DATABASE_TESTS=true ENABLE_LLM_TESTS=true python -m pytest tests/ -v
```

### 2. CI/CD环境
```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]

jobs:
  test-offline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Run Offline Tests
        run: |
          cd backend
          pip install -r requirements.txt
          TEST_MODE=offline python -m pytest tests/ -v

  test-integration:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Run Integration Tests
        env:
          TEST_MODE: integration
          ENABLE_DATABASE_TESTS: true
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest tests/ -v
```

### 3. 性能测试
```bash
# 运行性能测试
ENABLE_PERFORMANCE_TESTS=true python -m pytest tests/performance/ -v

# 性能基准测试
TEST_MODE=full ENABLE_PERFORMANCE_TESTS=true python -m pytest tests/performance/benchmarks.py -v
```

## 🧪 测试配置验证

### 配置验证命令
```python
# backend/tests/verify_test_config.py
from app.shared.testing_config import get_testing_config

def verify_test_config():
    """验证测试配置"""
    config = get_testing_config()

    print(f"Test Mode: {config.test_mode}")
    print(f"Database Tests: {config.should_run_database_tests}")
    print(f"LLM Tests: {config.should_run_llm_tests}")
    print(f"External API Tests: {config.enable_external_api_tests}")

    # 验证配置一致性
    if config.test_mode == TestMode.FULL:
        assert config.enable_database_tests, "Full mode should enable database tests"
        assert config.enable_llm_tests, "Full mode should enable LLM tests"
        assert config.enable_external_api_tests, "Full mode should enable external API tests"

if __name__ == "__main__":
    verify_test_config()
```

## 📊 配置组合表

| 测试模式 | 数据库测试 | LLM测试 | 外部API测试 | 性能测试 | 使用场景 |
|---------|-----------|---------|-------------|---------|---------|
| offline | ❌ | ❌ | ❌ | ❌ | 基础逻辑测试 |
| local | ✅ | ❌ | ❌ | ❌ | 本地开发调试 |
| integration | ✅ | ✅ | ❌ | ❌ | 集成测试 |
| full | ✅ | ✅ | ✅ | ✅ | 完整测试套件 |

## 🔄 实施计划

### 里程碑2 (卡片基础)
- [ ] 实现基础测试配置框架
- [ ] 添加数据库测试开关
- [ ] 创建测试装饰器

### 里程碑3 (资源管理)
- [ ] 添加外部API测试开关
- [ ] 实现URL内容提取测试
- [ ] 配置CI/CD测试流程

### 里程碑4 (高级生成)
- [ ] 完善LLM测试配置
- [ ] 添加LLM调用限制
- [ ] 实现测试成本控制

### 里程碑5 (学习功能)
- [ ] 添加性能测试配置
- [ ] 实现基准测试
- [ ] 创建性能监控

## 📚 相关文档

- [pytest配置文档](https://docs.pytest.org/)
- [测试配置最佳实践](./docs/testing-best-practices.md)
- [CI/CD配置指南](./docs/ci-cd-setup.md)

---

**这个配置化测试功能将在后续里程碑中逐步实现，确保项目的长期可维护性。**