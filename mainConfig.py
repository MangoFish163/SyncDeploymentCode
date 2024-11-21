# mainConfig.py

# 自定义配置
# 允许触发 Webhook 的分支
ALLOWED_BRANCHES = ['refs/heads/main', 'refs/heads/dev']
# 日志文件路径，用于记录 Webhook 请求日志
LOGFILE = './webhook-log.txt'
# Shell 脚本路径
SHELL_FILE = "./git_pull.sh"

# 同步部署目录配置
# 每个键值对表示一个同步项目，键为项目名称，值为项目在服务器上的部署路径
# 如果有多个同步项目，可以在这里追加
SYNC_DIR = {
    'Lar10':'/www/wwwroot/Lar/Lar10',
    # 'YourProjectDir':'/www/wwwroot/YourProjectDir'
}