import asyncio
import logging

from edgegap_logging import Color, Format
from pydantic import BaseModel

from ._runner import TaskRunner
from ._sleep import AsyncSleep
from ._task import Task
from .errors import ManualRunNotAllowedError


class Scheduler:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.__runners: dict[str, TaskRunner] = {}
        self.logger = logging.getLogger('scheduling.Scheduler')
        self.__async_sleep = AsyncSleep()

    def task(
        self,
        every: str = None,
        name: str = None,
        delay: str = None,
        identifier: str = None,
        continue_on_exception: bool = True,
        manual_run_allowed: bool = False,
        remove_running_time: bool = False,
        parameters: BaseModel | type[BaseModel] | None = None,
    ):
        def decorator(func):
            task = Task(
                name=name or func.__name__,
                identifier=identifier or name.lower().replace(' ', '_'),
                func=func,
                every=every,
                delay=delay,
                continue_on_exception=continue_on_exception,
                manual_run_allowed=manual_run_allowed,
                remove_running_time=remove_running_time,
                parameters=parameters if isinstance(parameters, BaseModel) or parameters is None else parameters(),
            )
            runner = TaskRunner(
                task=task,
                sleep=self.__async_sleep.sleep,
            )
            self.__register(task.identifier, runner)

        return decorator

    def __register(self, identifier: str, runner: TaskRunner) -> None:
        if identifier in self.__runners.keys():
            raise Exception(f'Task {Format.squared(identifier, Color.RED)} already exists')

        self.__runners[identifier] = runner

    def __get_or_raise(self, identifier: str) -> TaskRunner:
        runner = self.__runners.get(identifier)

        if runner is None:
            raise ValueError(f'Task [{identifier}] does not exist')

        return runner

    async def get(self, identifier) -> Task:
        runner = self.__get_or_raise(identifier)
        return runner.get_task()

    async def update(
        self,
        identifier: str,
        every: str | None,
        delay: str | None,
        parameters: dict | None,
    ) -> Task:
        runner = self.__get_or_raise(identifier)
        runner.update_task(
            every=every,
            delay=delay,
            parameters=parameters,
        )

        return runner.get_task()

    async def list(self) -> list[Task]:
        return [runner.get_task() for runner in self.__runners.values()]

    async def start(self, identifier: str) -> Task:
        runner = self.__get_or_raise(identifier)
        self.logger.info(f'Starting {runner}')
        task = runner.get_task()

        if task.safe_to_start:
            asyncio.ensure_future(runner.start())
        else:
            task.message = 'Task already started'

        return task

    async def start_all(self):
        self.logger.info('Starting All Tasks')
        for runner in self.__runners.values():
            if runner.should_schedule:
                await runner.start()

    async def stop(self, identifier: str) -> Task:
        runner = self.__get_or_raise(identifier)
        self.logger.info(f'Stopping {runner}')
        can_stop = runner.stop()
        task = runner.get_task()

        if can_stop:
            await self.__async_sleep.cancel_one(identifier)
        else:
            task.message = 'Could not stop the task since it is not in a running state'

        return task

    async def run(self, name: str, parameters: dict | None = None) -> Task:
        runner = self.__get_or_raise(name)

        task = runner.get_task()

        if not task.manual_run_allowed:
            raise ManualRunNotAllowedError(f'Task [{name}] is not allowed to be run manually')

        params = task.parameters.model_copy(update=parameters) if isinstance(parameters, dict) else None

        await runner.run(params)

        return runner.get_task()

    async def stop_all(self):
        self.logger.info('Stopping All Running Tasks')

        for runner in self.__runners.values():
            runner.stop()
            self.logger.info(f'Stopping {runner}')

        count = await self.__async_sleep.cancel_all()
        self.logger.info(f'{count} tasks stopped')
