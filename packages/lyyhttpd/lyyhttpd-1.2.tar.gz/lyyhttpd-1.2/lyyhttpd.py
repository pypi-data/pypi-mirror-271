# http_server.py
from fastapi import FastAPI, Request,HTTPException
from typing import Callable
import queue
from starlette.responses import Response
from f1999 import handle_root, handle_showmsg, handle_path2, show_reason  # 确保从正确的模块导入你的处理函数


from flask import Flask,request,Response,send_file

def flask_app(ip="127.0.0.1",port=8080,queue=None):
    app = Flask(__name__)

    @app.get("/favicon.ico")
    def favicon():
            #return Response(status=204)
            return send_file(r'D:\UserData\Pictures\ico\apple苹果8.ico', mimetype='image/x-icon')
    @app.get('/reason')
    def reason():
        #code = request.args.get('code')
        data = {"cmd": "reason"}
        data.update(request.args)
        queue.put(data)
        print("put code to queue,code=", dict(request.args))
        return f'Received code: { dict(request.args)}'
    
    @app.get('/jiepan')
    def jys_reason():
        #code = request.args.get('code')
        data = {"cmd": "jys_reason"}
        data.update(request.args)
        queue.put(data)
        print("put code to queue,code=", dict(request.args))
        return f'Received code: { dict(request.args)}'
    @app.post('/showmsg')
    def showmsg():
        data = request.get_json()
        print("showmsg",data)
        queue.put(data)
        return 'ok', 200
        # df["msgtype"] = "showsql"
        # json_text_list = df.iloc[::-1].apply(lambda row: json.dumps({k: (v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime) else v) for k, v in row.to_dict().items()}), axis=1).to_list()
        # data = json.dumps(json_text_list)
        # send_post_request("http://127.0.0.1:8088/showmsg",data=data, headers={'Content-Type': 'application/json'})

    @app.route('/{path_param}', methods=['GET', 'POST'])
    def route_handler(path_param):
        print(f"get /{path_param}")        
        return Response("Hello, World!")
    
    @app.errorhandler(404)
    def page_not_found(e):
        print(f"{request.method} request: {request.path} with args {dict(request.args)}, but not found")
        return "lyy404 Not Found", 404
    return app


# 定义一个字典，映射路径参数到不同的处理函数
path_to_handler: dict[str, Callable[[str, queue.Queue], Response]] = {
    "root": handle_root,
    "showmsg": lambda data, queue: handle_showmsg(data, queue),
    "path2": lambda data, queue: handle_path2(data, queue),
    "reason": lambda data, queue: show_reason(data, queue),
    # 可以根据需要添加更多的路径和处理函数
}

def lyyfastapi_multi(path_to_handler: dict[str, Callable[[str, queue.Queue], Response]], fastapi_queue: queue.Queue) -> FastAPI:
    app = FastAPI()

    @app.get("/favicon.ico")
    async def favicon():
        return Response(content="", media_type="image/x-icon")

    @app.route("/{path_param}", methods=['GET', 'POST'])
    async def route_handler(request: Request):
        path_param =request.path_params.get("path_param")
        print(f"route_handler Received request for path_param: /{path_param}")
        data = await request.body()
        data = data.decode()
        if request.method == "GET":
            data_dict =dict(request.query_params)
            data_dict["cmd"] = path_param
            if fastapi_queue is not None:
                #print("put data to queue,data=",data_dict)
                fastapi_queue.put(data_dict)
            else:
                print("no fastapi_queue")
            return Response("Reason OK")
        
        elif request.method == "POST":
            data = await  request.json()
            print("data = await request.body()=",request.body(),data)
            if fastapi_queue is not None:
                fastapi_queue.put(data)

        if path_param in path_to_handler:
            return path_to_handler[path_param](data, fastapi_queue)
        else:
            return Response("No handler for this path", status_code=404)

    @app.get("/{path_param:path}")
    async def catch_all(path_param: str):
        print(f"catch_all Received request for path_param: /{path_param}")
        if path_param == "":
            print("""# 如果path_param为空，表示请求的是根目录，不应该被catch_all处理""")
            pass
        else:
            raise HTTPException(status_code=404, detail="Not Found")

    return app

def create_application(path_to_handler: dict[str, Callable[[str, queue.Queue], Response]], fastapi_queue: queue.Queue):
    return lyyfastapi_multi(path_to_handler, fastapi_queue)

# 导出 FastAPI 应用实例

if __name__ == "__main__":
    import uvicorn
    # 此行将由 Gunicorn 使用来启动 Uvicorn
    q = queue.Queue()
    app = flask_app(q)
    uvicorn.run(app, host="0.0.0.0", port=8088)