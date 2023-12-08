# this is simply a process for converting ASTs into dense vectors utilizing a trained code2seq model
import pickle
import numpy as np
import tensorflow as tf

from config import Config
from interactive_predict import InteractivePredictor
from modelrunner import ModelRunner
from args import read_args

if __name__ == '__main__':
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices):
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
        # tf.config.set_visible_devices([], 'GPU')

    args = read_args()

    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)

    # get the encoded file path 
    file_to_encode = args.encode
    if not file_to_encode: 
        print('Please provide a file for encoding')
        exit(-1)
    else: 
        with open(file_to_encode, 'r') as file: 
            data_lines = file.readlines()

    if args.debug:
        config = Config.get_debug_config(args)
        tf.config.experimental_run_functions_eagerly(True)
    else:
        config = Config.get_default_config(args)

    print('Configuration established')
    if config.LOAD_PATH:
        print(f'Loading model from path: {config.LOAD_PATH}')
        model = ModelRunner(config)
        reader = model.test_dataset_reader
        encoded_lines = {}
        error_count = 0
        for line in data_lines:
            #encoded_lines = model.encode(data_lines)
            line_count = len(line.split(' '))
            
            # this is a terrible fix 
            if line_count == 1001: 
                line = line[:-1] + ' \n'

            line_count = len(line.split(' '))

            try:
                input_tensors = reader.process_from_placeholder(line)
                print(f'proper_line_count: {line_count}')
            except Exception as e: 
                print(f'error while attempting to get tensors: {e}')    
                error_count += 1
                print(f'failing line: {line_count}')
                encoded_lines[line.strip()] = None
                continue

            try:
                contexts = model.model.run_encoder(input_tensors, is_training=False)
                # encoded_lines.append(contexts)
                encoded_lines[line.strip()] = contexts
            except Exception as e:
                print(f'error while attempting to encode tensors: {e}')
                error_count += 1
                print(f'failing line: {line_count}')
                encoded_lines[line.strip()] = None
                continue
        print(f'total line count: {len(data_lines)}')
        print(f'total failing: {error_count}')
        with open('eval_encoded_lines.pkl', 'wb') as file:
            pickle.dump(encoded_lines, file)
            print('successfully pickled the tensors')
    else: 
        print(f'Please specify a path through which to load the model')