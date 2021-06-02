from typing import Any, Callable


class CustomSerializable:
    def pack(self, packer: Callable) -> Any:
        raise NotImplementedError()
