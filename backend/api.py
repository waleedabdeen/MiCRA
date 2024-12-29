import logging
from flask import request
from flask_restful import Resource
from flask_cors import cross_origin
from classifier.zsc import ZSC
from classifier.configurations import classifier_config, read_env_vars
from classifier.dataparser import parse
from classifier.artifact import Artifact
from classifier.db import write_artifact, read_artifacts

# env
conf = read_env_vars()

# logging
loggingLevel = logging.INFO if conf["server_env"] == "production" else logging.DEBUG
logging.basicConfig(level=loggingLevel)
logger = logging.getLogger("API")

# classifier
zsc = ZSC(classifier_config)


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
        logger.debug("Got a GET request /requirements")

        condition = None
        labelsStr = request.args.get("labels")
        cs = request.args.get("cs")
        dimension = request.args.get("dimension")
        returntype = request.args.get("returntype")
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

        if returntype == "count":
            return {"count": len(reqsDics)}

        return {"labels": labelsStr, "requirements": reqsDics}
    

class Artifacts(Resource):
    @cross_origin()
    def get(self):
        logger.debug("Got a GET request /artifacts")
        type = request.args.get("type")
        labelsStr = request.args.get("labels")
        artifacts_list = []
        if labelsStr != None:
            logger.debug("labels:" + labelsStr)
            labels = labelsStr.split(",")
            artifacts_list = read_artifacts(type, labels)
        else:
            artifacts_list = read_artifacts(type, None)    

        return [a.to_dictionary() for a in artifacts_list]

    @cross_origin()
    def post(self):
        try:
            logger.debug("Got a POST request /artifacts")
            
            data = request.get_json()
            logger.debug('data received: ' + str(data))

            artifact = Artifact()
            artifact.text = data['text'].strip()
            artifact.type = data['type'].strip()
            artifact.labels = [{"label": e,
                                "label_name": zsc.taxonomy.loc[zsc.taxonomy["identifier"] == e, "name_eng"].item()} for e in data["labels"]]
            logger.debug('Artifact: ' + str(artifact.to_dictionary()))

            id = write_artifact(artifact)

            return {'error': False, 'id': str(id)}
        
        except Exception as e:
            logger.error(e)
            return {'error': True}