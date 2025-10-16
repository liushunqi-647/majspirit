import asyncio
import websockets
import datetime

# 存储所有已连接的客户端
connected_clients = set()

async def handler(websocket, path):
    """
    处理新的 WebSocket 连接和消息的函数
    :param websocket: 当前连接的 WebSocket 对象
    :param path: 连接路径（在本例中未用到）
    """
    # 1. 注册新连接
    connected_clients.add(websocket)
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] 新客户端已连接. 当前连接数: {len(connected_clients)}")

    try:
        # 2. 循环接收消息
        async for message in websocket:
            print(f"[{now}] 收到消息: {message}")
            
            # 3. 构造回复消息（服务器回显）
            response = f"服务器已收到: {message}"
            
            # 4. 发送回复给客户端 (你也可以选择广播给所有客户端)
            await websocket.send(response)
            
            # 示例：广播给所有连接的客户端
            # broadcast_message = f"[{now}] 某客户端说: {message}"
            # await asyncio.gather(*[client.send(broadcast_message) for client in connected_clients])

    except websockets.exceptions.ConnectionClosedOK:
        # 客户端正常关闭连接
        print(f"[{now}] 客户端连接已正常关闭.")
    except Exception as e:
        # 捕获其他异常（如网络错误）
        print(f"[{now}] 连接发生错误: {e}")
    finally:
        # 5. 移除已关闭的连接
        connected_clients.remove(websocket)
        print(f"[{now}] 客户端已断开. 当前连接数: {len(connected_clients)}")

async def main():
    """
    启动 WebSocket 服务器
    """
    # 监听所有网络接口 (0.0.0.0) 的 8765 端口
    host = "0.0.0.0"
    port = 8765
    print(f"WebSocket 服务器正在 {host}:{port} 上运行...")
    
    # 启动服务器
    async with websockets.serve(handler, host, port):
        # 保持主线程运行，直到接收到停止信号
        await asyncio.Future() 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止.")