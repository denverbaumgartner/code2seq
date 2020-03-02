from argparse import ArgumentParser
import numpy as np
import tensorflow as tf

from config import Config
from interactive_predict import InteractivePredictor
from modelrunner import ModelRunner

tf.config.experimental_run_functions_eagerly(True)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--data", dest="data_path",
                        help="path to preprocessed dataset", required=False)
    parser.add_argument("-te", "--test", dest="test_path",
                        help="path to test file", metavar="FILE", required=False)

    parser.add_argument("-s", "--save_prefix", dest="save_path_prefix",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-l", "--load", dest="load_path",
                        help="path to saved file", metavar="FILE", required=False)
    parser.add_argument('--release', action='store_true',
                        help='if specified and loading a trained model, release the loaded model for a smaller model '
                             'size.')
    parser.add_argument('--predict', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--seed', type=int, default=239)
    args = parser.parse_args()

    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)

    if args.debug:
        config = Config.get_debug_config(args)
    else:
        config = Config.get_default_config(args)

    print('Created model')
    if config.TRAIN_PATH:
        model = ModelRunner(config, is_training=True)
        model.train()
    if config.TEST_PATH and not args.data_path:
        model = ModelRunner(config, is_training=False)
        results, precision, recall, f1, rouge = model.evaluate()
        print('Accuracy: ' + str(results))
        print('Precision: ' + str(precision) + ', recall: ' + str(recall) + ', F1: ' + str(f1))
        print('Rouge: ', rouge)
    if args.predict:
        model = ModelRunner(config, is_training=False)
        predictor = InteractivePredictor(config, model)
        predictor.predict()
    if args.release and args.load_path:
        model = ModelRunner(config, is_training=False)
        model.evaluate(release=True)
