import logging
import argparse
from threading import Thread
from pyftg import Gateway, ObserverGateway, ObserverHandler, DataFlag
from pyftg.struct import AudioData, FrameData, GameData, RoundResult, ScreenData


class Collector(ObserverHandler):
    def __init__(self) -> None:
        self.collected_frames = list()

    def on_initialize(self, game: GameData):
        logging.info("initialize")

    def on_game_update(self, frame: FrameData, screen: ScreenData, audio: AudioData):
        self.collected_frames.append(frame)
    
    def on_round_end(self, result: RoundResult, game_end_flag: bool):
        logging.info("round end")
        logging.info("length: %s", len(self.collected_frames))
        self.collected_frames.clear()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', default='INFO', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('--port', default=50051, type=int, help='Port used by DareFightingICE')
    args = parser.parse_args()
    logging.basicConfig(level=args.log)
    port = args.port
    character = 'ZEN'
    game_num = 1

    collector = Collector()
    observer_gateway = ObserverGateway(collector, DataFlag.FRAME_DATA, interval=60, port=port)
    observing_thread = Thread(target=observer_gateway.start)
    observing_thread.start()
    logging.info('Observer is started.')

    gateway = Gateway(port=port)
    gateway.run_game([character, character], ["BlackMamba", "MctsAi"], game_num)
    gateway.close()
    logging.info('Starting game ...')

    observing_thread.join()
    observer_gateway.close()
