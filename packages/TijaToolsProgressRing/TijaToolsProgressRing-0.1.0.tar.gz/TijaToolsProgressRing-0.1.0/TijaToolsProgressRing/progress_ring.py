import asyncio
import sys
import time
import enum

class AnimationMode(enum.Enum):
    ROTATE = 'rotate'
    BOUNCE = 'bounce'
    BOUNCE2 = 'bounce2'
    LOADING = 'loading'

class ProgressRing:
    def __init__(self, total_steps=100, width=10, rotate_symbols=None):
        self.total_steps = total_steps
        self.current_step = 0
        self.is_running = False
        # Ha nincsenek egyéni szimbólumok megadva, használja az alapértelmezettet
        self.symbols = rotate_symbols if rotate_symbols is not None else ['|', '/', '-', '\\']
        self.width = width

    def start(self):
        self.is_running = True
        self.current_step = 0

    def stop(self, message="Task completed..."):
        print('\r', end='')  # Kurzort az aktuális sor elejére mozgatja
        for char in message:
            print(char, end='', flush=True)
            time.sleep(0.050)  # Kis szünet minden karakter között
        print()  # Új sorba ugrik
        self.is_running = False

    def update_display(self, mode=AnimationMode.ROTATE):
        if mode == AnimationMode.ROTATE:
            print('\r', end='')
            print(f'{self.symbols[self.current_step % len(self.symbols)]}', end='')
        elif mode == AnimationMode.BOUNCE or mode == AnimationMode.BOUNCE2:
            position = self.current_step % (2 * self.width - 2)
            if position >= self.width:
                position = 2 * self.width - 2 - position
            print('\r' + ' ' * (self.width * 2), end='')  # Törli a sor tartalmát
            print('\r' + ' ' * position + self.shape, end='')
        elif mode == AnimationMode.LOADING:
            dots = '.' * (self.current_step % 4 + 1)
            print(f'\rLoading{dots}   ', end='')
        sys.stdout.flush()
        self.current_step += 1

    async def run_with_animation(self, task, mode=AnimationMode.ROTATE, shape="*"):
        if shape:
            self.shape = shape
        self.start()
        task = asyncio.create_task(task)
        while not task.done():
            self.update_display(mode)
            await asyncio.sleep(0.1)
        self.stop()
