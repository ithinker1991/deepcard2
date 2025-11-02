/**
 * DeepCard 前端配置文件
 * 支持多种后端环境和端口配置
 */

// 配置对象
const Config = {
    // 当前环境 - 可通过URL参数 ?env=development 来切换
    current: 'development',

    // 环境配置
    environments: {
        // 开发环境 - 本地开发
        development: {
            name: '开发环境',
            apiBaseUrl: 'http://localhost:8004',
            wsUrl: 'ws://localhost:8004/ws',
            debug: true,
            timeout: 30000
        },

        // 测试环境 - 测试服务器
        testing: {
            name: '测试环境',
            apiBaseUrl: 'http://localhost:8005',
            wsUrl: 'ws://localhost:8005/ws',
            debug: true,
            timeout: 25000
        },

        // 生产环境 - 生产服务器
        production: {
            name: '生产环境',
            apiBaseUrl: 'https://api.deepcard.app',
            wsUrl: 'wss://api.deepcard.app/ws',
            debug: false,
            timeout: 20000
        },

        // 自定义环境 - 用户手动配置
        custom: {
            name: '自定义环境',
            apiBaseUrl: this.getCustomBaseUrl() || 'http://localhost:8004',
            wsUrl: this.getCustomWsUrl() || 'ws://localhost:8004/ws',
            debug: true,
            timeout: 30000
        }
    },

    // API端点配置
    endpoints: {
        cards: '/api/v1/cards',
        generate: '/api/v1/cards/generate',
        health: '/health',
        docs: '/docs'
    },

    // 应用配置
    app: {
        name: 'DeepCard',
        version: '1.0.0',
        defaultUserId: 'user-001',
        pagination: {
            defaultLimit: 20,
            maxLimit: 100
        }
    },

    // 获取当前环境配置
    getCurrent() {
        // 从URL参数获取环境
        const urlParams = new URLSearchParams(window.location.search);
        const envParam = urlParams.get('env');
        if (envParam && this.environments[envParam]) {
            this.current = envParam;
        }

        // 从localStorage获取用户配置
        const savedEnv = localStorage.getItem('deepcard_env');
        if (savedEnv && this.environments[savedEnv]) {
            this.current = savedEnv;
        }

        return this.environments[this.current] || this.environments.development;
    },

    // 切换环境
    switchEnvironment(envName) {
        if (this.environments[envName]) {
            this.current = envName;
            localStorage.setItem('deepcard_env', envName);
            return true;
        }
        return false;
    },

    // 获取完整的API URL
    getApiUrl(endpoint) {
        const config = this.getCurrent();
        const baseUrl = config.apiBaseUrl.replace(/\/$/, ''); // 移除末尾斜杠
        const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
        return `${baseUrl}${cleanEndpoint}`;
    },

    // 获取自定义后端URL
    getCustomBaseUrl() {
        return localStorage.getItem('deepcard_custom_backend');
    },

    // 获取自定义WebSocket URL
    getCustomWsUrl() {
        return localStorage.getItem('deepcard_custom_ws');
    },

    // 设置自定义后端配置
    setCustomBackend(apiBaseUrl, wsUrl = null) {
        localStorage.setItem('deepcard_custom_backend', apiBaseUrl);
        if (wsUrl) {
            localStorage.setItem('deepcard_custom_ws', wsUrl);
        }
        this.environments.custom.apiBaseUrl = apiBaseUrl;
        if (wsUrl) {
            this.environments.custom.wsUrl = wsUrl;
        }
    },

    // 获取所有可用环境
    getAvailableEnvironments() {
        return Object.keys(this.environments).map(key => ({
            key,
            name: this.environments[key].name,
            baseUrl: this.environments[key].apiBaseUrl,
            isCurrent: key === this.current
        }));
    },

    // 配置验证
    validateConfig() {
        const config = this.getCurrent();
        const required = ['apiBaseUrl'];
        const missing = required.filter(key => !config[key]);

        if (missing.length > 0) {
            console.error(`配置错误: 缺少必要配置项 ${missing.join(', ')}`);
            return false;
        }

        return true;
    },

    // 调试日志
    log(message, ...args) {
        const config = this.getCurrent();
        if (config.debug) {
            console.log(`[DeepCard Config] ${message}`, ...args);
        }
    }
};

// 导出配置（支持多种模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Config;
} else if (typeof window !== 'undefined') {
    window.DeepCardConfig = Config;
}

// 自动初始化
if (typeof window !== 'undefined') {
    // 在页面加载时验证配置
    document.addEventListener('DOMContentLoaded', () => {
        Config.log('初始化配置', Config.getCurrent());

        if (!Config.validateConfig()) {
            console.error('配置验证失败，请检查配置');
        }
    });
}