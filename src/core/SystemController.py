import threading

from src.service.ClientService import ClientService
from src.util.PhoenixIOUtil import PhoenixIOUtil


class SystemController:

    def __init__(self, connector, feedback_loader, feedbackv2_loader):
        self.connector = connector
        self.feedback_loader = feedback_loader
        self.feedbackv2_loader = feedbackv2_loader


    # if the system is fetching a selection of user ids, then there is no need to
    # block the process from running again, since latest records will only be stored in
    # the database if they don't exist already.
    def run_feedbackv2_load(self, userIds : list[str]):
        if len(userIds) == 0:
            return PhoenixIOUtil.handle_response_message(
                "ERROR", "A job was submitted to download feedback-v2 entries for 0 userIds.", "")
        load_thread = threading.Thread(target=self.feedbackv2_loader.load_by_userId, args=(userIds,), name="load-feedback-v2-by-userids")
        load_thread.start()
        return PhoenixIOUtil.handle_response_message("STARTED", "A load for feedback-v2 has started.", "")

    def run_load(self, load_type, parameter):
        # if the load_type = region, then parameter could be 1,2 3,n
        if load_type == "region":
            thread_name = "LOAD_REGION_" + parameter  # e.g. LOAD_REGION_1
            # check that there is no existing thread running this process:
            if self.is_thread_running(thread_name):
                return PhoenixIOUtil.handle_response_message("ERROR",
                                                             f"A load for region {parameter} is currently in progress.","")
            # initialise required I/O for this workflow
            self.connector.start()

            load_thread = threading.Thread(target=self.connector.main, args=(parameter,), name=thread_name)
            load_thread.start()
            return PhoenixIOUtil.handle_response_message("STARTED", f"A load for region {parameter} has started.","")
        elif load_type == "feedback":
            thread_name = "LOAD_FEEDBACK"
            if self.is_thread_running(thread_name):
                return PhoenixIOUtil.handle_response_message("ERROR","Feedback loading is currently in progress.","")
            load_thread = threading.Thread(target=self.feedback_loader.main, args=(["feedback","--standard"],), name=thread_name)
            load_thread.start()
            return PhoenixIOUtil.handle_response_message("STARTED", "Feedback loading has started.", "")

    def is_thread_running(self, thread_name):
        thread_list = threading.enumerate()
        for t in thread_list:
            if t.name == thread_name:
                return True
        return False
