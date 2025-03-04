from typing import TypeVar, Iterator, Tuple, Optional, Iterable

T = TypeVar('T')

def ipcn_enumerate(iterable: Iterable[T]) -> Iterator[Tuple[int, Optional[T], Optional[T], Optional[T]]]:
    """
    This is a generator that yields a tuple of the 
    - i: index of the current element
    - p: previous element Or None
    - c: current element
    - n: next element Or None
    """
    p = None
    c = None
    n = None
    
    # 空のイテラブルに対応するためのチェック
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        # 空のイテラブルの場合は何もyieldせずに終了
        return

    # 最初の要素を処理
    i = 0
    n = first
    
    # 残りの要素を処理
    for i, e in enumerate(iterator, start=1):
        p = c
        c = n
        n = e
        if c is not None:
            yield (i-1, p, c, e)
    
    # 最後の要素を処理
    p = c
    c = n
    n = None
    yield (i, p, c, n)