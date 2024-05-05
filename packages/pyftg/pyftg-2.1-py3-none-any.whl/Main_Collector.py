from pyftg.struct import GameData, FrameData, ScreenData, AudioData, RoundResult
from pyftg.enum import DataFlag
from pyftg import ObserverGateway, ObserverHandler
from enum import Enum
from pathlib import Path
import os
import logging
import argparse
import json
import datetime

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif isinstance(obj, Enum):
        return str(obj)
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.items() 
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj

class Collector(ObserverHandler):
    def __init__(self) -> None:
        self.collector_path = Path('Collector')
        self.frames = list()
        self.counter = 0
        if not os.path.exists(self.collector_path):
            os.mkdir(self.collector_path)

    def on_initialize(self, game: GameData):
        logging.info('initialize')
        self.game_data = game
        self.change_directory()

    def on_game_update(self, frame_data: FrameData, screen_data: ScreenData, audio_data: AudioData):
        logging.info('round number: %s', frame_data.current_frame_number)

        self.frames.append(todict(frame_data))
        self.counter += 1

    def on_round_end(self, round_result: RoundResult, is_game_end: bool):
        logging.info('round end: %s', round_result.elapsed_frame)

        with open(os.path.join(self.path, "game_log.json"), 'w') as file:
            file.write(json.dumps(self.frames, indent=2))

        with open(os.path.join(self.path, "result.json"), 'w') as file:
            file.write(json.dumps(todict(round_result), indent=2))
        
        self.frames.clear()
        if not is_game_end:
            self.change_directory()

    def change_directory(self):
        self.counter = 0
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y.%m.%d-%H.%M.%S")
        self.path = os.path.join(self.collector_path, formatted_datetime)
        os.mkdir(self.path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50051, type=int, help='Port used by DareFightingICE')
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    collector = Collector()
    gateway = ObserverGateway(handler=collector, data_flag=DataFlag.FRAME_DATA, interval=60, port=args.port)
    logging.info('Observer is started.')
    try:
        gateway.start()
    except KeyboardInterrupt:
        pass
    finally:
        gateway.close()
        logging.info('Observer is stopped.')
