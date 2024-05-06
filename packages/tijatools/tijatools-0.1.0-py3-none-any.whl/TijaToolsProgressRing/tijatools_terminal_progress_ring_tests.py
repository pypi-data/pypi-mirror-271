import asyncio
from progress_ring import ProgressRing, AnimationMode

async def do_some_work(duration):
    await asyncio.sleep(duration)

class ATest:
    async def run_test(self, duration):
        #rotate_symbols=['⬊', '⬉', '⬈', '⬋']
        # '↻', '↺'
        # '◐', '◓', '◑', '◒'
        # '◴', '◵', '◶', '◷'
        ring = ProgressRing(rotate_symbols=['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'])
        print("ROTATE:")
        await ring.run_with_animation(do_some_work(duration), AnimationMode.ROTATE)
        print("BOUNCE:")
        await ring.run_with_animation(do_some_work(duration), AnimationMode.BOUNCE, shape="😀")
        print("BOUNCE2:")
        await ring.run_with_animation(do_some_work(duration), AnimationMode.BOUNCE2)
        print("LOADING:")
        await ring.run_with_animation(do_some_work(duration), AnimationMode.LOADING)

if __name__ == "__main__":
    test = ATest()
    asyncio.run(test.run_test(10))  # A teszt időtartama 60 másodperc
