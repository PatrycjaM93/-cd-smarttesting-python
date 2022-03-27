class CeleryWannabeTask:
    def delay(self, *_args, **_kwargs) -> None:
        raise NotImplementedError


send_email = CeleryWannabeTask()
