# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from humanloop.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    PROJECTS = "Projects"
    EVALUATIONS = "Evaluations"
    DATASETS = "Datasets"
    LOGS = "Logs"
    MODEL_CONFIGS = "Model Configs"
    EXPERIMENTS = "Experiments"
    EVALUATORS = "Evaluators"
    COMPLETIONS = "Completions"
    CHATS = "Chats"
    SESSIONS = "Sessions"
    DATAPOINTS = "Datapoints"
    FEEDBACK = "Feedback"
    AUTHENTICATION = "Authentication"
