from __future__ import annotations

import json

from typing import Union, Sequence
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QDialog, QFileDialog, QInputDialog, QMessageBox
from tpds.servers import Messages, MessageContext, ReservedMessageId
from .msg_handler_tflx import tflx_proto_provisioning_handle, tflx_provisioningXML_handle
from .provision_user_inputs import ProvisionUserInputs


class TPDSAppMessage(QObject):
    """
    This is an empty base class for message handlers. Do not subclass this
    directly - instead use the tpds_app_message decorator
    """


def tpds_app_message(id: ReservedMessageId):
    """
    Decorator to enable message processing correctly for the tpds QT application.

    Under most circumstances it is not necessary to use this decorator. It is only required if one needs
    to communicate with the QT application through the websocket. Using the QT objects directly are considered
    legacy/deprecated and should not be done for new features. Instead render them properly using a react
    component.

    Example Declaration of a message handler:

    @tpds_app_message(ReservedMessageId.user_input_text_box)
    def user_input_text_box(title: str, label: str) -> str:
        tB, accept = QInputDialog.getText(None, title, label)
        return tB if accept else None

    Example for registering the message handler:

    get_app_ref().messages.add_message(user_input_text_box)

    """

    def wrapper(func):
        params, is_member = Messages.get_func_param_types(func)

        class TPDSAppMessageHandler(TPDSAppMessage):
            _signal = Signal(*params)

            def __init__(self, parent) -> None:
                super().__init__(parent)
                self._result = None
                self._context = None
                self._parent = parent
                self._class_func: bool = is_member
                self._signal.connect(self._run_handler)
                Messages.add(id)(self._wrapper)

            def _wait_for_response(self) -> str:
                self._result = "BUSY"
                while self._result == "BUSY":
                    continue
                return self._result

            def _wrapper(self, ctx: MessageContext, *args):
                self.context = ctx
                self._signal.emit(*args)
                return self._wait_for_response()

            @Slot(*params)
            def _run_handler(self, *args):
                self._result = func(self._parent, *args) if self._class_func else func(*args)
                self.context = None

        return TPDSAppMessageHandler

    return wrapper


class TPDSAppMessages(QObject):
    _messages = []

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent
        self.register(self.user_input_file_upload)
        self.register(self.user_input_text_box)
        self.register(self.user_input_dropdown)
        self.register(self.user_message_box)

        # These are legacy handlers
        self.register(self.tflex_provisioningXML)
        self.register(self.tflx_proto_provisioning)
        self.register(self.provision_inputs)

    def log(self, message):
        self._parent.log(message)

    def _register_handler(self, msg: TPDSAppMessage) -> None:
        if issubclass(msg, TPDSAppMessage):
            self._messages += [msg(self)]
        else:
            raise ValueError(
                f"The type {msg} is not a valid message - use the tpds_app_message decorator on the handling function"
            )

    def register(self, handlers: Union[TPDSAppMessage, list[TPDSAppMessage]]) -> None:
        if not isinstance(handlers, Sequence):
            handlers = [handlers]
        for handler in handlers:
            self._register_handler(handler)

    @tpds_app_message(ReservedMessageId.user_input_file_upload)
    def user_input_file_upload(self, caption: str, filters: list[str], directory: str) -> str:
        self.log(f"File filter: {filters}")
        self.log(directory)
        dlg = QFileDialog(
            None, caption=caption, filter=f"({' '.join(filters)})", directory=directory
        )
        result = dlg.exec()
        filepath = dlg.selectedFiles()[0] if result == QDialog.Accepted else None
        self.log(filepath)
        return filepath

    @tpds_app_message(ReservedMessageId.user_input_text_box)
    def user_input_text_box(self, title: str, label: str) -> str:
        tB, accept = QInputDialog.getText(None, title, label)
        return tB if accept else None

    @tpds_app_message(ReservedMessageId.user_input_dropdown)
    def user_input_dropdown(self, title: str, items: list[str], label: str):
        item, ok = QInputDialog.getItem(None, title, label, items, 0, False)
        self.log(f"{ok}: {item}")
        return item if ok and item else None

    @tpds_app_message(ReservedMessageId.user_message_box)
    def user_message_box(self, title: str, text: str) -> str:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        reply = msg_box.exec()
        return "OK" if reply == QMessageBox.Ok else "Cancel"

    # The following are legacy handlers with a lot of business logic
    # they need to be deprecated long term

    @tpds_app_message(ReservedMessageId.tflex_provisioningXML)
    def tflex_provisioningXML(self, data: str):
        tflx_provisioningXML_handle(json.dumps(json.loads(data)))
        return ""

    @tpds_app_message(ReservedMessageId.tflx_proto_provisioning)
    def tflx_proto_provisioning(self, id: str):
        tflx_proto_provisioning_handle(id)
        return ""

    @tpds_app_message(ReservedMessageId.provision_inputs)
    def provision_inputs(self, args: list[str]):
        obj = ProvisionUserInputs(xml_type=args[0], cert_type=args[1])
        obj.exec()
        return f"{obj.user_data}"
