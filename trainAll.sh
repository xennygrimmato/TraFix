#!/bin/bash
notify ./generateManyBaseDatasets.sh
notify python measureTrainTime.py $1 13371337
notify python measureTrainTimeL2.py $1 13371337