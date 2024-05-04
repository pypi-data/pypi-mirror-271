import time
from functools import wraps

import frida
from frida.core import Device, Script, Session
from heradata import ElasticsearchSingleton

from ._exceptions import FridaProcessNotAttachedException, \
    FridaServerNotRunningException, FridaTargetNotRunningException, \
    FridaPackageNotInstalledException
from ._modules import AresMessage


class FridaHooker:
    _serial: str
    _device: Device = None
    _session: Session = None
    _session_id: str = None
    _package_name: str = None
    _attached_process_name: str = None
    _attached_pid: int = None
    _running_script: dict[str, Script] = {}
    _es_client: ElasticsearchSingleton = None

    @staticmethod
    def __check_session(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            if self._session is None:
                raise FridaProcessNotAttachedException()
            return func(self, *args, **kwargs)

        return inner

    @staticmethod
    def __get_frida_device(device_serial: str) -> [Device | None]:
        try:
            return frida.get_device(device_serial)
        except frida.ServerNotRunningError:
            return None

    def __init__(self, device_serial: str):
        self._device = self.__get_frida_device(device_serial)
        if self._device is None:
            raise FridaServerNotRunningException(device_serial)
        self._serial = device_serial
        self._es_client = ElasticsearchSingleton()

    def __del__(self):
        if self._running_script:
            for script in self._running_script:
                script.unload()
        if self._session is not None:
            self._session.detach()

    def __is_package_running(self, target: [str | int]) -> bool:
        return target in [process.pid if isinstance(target, int) else process.name
                          for process in self._device.enumerate_processes()]

    def __is_package_installed(self, package_name: str) -> bool:
        return package_name in [app.identifier for app in
                                self._device.enumerate_applications()]

    def __get_pid(self, target: [str | int]) -> int:
        if isinstance(target, int):
            return target
        return self._device.get_process(target).pid

    def __get_process_name(self, target: int) -> str:
        for process in self._device.enumerate_processes():
            if process.pid == target:
                return process.name

    def attach(self, target: [str | int]) -> "FridaHooker":
        if not self.__is_package_running(target):
            raise FridaTargetNotRunningException(target)
        if isinstance(target, str):
            self._package_name = target
        target = self.__get_pid(target)
        if self._session is None:
            self._session = self._device.attach(target)
            self._attached_pid = target
        else:
            self._session.detach()
            self._session = self._device.attach(target)
            self._attached_pid = target
        self._session_id = self.__get_process_name(
            self._attached_pid
        ) + '_' + str(int(time.time() * 1000))
        return self

    def spawn(self, package_name: str, resume=True) -> "FridaHooker":
        if not self.__is_package_installed(package_name):
            raise FridaPackageNotInstalledException(package_name)
        self._package_name = package_name
        pid = self._device.spawn(package_name)
        self._session = self._device.attach(pid)
        self._attached_pid = pid
        if resume:
            self.resume()
        self._session_id = self.__get_process_name(
            self._attached_pid
        ) + '_' + str(int(time.time() * 1000))
        return self

    def resume(self) -> "FridaHooker":
        if self._attached_pid is not None:
            self._device.resume(self._attached_pid)
        return self

    def __logger_bind_script_name(self, script_name):
        def on_logger(level, text):
            self._es_client.es.index(
                index='ares',
                body=AresMessage(
                    device_serial=self._serial,
                    package_name=self._package_name,
                    pid=self._attached_pid,
                    session_id=self._session_id,
                    script_name=script_name,
                    message_type='log',
                    message={
                        'level': level,
                        'text': text
                    },
                    timestamp=int(time.time() * 1000)
                ).dict()
            )

        return on_logger

    def __message_bind_script_name(self, script_name):
        def on_message(message, data):
            self._es_client.es.index(
                index='ares',
                body=AresMessage(
                    device_serial=self._serial,
                    package_name=self._package_name,
                    pid=self._attached_pid,
                    session_id=self._session_id,
                    script_name=script_name,
                    message_type='message',
                    message={
                        'message': message,
                        'data': data
                    },
                    timestamp=int(time.time() * 1000)
                ).dict()
            )

        return on_message

    @__check_session
    def run_script(self, script_content: str, script_name: str) -> "FridaHooker":
        if script_name in self._running_script:
            self._running_script[script_name].unload()
        script: Script = self._session.create_script(script_content)
        script.set_log_handler(self.__logger_bind_script_name(script_name))
        script.on('message', self.__message_bind_script_name(script_name))
        script.load()
        self._running_script[script_name] = script
        return self

    def get_session_id(self):
        return self._session_id

    def get_script_names(self):
        return self._running_script.keys()

    def get_script(self, name):
        return self._running_script[name]
