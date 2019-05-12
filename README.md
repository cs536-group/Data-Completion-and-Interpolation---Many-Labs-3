# Data Completion and Interpolation - Many Labs 3

## Description
This is the final project for **CS 536: Machine Learning**.

## File Structure
```
├─code							# is for storing codes
│     dataFormat.py				# encode and decode dataset
│     funcs.py					# activation and loss functions
│     layers.py					# a layer in autoencoder
│     preprocess.py				# preprocess encoded data and postprocess
│     train.py					# autoencoder
├─data							# is for storing variables
│      dataScaledMatrix.pkl		# preprocessed dataset
│      deSortMap.pkl			# map from preprocessed set to original set
│      difDataMatrix.pkl		# max - min for each feature
│      flagScaledMatrix.pkl		# preprocessed NA mask
│      formatFun.pkl			# functions for encode and decode
│      minDataMatrix.pkl		# min for each features
│      ML3AllSitesC.csv			# dataset fixed bug in row 1177
│      realScaledMatrix.pkl		# preprocessed real/prob mask
│      splitedData.pkl			# data and masks splited into train, dev and test
├─docs							# is for storing documents
│      report.pdf				# the report of this project
└─README.md
```