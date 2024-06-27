import asyncio
import random
import time


"""
Each step in the pipeline should be executed as an asynchronous / multi-threaded batch
Once a step has been finalized the output will be passed to the next step as an iterable

- create 100 elements
- wait for 0-2.5 seconds
- add timestamp
- filter out anything with timestamp > 1
"""

elements = range(1, 100)


async def add_watermark(element):
    secs = random.randint(0, 5)
    await asyncio.sleep(secs)

    return {
        "value": element,
        "watermark": secs
    }

async def main():
    tasks = []

    async with asyncio.TaskGroup() as tg:
        for element in elements:
            t = tg.create_task(add_watermark(element))
            tasks.append(t)

    print(f"All tasks have completed now: {tasks[0].result()}, {tasks[-1].result()}")
    results = [t.result() for t in tasks]
    return results

start_time = time.time()

asyncio.run(main())

end_time = time.time()

print(f"The function took {end_time - start_time} seconds to complete.")
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()
