try:
    # dotenv仅用于开发环境， 正式环境使用其他方式配置环境变量（例如supervisor)
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import uvicorn

from app import app

if __name__ == '__main__':
    uvicorn.run('app:app', port=8001, host='0.0.0.0', reload=False, proxy_headers=True)