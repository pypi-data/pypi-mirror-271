import asyncio
from asyncio import Future

from ..base.typing import TYPE_CHECKING, cast
from ..context.session import ActionResponse

if TYPE_CHECKING:
    from ..base.abc import AbstractConnector, BotAction
    from ..utils.logger import BotLogger


class BotResponder:
    """Bot 响应模块，是 action 发送方和 bot 连接模块的媒介。 提供 action 发送、响应回送功能"""

    def __init__(self) -> None:
        super().__init__()
        self._resp_table: dict[str, Future[ActionResponse]] = {}
        self.logger: "BotLogger"
        self._action_sender: "AbstractConnector"

        self._ready_signal = asyncio.Event()

    def _bind(self, logger: "BotLogger", connector: "AbstractConnector") -> None:
        self.logger = logger
        self._action_sender = connector

    def _set_ready(self) -> None:
        self._ready_signal.set()

    async def respond(self, resp: ActionResponse) -> None:
        await self._ready_signal.wait()

        try:
            if self.logger._check_level("DEBUG"):
                self.logger.obj(resp.raw, f"收到 resp {resp:hexid}")

            if resp.id is None:
                return

            else:
                resp_fut = self._resp_table.get(resp.id)
                if resp_fut is None:
                    self.logger.obj(resp.raw, "收到了不匹配携带 id 的响应", level="ERROR")
                    return

                resp_fut.set_result(resp)
                self._resp_table.pop(resp.id)

        except asyncio.InvalidStateError:
            self.logger.warning(
                "响应的等待被取消，这可能意味着连接质量差，或等待超时时间太短"
            )
            self._resp_table.pop(cast(str, resp.id))

        except Exception as e:
            self.logger.error("bot responder.dispatch 抛出异常")
            self.logger.obj(resp, "异常点 resp_event", level="ERROR")
            self.logger.exc(locals=locals())

    async def take_action(self, action: "BotAction") -> None:
        """响应器发送 action, 不等待完成"""
        await self._ready_signal.wait()

        await self._action_sender._send(action)
        return None

    async def take_action_wait(self, action: "BotAction") -> Future[ActionResponse]:
        """响应器发送 action，并返回一个 Future 用于等待完成"""
        await self._ready_signal.wait()

        fut: Future[ActionResponse] = Future()
        fut_id = cast(str, action.resp_id)
        self._resp_table[fut_id] = fut

        await self._action_sender._send(action)
        return fut
