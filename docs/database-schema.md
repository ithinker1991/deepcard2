# 数据库Schema设计

## 概述

基于SQLite数据库设计，支持后续平滑迁移到PostgreSQL。采用规范化设计，确保数据一致性和查询效率。

## 表结构设计

### 1. 用户表 (users)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url VARCHAR(255),
    preferences JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### 2. 资源表 (resources)

```sql
CREATE TABLE resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000),
    content TEXT,
    content_type VARCHAR(50) NOT NULL, -- 'article', 'book', 'social_post', 'webpage', 'document'
    author VARCHAR(200),
    source_name VARCHAR(100), -- 来源平台名称
    published_at TIMESTAMP,
    tags JSON DEFAULT '[]',
    metadata JSON DEFAULT '{}', -- 额外的元数据
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'archived', 'deleted'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_resources_user_id ON resources(user_id);
CREATE INDEX idx_resources_content_type ON resources(content_type);
CREATE INDEX idx_resources_status ON resources(status);
CREATE INDEX idx_resources_created_at ON resources(created_at);
CREATE INDEX idx_resources_url ON resources(url(255));
```

### 3. 卡片表 (cards)

```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    source_resource_id INTEGER, -- 可选，关联到原始资源
    front_content TEXT NOT NULL,
    back_content TEXT NOT NULL,
    card_type VARCHAR(20) DEFAULT 'basic', -- 'basic', 'cloze', 'qna', 'concept'
    extra_info TEXT, -- 额外的提示信息
    tags JSON DEFAULT '[]',
    difficulty_level INTEGER DEFAULT 1, -- 1-5 难度等级
    generation_method VARCHAR(50), -- 'manual', 'llm_generated', 'extracted'
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'archived', 'deleted'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (source_resource_id) REFERENCES resources(id) ON DELETE SET NULL
);

-- 索引
CREATE INDEX idx_cards_user_id ON cards(user_id);
CREATE INDEX idx_cards_source_resource_id ON cards(source_resource_id);
CREATE INDEX idx_cards_card_type ON cards(card_type);
CREATE INDEX idx_cards_status ON cards(status);
CREATE INDEX idx_cards_difficulty_level ON cards(difficulty_level);
CREATE INDEX idx_cards_created_at ON cards(created_at);

-- 全文搜索索引 (SQLite FTS5)
CREATE VIRTUAL TABLE cards_fts USING fts5(
    card_id,
    front_content,
    back_content,
    content='cards',
    content_rowid='id'
);

-- 触发器，保持FTS索引同步
CREATE TRIGGER cards_fts_insert AFTER INSERT ON cards BEGIN
    INSERT INTO cards_fts(card_id, front_content, back_content)
    VALUES (new.id, new.front_content, new.back_content);
END;

CREATE TRIGGER cards_fts_delete AFTER DELETE ON cards BEGIN
    INSERT INTO cards_fts(cards_fts, card_id, front_content, back_content)
    VALUES ('delete', old.id, old.front_content, old.back_content);
END;

CREATE TRIGGER cards_fts_update AFTER UPDATE ON cards BEGIN
    INSERT INTO cards_fts(cards_fts, card_id, front_content, back_content)
    VALUES ('delete', old.id, old.front_content, old.back_content);
    INSERT INTO cards_fts(card_id, front_content, back_content)
    VALUES (new.id, new.front_content, new.back_content);
END;
```

### 4. 学习记录表 (learning_records)

```sql
CREATE TABLE learning_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    ease_factor REAL DEFAULT 2.5, -- 难度因子 (1.3 - 2.5)
    interval_days INTEGER DEFAULT 1, -- 复习间隔（天）
    repetitions INTEGER DEFAULT 0, -- 重复次数
    quality INTEGER DEFAULT 0, -- 最后一次复习质量 (0-5)
    last_review TIMESTAMP,
    next_review TIMESTAMP DEFAULT (datetime('now', '+1 day')),
    total_reviews INTEGER DEFAULT 0,
    correct_reviews INTEGER DEFAULT 0,
    average_response_time REAL, -- 平均响应时间（秒）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_learning_records_user_id ON learning_records(user_id);
CREATE INDEX idx_learning_records_card_id ON learning_records(card_id);
CREATE INDEX idx_learning_records_next_review ON learning_records(next_review);
CREATE INDEX idx_learning_records_due_review ON learning_records(user_id, next_review);
CREATE UNIQUE INDEX idx_learning_records_user_card ON learning_records(user_id, card_id);
```

