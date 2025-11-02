# 领域模型设计

## 概述

基于DDD (Domain-Driven Design) 原则，我们将系统划分为四个核心领域，每个领域负责特定的业务逻辑。

## 核心领域

### 1. 卡片领域 (Card Domain)

#### 实体 (Entities)

**Card (卡片)**
```python
class Card:
    id: CardId
    front: str          # 正面内容
    back: str           # 背面内容
    type: CardType      # 卡片类型
    source_id: Optional[ResourceId]  # 来源资源
    created_at: datetime
    updated_at: datetime

    # 业务方法
    def update_content(self, front: str, back: str) -> None
    def link_to_resource(self, resource_id: ResourceId) -> None
    def is_valid(self) -> bool
```

**CardType (卡片类型枚举)**
- `BASIC`: 基础问答卡
- `CLOZE`: 填空卡
- `QNA`: 问答卡
- `CONCEPT`: 概念卡

#### 值对象 (Value Objects)

**CardId**: 卡片唯一标识符
**CardContent**: 卡片内容值对象，包含正面和背面内容

#### 领域服务 (Domain Services)

**CardValidationService**: 卡片内容验证
- 验证卡片内容是否符合格式要求
- 检查内容长度和敏感词

**CardFactory**: 卡片创建工厂
- 根据不同类型创建卡片
- 内容标准化处理

### 2. 资源领域 (Resource Domain)

#### 实体 (Entities)

**Resource (资源)**
```python
class Resource:
    id: ResourceId
    title: str
    url: Optional[str]
    content: str
    type: ResourceType
    metadata: Dict[str, Any]
    created_at: datetime

    # 业务方法
    def extract_key_points(self) -> List[str]
    def get_summary(self) -> str
    def is_accessible(self) -> bool
```

**ResourceType (资源类型枚举)**
- `ARTICLE`: 文章
- `BOOK`: 书籍
- `SOCIAL_POST`: 社交媒体帖子
- `WEBPAGE`: 网页
- `DOCUMENT`: 文档

#### 值对象 (Value Objects)

**ResourceId**: 资源唯一标识符
**ResourceMetadata**: 资源元数据（作者、发布时间、标签等）

#### 领域服务 (Domain Services)

**ContentExtractor**: 内容提取服务
- 从URL获取网页内容
- 解析不同格式的文档
- 清理和标准化内容

**ResourceParser**: 资源解析服务
- 解析文章结构
- 提取关键信息
- 生成内容摘要

### 3. 学习领域 (Learning Domain)

#### 实体 (Entities)

**LearningRecord (学习记录)**
```python
class LearningRecord:
    id: LearningRecordId
    card_id: CardId
    user_id: UserId
    ease_factor: float     # 难度因子
    interval: int          # 复习间隔（天）
    repetitions: int       # 重复次数
    next_review: datetime  # 下次复习时间
    last_review: Optional[datetime]

    # 业务方法
    def update_review(self, quality: int) -> None
    def is_due_for_review(self) -> bool
    def calculate_next_review(self, quality: int) -> datetime
```

**StudySession (学习会话)**
```python
class StudySession:
    id: SessionId
    user_id: UserId
    start_time: datetime
    end_time: Optional[datetime]
    cards_studied: int
    correct_answers: int

    # 业务方法
    def add_card_result(self, correct: bool) -> None
    def finish_session(self) -> None
    def get_accuracy(self) -> float
```

#### 值对象 (Value Objects)

**LearningRecordId**: 学习记录标识符
**SessionId**: 学习会话标识符
**ReviewQuality**: 复习质量评级 (0-5)

#### 领域服务 (Domain Services)

**SpacedRepetitionService**: 间隔重复算法服务
- 实现SuperMemo 2或Anki算法
- 计算下次复习时间
- 调整难度因子

**LearningScheduler**: 学习调度服务
- 生成每日学习计划
- 优化卡片复习顺序

### 4. 生成领域 (Generation Domain)

#### 实体 (Entities)

**GenerationTask (生成任务)**
```python
class GenerationTask:
    id: TaskId
    source_id: ResourceId
    strategy: GenerationStrategy
    status: TaskStatus
    parameters: Dict[str, Any]
    result: Optional[List[CardId]]
    created_at: datetime
    completed_at: Optional[datetime]

    # 业务方法
    def start_generation(self) -> None
    def complete_with_result(self, cards: List[CardId]) -> None
    def fail_with_error(self, error: str) -> None
```

#### 值对象 (Value Objects)

**GenerationStrategy**: 生成策略枚举
- `KEY_POINT_EXTRACTION`: 关键点提取
- `SUMMARY_BASED`: 基于摘要生成
- `CONCEPT_MAPPING`: 概念映射
- `CUSTOM_PROMPT`: 自定义提示

**TaskStatus**: 任务状态枚举
- `PENDING`: 等待中
- `RUNNING`: 运行中
- `COMPLETED`: 已完成
- `FAILED`: 失败

#### 领域服务 (Domain Services)

**ContentGenerator**: 内容生成服务
- 调用LLM API生成卡片
- 处理不同的生成策略
- 结果后处理和验证

**PromptBuilder**: 提示词构建服务
- 根据策略构建LLM提示词
- 优化提示词效果
- 管理提示词模板

## 领域关系图

```
Resource (1) -----> (*) Card
     |                   |
     |                   |
     v                   v
GenerationTask (*)     (*) LearningRecord
                           |
                           |
                           v
                    StudySession (1)
```

## 聚合根 (Aggregate Roots)

1. **CardAggregate**: Card实体为聚合根，管理卡片相关的所有操作
2. **ResourceAggregate**: Resource实体为聚合根，管理资源相关的所有操作
3. **LearningAggregate**: LearningRecord实体为聚合根，管理学习相关的所有操作
4. **GenerationAggregate**: GenerationTask实体为聚合根，管理生成相关的所有操作

## 领域事件 (Domain Events)

### Card Domain
- `CardCreated`: 卡片创建事件
- `CardUpdated`: 卡片更新事件
- `CardDeleted`: 卡片删除事件

### Resource Domain
- `ResourceAdded`: 资源添加事件
- `ResourceContentUpdated`: 资源内容更新事件

### Learning Domain
- `CardReviewed`: 卡片复习事件
- `StudySessionCompleted`: 学习会话完成事件

### Generation Domain
- `GenerationStarted`: 生成开始事件
- `GenerationCompleted`: 生成完成事件
- `GenerationFailed`: 生成失败事件

## 数据一致性保证

1. **强一致性**: 聚合内部操作保证强一致性
2. **最终一致性**: 跨聚合操作通过领域事件保证最终一致性
3. **事务边界**: 每个聚合根定义事务边界

## 扩展性考虑

1. **新卡片类型**: 通过CardType枚举扩展，无需修改核心逻辑
2. **新资源类型**: 通过ResourceType枚举扩展，增加对应的解析器
3. **新生成策略**: 通过GenerationStrategy枚举扩展，增加新的生成算法
4. **新记忆算法**: 通过LearningScheduler接口扩展，支持不同的记忆算法