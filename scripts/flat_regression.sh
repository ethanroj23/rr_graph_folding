# this script 
# 1. checks out git branch of argument $1
# 2. checks if folded graphs exist in rr_graph_folding/folded_graphs/
# 3. runs regression

export FOLDING_METHOD=flat
export RRGF_DIR=/home/ethan/workspaces/ethanroj23/rr_graph_folding

# month date hour minute
now=$(date +"%m_%d_%H_%M")
dir_name="${FOLDING_METHOD}_${now}"
mkdir ../runs/$dir_name

export CUR_DIR=$PWD/../runs/$dir_name
export SCRIPTS_DIR=$PWD

echo "Beginning regressions and storing results in rr_graph_folding/runs/$dir_name"
echo "To kill process run the following command:"
echo "kill -9 $$"
echo $$ > $CUR_DIR/current_pid.out

# nodes_all_attr testing


export perf_options="sudo perf stat -B -e cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,LLC-loads,LLC-load-misses,LLC-stores"

# EArch tseng
echo "EArch tseng..."
cd ~/vtr_work/quickstart/vpr_tseng
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/timing/EArch.xml $VTR_ROOT/vtr_flow/benchmarks/blif/tseng.blif \
--route_chan_width 100 --read_rr_graph \
$RRGF_DIR/flat_graphs/EArch_tseng.xml \
> $CUR_DIR/EArch_tseng.log
cp perf.out $CUR_DIR/EArch_tseng_perf.out

# k6 arm_core
echo "k6_arm_core..."

cd $VTR_ROOT/vtr_flow/tasks/regression_tests/vtr_reg_nightly_test3/vtr_reg_qor_chain/run001/k6_frac_N10_frac_chain_mem32K_40nm.xml/arm_core.v/common
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr k6_frac_N10_frac_chain_mem32K_40nm.xml arm_core \
--circuit_file arm_core.pre-vpr.blif \
--route_chan_width 120 --read_rr_graph \
$RRGF_DIR/flat_graphs/k6_frac_N10_frac_chain_mem32K_40nm_arm_core.xml \
> $CUR_DIR/k6_arm_core.log 
cp perf.out $CUR_DIR/k6_arm_core_perf.out

# stratixiv cholesky
echo "stratixiv cholesky..."

cd $VTR_ROOT/vtr_flow/tasks/regression_tests/vtr_reg_weekly/vtr_reg_titan/run003/stratixiv_arch.timing.xml/cholesky_mc_stratixiv_arch_timing.blif/common
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr stratixiv_arch.timing.xml \
   cholesky_mc_stratixiv_arch_timing \
   --circuit_file \
   cholesky_mc_stratixiv_arch_timing.pre-vpr.blif \
   --route_chan_width 300 \
   --max_router_iterations 400 \
   --router_lookahead map \
   --read_rr_graph $RRGF_DIR/flat_graphs/stratixiv_cholesky.xml \
   >> $CUR_DIR/stratixiv_cholesky.log
cp perf.out $CUR_DIR/stratixiv_cholesky_perf.out


# mv /home/ethan/vtr_regressions/nohup.out /home/ethan/vtr_regressions/$dir_name/nohup.out
# cd  /home/ethan/vtr_regressions/$dir_name
python3 $SCRIPTS_DIR/parse_regression.py $CUR_DIR >> reg_results.md
rm $CUR_DIR/current_pid.out












