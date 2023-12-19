import os 
import numpy as np
from flask import Flask
from .config import Config
from .args import read_args

import tensorflow as tf
from .interactive_predict import InteractivePredictor
from .modelrunner import ModelRunner

app = Flask(__name__)

MAX_DATA_CONTEXTS = int(os.getenv('MAX_DATA_CONTEXTS', '1000'))
LOAD_PATH = os.getenv('LOAD_PATH', 'models/sql-default/model/')
SEED = int(os.getenv('SEED', '239'))

@app.route('/')
def hello_world():
    return 'Hello, this is a message from the Flask app!'

def encode_line(line): 
    """A function to encode a single line of code using the code2vec model."""
    try:
        encoded_line = app.model.run_encoder(line, is_training=False)
        return encoded_line
    except Exception as e:
        print(f'Error while attempting to encode line: {e}')
        return str(e)

def process_line(line): 
    """A function to process a single line to be encoded by the code2seq model.
    
    :param line: The line to be processed (AST path specially formatted string)
    :type line: str
    """

    parts = line.rstrip('\n').split(' ')
    target_name = parts[0]
    contexts = parts[1:]
    max_data_contexts = MAX_DATA_CONTEXTS

    if len(contexts) > max_data_contexts:
        contexts = np.random.choice(contexts, max_data_contexts, replace=False)

    line_padded = " " * (max_data_contexts - len(contexts))

    try:
        processed_line = app.reader.process_from_placeholder(line_padded)
        return processed_line
    except Exception as e:
        print(f'Error while attempting to process line: {e}')
        return str(e)

if __name__ == '__main__':

    # get the config
    args = read_args()
    config = Config.get_default_config(args)
    config.LOAD_PATH = LOAD_PATH

    try:
        physical_devices = tf.config.list_physical_devices('GPU')
        if len(physical_devices):
            tf.config.experimental.set_memory_growth(physical_devices[0], True)
            tf.random.set_seed(SEED)
    except Exception as e:
        print(f'Error while attempting to set memory growth: {e}')

    np.random.seed(SEED)

    if config.LOAD_PATH:
        try:
            model = ModelRunner(config)
            reader = model.test_dataset_reader
            app.model = model
            app.reader = reader
        except Exception as e:
            print(f'Error while attempting to load model: {e}')

    app.run(debug=True, host='0.0.0.0', port=5001)
