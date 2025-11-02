#!/bin/bash

# DeepCard 开发环境停止脚本

echo "🛑 DeepCard 开发环境停止中..."

# 停止所有相关进程
pkill -f "uvicorn" || true
pkill -f "python.*http.server" || true

echo "✅ 所有服务已停止"

# 清理日志文件（可选）
if [ "$1" = "--clean-logs" ]; then
    echo "🧹 清理日志文件..."
    rm -f logs/*.log
    echo "✅ 日志文件已清理"
fi

echo "🎯 开发环境已完全停止"