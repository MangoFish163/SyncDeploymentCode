#!/bin/bash

# 检查是否运行在 root 下
if [ "$EUID" -ne 0 ]; then
  echo "Switching to root..."
  sudo "$0" "$@"
  exit
fi

# 加载必要环境
if [ -f /etc/profile ]; then
    source /etc/profile
fi

# 脚本逻辑
PROJECT_PATH=$1
BRANCH_NAME=$2

echo "Running as root"
echo "Project path: $PROJECT_PATH"
echo "Pulling branch: $BRANCH_NAME"

cd "$PROJECT_PATH" || exit
sudo git pull origin "$BRANCH_NAME"

# 如果需要更多命令操作直接自行追加