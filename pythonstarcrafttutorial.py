import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
    CYBERNETICSCORE, STALKER


# inherent form BotAT
class RonBot(sc2.BotAI):
    async def on_step(self, iteration):  # on_step - game itearation
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()
        await self.offensive_force_buildings()
        await self.build_offensive_force()

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

    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(15.0, nexus)
            for vaspene in vaspenes:
                if not self.can_afford(ASSIMILATOR):
                    break

                # grab a worker closest to the vaspene gas
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                # Test if there's already an assimilator on current vaspene
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(ASSIMILATOR, vaspene)) # what to build, where to
    async def expand(self):
        if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS):
            await self.expand_now() # built in function


    async def offensive_force_buildings(self):
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random
            if self.units(GATEWAY).ready.exists:
                if not self.units(CYBERNETICSCORE):
                    if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                        await self.build(CYBERNETICSCORE, near=pylon)
            else:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)
    async def build_offensive_force(self):
        for gw in self.units(GATEWAY).ready.noqueue:
            if self.can_afford(STALKER) and self.supply_left > 0:
                await self.do(gw.train(STALKER))





run_game(maps.get("AbyssalReefLE"),[
    Bot(Race.Protoss, RonBot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False)
