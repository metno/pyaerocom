#!/usr/bin/bash

LUSTRE=/lustre/storeB/project/fou/kl/CAMS2_83

# forecast-last-week
cams2_83_run -n \
    $(date +%F -d "9 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --cache         $LUSTRE/evaluation/_cache_last-week \
    --name          "CAMS regional evaluation (forecast)" \
    --id            forecast-last-week \
    --description   "Evaluation of the forecast for the latest week for which both model data and observations are available, using EEA NRT obs." \
    --eval-type      week

# forecast-last-day
cams2_83_run -n \
    $(date +%F -d "2 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --cache         $LUSTRE/evaluation/_cache_last-day \
    --name          "CAMS regional evaluation (forecast)" \
    --id            forecast-last-day \
    --description   "Evaluation of the forecast for the latest day for which both model data and observations are available, using EEA NRT obs." \
    --eval-type     day

# analysis-last-week
cams2_83_run -n \
    $(date +%F -d "9 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --cache         $LUSTRE/evaluation/_cache_analysis_last-week \
    --name          "CAMS regional evaluation (analysis)" \
    --id            analysis-last-week \
    --description   "Evaluation of the analysis for the latest week for which both model data and observations are available, using EEA NRT obs." \
    --eval-type     week \
    --analysis

# analysis-last-day
cams2_83_run -n \
    $(date +%F -d "2 days ago") \
    $(date +%F -d "2 days ago") \
    --model-path    $LUSTRE/model \
    --obs-path      $LUSTRE/obs  \
    --data-path     $LUSTRE/evaluation/data \
    --coldata-path  $LUSTRE/evaluation/coldata \
    --cache         $LUSTRE/evaluation/_cache_analysis_last-day \
    --name          "CAMS regional evaluation (analysis)" \
    --id            analysis-last-day \
    --description   "Evaluation of the analysis for the latest day for which both model data and observations are available, using EEA NRT obs." \
    --eval-type     day \
    --analysis
