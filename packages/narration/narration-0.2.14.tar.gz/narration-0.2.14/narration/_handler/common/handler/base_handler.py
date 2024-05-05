import logging
import os
import threading
from typing import Optional, Protocol, Tuple
from typing import runtime_checkable

from narration._broker.dispatch_broker import DISPATCH_BROKER
from narration._broker.group_broker import GROUPIDBROKER
from narration._debug.myself import get_debug_logger
from narration._handler.common.callable import Record_Signal
from narration._handler.common.misc.op_type import OpType
from narration._handler.server.common.thread.base_receiver_thread import BaseReceiverThread
from narration._misc.constants import DispatchMode, NARRATION_DEBUG_HANDLER_PREFIX

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_PREFIX)

_dispatch_ASSIGNMENT_LOCK = threading.Lock()


@runtime_checkable
class NarrationHandler(Protocol):
    """Function(s) to be implemented by BaseHandler"""

    def is_narration_handler(self) -> None: ...


dispatchAssignedStatus = Tuple[threading.Event, str]
dispatchUnassignedStatus = threading.Event


class BaseHandler(logging.Handler):
    def __init__(
        self,
        uuid: str = None,
        name: str = None,
        type: OpType = None,
        level: Optional[int] = None,
        on_close_timeout: float = 1.0,
        message_dispatching: DispatchMode = DispatchMode.SYNC,
        group_id: str = None,
    ) -> None:
        super().__init__(level)
        self._ppid = os.getppid()
        self._pid = os.getpid()
        self._uuid = uuid
        self.name = name
        self._type = type
        self._background_shutdown_timeout = on_close_timeout  # in seconds
        self._message_dispatching = message_dispatching
        self._dispatch_broker = DISPATCH_BROKER
        self._groupid_broker = GROUPIDBROKER
        self._dispatch = None
        self._group_id = None
        self._shutdown_completed = None

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def pid(self):
        return self._pid

    @property
    def ppid(self):
        return self._ppid

    @property
    def group_id(self) -> str:
        return self._group_id

    def _assign_dispatch(
        self,
        group_id: str = None,
        record_emitter: Record_Signal = None,
    ) -> dispatchAssignedStatus:
        with _dispatch_ASSIGNMENT_LOCK:
            # Client _handler always have their server's group id
            unique_group_id = (
                self._groupid_broker.get_ugid(group_id)
                if not self._groupid_broker.is_ugid(group_id)
                else group_id
            )

            def thread_create():
                name = f"narration_dispatch_{self._type.value}_{unique_group_id}"
                return self._create_dispatch_thread(
                    thread_name=name, dispatching_ready=threading.Event()
                )

            def thread_destroy(thread: threading.Thread = None):
                if thread is not None and thread.is_alive:
                    thread.shutdown(timeout=self._background_shutdown_timeout)

            self._dispatch = self._dispatch_broker.bind(
                role_type=self._type,
                group_id=unique_group_id,
                handler_id=self._uuid,
                thread_create=thread_create,
                thread_destroy=thread_destroy,
                record_emitter=record_emitter,
            )

            return self._dispatch.thread.startup_completed, unique_group_id

    def _unassign_dispatch(self, group_id: str = None) -> dispatchUnassignedStatus:
        with _dispatch_ASSIGNMENT_LOCK:
            unique_group_id = (
                self._groupid_broker.get_ugid(group_id)
                if not self._groupid_broker.is_ugid(group_id)
                else group_id
            )

            shutdown_completed = self._dispatch_broker.unbind(
                role_type=self._type, group_id=unique_group_id, handler_id=self._uuid
            )
            return shutdown_completed

    def _create_dispatch_thread(
        self, thread_name: str = None, dispatching_ready: threading.Event = None
    ) -> BaseReceiverThread:
        raise NotImplementedError()

    def close(self):
        if self._shutdown_completed is None:
            self._shutdown_completed = self._unassign_dispatch(group_id=self._group_id)
            super().close()

        # Needed only for unit tests
        return self._shutdown_completed

    def is_narration_handler(self) -> None:
        pass
