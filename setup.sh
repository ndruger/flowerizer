#!/bin/bash

git clone https://github.com/affinelayer/pix2pix-tensorflow.git
cd pix2pix-tensorflow
git reset --hard d6f8e4ce00a1fd7a96a72ed17366bfcb207882c7
cd ..
git clone https://github.com/lengstrom/fast-style-transfer.git
cd fast-style-transfer
git reset --hard 55809f4eafbe7d22632ac8fa254632ec41386d57
cd ..

mkdir -p pix2pix_train_data/orig
mkdir -p pix2pix_train_result
mkdir -p pix2pix_models
mkdir -p fast_style_transfer_train_result
mkdir -p fast_style_transfer_train_test_result
mkdir -p fast_style_transfer_test_result


cd pix2pix_train_data/orig/
# wget http://www.robots.ox.ac.uk/~vgg/data/flowers/102/102flowers.tgz
# wget http://www.robots.ox.ac.uk/~vgg/data/flowers/102/102segmentations.tgz
# wget http://www.robots.ox.ac.uk/~vgg/data/flowers/102/imagelabels.mat
#tar zxvf 102flowers.tgz
#tar zxvf 102segmentations.tgz
