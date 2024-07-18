from time import sleep
import logging
import asyncio

from drvPgva import PGVA
from VaemDriver import vaemDriver
from dataTypes import VaemConfig

try:
    # pgva = PGVA("tcp/ip", tcpPort=8502, host="192.168.0.118")
    vaemConfig = VaemConfig('192.168.8.118', 502, 0)
    vaem = vaemDriver(vaemConfig, logger=logging)
except Exception as e:
    print(e)

# def pressurize_valves() -> None:
#     pgva.calibration()
#     pgva.setPumpPressure(650,650)
#     pgva.aspirate(100, -40)
#     pgva.dispense(100, 40)
#     pgva.readSensData()

async def dispense_valve(valve_id: int) -> None:
    initial_valve = valve_id + 4

    print(vaem.read_status())
    await vaem.configure_valves(initial_valve, 10000)
    await vaem.configure_valves(valve_id, 10000)
    await vaem.select_valve(initial_valve)
    await vaem.open_valve()
    await vaem.select_valve(valve_id)
    await vaem.open_valve()
    await vaem.close_valve()
    print(vaem.read_status())


if __name__ == "__main__":
    # pressurize_valves()
    dispense_loop = asyncio.get_event_loop()
    dispense_loop.run_until_complete(dispense_valve(0))