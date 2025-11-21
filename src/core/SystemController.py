import threading


class SystemController:

    def __init__(self, connector, feedback_loader):
        self.connector = connector
        self.feedback_loader = feedback_loader

    def run_load(self, load_type, parameter):
        # if the load_type = region, then parameter could be 1,2 3,n
        if load_type == "region":
            thread_name = "LOAD_REGION_" + parameter  # e.g. LOAD_REGION_1
            # check that there is no existing thread running this process:
            if self.is_thread_running(thread_name):
                return {"error": "A load for region " + parameter + " is currently in progress."}
            load_thread = threading.Thread(target=self.connector.main, args=(parameter,), name=thread_name)
            load_thread.start()
            return {"started", "A load for region " + parameter + " has started."}
        elif load_type == "feedback":
            thread_name = "LOAD_FEEDBACK"
            if self.is_thread_running(thread_name):
                return {"error": "Feedback loading is currently in progress."}
            load_thread = threading.Thread(target=self.feedback_loader.main, args=["--standard"], name=thread_name)
            load_thread.start()
            return {"started", "Feedback loading has started."}

    def is_thread_running(self, thread_name):
        thread_list = threading.enumerate()
        for t in thread_list:
            if t.name == thread_name:
                return True
        return False
