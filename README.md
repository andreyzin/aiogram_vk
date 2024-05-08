# aiogram_vk


**aiogram_vk** is a experemental fork from [aiogram](https://github.com/aiogram/aiogram)

> [!CAUTION]
> Currently in **VERY** experemental. Looking for your pull requests

> [!NOTE] 
> Currently supports only these methods:
> - Account.get_info
> - Audio.get_by_id
> - Audio.get_count
> - Audio.get
> - Audio.search

[Vk API](https://dev.vk.com/en/method) written in Python 3.8 using
[asyncio](https://docs.python.org/3/library/asyncio.html) and
[aiohttp](https://github.com/aio-libs/aiohttp).


Features
----

- Asynchronous ([asyncio docs](https://docs.python.org/3/library/asyncio.html), `492`)
- Has type hints (`484`) and can be used with [mypy](http://mypy-lang.org/)
- Supports [PyPy](https://www.pypy.org/)
- Has TokenProvider (to recieve token for user)
- Supports audio methods


> [!WARNING]  
    It is strongly advised that you have prior experience working
    with [asyncio](https://docs.python.org/3/library/asyncio.html)
    before beginning to use **aiogram_vk**.



# TODO
- [ ] Make code generator for methods and objects from [Vk Api Schema](https://github.com/VKCOM/vk-api-schema), like aiogram's `Butcher`
- [ ] Write docs 
- [ ] Add dispatcher
