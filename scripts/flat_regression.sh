# This script
# Arguments
#     1. parent directory to store inside (optional)



export RUNS_DIR=../runs
if (( $# == 1))
then
        RUNS_DIR=../runs/$1
         # create directory if it doesn't exist
         if [ ! -d $RUNS_DIR ]; then
            mkdir $RUNS_DIR
         fi
fi

export FOLDING_METHOD=flat
export RRGF_DIR=/home/ethan/workspaces/ethanroj23/rr_graph_folding

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

directrf
echo "directrf..."

cd $VTR_ROOT/vtr_flow/tasks/regression_tests/titan/directrf
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/titan/stratixiv_arch.timing.xml \
   $VTR_ROOT/vtr_flow/benchmarks/titan_blif/directrf_stratixiv_arch_timing.blif \
   --sdc_file $VTR_ROOT/vtr_flow/benchmarks/titan_blif/directrf_stratixiv_arch_timing.sdc \
   --route_chan_width 300  \
   --read_rr_graph $RRGF_DIR/flat_graphs/directrf.xml \
   >> $CUR_DIR/directrf.log
cp perf.out $CUR_DIR/directrf_perf.out

python3 $SCRIPTS_DIR/parse_regression.py $CUR_DIR > reg_results.md
rm $CUR_DIR/current_pid.out
exit 1

export X50_RRGRAPH=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/rr_graph_xc7a50t_test.rr_graph.real.bin
export X100_RRGRAPH=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a100t_test/rr_graph_xc7a100t_test.rr_graph.real.bin
export X200_RRGRAPH=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a200t_test/rr_graph_xc7a200t_test.rr_graph.real.bin

export X50_ARCH=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/arch.timing.xml
export X50_ARCH=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a100t_test/arch.timing.xml
export X50_ARCH=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a200t_test/arch.timing.xml

export X50_LOOKAHEAD=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/rr_graph_xc7a50t_test.lookahead.bin
export X100_LOOKAHEAD=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a100t_test/rr_graph_xc7a100t_test.lookahead.bin
export X200_LOOKAHEAD=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a200t_test/rr_graph_xc7a200t_test.lookahead.bin

export X50_PDELAY=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/rr_graph_xc7a50t_test.place_delay.bin 
export X100_PDELAY=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a100t_test/rr_graph_xc7a100t_test.place_delay.bin 
export X200_PDELAY=/home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a200t_test/rr_graph_xc7a200t_test.place_delay.bin 


export VTR_ROOT=/home/ethan/workspaces/ethanroj23/vtr
export perf_options="sudo perf stat -B -e cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,LLC-loads,LLC-load-misses,LLC-stores"

export SYM_ARCH=$VTR_ROOT/vtr_flow/arch/symbiflow
export SYM_BLIF=$VTR_ROOT/vtr_flow/benchmarks/symbiflow
export CUR_DEVICE=xc7a50t_test

for SYM_DIR in linux_arty picosoc_basys3_full_50 picosoc_basys3_full_100 minilitex_arty
# for SYM_DIR in linux_arty_100t
do
   if [ ! -d $RRGF_DIR/temp_runs/$SYM_DIR ]; then
      mkdir $RRGF_DIR/temp_runs/$SYM_DIR
   fi
   cd $RRGF_DIR/temp_runs/$SYM_DIR
   

   echo "${SYM_DIR}"
   $perf_options --output perf.out \
   $VTR_ROOT/vpr/vpr $SYM_ARCH/$CUR_DEVICE/arch.timing.xml $SYM_BLIF/$SYM_DIR.eblif \
   --read_rr_graph $RRGF_DIR/flat_graphs/xc7a50t_test.xml --read_router_lookahead $SYM_ARCH/$CUR_DEVICE/rr_graph_$CUR_DEVICE.lookahead.bin --read_placement_delay_lookup $SYM_ARCH/$CUR_DEVICE/rr_graph_$CUR_DEVICE.place_delay.bin --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold 1000 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta_override --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --initial_pres_fac 4.0 --check_rr_graph off \
   --fix_clusters /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/place_constr/$SYM_DIR.place \
   --sdc_file /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/sdc/$SYM_DIR.sdc \
   > $CUR_DIR/$SYM_DIR.log
   cp perf.out $CUR_DIR/EArch_tseng_perf.out

done


# EArch tseng
echo "EArch tseng..."
cd $RRGF_DIR/temp_runs/EArch_tseng
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/timing/EArch.xml $VTR_ROOT/vtr_flow/benchmarks/blif/tseng.blif \
--route_chan_width 100 --read_rr_graph \
$RRGF_DIR/flat_graphs/EArch_tseng.xml \
> $CUR_DIR/EArch_tseng.log
cp perf.out $CUR_DIR/EArch_tseng_perf.out


# k6 arm_core
echo "k6_arm_core..."

cd $RRGF_DIR/temp_runs/k6_arm_core
$perf_options --output perf.out \
$VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/timing/k6_frac_N10_frac_chain_mem32K_40nm.xml arm_core \
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

# directrf
# echo "directrf..."

# cd $VTR_ROOT/vtr_flow/tasks/regression_tests/titan/directrf
# $perf_options --output perf.out \
# $VTR_ROOT/vpr/vpr $VTR_ROOT/vtr_flow/arch/titan/stratixiv_arch.timing.xml \
#    $VTR_ROOT/vtr_flow/benchmarks/titan_blif/directrf_stratixiv_arch_timing.blif \
#    --sdc_file $VTR_ROOT/vtr_flow/benchmarks/titan_blif/directrf_stratixiv_arch_timing.sdc \
#    --route_chan_width 300  \
#    --read_rr_graph $RRGF_DIR/flat_graphs/directrf.xml \
#    >> $CUR_DIR/directrf.log
# cp perf.out $CUR_DIR/directrf_perf.out




# arty 35
# vpr /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/arch.timing.xml linux_arty.eblif --device xc7a50t-test --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold -1 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --acc_fac 0.7 --astar_fac 1.8 --initial_pres_fac 2.828 --pres_fac_mult 1.2 --check_rr_graph off --suppress_warnings ,sum_pin_class:check_unbuffered_edges:load_rr_indexed_data_T_values:check_rr_node:trans_per_R:check_route:set_rr_graph_tool_comment:calculate_average_switch --read_rr_graph /home/ethan/rr_graphs/fpt/arty_35.xml --read_router_lookahead /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/rr_graph_xc7a50t_test.lookahead.bin --read_placement_delay_lookup /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/rr_graph_xc7a50t_test.place_delay.bin --fix_clusters constraints.place --sdc_file linux_arty.sdc --place_file linux_arty.place
# vpr /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/arch.timing.xml top.eblif --device xc7a50t-test --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold -1 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --acc_fac 0.7 --astar_fac 1.8 --initial_pres_fac 2.828 --pres_fac_mult 1.2 --check_rr_graph off --suppress_warnings ,sum_pin_class:check_unbuffered_edges:load_rr_indexed_data_T_values:check_rr_node:trans_per_R:check_route:set_rr_graph_tool_comment:calculate_average_switch --read_rr_graph /home/ethan/rr_graphs/fpt/arty_35.xml --read_router_lookahead /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/rr_graph_xc7a50t_test.lookahead.bin --read_placement_delay_lookup /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a50t_test/rr_graph_xc7a50t_test.place_delay.bin --fix_clusters constraints.place --sdc_file linux_arty.sdc --place_file linux_arty.place

# arty 100
# vpr /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a100t_test/arch.timing.xml top.eblif --device xc7a100t-test --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold -1 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --acc_fac 0.7 --astar_fac 1.8 --initial_pres_fac 2.828 --pres_fac_mult 1.2 --check_rr_graph off --suppress_warnings ,sum_pin_class:check_unbuffered_edges:load_rr_indexed_data_T_values:check_rr_node:trans_per_R:check_route:set_rr_graph_tool_comment:calculate_average_switch --read_rr_graph /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a100t_test/rr_graph_xc7a100t_test.rr_graph.real.bin --read_router_lookahead /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a100t_test/rr_graph_xc7a100t_test.lookahead.bin --read_placement_delay_lookup /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a100t_test/rr_graph_xc7a100t_test.place_delay.bin --route --write_rr_graph /home/ethan/rr_graphs/fpt/arty_100.xml

# arty 200
# vpr /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a200t_test/arch.timing.xml top.eblif --device xc7a200t-test --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold -1 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --acc_fac 0.7 --astar_fac 1.8 --initial_pres_fac 2.828 --pres_fac_mult 1.2 --check_rr_graph off --suppress_warnings ,sum_pin_class:check_unbuffered_edges:load_rr_indexed_data_T_values:check_rr_node:trans_per_R:check_route:set_rr_graph_tool_comment:calculate_average_switch --read_rr_graph /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a200t_test/rr_graph_xc7a200t_test.rr_graph.real.bin --read_router_lookahead /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a200t_test/rr_graph_xc7a200t_test.lookahead.bin --read_placement_delay_lookup /home/ethan/opt/symbiflow/xc7/install/share/symbiflow/arch/xc7a200t_test/rr_graph_xc7a200t_test.place_delay.bin --route --write_rr_graph /home/ethan/rr_graphs/fpt/nexys_video.xml



#linux_arty.eblif  minilitex_arty.eblif  minilitex_ddr_arty.eblif  minilitex_ddr_eth_arty.eblif  picosoc_basys3_full_100.eblif  picosoc_basys3_full_50.eblif

# The entire flow of VPR took 464.79 seconds (max_rss 3545.4 MiB) - linux_arty
# The entire flow of VPR took 234.15 seconds (max_rss 3423.5 MiB) - minilitex_arty
# The entire flow of VPR took 336.66 seconds (max_rss 3485.3 MiB) - minilitex_ddr_arty
# The entire flow of VPR took 376.56 seconds (max_rss 3502.1 MiB) - minilitex_ddr_eth_arty
# The entire flow of VPR took 154.83 seconds (max_rss 3395.6 MiB) - picosoc_basys3_full_100
# The entire flow of VPR took 84.83 seconds (max_rss 3394.9 MiB) - picosoc_basys3_full_50


# linux_arty
# /home/ethan/workspaces/ethanroj23/vtr/vpr/vpr arch.timing.xml linux_arty --circuit_file linux_arty.pre-vpr.eblif \
# --read_rr_graph /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.rr_graph.real.bin --read_router_lookahead /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.lookahead.bin --read_placement_delay_lookup /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.place_delay.bin --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold 1000 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta_override --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --initial_pres_fac 4.0 --check_rr_graph off \
# --fix_clusters /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/place_constr/linux_arty.place \
# --sdc_file /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/sdc/linux_arty.sdc

# # pico_50
# /home/ethan/workspaces/ethanroj23/vtr/vpr/vpr arch.timing.xml picosoc_basys3_full_50 --circuit_file picosoc_basys3_full_50.pre-vpr.eblif \
# --read_rr_graph /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.rr_graph.real.bin --read_router_lookahead /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.lookahead.bin --read_placement_delay_lookup /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.place_delay.bin --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold 1000 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta_override --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --initial_pres_fac 4.0 --check_rr_graph off \
# --fix_clusters /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/place_constr/picosoc_basys3_full_50.place \
# --sdc_file /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/sdc/picosoc_basys3_full_50.sdc

# # pico_100
# /home/ethan/workspaces/ethanroj23/vtr/vpr/vpr arch.timing.xml picosoc_basys3_full_100 --circuit_file picosoc_basys3_full_100.pre-vpr.eblif \
# --read_rr_graph /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.rr_graph.real.bin --read_router_lookahead /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.lookahead.bin --read_placement_delay_lookup /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.place_delay.bin --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold 1000 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta_override --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --initial_pres_fac 4.0 --check_rr_graph off \
# --fix_clusters /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/place_constr/picosoc_basys3_full_100.place \
# --sdc_file /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/sdc/picosoc_basys3_full_100.sdc

# # minilitex
# /home/ethan/workspaces/ethanroj23/vtr/vpr/vpr arch.timing.xml minilitex_arty --circuit_file minilitex_arty.pre-vpr.eblif \
# --read_rr_graph /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.rr_graph.real.bin --read_router_lookahead /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.lookahead.bin --read_placement_delay_lookup /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.place_delay.bin --max_router_iterations 500 --routing_failure_predictor off --router_high_fanout_threshold 1000 --constant_net_method route --route_chan_width 500 --router_heap bucket --clock_modeling route --place_delta_delay_matrix_calculation_method dijkstra --place_delay_model delta_override --router_lookahead extended_map --check_route quick --strict_checks off --allow_dangling_combinational_nodes on --disable_errors check_unbuffered_edges:check_route --congested_routing_iteration_threshold 0.8 --incremental_reroute_delay_ripup off --base_cost_type delay_normalized_length_bounded --bb_factor 10 --initial_pres_fac 4.0 --check_rr_graph off \
# --fix_clusters /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/place_constr/minilitex_arty.place \
# --sdc_file /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/benchmarks/symbiflow/sdc/minilitex_arty.sdc



# /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.rr_graph.real.bin 50
# /home/ethan/workspaces/ethanroj23/vtr/vtr_flow/arch/symbiflow/rr_graph_xc7a50t_test.rr_graph.real.bin 100



# mv /home/ethan/vtr_regressions/nohup.out /home/ethan/vtr_regressions/$dir_name/nohup.out
# cd  /home/ethan/vtr_regressions/$dir_name
python3 $SCRIPTS_DIR/parse_regression.py $CUR_DIR > reg_results.md
rm $CUR_DIR/current_pid.out












