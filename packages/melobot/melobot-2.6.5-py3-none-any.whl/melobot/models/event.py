import json
import re

from ..base.abc import BotEvent
from ..base.typing import Any, Callable, Literal, MsgSegment, Optional, cast
from .msg import get_seg_datas, get_segs, to_cq_str, to_segments


class BotEventBuilder:
    @staticmethod
    def try_build(rawEvent: dict | str) -> BotEvent | None:
        if isinstance(rawEvent, str):
            raw: dict[str, str | float | int] = json.loads(rawEvent)
        else:
            raw = rawEvent

        match raw.get("post_type"):
            case "message_sent" | "message":
                return MessageEvent(raw)
            case "request":
                return RequestEvent(raw)
            case "notice":
                return NoticeEvent(raw)
            case "meta_event":
                return MetaEvent(raw)
            case _:
                return None


class MessageEvent(BotEvent):
    """消息事件类型

    .. admonition:: 提示
       :class: tip

       一般无需手动实例化该类，多数情况会直接使用本类对象，或将本类用作类型注解。
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)
        #: 收到事件的机器人 qq 号
        self.bot_id: int = cast(int, raw.get("self_id"))
        #: 消息事件的消息 id
        self.id: int
        #: 消息事件的发送者数据结构
        self.sender: MessageEvent.Sender
        #: 消息事件的来源群号，私聊时此属性也存在并为 :obj:`None`
        self.group_id: Optional[int]
        #: 使用 CQ 字符串表示的，本事件的所有消息内容
        self.raw_content: str
        #: 使用消息段对象列表表示的，本事件的所有消息内容
        self.content: list[MsgSegment]
        #: 本事件的所有消息内容中，纯文本消息的合并字符串
        self.text: str
        #: 消息字体
        self.font: int
        #: 临时消息的来源标记，不是临时消息时为 :obj:`None`
        self.temp_src: Optional[str]

        self._cq_regex = re.compile(r"\[CQ:.*?\]")

        self.id = raw["message_id"]
        self.raw_content = self._format_to_str(raw["raw_message"])
        self.content = self._format_to_array(raw["message"])
        self.sender = MessageEvent.Sender(
            raw=raw,
            isGroup=self.is_group(),
            isGroupAnonym=self.is_group_anonym(),
        )
        self.group_id = raw.get("group_id")

        self.text = self._get_text(self.content)
        self.font = raw["font"]

        self.temp_src = None
        if src := raw.get("temp_source"):
            self.temp_src = MessageEvent._TEMP_SRC_MAP[src]

    @property
    def time(self) -> int:
        """事件发生时刻的时间戳"""
        return cast(int, self.raw.get("time"))

    @property
    def type(self) -> Literal["message"]:
        """事件的类型（返回指定字面量）"""
        return "message"

    _TEMP_SRC_MAP = {
        0: "群聊",
        1: "QQ咨询",
        2: "查找",
        3: "QQ电影",
        4: "热聊",
        6: "验证消息",
        7: "多人聊天",
        8: "约会",
        9: "通讯录",
    }

    def _format_to_str(self, content: list | str) -> str:
        """对外部零信任，强制转换为 cq 字符串格式"""
        if not isinstance(content, str):
            return to_cq_str(content)
        else:
            return content

    def _format_to_array(self, content: list | str) -> list[MsgSegment]:
        """对外部零信任，强制转换为消息段格式"""
        if isinstance(content, str):
            return to_segments(content)

        for item in content:
            if item["type"] == "text":
                continue

            for k, v in item["data"].items():
                if not isinstance(v, str):
                    continue
                if v.isdigit() or (len(v) >= 2 and v[0] == "-" and v[1:].isdigit()):
                    item["data"][k] = int(v)
                    continue

                try:
                    item["data"][k] = float(v)
                except Exception:
                    pass
        return content

    def _get_text(self, content: list[MsgSegment]) -> str:
        """获取消息中所有文本消息，返回合并字符串"""
        text_list = [
            cast(str, item["data"]["text"]) for item in content if item["type"] == "text"
        ]
        return "".join(text_list)

    def get_segments(self, type: str) -> list[MsgSegment]:
        """提取指定类型的，消息段对象组成的消息段对象列表

        :param type: 消息段类型（对应 OneBot 标准中每种消息段对象的 type）
        :return: 消息段对象列表
        """
        return get_segs(self.content, type)

    def get_datas(
        self, type: str, data: str, convert: Optional[Callable[[Any], Any]] = None
    ) -> list[Any]:
        """提取指定类型的消息段对象中的指定数据

        当没有任何对应类型的消息段时，为空列表。如果有对应类型的消息段，但是指定的数据键名不存在，
        则在列表中产生 :obj:`None` 值.

        可以指定 `convert` 来强制转换类型，不填则不使用类型转换

        使用示例如下：

        .. code:: python

           # 假设 event 是 MessageEvent 对象，即象征一个消息事件
           datas = event.get_datas('at', 'qq')
           # datas 将是此事件中，所有 at 消息段的 "qq" 数据值所组成的列表

        :param type: 消息段类型（对应 OneBot 标准中每种消息段对象的 type）
        :param data: 消息段对象 `data` 中的键名
        :param convert: 类型转换使用的函数
        :return: 值列表
        """
        return get_seg_datas(self.content, type, data, convert)

    def is_private(self) -> bool:
        """是否为私聊消息（注意群临时会话属于该类别）"""
        return self.raw["message_type"] == "private"

    def is_friend(self) -> bool:
        """是否为好友消息"""
        return self.raw["message_type"] == "private" and self.raw["sub_type"] == "friend"

    def is_group(self) -> bool:
        """是否为群消息（正常群消息、群匿名消息、群自身消息、群系统消息属于该类型）"""
        return self.raw["message_type"] == "group"

    def is_group_normal(self) -> bool:
        """是否为正常群消息"""
        return self.raw["message_type"] == "group" and self.raw["sub_type"] == "normal"

    def is_group_anonym(self) -> bool:
        """是否为匿名群消息"""
        return self.raw["message_type"] == "group" and self.raw["sub_type"] == "anonymous"

    def is_group_self(self) -> bool:
        """是否为群自身消息（即 bot 自己群中发的消息）"""
        return (
            self.raw["message_type"] == "group" and self.raw["sub_type"] == "group_self"
        )

    def is_group_temp(self) -> bool:
        """是否为群临时会话（属于私聊的一种）"""
        return self.raw["message_type"] == "private" and self.raw["sub_type"] == "group"

    def is_temp(self) -> bool:
        """是否为临时会话（属于私聊的一种）"""
        return "temp_source" in self.raw.keys()

    def is_group_notice(self) -> bool:
        """是否为群中的\"系统消息\" """
        return self.raw["message_type"] == "group" and self.raw["sub_type"] == "notice"

    class Sender:
        """消息事件发送者数据结构

        .. admonition:: 提示
           :class: tip

           一般无需手动实例化该类，多数情况会直接使用本类对象，或将本类用作类型注解。
        """

        def __init__(self, raw: dict, isGroup: bool, isGroupAnonym: bool) -> None:
            self._rawEvent = raw
            self._isGroup = isGroup
            self._isGroupAnonym = isGroupAnonym

            #: 发送者的 qq 号
            self.id: int
            #: 发送者昵称
            self.nickname: Optional[str]
            #: 发送者性别
            self.sex: Optional[str]
            #: 发送者年龄
            self.age: Optional[int]
            #: 发送者的群名片
            self.group_card: Optional[str]
            #: 发送者的群中角色
            self.group_role: Optional[Literal["owner", "admin", "member", "anonymous"]]
            #: 发送者的群头衔
            self.group_title: Optional[str]
            #: 发送者的地区
            self.group_area: Optional[str]
            #: 发送者的群等级
            self.group_level: Optional[str]

            #: 匿名发送者的 id（此属性只在事件为群匿名消息事件时存在）
            self.anonym_id: Optional[int]
            #: 匿名发送者的名字（此属性只在事件为群匿名消息事件时存在）
            self.anonym_name: Optional[str]
            #: 匿名发送者的匿名 flag（此属性只在事件为群匿名消息事件时存在）
            self.anonym_flag: Optional[str]

            self.id = raw["user_id"]
            self.nickname = raw["sender"].get("nickname")
            self.sex = raw["sender"].get("sex")
            self.age = raw["sender"].get("age")

            self.group_card = raw["sender"].get("card")
            self.group_role = raw["sender"].get("role")
            self.group_title = raw["sender"].get("title")
            self.group_area = raw["sender"].get("area")
            self.group_level = raw["sender"].get("level")

            if isGroup and isGroupAnonym:
                self.anonym_id = raw["anonymous"].get("id")
                self.anonym_name = raw["anonymous"].get("name")
                self.anonym_flag = raw["anonymous"].get("flag")

        def is_group_owner(self) -> bool:
            """判断是否为群主，若不是或不是群类型消息，返回 False"""
            if not self._isGroup:
                return False
            else:
                return self.group_role == "owner"

        def is_group_admin(self) -> bool:
            """判断是否为群管理（包含群主），若不是或不是群类型消息，返回 False"""
            if not self._isGroup:
                return False
            else:
                return self.group_role == "admin" or self.group_role == "owner"

        def only_group_member(self) -> bool:
            """判断是否只是群员（注意只是群员，不包括群主、管理和匿名），若不是或不是群类型消息，返回 False"""
            if not self._isGroup:
                return False
            else:
                return self.group_role == "member"

        def is_bot(self) -> bool:
            """判断消息是否是bot自己发送的"""
            return self.id == self._rawEvent["self_id"]


