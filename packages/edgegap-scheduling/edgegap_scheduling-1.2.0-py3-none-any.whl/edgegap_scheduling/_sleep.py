import asyncio


class AsyncSleep:
    def __init__(self):
        self.tasks = {}

    async def sleep(self, identifier: str, delay, result=None):
        coro = asyncio.sleep(delay, result=result)
        task = asyncio.ensure_future(coro)
        self.tasks[identifier] = task

        try:
            return await task
        except asyncio.CancelledError:
            return result
        finally:
            self.tasks.pop(task, None)

    def __cancel_one_helper(self, identifier: str):
        task = self.tasks.get(identifier)
        task.cancel()

        return task

    async def cancel_one(self, identifier: str):
        task = self.__cancel_one_helper(identifier)

        await asyncio.wait([task])

        return self.tasks.pop(task, None)

    def __cancel_all_helper(self) -> dict:
        cancelled = {}

        for identifier, task in self.tasks.items():
            if task.cancel():
                cancelled[identifier] = task

        return cancelled

    async def cancel_all(self):
        cancelled = self.__cancel_all_helper()

        await asyncio.wait(self.tasks.values())

        for identifier, _ in cancelled.items():
            self.tasks.pop(identifier)

        return len(cancelled)
