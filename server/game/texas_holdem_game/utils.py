from typing import Any, Generator, Sequence


def add_cycle(arr: Sequence) -> Generator[Any, None, None]:
    """Cyclic iterator. Unlike itertools.cycle, you can add new elements to the sequence during iteration."""
    iter = 0
    while True:
        yield arr[iter % len(arr)]
        iter = (iter + 1) % len(arr)
