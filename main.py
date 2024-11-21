from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from logger import get_logger
from mainConfig import ALLOWED_BRANCHES,SHELL_FILE,SYNC_DIR
import subprocess

app = FastAPI()

@app.post("/git-webhook-code")
async def git_webhook(request: Request):
    try:
        # FastAPI 使用 `request.json()` 获取请求体
        payload = await request.json()
        ref = payload.get('ref')
        ProjectName = payload.get('repository').get('name')

        # 日志记录代码...
        logObj = get_logger(ProjectName)
        logObj.info(f"提交记录: {request.headers}")

        if ref in ALLOWED_BRANCHES:

            # 参数
            project_path = SYNC_DIR[ProjectName]
            branch_name = ref.split("/")[-1]
            command = f"cd {project_path} && git pull origin {branch_name}"
            # 执行 Shell 脚本
            result = subprocess.run(
                ["bash", SHELL_FILE, project_path, branch_name],
                capture_output=True,
                text=True
            )

            stdout = result.stdout
            stderr = result.stderr
            error = result.returncode

            log_data = f"""
            === Webhook Triggered ===
            Date: {datetime.now().isoformat()}
            Command: {command}
            ------------------------
            stdout: {stdout}
            stderr: {stderr}
            error: {'No error' if error == 0 else 'Error occurred'}
            ------------------------
            """

            # 将日志写入文件
            logObj.info(log_data)
            return JSONResponse({"message": "Git pull executed successfully!"}, status_code=200)

        else:
            logObj.warning(f"Webhook received, but not a valid push branch")
            return JSONResponse({"message": "Webhook received, but not a valid push branch"}, status_code=200)

    except Exception as e:
        logObj.error(f"Error during git pull: {str(e)}")
        return JSONResponse({"message": f"Error during git pull: {str(e)}"}, status_code=500)
    finally:
        # 日志记录此次提交的触发
        finallyLog = get_logger()
        finallyLog.info(f"Webhook Triggered: {datetime.now().isoformat()}")

# if __name__ == '__main__':
#     # 设置 Webhook 服务器端口
#     port = 16310
#     app.run(host='0.0.0.0', port=port)