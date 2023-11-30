from flask import request
from flask_restful import Resource
from flask_cors import cross_origin
from backend.classifier.zsc import ZSC
from backend.classifier.configurations import classifier_config, read_config
import logging
from classifier.dataparser import parse

logger = logging.getLogger("API")
logging.basicConfig(level=logging.DEBUG)

logger.info("**********************initializing**********************")
zsc = ZSC(classifier_config)
logger.info("******************finished initializing*****************")

conf = read_config()


class Classification(Resource):
    @cross_origin()
    def get(self):
        text = request.args.get("text")
        k = request.args.get("k")
        if k != None:
            classifier_config["k"] = int(k)
        return {"text": text, "labels": zsc.classify_single(text)}


class Requirements(Resource):
    @cross_origin()
    def get(self):
        logger.debug("Got a GET request to requirements")

        condition = None
        labelsStr = request.args.get("labels")
        cs = request.args.get("cs")
        dimension = request.args.get("dimension")
        if labelsStr != None:
            logger.debug("query params")
            logger.debug("labels:" + labelsStr)
            labels = labelsStr.split(",")
            condition = (
                lambda ann: ann.cs == classifier_config["cs"]
                and ann.table == classifier_config["dimension"]
                and ann.label in labels
            )

        elif cs != None and dimension != None:
            logger.debug("cs: " + cs + ", dimension: " + dimension)
            condition = lambda ann: ann.cs == cs and ann.table == dimension

        reqs = parse(conf["data"], condition)
        reqsDics = [r.to_dictionary("en") for r in reqs]
        return {"labels": labelsStr, "requirements": reqsDics}
