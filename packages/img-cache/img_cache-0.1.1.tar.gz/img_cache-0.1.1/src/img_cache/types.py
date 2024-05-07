import typing as t

ReadFunc = t.Callable[[t.Any], t.Any]
ReadCache = t.Callable[[t.Any], t.Any]
WriteCache = t.Callable[[t.Any, t.Any], t.Any]
Serialize = t.Callable[[t.Any], str]
