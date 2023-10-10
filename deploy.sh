echo "deploying to $1"
folder=$1

rm -rf $folder/bin/*
cp -R dist/ $folder/bin/

