import sys
import os

import argparse

parser = argparse.ArgumentParser(description="Train translation model")
parser.add_argument('training_dataset', type=str, help="training dataset to use")
parser.add_argument('validation_dataset', type=str, help="validation dataset to use")
parser.add_argument('model_directory', type=str, help="directory in which to save trained model")
parser.add_argument('model_name', type=str, help="name of trained model")
parser.add_argument('-e', '--external-validation', dest='validation_script', type=str, help="script to use for external validation")
parser.add_argument('-po', '--post-order', dest='po', help="use c code in post order", action='count')
args = parser.parse_args()

f = args.training_dataset
v = args.validation_dataset
mdir = args.model_directory
m = args.model_name
e = args.validation_script

import nematus.nmt as nmt

# set up logging
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

nmt.train(saveto=os.path.join(mdir,m),
		  datasets=[f+'.corpus.ll'), f+'.corpus.'+('po' if args.po else 'c')],
		  dictionaries=[f+'.vocab.ll.json', f+'.vocab.'+('po' if args.po else 'c')+'.json'],
		  batch_size=150,
		  valid_datasets=[v+'.corpus.ll', v+'.corpus.'+('po' if args.po else 'c')],
		  validFreq=1000,
		  patience=20,
		  valid_batch_size=150,
		  external_validation_script=e,
		  enc_depth=2,
		  dec_depth=2,
		  dim_word=32,
		  dim=500)
		  
if m.endswith('.npz'):
	m = m[:-4]
def cleanup():
	reserveFiles = [m+'.npz',m+'.npz.json']
	for f in os.listdir(mdir):
		if f.startswith(m):
			if not f in reserveFiles:
				os.remove(os.path.join(mdir,f))
cleanup()