"""
测试配置验证脚本
"""

from app.shared.testing_config import get_testing_config, TestMode


def verify_test_config():
    """验证测试配置"""
    config = get_testing_config()

    print("=" * 50)
    print("测试配置验证")
    print("=" * 50)

    print(f"测试模式: {config.test_mode}")
    print(f"数据库测试: {config.should_run_database_tests}")
    print(f"LLM测试: {config.should_run_llm_tests}")
    print(f"外部API测试: {config.enable_external_api_tests}")
    print(f"性能测试: {config.enable_performance_tests}")
    print()

    print("详细配置:")
    print(f"  测试数据库URL: {config.test_database_url}")
    print(f"  清理测试数据: {config.cleanup_test_data}")
    print(f"  LLM测试提供商: {config.llm_test_provider}")
    print(f"  LLM测试模型: {config.llm_test_model}")
    print(f"  最大LLM测试调用: {config.max_llm_test_calls}")
    print(f"  性能测试超时: {config.performance_test_timeout}秒")
    print()

    # 验证配置一致性
    warnings = []
    errors = []

    if config.test_mode == TestMode.FULL:
        if not config.enable_database_tests:
            errors.append("Full模式应该启用数据库测试")
        if not config.enable_llm_tests:
            errors.append("Full模式应该启用LLM测试")
        if not config.enable_external_api_tests:
            errors.append("Full模式应该启用外部API测试")

    if config.test_mode == TestMode.INTEGRATION:
        if not config.enable_database_tests:
            errors.append("Integration模式应该启用数据库测试")
        if not config.enable_llm_tests:
            errors.append("Integration模式应该启用LLM测试")

    if config.test_mode == TestMode.LOCAL:
        if not config.enable_database_tests:
            errors.append("Local模式应该启用数据库测试")
        if config.enable_llm_tests:
            warnings.append("Local模式通常不需要LLM测试")

    # 输出结果
    if errors:
        print("❌ 配置错误:")
        for error in errors:
            print(f"  - {error}")
        print()

    if warnings:
        print("⚠️  配置警告:")
        for warning in warnings:
            print(f"  - {warning}")
        print()

    if not errors and not warnings:
        print("✅ 配置验证通过！")
    elif not errors:
        print("✅ 配置基本正确，但有一些建议")
    else:
        print("❌ 配置存在问题，请修复后重试")

    print("=" * 50)
    return len(errors) == 0


def print_usage_examples():
    """打印使用示例"""
    print("使用示例:")
    print()
    print("1. 运行基础测试（无外部依赖）:")
    print("   TEST_MODE=offline python -m pytest tests/ -v")
    print()
    print("2. 运行包含数据库的测试:")
    print("   TEST_MODE=local ENABLE_DATABASE_TESTS=true python -m pytest tests/ -v")
    print()
    print("3. 运行完整集成测试:")
    print("   TEST_MODE=integration ENABLE_DATABASE_TESTS=true ENABLE_LLM_TESTS=true python -m pytest tests/ -v")
    print()
    print("4. 运行完整测试套件:")
    print("   TEST_MODE=full ENABLE_DATABASE_TESTS=true ENABLE_LLM_TESTS=true ENABLE_EXTERNAL_API_TESTS=true python -m pytest tests/ -v")
    print()
    print("5. 只运行数据库测试:")
    print("   TEST_MODE=local ENABLE_DATABASE_TESTS=true python -m pytest tests/ -v -k database")
    print()
    print("6. 只运行LLM测试:")
    print("   TEST_MODE=integration ENABLE_DATABASE_TESTS=true ENABLE_LLM_TESTS=true python -m pytest tests/ -v -k llm")


if __name__ == "__main__":
    success = verify_test_config()
    print()
    print_usage_examples()

    if not success:
        exit(1)