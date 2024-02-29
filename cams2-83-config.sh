#!/usr/bin/bash

LUSTRE=/lustre/storeB/project/fou/kl/CAMS2_83

cams2-83 conf $(date +%Y%m%d_forecast-last-week.json) \
    $(date +%F -d "9 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --name          "CAMS regional evaluation (forecast)" \
    --id            forecast-last-week \
    --description   "Evaluation of the forecast for the latest week for which both model data and observations are available, using EEA NRT obs." \
    --eval-type      week

cams2-83 conf $(date +%Y%m%d_forecast-last-day.json) \
    $(date +%F -d "2 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --name          "CAMS regional evaluation (forecast)" \
    --id            forecast-last-day \
    --description   "Evaluation of the forecast for the latest day for which both model data and observations are available, using EEA NRT obs." \
    --eval-type     day

cams2-83 conf $(date +%Y%m%d_analysis-last-week.json) \
    $(date +%F -d "9 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --name          "CAMS regional evaluation (analysis)" \
    --id            analysis-last-week \
    --description   "Evaluation of the analysis for the latest week for which both model data and observations are available, using EEA NRT obs." \
    --eval-type     week \
    --analysis

cams2-83 conf $(date +%Y%m%d_analysis-last-day.json) \
    $(date +%F -d "2 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --name          "CAMS regional evaluation (analysis)" \
    --id            analysis-last-day \
    --description   "Evaluation of the analysis for the latest day for which both model data and observations are available, using EEA NRT obs." \
    --eval-type     day \
    --analysis


cams2-83 conf $(date +%Y%m%d_forecast-last-seasons.json) \
    2021-06-01 \
    2024-02-29 \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --name          "CAMS regional evaluation (forecast)" \
    --id            forecast-last-seasons \
    --description   "Evaluation of the forecast for the 8 latest available complete seasons using EEA NRT obs." \
    --eval-type     long

cams2-83 conf $(date +%Y%m%d_analysis-last-seasons.json) \
    2021-06-01 \
    2024-02-29 \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --name          "CAMS regionalevaluation (analysis)" \
    --id            analysis-last-seasons \
    --description   "Evaluation of the analysis for the 8 latest available complete seasons, using EEA NRT obs." \
    --eval-type     long \
    --analysis --addmap
