import pandas as pd
from .requirement import Requirement, Annoation
from .artifact import Artifact
import os
import logging
import json

logger = logging.getLogger("db")
file = 'data/artifacts_with_labels.csv'

def read_artifacts(type, labels = None):
    global file
    try:    
        # if os.path.exists(file):
        data = pd.read_csv(file, delimiter=';')
        labels_filter = None
        if labels != None:
            logger.debug('found labels filter')
            logger.debug(labels)
            labels_filter = (lambda l: l['label'] in labels)

        result = []
        for row in data.values.tolist():
            art = Artifact()
            art.id = row[0]
            art.type = row[1]
            art.text = row[2]            
            art.labels = json.loads(row[3].replace("'", "\""))
            
            if art.type == type and art.has_labels(labels_filter):
                result.append(art)
        
        return result
        # return pd.DataFrame([{
        #     'id' : [],
        #     'text': [],
        #     'type': [],
        #     'labels': []
        # }]).to_dict(orient='index')
    
    except Exception as e:
        logger.error("Could not read artifact from database")
        logger.error(e)
        raise

def write_artifact(artifact: Artifact):
    global file
    try:
        new_id = 1

        data = pd.DataFrame([{
            'id' : [],
            'text': [],
            'type': [],
            'labels': []
        }])

        if os.path.exists(file):
            logger.debug('file db: ' +  file)
            data = pd.read_csv(file, delimiter=';')
            if len(data) > 0:
                new_id = data.iloc[-1].id + 1
                logger.info(new_id)

        artifact.id = new_id
        data.loc[-1] = artifact.to_dictionary()
        
        data.to_csv(file, index=False, sep=';')
        logger.info('Data saved in csv')

        return new_id
    
    except Exception as e:
        logger.error("Could not write artifact to database")
        logger.error(e)
        raise
