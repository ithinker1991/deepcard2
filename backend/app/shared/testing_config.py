"""测试配置管理"""

from enum import Enum
from typing import Optional
import os

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

from app.shared.config import get_settings


class TestMode(str, Enum):
    """测试模式枚举"""
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
    llm_test_provider: str = "siliconflow"
    llm_test_model: str = "deepseek-ai/DeepSeek-V3"
    max_llm_test_calls: int = 5

    # 性能测试配置
    enable_performance_tests: bool = False
    performance_test_timeout: int = 30

    class Config:
        extra = "ignore"
        env_file = ".env.testing"

    @property
    def should_run_database_tests(self) -> bool:
        """是否应该运行数据库测试"""
        return (
            self.enable_database_tests and
            self.test_mode in [TestMode.LOCAL, TestMode.INTEGRATION, TestMode.FULL]
        )

    @property
    def should_run_llm_tests(self) -> bool:
        """是否应该运行LLM测试"""
        return (
            self.enable_llm_tests and
            self.test_mode in [TestMode.INTEGRATION, TestMode.FULL]
        )

    @property
    def should_run_external_api_tests(self) -> bool:
        """是否应该运行外部API测试"""
        return (
            self.enable_external_api_tests and
            self.test_mode == TestMode.FULL
        )


def get_testing_config() -> TestingConfig:
    """获取测试配置"""
    # 从环境变量读取测试模式
    test_mode = os.getenv("TEST_MODE", "offline")

    # 读取功能开关
    enable_db = os.getenv("ENABLE_DATABASE_TESTS", "false").lower() == "true"
    enable_llm = os.getenv("ENABLE_LLM_TESTS", "false").lower() == "true"
    enable_external = os.getenv("ENABLE_EXTERNAL_API_TESTS", "false").lower() == "true"

    # 创建配置
    config = TestingConfig(
        test_mode=TestMode(test_mode),
        enable_database_tests=enable_db,
        enable_llm_tests=enable_llm,
        enable_external_api_tests=enable_external,
        test_database_url=os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db"),
        llm_test_provider=os.getenv("LLM_TEST_PROVIDER", "siliconflow"),
        llm_test_model=os.getenv("LLM_TEST_MODEL", "deepseek-ai/DeepSeek-V3"),
        max_llm_test_calls=int(os.getenv("MAX_LLM_TEST_CALLS", "5")),
        cleanup_test_data=os.getenv("CLEANUP_TEST_DATA", "true").lower() == "true",
        enable_performance_tests=os.getenv("ENABLE_PERFORMANCE_TESTS", "false").lower() == "true",
        performance_test_timeout=int(os.getenv("PERFORMANCE_TEST_TIMEOUT", "30"))
    )

    return config