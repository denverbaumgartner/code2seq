IMAGE=tensorflow/tensorflow:2.1.0-gpu 
AST_TRAINING_GIST=https://gist.githubusercontent.com/denverbaumgartner/f1a4c4db0056a3a078b01c0c4e3c9de1/raw/14103fa6d031d0f92d05a9675a4863faf69005ce/file.txt
AST_TEST_GIST=https://gist.githubusercontent.com/denverbaumgartner/9837d66d94dee897c4f8205baad4c7c0/raw/1ccf7f3e0583c2d2fec646743b3090c79506a076/file.txt
AST_EVAL_GIST=https://gist.githubusercontent.com/denverbaumgartner/fef56cf1af35c25cddfd454e520fedf0/raw/66b79db780b5bc0ea213fdb85b702c8b4a0c79e3/file.txt
AST_TRAINING_NAME=train_output_file.txt
AST_TEST_NAME=test_output_file.txt
AST_EVAL_NAME=valid_output_file.txt

# install gh 
sudo snap install gh

# download the docker image
sudo docker pull $IMAGE

# load the submodule
git submodule init
git submodule update --recursive

# load the data
cd SQLExtractor/data
curl -L -o $AST_TRAINING_NAME $AST_TRAINING_GIST
curl -L -o $AST_TEST_NAME $AST_TEST_GIST 
curl -L -o $AST_EVAL_NAME $AST_EVAL_GIST

# cd ../../..
# sudo docker run -it $IMAGE

# sudo docker cp code2seq/ b6ff5d430193:/tmp/

# once inside the docker image
# DATA_DIR=data/
# SEED=239

# cd code2seq/SQLExtractor/
# bash preprocess.sh $DATA_DIR

# DESC=default
# CUDA=0
# DATA_DIR=SQLExtractor/data/
# cd ../../

# apt-get update
# apt-get install python3-venv
# cd ..
# python3 -m venv venv 
# source venv/bin/activate
# pip install --upgrade pip
# pip install -r requirements.txt

# bash train_python150k.sh $DATA_DIR $DESC $CUDA $SEED

# DATA_DIR=SQLExtractor/data/data
# python reader.py -d $DATA_DIR