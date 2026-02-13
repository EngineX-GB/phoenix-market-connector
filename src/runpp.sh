#!/bin/sh

# if the shell/logs folder does not exist in the PHOENIX_HOME directory, then create one.
LOGS_DIR="../shell/logs"

mkdir -p "$LOGS_DIR"

run_region_1() {
  sh runp.sh --regionx 1 --range 0 3 > region-1-r0_3.txt 2>&1 &
  sh runp.sh --regionx 1 --range 4 6 > region-1-r4_6.txt 2>&1 &
  sh runp.sh --regionx 1 --range 7 9 > region-1-r7_9.txt 2>&1 &
  sh runp.sh --regionx 1 --range 10 12 > region-1-r10_12.txt 2>&1 &
  sh runp.sh --regionx 1 --range 13 15 > region-1-r13_15.txt 2>&1 &
}

run_region_2() {
  sh runp.sh --regionx 2 --range 0 3 > $LOGS_DIR/region-2-r0_3.txt 2>&1 &
  sh runp.sh --regionx 2 --range 4 6 > $LOGS_DIR/region-2-r4_6.txt 2>&1 &
  sh runp.sh --regionx 2 --range 7 10 > $LOGS_DIR/region-2-r7_10.txt 2>&1 &
}

run_region_3() {
  sh runp.sh --regionx 3 --range 0 2 > $LOGS_DIR/region-3-r0_2.txt 2>&1 &
  sh runp.sh --regionx 3 --range 3 5 > $LOGS_DIR/region-3-r3_5.txt 2>&1 &
}

run_region_4() {
  sh runp.sh --regionx 4 --range 0 2 > $LOGS_DIR/region-4-r0_2.txt 2>&1 &
  sh runp.sh --regionx 4 --range 3 5 > $LOGS_DIR/region-4-r3_5.txt 2>&1 &
}

run_region_5() {
  sh runp.sh --regionx 5 --range 0 2 > $LOGS_DIR/region-5-r0_2.txt 2>&1 &
  sh runp.sh --regionx 5 --range 3 4 > $LOGS_DIR/region-5-r3_4.txt 2>&1 &
  sh runp.sh --regionx 5 --range 5 6 > $LOGS_DIR/region-5-r5_6.txt 2>&1 &
}

run_region_7() {
  sh runp.sh --region 7 > $LOGS_DIR/region-7.txt 2>&1 &
}

run_region_8() {
  sh runp.sh --region 8 > $LOGS_DIR/region-8.txt 2>&1 &
}

run_region_9() {
  sh runp.sh --regionx 9 --range 0 3 > $LOGS_DIR/region-9-r0_3.txt 2>&1 &
  sh runp.sh --regionx 9 --range 4 6 > $LOGS_DIR/region-9-r4_6.txt 2>&1 &
  sh runp.sh --regionx 9 --range 7 9 > $LOGS_DIR/region-9-r7_9.txt 2>&1 &
}

run_region_10() {
  sh runp.sh --region 10 > $LOGS_DIR/region-10.txt 2>&1 &
}

run_region_block_1() {
  sh runp.sh --region 6 > $LOGS_DIR/region-6.txt 2>&1 &
  sh runp.sh --region 11 > $LOGS_DIR/region-11.txt 2>&1 &
  sh runp.sh --region 12 > $LOGS_DIR/region-12.txt 2>&1 &
  sh runp.sh --region 14 > $LOGS_DIR/region-14.txt 2>&1 &
}

if [ "$1" = "r1" ]
  then run_region_1
elif [ "$1" = "r2" ]
  then run_region_2
elif [ "$1" = "r3" ]
  then run_region_3
elif [ "$1" = "r4" ]
  then run_region_4
elif [ "$1" = "r5" ]
  then run_region_5
elif [ "$1" = "r7" ]
  then run_region_7
elif [ "$1" = "r8" ]
  then run_region_8
elif [ "$1" = "r9" ]
  then run_region_9
elif [ "$1" = "r10" ]
  then run_region_10
elif [ "$1" = "rx" ]
  then run_region_block_1
fi
