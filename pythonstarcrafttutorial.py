import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON


# inherent form BotAT
class RonBot(sc2.BotAI):
    async def on_step(self, iteration):  # on_step - game itearation
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()

    # Method, needs to pass 'self'
    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    # Method, needs to pass 'self'
    async  def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):  # supply = population
            nexues = self.units(NEXUS).ready # ready = not being built
            if nexues.exists:
                if self.can_afford(PYLON):
                    # need to specify where to build. builds next to the first nexus.
                    await self.build(PYLON, near=nexues.first)

run_game(maps.get("AbyssalReefLE"),[
    Bot(Race.Protoss, RonBot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True)
