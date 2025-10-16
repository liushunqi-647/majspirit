import random
from typing import List, Dict, Optional

# -------------------------
# 1. 房间状态和数据结构
# -------------------------

class RoomState:
    """定义房间的各种状态"""
    WAITING = "等待中"    # 房间已创建，等待玩家加入
    FULL = "满员"       # 房间人数已满，可以开始游戏
    IN_GAME = "游戏中"    # 游戏已经开始
    CLOSED = "已关闭"    # 房间已解散或游戏结束

class Room:
    """游戏房间的数据结构"""
    def __init__(self, room_id: str, host_id: str):
        self.room_id: str = room_id                  # 房间唯一ID/代码
        self.host_id: str = host_id                  # 房主ID
        self.max_players: int = 4                    # 最大玩家数
        self.players: List[str] = [host_id]          # 当前玩家列表 (包含房主)
        self.state: str = RoomState.WAITING          # 房间当前状态

    def get_current_player_count(self) -> int:
        """获取当前房间人数"""
        return len(self.players)

    def is_full(self) -> bool:
        """检查房间是否满员"""
        return self.get_current_player_count() == self.max_players

    def __str__(self) -> str:
        """用于友好的打印输出"""
        return (f"房间ID: {self.room_id}, 房主: {self.host_id}, "
                f"人数: {self.get_current_player_count()}/{self.max_players}, "
                f"状态: {self.state}")

# -------------------------
# 2. 房间管理器
# -------------------------

class RoomManager:
    """管理所有房间的创建、加入和游戏开始逻辑"""
    def __init__(self):
        # 存储所有房间 {room_id: Room object}
        self.rooms: Dict[str, Room] = {}
        # 存储玩家ID -> 所在房间ID 的映射，用于快速查找玩家是否已在房间
        self.player_to_room: Dict[str, str] = {}

    def _generate_unique_room_id(self) -> str:
        """生成一个唯一的房间ID (这里使用简单的随机数，实际应用中可能需要更健壮的机制)"""
        while True:
            room_id = str(random.randint(1000, 9999))
            if room_id not in self.rooms:
                return room_id

    # 1. 创建房间
    def create_room(self, host_id: str) -> Dict:
        """允许一个玩家创建一个新房间并成为房主"""
        if host_id in self.player_to_room:
            return {"success": False, "message": f"玩家 {host_id} 已在房间 {self.player_to_room[host_id]} 中。"}

        new_room_id = self._generate_unique_room_id()
        new_room = Room(new_room_id, host_id)
        
        self.rooms[new_room_id] = new_room
        self.player_to_room[host_id] = new_room_id
        
        print(f"[创建] 房间 {new_room_id} 创建成功，房主：{host_id}")
        return {"success": True, "room": new_room}

    # 2. 玩家加入房间
    def join_room(self, room_id: str, player_id: str) -> Dict:
        """玩家加入指定ID的房间"""
        if player_id in self.player_to_room:
            return {"success": False, "message": f"玩家 {player_id} 已在房间 {self.player_to_room[player_id]} 中。"}
        
        room = self.rooms.get(room_id)
        if not room:
            return {"success": False, "message": "房间不存在。"}

        if room.state != RoomState.WAITING:
            return {"success": False, "message": f"房间状态为 '{room.state}'，无法加入。"}

        if room.is_full():
            return {"success": False, "message": "房间已满员。"}

        # 玩家加入
        room.players.append(player_id)
        self.player_to_room[player_id] = room_id
        print(f"[加入] 玩家 {player_id} 加入房间 {room_id}。当前人数: {room.get_current_player_count()}")

        # 检查人数是否达到上限 (满四人)
        if room.is_full():
            room.state = RoomState.FULL
            print(f"[状态] 房间 {room_id} 达到满员状态 ({room.max_players} 人)。")
            # 实际应用中，这里会触发通知所有玩家“房间已满，房主可以开始游戏”的事件

        return {"success": True, "room": room}

    # 3. 房间人数满四人后可以开始游戏
    def start_game(self, room_id: str, initiator_id: str) -> Dict:
        """开始游戏，仅房主在满员时可操作"""
        room = self.rooms.get(room_id)
        if not room:
            return {"success": False, "message": "房间不存在。"}

        if initiator_id != room.host_id:
            return {"success": False, "message": "只有房主才能开始游戏。"}
        
        if not room.is_full():
            return {"success": False, "message": f"房间人数不足，需要 {room.max_players} 人，当前 {room.get_current_player_count()} 人。"}

        if room.state == RoomState.IN_GAME:
            return {"success": False, "message": "游戏已在进行中。"}
        
        # 游戏开始逻辑
        room.state = RoomState.IN_GAME
        print(f"🎉 [开始] 房间 {room_id} 游戏开始！玩家列表: {room.players}")
        # 实际应用中，这里会触发通知所有玩家加载游戏场景的事件

        return {"success": True, "message": "游戏开始。"}

# -------------------------
# 4. 演示代码
# -------------------------

if __name__ == "__main__":
    manager = RoomManager()

    # 定义玩家ID
    P1_HOST = "Alice"
    P2 = "Bob"
    P3 = "Charlie"
    P4 = "David"
    P5_EXTRA = "Eve"

    print("=" * 40)
    print("      游戏房间系统演示")
    print("=" * 40)

    # 1. Alice 创建房间
    result_create = manager.create_room(P1_HOST)
    if not result_create["success"]:
        print(f"错误: {result_create['message']}")
        exit()
        
    room_id = result_create['room'].room_id
    print(manager.rooms[room_id])
    print("-" * 40)

    # 尝试 P1 (房主) 在人数不足时开始游戏
    print(f"尝试开始 (当前人数: {manager.rooms[room_id].get_current_player_count()})...")
    result_start_fail = manager.start_game(room_id, P1_HOST)
    print(f"结果: {result_start_fail['message']}")
    print("-" * 40)

    # 2. Bob 和 Charlie 加入房间
    manager.join_room(room_id, P2)
    manager.join_room(room_id, P3)
    print(manager.rooms[room_id])
    print("-" * 40)

    # 尝试 P2 (非房主) 开始游戏
    print("尝试 P2 开始游戏 (应失败)...")
    result_p2_start = manager.start_game(room_id, P2)
    print(f"结果: {result_p2_start['message']}")
    print("-" * 40)

    # 2. David 加入房间 (房间满员)
    manager.join_room(room_id, P4)
    room = manager.rooms[room_id]
    print(room)
    print("-" * 40)

    # 3. 房主 Alice 开始游戏 (人数已满)
    print("尝试 P1 开始游戏 (人数已满)...")
    result_start_success = manager.start_game(room_id, P1_HOST)
    print(f"结果: {result_start_success['message']}")
    print(manager.rooms[room_id])
    print("-" * 40)

    # 尝试 P5 加入已开始游戏的房间 (应失败)
    print("尝试 Eve 加入已开始游戏的房间...")
    result_join_fail = manager.join_room(room_id, P5_EXTRA)
    print(f"结果: {result_join_fail['message']}")
    
    print("=" * 40)