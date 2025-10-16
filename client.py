import asyncio
import websockets
import datetime

async def connect_and_send():
    """
    连接到 WebSocket 服务器并发送消息
    """
    uri = "ws://localhost:8765" # 注意：使用 ws:// 而不是 http://
    
    try:
        # 建立连接
        async with websockets.connect(uri) as websocket:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] 已连接到服务器: {uri}")
            
            # 循环发送消息
            for i in range(5):
                message = f"Hello WebSocket, 这是第 {i+1} 条消息"
                
                # 1. 发送消息
                await websocket.send(message)
                print(f"[{now}] 客户端发送: {message}")

                # 2. 接收服务器回复
                response = await websocket.recv()
                print(f"[{now}] 客户端接收: {response}")
                
                # 稍微等待一下
                await asyncio.sleep(1) 
            
            # 3. 发送完毕，关闭连接
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] 消息发送完毕，客户端即将关闭连接。")

    except ConnectionRefusedError:
        print(f"[{now}] 错误：连接被拒绝，请确保服务器 (server.py) 正在运行。")
    except Exception as e:
        print(f"[{now}] 发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(connect_and_send())
