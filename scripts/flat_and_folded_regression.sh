export SCRIPTS_DIR=$PWD

cd $VTR_ROOT && \
git checkout vtr_master && \
cd $VTR_ROOT && \
make && \

cd $SCRIPTS_DIR && \
./flat_regression.sh























