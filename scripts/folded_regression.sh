# This script
# Arguments
#     1. folding method
#     2. parent directory to store inside (optional)

export RUNS_DIR=../runs
if (( $# == 2))
then
        RUNS_DIR=../runs/$2
         # create directory if it doesn't exist
         if [ ! -d $RUNS_DIR ]; then
            mkdir $RUNS_DIR
         fi
fi

export FOLDING_METHOD=$1
export RRGF_DIR=/home/ethan/workspaces/ethanroj23/rr_graph_folding
export VTR_ROOT=/home/ethan/workspaces/ethanroj23/vtr

# month date hour minute
now=$(date +"%m_%d_%H_%M")
dir_name="${FOLDING_METHOD}_${now}"
mkdir $RUNS_DIR/$dir_name

export CUR_DIR=$PWD/$RUNS_DIR/$dir_name
export SCRIPTS_DIR=$PWD

echo "Beginning regressions and storing results in rr_graph_folding/$RUNS_DIR/$dir_name"
echo "To kill process run the following command:"
echo "kill -9 $$"
echo $$ > $CUR_DIR/current_pid.out



export perf_options="sudo perf stat -B -e cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,LLC-loads,LLC-load-misses,LLC-stores"

# EArch tseng
echo "EArch tseng..."
CUR_FILE="${RRGF_DIR}/folded_graphs/${FOLDING_METHOD}_EArch_tseng.xml"
cd $RRGF_DIR/temp_runs/EArch_tseng
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/timing/EArch.xml $VTR_ROOT/vtr_flow/benchmarks/blif/tseng.blif \
--route_chan_width 100 --read_rr_graph \
$CUR_FILE \
> $CUR_DIR/EArch_tseng.log
cp perf.out $CUR_DIR/EArch_tseng_perf.out


# k6 arm_core
echo "k6_arm_core..."
CUR_FILE="${RRGF_DIR}/folded_graphs/${FOLDING_METHOD}_k6_frac_N10_frac_chain_mem32K_40nm_arm_core.xml"

cd $VTR_ROOT/vtr_flow/tasks/regression_tests/vtr_reg_nightly_test3/vtr_reg_qor_chain/run001/k6_frac_N10_frac_chain_mem32K_40nm.xml/arm_core.v/common
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr k6_frac_N10_frac_chain_mem32K_40nm.xml arm_core \
--circuit_file arm_core.pre-vpr.blif \
--route_chan_width 120 --read_rr_graph \
$CUR_FILE \
> $CUR_DIR/k6_arm_core.log 
cp perf.out $CUR_DIR/k6_arm_core_perf.out

# stratixiv cholesky
echo "stratixiv_cholesky..."
CUR_FILE="${RRGF_DIR}/folded_graphs/${FOLDING_METHOD}_stratixiv_cholesky.xml"

cd $VTR_ROOT/vtr_flow/tasks/regression_tests/vtr_reg_weekly/vtr_reg_titan/run003/stratixiv_arch.timing.xml/cholesky_mc_stratixiv_arch_timing.blif/common
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr stratixiv_arch.timing.xml \
   cholesky_mc_stratixiv_arch_timing \
   --circuit_file \
   cholesky_mc_stratixiv_arch_timing.pre-vpr.blif \
   --route_chan_width 300 \
   --max_router_iterations 400 \
   --router_lookahead map \
   --read_rr_graph $CUR_FILE \
   >> $CUR_DIR/stratixiv_cholesky.log
cp perf.out $CUR_DIR/stratixiv_cholesky_perf.out


# ---------------- SYMBIFLOW ----------------------

export SYM_ARCH=$VTR_ROOT/vtr_flow/arch/symbiflow

for SYM_DIR in linux_arty picosoc_basys3_full_50 picosoc_basys3_full_100 minilitex_arty
do
   if [ ! -d $RRGF_DIR/temp_runs/$SYM_DIR ]; then
      mkdir $RRGF_DIR/temp_runs/$SYM_DIR
   fi
   cd $RRGF_DIR/temp_runs/$SYM_DIR

   CUR_FILE="${RRGF_DIR}/folded_graphs/${FOLDING_METHOD}_xc7a50t_test.xml"

   echo "${SYM_DIR}"
   cd /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/tasks/regression_tests/vtr_reg_nightly_test1/symbiflow/run002/arch.timing.xml/$SYM_DIR.eblif/common/
   $perf_options --output perf.out \
   $VTR_ROOT/vpr/vpr arch.timing.xml $SYM_DIR --circuit_file $SYM_DIR.pre-vpr.eblif \
   --read_rr_graph $CUR_FILE --read_router_lookahead $SYM_ARCH/rr_graph_xc7a50t_test.lookahead.bin --read_placement_delay_lookup $SYM_ARCH/rr_graph_xc7a50t_test.place_delay.bin --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold 1000 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta_override --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --initial_pres_fac 4.0 --check_rr_graph off \
   --fix_clusters /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/place_constr/$SYM_DIR.place \
   --sdc_file /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/sdc/$SYM_DIR.sdc \
   > $CUR_DIR/$SYM_DIR.log
   cp perf.out $CUR_DIR/EArch_tseng_perf.out

done



echo "directrf..."
CUR_FILE="${RRGF_DIR}/folded_graphs/${FOLDING_METHOD}_directrf.xml"

cd $VTR_ROOT/vtr_flow/tasks/regression_tests/titan/directrf
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/titan/stratixiv_arch.timing.xml \
   $VTR_ROOT/vtr_flow/benchmarks/titan_blif/directrf_stratixiv_arch_timing.blif \
   --sdc_file $VTR_ROOT/vtr_flow/benchmarks/titan_blif/directrf_stratixiv_arch_timing.sdc \
   --route_chan_width 300  \
   --read_rr_graph $CUR_FILE \
   >> $CUR_DIR/directrf.log
cp perf.out $CUR_DIR/directrf_perf.out

# mv /home/ethan/vtr_regressions/nohup.out /home/ethan/vtr_regressions/$dir_name/nohup.out
# cd  /home/ethan/vtr_regressions/$dir_name
python3 $SCRIPTS_DIR/parse_regression.py $CUR_DIR > reg_results.md
rm $CUR_DIR/current_pid.out












