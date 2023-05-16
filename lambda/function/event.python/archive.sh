#! /bin/bash

# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

SOURCE_FILES=(
  lambda_function.py
)
ZIP_FILE_NAME=function.zip
ROOT_PATH=$PWD
SOURCE_PATH=$ROOT_PATH/src

if [ ! -d build ]; then
  mkdir build
fi
cd build

if [ -d package ]; then
  rm -rf package
fi
pip install --target package -r $SOURCE_PATH/requirements.txt
cd package

rm ../$ZIP_FILE_NAME
if [ -n "$(ls)" ]; then
  zip -r ../$ZIP_FILE_NAME .
fi
cd ..
rm -rf package

cd $SOURCE_PATH
for SOURCE_FILE in ${SOURCE_FILES[@]} ; do
  zip ../build/$ZIP_FILE_NAME $SOURCE_FILE
done
