# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import uvicorn

from app.server.common.enviroment_conf import env_check

if __name__ == '__main__':
    env_check()
    uvicorn.run("app.server.app:app", host="0.0.0.0", port=8000, reload=True)



