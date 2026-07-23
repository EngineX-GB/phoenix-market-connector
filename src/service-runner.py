import multiprocessing
import os

import uvicorn
from fastapi import FastAPI

from PathController import PathController
from loader.PhoenixMobileConnector import PhoenixMobileConnector
from model.PropertyManager import PropertyManager
from persistence.PersistenceNET import PersistenceNET
from core.SystemController import SystemController
from loader.PhoenixFeedbackFetcher import PhoenixFeedbackFetcher
from PhoenixFeedbackV2Loader import PhoenixFeedbackV2Loader
from util.PhoenixIOUtil import PhoenixIOUtil
from util.PropertyFileReader import PropertyFileReader


def check_and_setup_default_properties():
    if not os.path.exists(".././properties/config.properties") or not os.path.exists(".././properties/headers.json"):
        print("[WARN] Required config files do not exist. Preparing setup to create default ones....")
        provider_domain_name = input("Enter the provider domain name: ")
        content_domain_name = input("Enter the content domain name: ")
        ukp_domain_name = input("Enter the UKP domain name: ")
        domain_properties_map = {"provider_domain_name": provider_domain_name,
                                 "content_domain_name": content_domain_name, "ukp_domain_name": ukp_domain_name}

        create_default_properties(".././properties/config.properties", "template/config.properties.template",
                                  domain_properties_map)
        create_default_properties(".././properties/headers.json", "template/headers.json.template",
                                  domain_properties_map)


def create_default_properties(config_file_path: str, template_file_path: str, domain_properties_map):
    if not os.path.exists(config_file_path):
        print("[WARN] " + config_file_path + " file does not exist. Creating a default one.")
        os.makedirs(".././properties", exist_ok=True)
        # read the template file
        config_template = open(PathController.resource_path(template_file_path), 'r', encoding='UTF-8')
        new_lines = list()
        lines = config_template.readlines()
        for line in lines:
            if "{provider.domain.name}" in line:
                line = line.replace("{provider.domain.name}", domain_properties_map["provider_domain_name"])
            if "{content2.domain.name}" in line:
                line = line.replace("{content2.domain.name}", domain_properties_map["content_domain_name"])
            if "{ukp.domain.name}" in line:
                line = line.replace("{ukp.domain.name}", domain_properties_map["ukp_domain_name"])
            if line.startswith("request.payload="):
                line = line.replace("request.payload=", "").strip()
                r_line = line[::-1]
                line = "request.payload=" + str(r_line) + "\n"
            if line.startswith("request.payload.next="):
                line = line.replace("request.payload.next=", "").strip()
                r_line = line[::-1]
                line = "request.payload.next=" + str(r_line) + "\n"
            if "\"cookie\":" in line:
                line = line.replace("\"cookie\":", "").strip()
                r_line = line[::-1]
                line = "\t\"cookie\":  " + str(r_line) + "\n"
            new_lines.append(line)
        config_template.close()
        # create a new config file with the string interpolation
        config_file = open(config_file_path, 'w', encoding='utf-8')
        config_file.writelines(new_lines)
        config_file.close()


app = FastAPI()

# Run this check to see if the required config files are present. If not, create them from scratch.
check_and_setup_default_properties()

propertyFileReader = PropertyFileReader(".././properties/config.properties")
propertyManager = PropertyManager(propertyFileReader)
persistence = PersistenceNET(propertyManager)
connector = PhoenixMobileConnector(propertyManager, persistence, True)
feedback_fetcher = PhoenixFeedbackFetcher(propertyManager)
feedbackv2_loader = PhoenixFeedbackV2Loader(propertyManager, True)
system_controller = SystemController(connector, feedback_fetcher, feedbackv2_loader)


@app.get('/ping')
def ping():
    return {"response": "pong"}


@app.post('/load/region/{regionid}')
def run_load_by_region(regionid: str):
    return system_controller.run_load("region", regionid)


@app.post('/load/feedback')
def run_feedback_load():
    return system_controller.run_load("feedback", None)

@app.post("/load/feedbackv2")
def run_feedbackv2_load(userIds: list[str]):
    return system_controller.run_feedbackv2_load(userIds)

if __name__ == "__main__":
    print(f"Running Phoenix Market Connector Service for {PhoenixIOUtil.get_os_name()}")
    multiprocessing.freeze_support()
    uvicorn.run("service-runner:app", host="127.0.0.1", port=8001)
