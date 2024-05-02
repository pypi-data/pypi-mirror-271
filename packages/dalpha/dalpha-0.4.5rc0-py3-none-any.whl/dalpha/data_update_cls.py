import sys
import time
import traceback
from typing import Callable, Dict

from dalpha.dto import InferenceResult
from dalpha.logging import logger
from dalpha.exception import ExpectedError
from dalpha.agent import Agent

class DalphaDataUpdater:
    def __init__(
        self,
        kafka_topic: str,
        inference: Callable[[Agent, Dict, int, int, bool], InferenceResult], # TODO: InferenceResult에 해당하는 UpdateResult가 있는지?
        load_globals: Callable[[], Dict],
    ):
        self.agent = Agent(api_id=0, kafka_topic=kafka_topic)
        self.inference = inference
        self.globals = load_globals()

    def _poll_input(self):
        try:
            return self.agent.update_poll()
        except SystemExit:
            logger.info("SystemExit caught, exiting.")
            sys.exit(0)
        except Exception as e:
            logger.warning(f"Error during update_poll: {e}")
            return None

    def _pipeline(self):
        input_json = self._poll_input()
        if input_json is None:
            logger.info("No input for update")
            return
        
        logger.info("processing...")

        try:
            file = input_json["file"]
            bucket, key, size = (
                file["bucket"],
                file["key"],
                file["size"],
            )
        except KeyError as e:
            error_message = f"input format is not correct!\n{e}"
            logger.error(error_message)
            error_json = {"reason": error_message}
            self.agent.update_error(output=error_json)
            return
        
        try:
            download_path = 'temp'
            self.agent.download_from_s3(
                bucket, key, download_path
            )
        except Exception as e:
            error_message = f"Error during download_from_s3: {e}\n{traceback.format_exc()}"
            logger.error(error_message)
            error_json = {"reason": error_message}
            self.agent.update_error(output=error_json)
            return
        
        try:
            logger.info("Data update starts...")
            update_start_time = time.time()
            ## TODO : data update code
            update_end_time = time.time()
            logger.info(f"Data update is done. Time taken: {update_end_time - update_start_time:.2f} sec")
        except ExpectedError as expected_error:
            self.agent.update_error(output=expected_error.error_json)
            return
        except Exception as unexpected_error:
            error_message = f"Unexpected error occurred while data update : \033[31m{unexpected_error}\033[0m\n{traceback.format_exc()}\n"
            logger.error(error_message)
            error_json = {"reason": f"Unexpected error occurred while data update: {unexpected_error}"}
            self.agent.update_error(output=error_json)
            return
        
        self.agent.update_complete(alert=False) # alert_data_update 채널에 알람 보내기

    def run(self):
        self._pipeline()
