IMAGE=tensorflow/tensorflow:2.1.0-gpu 
AST_TRAINING_GIST=https://gist.githubusercontent.com/denverbaumgartner/0f7357362edc7f2a737897b23e3a52e2/raw/8c824b8d643665afd4b93da2db1031adaaef1927/file.txt
AST_TEST_GIST=https://gist.githubusercontent.com/denverbaumgartner/706f31886fc87b2eb8c3d2d11218b85f/raw/a4b9c9edce9609a53984655a9c8b9fc21f439b5c/file.txt
AST_EVAL_GIST=https://gist.githubusercontent.com/denverbaumgartner/7044017043fd28a16302d19cad61d703/raw/ced3e3bc95b00b87a5381b6ba350e949dea2c6e1/file.txt
AST_TRAINING_NAME=train_output_file.txt
AST_TEST_NAME=test_output_file.txt
AST_EVAL_NAME=valid_output_file.txt

AST_TESTSET_OG=https://gist.github.com/denverbaumgartner/b220ef2596c02907e705c20a1c2c5e17
AST_TESTSET_VARIANT=https://gist.github.com/denverbaumgartner/e118ff73ce4fd5dfd83b1a3964428257
AST_TESTSET_OG_NAME=testset_og.txt
AST_TESTSET_VARIANT_NAME=testset_variant.txt
# curl -L -o $AST_TESTSET_OG_NAME $AST_TESTSET_OG 
# curl -L -o $AST_TESTSET_VARIANT_NAME $AST_TESTSET_VARIANT

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

# sudo docker cp code2seq/ a5d8ef8b4807:/tmp/

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

# python -u code2vec.py --load_path=$DATA_DIR --seed=$SEED

# DATA_DIR=SQLExtractor/data/data
# python reader.py -d $DATA_DIR

# ENCODE=SQLExtractor/encode/encode.train.c2s
# python -u code2vec.py --load_path=$LOAD_PATH --encode=$ENCODE --seed=$SEED