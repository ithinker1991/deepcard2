#!/bin/bash

# DeepCard 开发环境启动脚本
# 解决端口管理、CORS和前后端联调问题

set -e

echo "🚀 DeepCard 开发环境启动中..."

# ���置
BACKEND_PORT=8004
FRONTEND_PORT=3000
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"

# 检查目录
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ 错误: backend目录不存在"
    exit 1
fi

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ 错误: frontend目录不存在"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "$BACKEND_DIR/.venv" ]; then
    echo "❌ 错误: 虚拟环境不存在，请先创建: cd backend && python -m venv .venv"
    exit 1
fi

# 停止现有进程
echo "🧹 清理现有进程..."
pkill -f "uvicorn.*$BACKEND_PORT" || true
pkill -f "python.*http.server.*$FRONTEND_PORT" || true

# 等待进程完全停止
sleep 2

# 启动后端
echo "🔧 启动后端服务 (端口: $BACKEND_PORT)..."
cd "$BACKEND_DIR"
source .venv/bin/activate

# 设置环境变量，确保CORS配置正确
export CORS_ORIGINS="http://localhost:$FRONTEND_PORT,http://127.0.0.1:$FRONTEND_PORT,file://"
export DEBUG=true

# 启动后端（后台运行）
nohup uvicorn app.main:app \
    --host 0.0.0.0 \
    --port $BACKEND_PORT \
    --reload \
    --log-level info > ../logs/backend.log 2>&1 &

BACKEND_PID=$!
echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 3

# 检查后端健康状态
if curl -s "http://localhost:$BACKEND_PORT/health" > /dev/null; then
    echo "✅ 后端服务健康检查通过"
else
    echo "❌ 后端服务启动失败"
    exit 1
fi

# 启动前端
echo "🎨 启动前端服务 (端口: $FRONTEND_PORT)..."
cd "../$FRONTEND_DIR"

# 前端现在使用配置系统，无需手动修改地址

# 启动前端HTTP服务器（后台运行）
nohup python -m http.server $FRONTEND_PORT > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"

# 等待前端启动
sleep 2

echo ""
echo "🎉 开发环境启动完成！"
echo ""
echo "📍 服务地址:"
echo "   前端: http://localhost:$FRONTEND_PORT"
echo "   后端: http://localhost:$BACKEND_PORT"
echo "   API文档: http://localhost:$BACKEND_PORT/docs"
echo ""
echo "🔧 调试信息:"
echo "   后端PID: $BACKEND_PID"
echo "   前端PID: $FRONTEND_PID"
echo "   日志位置: logs/backend.log, logs/frontend.log"
echo ""
echo "🛑 停止服务:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   或运行: ./stop_dev.sh"
echo ""
echo "🌐 自��打开浏览器..."
if command -v open > /dev/null; then
    sleep 1
    open "http://localhost:$FRONTEND_PORT"
elif command -v xdg-open > /dev/null; then
    sleep 1
    xdg-open "http://localhost:$FRONTEND_PORT"
fi

echo "✨ 开始使用 DeepCard 吧！"