### 5. 学习会话表 (study_sessions)

```sql
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    cards_studied INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    total_response_time REAL DEFAULT 0, -- 总���应时间
    session_type VARCHAR(20) DEFAULT 'review', -- 'review', 'new', 'mixed'
    settings JSON DEFAULT '{}', -- 会话设置
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_study_sessions_user_id ON study_sessions(user_id);
CREATE INDEX idx_study_sessions_start_time ON study_sessions(start_time);
CREATE INDEX idx_study_sessions_session_type ON study_sessions(session_type);
```

### 6. 会话详情表 (session_details)

```sql
CREATE TABLE session_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    response_time REAL, -- 响应时间（秒）
    quality INTEGER NOT NULL, -- 复习质量 (0-5)
    is_correct BOOLEAN NOT NULL,
    review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id) REFERENCES study_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_session_details_session_id ON session_details(session_id);
CREATE INDEX idx_session_details_card_id ON session_details(card_id);
CREATE INDEX idx_session_details_review_time ON session_details(review_time);
```

### 7. 生成任务表 (generation_tasks)

```sql
CREATE TABLE generation_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    source_resource_id INTEGER,
    strategy VARCHAR(50) NOT NULL, -- 'key_point_extraction', 'summary_based', 'concept_mapping', 'custom_prompt'
    parameters JSON DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed'
    progress INTEGER DEFAULT 0, -- 进度百分比
    result_summary JSON, -- 生成结果摘要
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (source_resource_id) REFERENCES resources(id) ON DELETE SET NULL
);

-- 索引
CREATE INDEX idx_generation_tasks_user_id ON generation_tasks(user_id);
CREATE INDEX idx_generation_tasks_status ON generation_tasks(status);
CREATE INDEX idx_generation_tasks_strategy ON generation_tasks(strategy);
CREATE INDEX idx_generation_tasks_created_at ON generation_tasks(created_at);
```

### 8. 生成的卡片关联表 (generated_cards)

```sql
CREATE TABLE generated_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    generation_confidence REAL, -- 生成置信度 (0-1)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (task_id) REFERENCES generation_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_generated_cards_task_id ON generated_cards(task_id);
CREATE INDEX idx_generated_cards_card_id ON generated_cards(card_id);
CREATE UNIQUE INDEX idx_generated_cards_task_card ON generated_cards(task_id, card_id);
```

### 9. 用户统计表 (user_statistics)

```sql
CREATE TABLE user_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stat_date DATE NOT NULL,
    total_cards INTEGER DEFAULT 0,
    new_cards INTEGER DEFAULT 0,
    reviewed_cards INTEGER DEFAULT 0,
    correct_reviews INTEGER DEFAULT 0,
    study_time INTEGER DEFAULT 0, -- 学习时间（分钟）
    cards_created INTEGER DEFAULT 0,
    resources_added INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 索引
CREATE UNIQUE INDEX idx_user_statistics_user_date ON user_statistics(user_id, stat_date);
CREATE INDEX idx_user_statistics_stat_date ON user_statistics(stat_date);
```

### 10. 系统配置表 (system_settings)

```sql
CREATE TABLE system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE, -- 是否对前端公开
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_system_settings_key ON system_settings(key);
CREATE INDEX idx_system_settings_is_public ON system_settings(is_public);
```

## 视图定义

### 1. 待复习卡片视图

```sql
CREATE VIEW due_cards AS
SELECT
    c.*,
    lr.ease_factor,
    lr.interval_days,
    lr.repetitions,
    lr.next_review,
    r.title as resource_title,
    r.url as resource_url
FROM cards c
LEFT JOIN learning_records lr ON c.id = lr.card_id
LEFT JOIN resources r ON c.source_resource_id = r.id
WHERE c.status = 'active'
  AND lr.next_review <= datetime('now')
  AND c.user_id = lr.user_id;
```

### 2. 用户学习统计视图