class RequestEvent(BotEvent):
    """请求事件类型，对应两种可能：加好友请求和加群请求

    .. admonition:: 提示
       :class: tip

       一般无需手动实例化该类，多数情况会直接使用本类对象，或将本类用作类型注解。
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        #: 收到事件的机器人 qq 号
        self.bot_id: int = cast(int, raw.get("self_id"))
        #: 事件的来源 qq 号
        self.operator_id: int
        #: 事件的来源群号，请求来源于私聊时此属性为 :obj:`None`
        self.group_id: Optional[int]
        #: 加群或加好友的验证消息
        self.req_comment: str
        #: 加群或加好友请求的 flag，调用相关 API 时，需要使用
        self.req_flag: str
        #: 加群请求类型：直接加入和邀请，请求来源于私聊时此属性为 :obj:`None`
        self.group_req_type: Optional[Literal["add", "invite"]]

        if self.is_friend_req():
            self.operator_id = raw["user_id"]
            self.req_comment = raw["comment"]
            self.req_flag = raw["flag"]
        elif self.is_group_req():
            self.group_req_type = raw.get("sub_type")
            self.operator_id = raw["user_id"]
            self.group_id = raw.get("group_id")
            self.req_comment = raw["comment"]
            self.req_flag = raw["flag"]

    @property
    def time(self) -> int:
        """事件发生时刻的时间戳"""
        return cast(int, self.raw.get("time"))

    @property
    def type(self) -> Literal["request"]:
        """事件的类型（返回指定字面量）"""
        return "request"

    def is_friend_req(self) -> bool:
        """是否为加好友请求"""
        return self.raw["request_type"] == "friend"

    def is_group_req(self) -> bool:
        """是否为加群请求"""
        return self.raw["request_type"] == "group"


class NoticeEvent(BotEvent):
    """通知事件类型

    .. admonition:: 提示
       :class: tip

       一般无需手动实例化该类，多数情况会直接使用本类对象，或将本类用作类型注解。

    .. admonition:: 注意
       :class: caution

       受 onebot 协议实现项目的影响，及对通知事件本身复杂性的考虑，通知事件大多数实例属性，
       只会在特定类别的通知事件中存在。各个属性的含义与存在的时机，已在下方的注释说明。

       如果你仍不确定某个属性在何时出现，建议直接调试查看存在的属性。例如通过
       `print(event.__dict__)` 或调试器查看。
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)
        #: 收到事件的机器人 qq 号
        self.bot_id: int = cast(int, raw.get("self_id"))

        #: 通知作用者或主体方的 id，如被禁言的一方
        self.user_id: int
        #: 通知若发生在群中的群 id
        self.group_id: int
        #: 通知发起者或操作方的 id，如禁言别人的管理员
        self.operator_id: int
        #: 通知涉及消息时的消息 id
        self.msg_id: int
        #: 入群通知事件的入群类型：管理员同意或管理员邀请
        self.join_group_type: Literal["approve", "invite"]
        #: 退群通知事件的退群类型：自退群、踢出、bot 账号被踢
        self.leave_group_type: Literal["leave", "kick", "kick_me"]
        #: 群管理员变动通知事件类型：设置管理员或取消管理员
        self.admin_change_type: Literal["set", "unset"]
        #: 文件上传通知事件的文件信息数据结构
        self.file: NoticeEvent.File
        #: 群禁言通知事件的类型：禁言、解除禁言
        self.group_ban_type: Literal["ban", "lift_ban"]
        #: 群禁言通知事件的禁言时长
        self.ban_time: int
        #: 群荣誉变更通知事件的荣誉类型：龙王、群聊之火、快乐源泉
        self.honor_change_type: Literal["talkactive", "performer", "emotion"]
        #: 群头衔变更通知事件的新头衔
        self.new_title: str
        #: 群名片更新通知事件的旧名片，名片为空时对应属性为空字符串
        self.old_card: str
        #: 群名片更新通知事件的新名片，名片为空时对应属性为空字符串
        self.new_card: str
        #: 客户端在线状态变更的通知事件的，客户端信息数据结构
        self.client: NoticeEvent.Client
        #: 精华消息变更通知事件的类型：添加或删除
        self.essence_change_type: Literal["add", "delete"]

        self._init()

    @property
    def time(self) -> int:
        return cast(int, self.raw.get("time"))

    @property
    def type(self) -> Literal["notice"]:
        return "notice"

    def _init(self) -> None:
        """外部确认为该类型事件时，调用此方法。"""
        rawEvent = self.raw

        if self.is_friend_recall():
            self.user_id = rawEvent["user_id"]
            self.msg_id = rawEvent["message_id"]

        elif self.is_group_recall():
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]
            self.operator_id = rawEvent["operator_id"]
            self.msg_id = rawEvent["message_id"]

        elif self.is_group_increase():
            self.join_group_type = rawEvent["sub_type"]
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]
            self.operator_id = rawEvent["operator_id"]

        elif self.is_group_decrease():
            self.leave_group_type = rawEvent["sub_type"]
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]
            self.operator_id = rawEvent["operator_id"]

        elif self.is_group_admin():
            self.admin_change_type = rawEvent["sub_type"]
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]

        elif self.is_group_upload():
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]
            self.file = NoticeEvent.File(rawEvent)

        elif self.is_group_ban():
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]
            self.operator_id = rawEvent["operator_id"]
            self.group_ban_type = rawEvent["sub_type"]
            self.ban_time = rawEvent["duration"]

        elif self.is_friend_add():
            self.user_id = rawEvent["user_id"]

        elif self.is_poke():
            self.user_id = rawEvent["target_id"]
            self.operator_id = rawEvent["user_id"]
            if "group_id" in rawEvent.keys():
                self.group_id = rawEvent["group_id"]

        elif self.is_lucky_king():
            self.user_id = rawEvent["target_id"]
            self.group_id = rawEvent["group_id"]
            self.operator_id = rawEvent["user_id"]

        elif self.is_honor():
            self.honor_change_type = rawEvent["honor_type"]
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]

        elif self.is_title():
            self.new_title = rawEvent["title"]
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]

        elif self.is_group_card():
            self.old_card = rawEvent["card_old"]
            self.new_card = rawEvent["card_new"]
            self.user_id = rawEvent["user_id"]
            self.group_id = rawEvent["group_id"]

        elif self.is_offline_file():
            self.user_id = rawEvent["user_id"]
            self.file = NoticeEvent.File(rawEvent)

        elif self.is_client_status():
            self.client = NoticeEvent.Client(rawEvent)

        elif self.is_essence():
            self.essence_change_type = rawEvent["sub_type"]
            self.user_id = rawEvent["sender_id"]
            self.group_id = rawEvent["group_id"]
            self.operator_id = rawEvent["operator_id"]
            self.msg_id = rawEvent["message_id"]

    def is_group(self) -> bool:
        """是否是来自群的通知事件"""
        return "group_id" in self.raw.keys()

    def is_group_upload(self) -> bool:
        """是否是群文件上传通知"""
        return self.raw["notice_type"] == "group_upload"

    def is_group_admin(self) -> bool:
        """是否是群管理员变更通知"""
        return self.raw["notice_type"] == "group_admin"

    def is_group_decrease(self) -> bool:
        """是否是群成员减少通知"""
        return self.raw["notice_type"] == "group_decrease"

    def is_group_increase(self) -> bool:
        """是否是群成员增加通知"""
        return self.raw["notice_type"] == "group_increase"

    def is_group_ban(self) -> bool:
        """是否是群禁言通知"""
        return self.raw["notice_type"] == "group_ban"

    def is_friend_add(self) -> bool:
        """是否是好友添加通知"""
        return self.raw["notice_type"] == "friend_add"

    def is_group_recall(self) -> bool:
        """是否是群聊消息撤回通知"""
        return self.raw["notice_type"] == "group_recall"

    def is_friend_recall(self) -> bool:
        """是否是私聊消息撤回通知"""
        return self.raw["notice_type"] == "friend_recall"

    def is_group_card(self) -> bool:
        """是否是群名片变更通知"""
        return self.raw["notice_type"] == "group_card"

    def is_offline_file(self) -> bool:
        """是否是离线文件上传通知（即私聊文件上传）"""
        return self.raw["notice_type"] == "offline_file"

    def is_client_status(self) -> bool:
        """是否是客户端状态通知"""
        return self.raw["notice_type"] == "client_status"

    def is_essence(self) -> bool:
        """是否是精华消息变更通知"""
        return self.raw["notice_type"] == "essence"

    def is_notify(self) -> bool:
        """是否为系统通知（包含群荣誉变更、戳一戳、群红包幸运王、群成员头衔变更）"""
        return self.raw["notice_type"] == "notify"

    def is_honor(self) -> bool:
        """是否是群荣誉变更通知"""
        return self.raw["notice_type"] == "notify" and self.raw["sub_type"] == "honor"

    def is_poke(self) -> bool:
        """是否是戳一戳通知"""
        return self.raw["notice_type"] == "notify" and self.raw["sub_type"] == "poke"

    def is_lucky_king(self) -> bool:
        """是否是群红包幸运王通知"""
        return (
            self.raw["notice_type"] == "notify" and self.raw["sub_type"] == "lucky_king"
        )

    def is_title(self) -> bool:
        """是否是群成员头衔变更通知"""
        return self.raw["notice_type"] == "notify" and self.raw["sub_type"] == "title"

    class File:
        """文件上传通知的文件信息数据结构

        .. admonition:: 提示
           :class: tip

           一般无需手动实例化该类，多数情况会直接使用本类对象，或将本类用作类型注解。
        """

        def __init__(self, raw: dict) -> None:
            #: 文件 id，私聊文件上传时为 :obj:`None`
            self.id: Optional[str] = None
            #: 文件名
            self.name: str
            #: 文件大小
            self.size: int
            #: 文件 busid，私聊文件上传时为 :obj:`None`
            self.busid: Optional[int] = None
            #: 文件 url 地址，群聊文件上传时为 :obj:`None`
            self.url: Optional[str] = None

            self.name = raw["file"]["name"]
            self.size = raw["file"]["size"]
            self.id = raw["file"].get("id")
            self.busid = raw["file"].get("busid")
            self.url = raw["file"].get("url")

    class Client:
        """客户端在线状态变更通知的客户端信息数据结构

        .. admonition:: 提示
           :class: tip

           一般无需手动实例化该类，多数情况会直接使用本类对象，或将本类用作类型注解。
        """

        def __init__(self, raw: dict) -> None:
            #: 当前客户端是否在线
            self.online: bool = raw["online"]
            #: 当前客户端 id
            self.id: int = raw["client"]["app_id"]
            #: 客户端设备名称
            self.name: str = raw["client"]["device_name"]
            #: 客户端设备类型
            self.kind: str = raw["client"]["device_kind"]


class MetaEvent(BotEvent):
    """元事件类型

    .. admonition:: 提示
       :class: tip

       一般无需手动实例化该类，多数情况会直接使用本类对象，或将本类用作类型注解。
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)
        #: 收到事件的机器人 qq 号
        self.bot_id: int = cast(int, raw.get("self_id"))

    @property
    def time(self) -> int:
        """事件发生时刻的时间戳"""
        return cast(int, self.raw.get("time"))

    @property
    def type(self) -> Literal["meta"]:
        """事件的类型（返回指定字面量）"""
        return "meta"

    def is_lifecycle(self) -> bool:
        """是否是生命周期类型的元事件"""
        return self.raw["meta_event_type"] == "lifecycle"

    def is_heartbeat(self) -> bool:
        """是否是心跳类型的元事件"""
        return self.raw["meta_event_type"] == "heartbeat"
