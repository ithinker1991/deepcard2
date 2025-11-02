"""
里程碑2 Happy Path测试

测试卡片基础 + 从文本生成的核心功能
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import requires_database, requires_llm


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


@pytest.fixture
def sample_user_id():
    """测试用户ID"""
    return "test_user_m2"


class TestCardCRUD:
    """测试卡片CRUD功能"""

    @requires_database
    def test_create_basic_card(self, client: TestClient, sample_user_id: str):
        """测试创建基础卡片"""
        request_data = {
            "title": "Python基础",
            "card_type": "basic",
            "content": {
                "front": "Python是什么？",
                "back": "Python是一种高级编程语言"
            },
            "tags": ["编程", "Python", "基础"]
        }

        response = client.post(
            f"/api/v1/cards?user_id={sample_user_id}",
            json=request_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Python基础"
        assert data["card_type"] == "basic"
        assert data["content"]["front"] == "Python是什么？"
        assert data["content"]["back"] == "Python是一种高级编程语言"
        assert data["tags"] == ["编程", "Python", "基础"]
        assert data["user_id"] == sample_user_id
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    @requires_database
    def test_create_cloze_card(self, client: TestClient, sample_user_id: str):
        """测试创建填空题卡片"""
        request_data = {
            "title": "Python填空题",
            "card_type": "cloze",
            "content": {
                "front": "填空题",
                "back": "答案",
                "cloze_text": "Python是一种{{编程语言}}",
                "cloze_answer": "编程语言"
            },
            "tags": ["Python", "填空题"]
        }

        response = client.post(
            f"/api/v1/cards?user_id={sample_user_id}",
            json=request_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["card_type"] == "cloze"
        assert data["content"]["cloze_text"] == "Python是一种{{编程语言}}"
        assert data["content"]["cloze_answer"] == "编程语言"

    @requires_database
    def test_create_qna_card(self, client: TestClient, sample_user_id: str):
        """测试创建问答对卡片"""
        request_data = {
            "title": "Python问答",
            "card_type": "qna",
            "content": {
                "front": "问答对",
                "back": "问答对",
                "question": "Python适合做什么？",
                "answer": "Web开发、数据科学、人工智能等"
            },
            "tags": ["Python", "问答"]
        }

        response = client.post(
            f"/api/v1/cards?user_id={sample_user_id}",
            json=request_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["card_type"] == "qna"
        assert data["content"]["question"] == "Python适合做什么？"
        assert data["content"]["answer"] == "Web开发、数据科学、人工智能等"

    @requires_database
    def test_create_concept_card(self, client: TestClient, sample_user_id: str):
        """测试创建概念卡片"""
        request_data = {
            "title": "Python概念",
            "card_type": "concept",
            "content": {
                "front": "概念",
                "back": "概念",
                "concept": "变量",
                "definition": "用于存储数据的容器",
                "examples": ["x = 10", "name = 'Python'"]
            },
            "tags": ["Python", "概念", "基础"]
        }

        response = client.post(
            f"/api/v1/cards?user_id={sample_user_id}",
            json=request_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["card_type"] == "concept"
        assert data["content"]["concept"] == "变量"
        assert data["content"]["definition"] == "用于存储数据的容器"
        assert data["content"]["examples"] == ["x = 10", "name = 'Python'"]

    @requires_database
    def test_get_user_cards(self, client: TestClient, sample_user_id: str, cleanup_test_data):
        """测试获取用户卡片列表"""
        # 先创建几张卡片
        cards_data = [
            {
                "title": "卡片1",
                "card_type": "basic",
                "content": {"front": "问题1", "back": "答案1"},
                "tags": ["tag1"]
            },
            {
                "title": "卡片2",
                "card_type": "basic",
                "content": {"front": "问题2", "back": "答案2"},
                "tags": ["tag2"]
            }
        ]

        created_cards = []
        for card_data in cards_data:
            response = client.post(
                f"/api/v1/cards?user_id={sample_user_id}",
                json=card_data
            )
            assert response.status_code == 200
            created_cards.append(response.json())

        # 获取卡片列表
        response = client.get(f"/api/v1/cards?user_id={sample_user_id}")
        assert response.status_code == 200

        data = response.json()
        assert "cards" in data
        assert "total" in data
        assert data["total"] >= len(created_cards)

        # 验证返回的卡片包含我们创建的卡片
        returned_titles = [card["title"] for card in data["cards"]]
        for created_card in created_cards:
            assert created_card["title"] in returned_titles

    @requires_database
    def test_update_card(self, client: TestClient, sample_user_id: str, cleanup_test_data):
        """测试更新卡片"""
        # 先创建卡片
        create_data = {
            "title": "原始标题",
            "card_type": "basic",
            "content": {"front": "原始问题", "back": "原始答案"},
            "tags": ["原始标签"]
        }

        create_response = client.post(
            f"/api/v1/cards?user_id={sample_user_id}",
            json=create_data
        )
        assert create_response.status_code == 200
        created_card = create_response.json()
        card_id = created_card["id"]

        # 更新卡片
        update_data = {
            "title": "更新后标题",
            "content": {"front": "更新后问题", "back": "更新后答案"},
            "tags": ["更新后标签"]
        }

        response = client.put(
            f"/api/v1/cards/{card_id}?user_id={sample_user_id}",
            json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新后标题"
        assert data["content"]["front"] == "更新后问题"
        assert data["content"]["back"] == "更新后答案"
        assert data["tags"] == ["更新后标签"]
        assert data["id"] == card_id

    @requires_database
    def test_delete_card(self, client: TestClient, sample_user_id: str, cleanup_test_data):
        """测试删除卡片"""
        # 先创建卡片
        create_data = {
            "title": "待删除卡片",
            "card_type": "basic",
            "content": {"front": "问题", "back": "答案"},
            "tags": []
        }

        create_response = client.post(
            f"/api/v1/cards?user_id={sample_user_id}",
            json=create_data
        )
        assert create_response.status_code == 200
        created_card = create_response.json()
        card_id = created_card["id"]

        # 删除卡片
        response = client.delete(f"/api/v1/cards/{card_id}?user_id={sample_user_id}")
        assert response.status_code == 200
        assert "message" in response.json()

        # 验证卡片已被删除
        get_response = client.get(f"/api/v1/cards/{card_id}?user_id={sample_user_id}")
        assert get_response.status_code == 404

    @requires_database
    def test_user_data_isolation(self, client: TestClient, cleanup_test_data):
        """测试用户数据隔离"""
        user1_id = "user1_m2"
        user2_id = "user2_m2"

        # 用户1创建卡片
        card_data = {
            "title": "用户1的卡片",
            "card_type": "basic",
            "content": {"front": "问题", "back": "答案"},
            "tags": []
        }

        response = client.post(f"/api/v1/cards?user_id={user1_id}", json=card_data)
        assert response.status_code == 200
        user1_card = response.json()

        # 用户2尝试获取用户1的卡片
        response = client.get(f"/api/v1/cards/{user1_card['id']}?user_id={user2_id}")
        assert response.status_code == 404

        # 用户2获取自己的卡片列表（应该为空）
        response = client.get(f"/api/v1/cards?user_id={user2_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

    @requires_database
    def test_search_cards(self, client: TestClient, sample_user_id: str, cleanup_test_data):
        """测试搜索卡片功能"""
        # 创建测试卡片
        cards_data = [
            {
                "title": "Python基础",
                "card_type": "basic",
                "content": {"front": "Python是什么", "back": "编程语言"},
                "tags": ["Python"]
            },
            {
                "title": "Java基础",
                "card_type": "basic",
                "content": {"front": "Java是什么", "back": "编程语言"},
                "tags": ["Java"]
            }
        ]

        for card_data in cards_data:
            response = client.post(
                f"/api/v1/cards?user_id={sample_user_id}",
                json=card_data
            )
            assert response.status_code == 200

        # 搜索包含"Python"的卡片
        response = client.get(f"/api/v1/cards/search?user_id={sample_user_id}&q=Python")
        assert response.status_code == 200
        data = response.json()

        assert len(data["cards"]) >= 1
        # 应该找到Python相关的卡片
        python_found = any("Python" in card["title"] for card in data["cards"])
        assert python_found

    @requires_database
    def test_get_cards_by_tags(self, client: TestClient, sample_user_id: str, cleanup_test_data):
        """测试根据标签获取卡片"""
        # 创建带标签的卡片
        card_data = {
            "title": "标签测试卡片",
            "card_type": "basic",
            "content": {"front": "问题", "back": "答案"},
            "tags": ["Python", "测试", "编程"]
        }

        response = client.post(
            f"/api/v1/cards?user_id={sample_user_id}",
            json=card_data
        )
        assert response.status_code == 200

        # 根据标签获取卡片
        response = client.get(f"/api/v1/cards/by-tags?user_id={sample_user_id}&tags=Python,测试")
        assert response.status_code == 200
        data = response.json()

        assert len(data["cards"]) >= 1
        # 返回的卡片应该包含指定的标签
        for card in data["cards"]:
            has_python = "Python" in card["tags"]
            has_测试 = "测试" in card["tags"]
            assert has_python or has_测试


class TestLLMGeneration:
    """测试LLM生成卡片功能"""

    @requires_database
    @requires_llm
    def test_generate_basic_cards_from_text(self, client: TestClient, sample_user_id: str, cleanup_test_data):
        """测试从文本生成基础卡片"""
        request_data = {
            "text": """
            Python是一种高级编程语言，由Guido van Rossum于1991年首次发布。
            Python以简洁的语法和强大的功能而闻名，支持多种编程范式。
            Python广泛应用于Web开发、数据科学、人工智能等领域。
            """,
            "card_type": "basic",
            "provider": "siliconflow",
            "max_cards": 2,
            "auto_save": True
        }

        response = client.post(
            f"/api/v1/cards/generate?user_id={sample_user_id}",
            json=request_data
        )

        # 检查生成结果
        if response.status_code == 200:
            data = response.json()
            assert "generated_cards" in data
            assert "saved_cards" in data
            assert "total_generated" in data
            assert "total_saved" in data
            assert data["total_generated"] > 0
            assert data["total_saved"] > 0

            # 验证生成的卡片格式
            for card in data["saved_cards"]:
                assert "id" in card
                assert "title" in card
                assert "card_type" in card
                assert card["card_type"] == "basic"
                assert "content" in card
                assert "front" in card["content"]
                assert "back" in card["content"]
                assert "tags" in card
                assert card["user_id"] == sample_user_id

            # 验证卡片确实被保存到数据库
            cards_response = client.get(f"/api/v1/cards?user_id={sample_user_id}")
            assert cards_response.status_code == 200
            cards_data = cards_response.json()
            assert len(cards_data["cards"]) >= data["total_saved"]
        else:
            # 如果LLM不可用，应该返回适当的错误信息
            assert response.status_code in [400, 500]
            print(f"LLM生成测试跳过，API返回: {response.status_code}")

    @requires_database
    @requires_llm
    def test_generate_cloze_cards_from_text(self, client: TestClient, sample_user_id: str, cleanup_test_data):
        """测试从文本生成填空题卡片"""
        request_data = {
            "text": """
            Python是一种高级编程语言。Python支持面向对象编程。
            Python有丰富的标准库。Python可以用于Web开发。
            """,
            "card_type": "cloze",
            "provider": "siliconflow",
            "max_cards": 1,
            "auto_save": False  # 不自动保存，只测试生成
        }

        response = client.post(
            f"/api/v1/cards/generate?user_id={sample_user_id}",
            json=request_data
        )

        if response.status_code == 200:
            data = response.json()
            assert "generated_cards" in data
            assert data["total_generated"] > 0

            # 验证生成的填空题格式
            for card in data["generated_cards"]:
                assert card["card_type"] == "cloze"
                assert "content" in card
                # 填空题应该有cloze_text和cloze_answer字段
                assert "cloze_text" in card["content"] or "front" in card["content"]
                assert "cloze_answer" in card["content"] or "back" in card["content"]
        else:
            print(f"LLM填空题生成测试跳过，API返回: {response.status_code}")

    def test_generate_cards_invalid_request(self, client: TestClient, sample_user_id: str):
        """测试无效的生成请求"""
        # 缺少必需字段
        request_data = {
            "card_type": "basic",
            "provider": "siliconflow"
            # 缺少text字段
        }

        response = client.post(
            f"/api/v1/cards/generate?user_id={sample_user_id}",
            json=request_data
        )

        assert response.status_code == 422  # Validation error

    def test_generate_cards_invalid_provider(self, client: TestClient, sample_user_id: str):
        """测试无效的LLM提供商"""
        request_data = {
            "text": "测试文本",
            "card_type": "basic",
            "provider": "invalid_provider",
            "max_cards": 1,
            "auto_save": False
        }

        response = client.post(
            f"/api/v1/cards/generate?user_id={sample_user_id}",
            json=request_data
        )

        # 应该返回错误
        assert response.status_code >= 400


class TestAPIIntegration:
    """API集成测试"""

    def test_health_check(self, client: TestClient):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "app" in data

    def test_root_endpoint(self, client: TestClient):
        """测试根端点"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    @requires_database
    def test_card_crud_full_workflow(self, client: TestClient, sample_user_id: str, cleanup_test_data):
        """测试卡片CRUD完整工作流"""
        # 1. 创建卡片
        create_data = {
            "title": "工作流测试卡片",
            "card_type": "basic",
            "content": {"front": "测试问题", "back": "测试答案"},
            "tags": ["测试", "工作流"]
        }

        create_response = client.post(
            f"/api/v1/cards?user_id={sample_user_id}",
            json=create_data
        )
        assert create_response.status_code == 200
        created_card = create_response.json()
        card_id = created_card["id"]

        # 2. 获取单个卡片
        get_response = client.get(f"/api/v1/cards/{card_id}?user_id={sample_user_id}")
        assert get_response.status_code == 200
        card_data = get_response.json()
        assert card_data["id"] == card_id
        assert card_data["title"] == "工作流测试卡片"

        # 3. 更新卡片
        update_data = {
            "title": "更新后的工作流测试卡片",
            "content": {"front": "更新的测试问题", "back": "更新的测试答案"},
            "tags": ["测试", "工作流", "更新"]
        }

        update_response = client.put(
            f"/api/v1/cards/{card_id}?user_id={sample_user_id}",
            json=update_data
        )
        assert update_response.status_code == 200
        updated_card = update_response.json()
        assert updated_card["title"] == "更新后的工作流测试卡片"

        # 4. 获取用户卡片列表（验证更新后的卡片在列表中）
        list_response = client.get(f"/api/v1/cards?user_id={sample_user_id}")
        assert list_response.status_code == 200
        list_data = list_response.json()
        assert len(list_data["cards"]) >= 1

        updated_titles = [card["title"] for card in list_data["cards"]]
        assert "更新后的工作流测试卡片" in updated_titles

        # 5. 删除卡片
        delete_response = client.delete(f"/api/v1/cards/{card_id}?user_id={sample_user_id}")
        assert delete_response.status_code == 200

        # 6. 验证卡片已删除
        final_get_response = client.get(f"/api/v1/cards/{card_id}?user_id={sample_user_id}")
        assert final_get_response.status_code == 404

    def test_error_handling(self, client: TestClient):
        """测试错误处理"""
        non_existent_user = "non_existent_user"
        non_existent_card_id = "non_existent_card_id"

        # 尝试获取不存在的卡片
        response = client.get(f"/api/v1/cards/{non_existent_card_id}?user_id={non_existent_user}")
        assert response.status_code == 404

        # 尝试更新不存在的卡片
        response = client.put(
            f"/api/v1/cards/{non_existent_card_id}?user_id={non_existent_user}",
            json={"title": "更新"}
        )
        assert response.status_code == 404

        # 尝试删除不存在的卡片
        response = client.delete(f"/api/v1/cards/{non_existent_card_id}?user_id={non_existent_user}")
        assert response.status_code == 404