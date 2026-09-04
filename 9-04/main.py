# async / await 
import asyncio
import time

# async def  fetch():
async def  fetch() -> str:
    await asyncio.sleep(0.1)
    return "fetched"

async def coroutine_is_lazy() -> None:
    obj = fetch()
    print(f'fetch() returned: {obj}, "-- coroutine object, nothing ran yet"')
    obj.close()




async def call_api(name:str,seconds:float) -> str:
    print(f'start {name}')
    await asyncio.sleep(seconds)
    print(f'end {name}')
    return f'{name} result'

async def one_at_a_time() -> None:
    print('one at a time')
    await call_api('A', 0.5)
    await call_api('B', 1.0)
    await call_api('C', 0.5)
    
async def all_together() -> None:
    print('all together')
    await asyncio.gather(
        call_api('A', 0.5),
        call_api('B', 0.6),
        call_api('C', 0.5),
        )
    
    
async def worked_example() -> None:
    t=time.perf_counter()
    await one_at_a_time()
    print(f'sequential time: {time.perf_counter()-t:.1f} ')
    
    t=time.perf_counter()
    await all_together()
    print(f'parallel time: {time.perf_counter()-t:.1f} ')

async def main() -> None:
    await coroutine_is_lazy()
    await worked_example()
if __name__ == "__main__":
    asyncio.run(main())
    
    
    
