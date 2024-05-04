from pydantic import BaseModel


class AresMessage(BaseModel):
    device_serial: str
    package_name: str
    pid: int
    session_id: str
    script_name: str
    message_type: str
    message: dict
    timestamp: int