```sql
CREATE VIEW user_learning_stats AS
SELECT
    u.id as user_id,
    u.username,
    COUNT(DISTINCT c.id) as total_cards,
    COUNT(DISTINCT CASE WHEN lr.next_review <= datetime('now') THEN c.id END) as due_cards,
    COUNT(DISTINCT r.id) as total_resources,
    COALESCE(SUM(ss.cards_studied), 0) as total_cards_studied,
    COALESCE(AVG(lr.average_response_time), 0) as avg_response_time
FROM users u
LEFT JOIN cards c ON u.id = c.user_id AND c.status = 'active'
LEFT JOIN learning_records lr ON c.id = lr.card_id
LEFT JOIN resources r ON u.id = r.user_id AND r.status = 'active'
LEFT JOIN study_sessions ss ON u.id = ss.user_id
GROUP BY u.id, u.username;
```

## 数据约束和触发器

### 1. 自动更新时间戳

```sql
-- 用户表更新时间触发器
CREATE TRIGGER update_users_timestamp
    AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- 资源表更新时间触发器
CREATE TRIGGER update_resources_timestamp
    AFTER UPDATE ON resources
BEGIN
    UPDATE resources SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- 卡片表更新时间触发器
CREATE TRIGGER update_cards_timestamp
    AFTER UPDATE ON cards
BEGIN
    UPDATE cards SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- 学习记录更新时间触发器
CREATE TRIGGER update_learning_records_timestamp
    AFTER UPDATE ON learning_records
BEGIN
    UPDATE learning_records SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

### 2. 数据完整性约束

```sql
-- 确保卡片内容不为空
CREATE TRIGGER validate_card_content
    BEFORE INSERT ON cards
BEGIN
    SELECT CASE
        WHEN NEW.front_content IS NULL OR TRIM(NEW.front_content) = ''
        THEN RAISE(ABORT, 'Card front content cannot be empty')
        WHEN NEW.back_content IS NULL OR TRIM(NEW.back_content) = ''
        THEN RAISE(ABORT, 'Card back content cannot be empty')
    END;
END;

-- 确保学习记录的数值范围
CREATE TRIGGER validate_learning_record_values
    BEFORE INSERT ON learning_records
BEGIN
    SELECT CASE
        WHEN NEW.ease_factor < 1.3 OR NEW.ease_factor > 2.5
        THEN RAISE(ABORT, 'Ease factor must be between 1.3 and 2.5')
        WHEN NEW.interval_days < 0
        THEN RAISE(ABORT, 'Interval days cannot be negative')
        WHEN NEW.repetitions < 0
        THEN RAISE(ABORT, 'Repetitions cannot be negative')
        WHEN NEW.quality < 0 OR NEW.quality > 5
        THEN RAISE(ABORT, 'Quality must be between 0 and 5')
    END;
END;
```

## 初始数据

### 1. 系统配置初始数据

```sql
INSERT INTO system_settings (key, value, description, is_public) VALUES
('default_difficulty', '1', '默认卡片难度等级', true),
('max_cards_per_session', '20', '每次学习会话最大卡片数', true),
('review_interval_multiplier', '1.0', '复习间隔倍数', false),
('llm_model', 'gpt-3.5-turbo', '默认LLM模型', false),
('auto_generate_summary', 'true', '是否自动生成摘要', true),
('enable_notifications', 'true', '是否启用通知', true);
```

## 性能优化建议

1. **分区策略**: 对于大量数据，可以考虑按用户ID进行分区
2. **索引优化**: 根据查询模式调整索引，避免过多索引影响写入性能
3. **缓存策略**: 对热点数据使用Redis缓存
4. **数据归档**: 定期归档历史数据，保持主表性能
5. **批量操作**: 对于批量数据操作，使用事务确保一致性

## 迁移到PostgreSQL的注意事项

1. **数据类型转换**:
   - SQLite的INTEGER PRIMARY KEY AUTOINCREMENT → PostgreSQL的SERIAL或BIGSERIAL
   - SQLite的TEXT → PostgreSQL的TEXT或VARCHAR
   - SQLite的JSON → PostgreSQL的JSONB

2. **函数差异**:
   - SQLite的datetime('now') → PostgreSQL的NOW()
   - SQLite的CURRENT_TIMESTAMP → PostgreSQL的CURRENT_TIMESTAMP

3. **全文搜索**:
   - SQLite的FTS5 → PostgreSQL的全文搜索功能

4. **约束和触发器**: 语法略有差异，需要调整

这个数据库设计支持项目的核心功能，具有良好的扩展性和性能。