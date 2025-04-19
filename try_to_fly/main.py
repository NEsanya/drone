import asyncio
import json

from connection.config import LOG_LEVEL
from logger import set_logger_config


async def start_websocket():
    from fly import run_to_point, drop_water, down, connection
    from PID import concat_engine

    await connection.set_connection()

    fire_position = json.loads(connection.receive_data())["firesPositions"]
    print(fire_position)
    fire_position = [fire_position[4], fire_position[2]]
    connection.send_data(concat_engine([0 for _ in range(8)], {"id": 0}, 0))

    for position in fire_position:
        run_to_point(position["x"], position["z"])
        drop_water()
        run_to_point(-77, 75)
        down()

    connection.close_connection()


if __name__ == "__main__":
    set_logger_config(LOG_LEVEL)
    asyncio.run(start_websocket())