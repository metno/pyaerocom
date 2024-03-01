#!/usr/bin/bash

ROOT=/lustre/storeB/project/fou/kl/CAMS2_83
EVAL=$ROOT/evaluation

cams2-83 conf forecast week \
    $(date +%Y%m%d_forecast-last-week.json) \
    $(date +%F -d "9 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $ROOT/model \
    --obs-path      $ROOT/obs  \
    --data-path     $EVAL/data \
    --coldata-path  $EVAL/coldata \
    --name          "CAMS regional evaluation (forecast)" \
    --id            forecast-last-week \
    --description   "Evaluation of the forecast for the latest week for which both model data and observations are available, using EEA NRT obs." \

cams2-83 conf forecast day \
    $(date +%Y%m%d_forecast-last-day.json) \
    $(date +%F -d "2 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $ROOT/model \
    --obs-path      $ROOT/obs  \
    --data-path     $EVAL/data \
    --coldata-path  $EVAL/coldata \
    --name          "CAMS regional evaluation (forecast)" \
    --id            forecast-last-day \
    --description   "Evaluation of the forecast for the latest day for which both model data and observations are available, using EEA NRT obs." \

cams2-83 conf analysis week \
    $(date +%Y%m%d_analysis-last-week.json) \
    $(date +%F -d "9 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $ROOT/model \
    --obs-path      $ROOT/obs  \
    --data-path     $EVAL/data \
    --coldata-path  $EVAL/coldata \
    --name          "CAMS regional evaluation (analysis)" \
    --id            analysis-last-week \
    --description   "Evaluation of the analysis for the latest week for which both model data and observations are available, using EEA NRT obs." \

cams2-83 conf forecast day \
    $(date +%Y%m%d_analysis-last-day.json) \
    $(date +%F -d "2 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $ROOT/model \
    --obs-path      $ROOT/obs  \
    --data-path     $EVAL/data \
    --coldata-path  $EVAL/coldata \
    --name          "CAMS regional evaluation (analysis)" \
    --id            analysis-last-day \
    --description   "Evaluation of the analysis for the latest day for which both model data and observations are available, using EEA NRT obs." \


cams2-83 conf forecast long \
    $(date +%Y%m%d_forecast-last-seasons.json) \
    2021-06-01 \
    2024-02-29 \
    --model-path    $ROOT/model \
    --obs-path      $ROOT/obs  \
    --data-path     $EVAL/data \
    --coldata-path  $EVAL/coldata \
    --name          "CAMS regional evaluation (forecast)" \
    --id            forecast-last-seasons \
    --description   "Evaluation of the forecast for the 8 latest available complete seasons, using EEA NRT obs." \

cams2-83 conf analysis long \
    $(date +%Y%m%d_analysis-last-seasons.json) \
    2021-06-01 \
    2024-02-29 \
    --model-path    $ROOT/model \
    --obs-path      $ROOT/obs  \
    --data-path     $EVAL/data \
    --coldata-path  $EVAL/coldata \
    --name          "CAMS regionalevaluation (analysis)" \
    --id            analysis-last-seasons \
    --description   "Evaluation of the analysis for the 8 latest available complete seasons, using EEA NRT obs." \
    --addmap
