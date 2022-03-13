import functools
import inspect

from celery import Task
from injector import get_bindings


def task_with_injectables(task: Task) -> Task:
    """Dekorator na taski, który zapewni wstrzykiwanie zależności.

    Od funkcji-taska wymagane jest, by wszystkie zależności do wstrzyknięte były
    argumentami pozycyjnymi zaś wszystkie argumenty niewstrzykiwane były zadeklarowane
    jako keyword-only.

    Jest to podyktowane uproszczeniami w tej integracji Celery z Injectorem. Przykład:
        ```
        @task_with_injectables
        @app.task(typing=False)
        def add(x: Inject[int], y: Inject[float], *, z: int) -> None:
            print(x + y + z)
        ```

    """
    # Safety-checks zanim przejdziemy dalej

    # Sprawdzamy, czy flaga typing jest ustawiona na False. Inaczej Celery protestuje,
    # że wyzwalamy taska bez przekazania wszystkich argumentów (także tych, które potem
    # będą wstrzyknięte)
    assert (
        task.typing is False
    ), "Wymagane jest wyłączenie sprawdzania argumentów przy schedulowaniu taska"
    # Upewnijmy się, że niewstrzykiwane argumenty są opisane jako keyword-only
    args_spec = inspect.getfullargspec(task.run)
    bindings = get_bindings(task.run)
    assert set(bindings) == set(
        args_spec.args
    ), "Wstrzykiwane argumenty muszą być pozycyjne"
    assert args_spec.varargs is None, "*args nie jest wspierane"
    assert args_spec.varkw is None, "**kwargs nie jest wspierane"

    actual_run = task.run

    @functools.wraps(actual_run)
    def wrapped_run(*args, **kwargs):
        injector = task.app.__injector__
        return injector.call_with_injection(actual_run, args=args, kwargs=kwargs)

    task.run = wrapped_run

    return task
