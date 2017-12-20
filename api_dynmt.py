def main(args):
	import os
	import ConfigParser
	config = ConfigParser.ConfigParser()
	dynmt = os.path.abspath('dynmt/src/dynmt.py')
	config.read(args['config'])
	train = os.path.abspath(args['training_dataset'])
	validation = os.path.abspath(args['validation_dataset'])
	test = os.path.abspath(args['test_dataset'])
	vocabs = os.path.abspath(args['vocabs'])
	ext = 'po' if args['post_order'] else 'c'
	model = os.path.abspath(args['model_path'] + '.ll-' + ext + '.dynmt')
	command = 'python ' + dynmt + ' --dynet-autobatch 0 {0}.corpus.ll {0}.corpus.{3} {1}.corpus.ll {1}.corpus.{3} ' \
								  '{2}.corpus.ll {2}.corpus.{3} {4} {17}.ll {17}.{3} --epochs={5} --batch-size={6} --eval-after={7} ' \
								  '--max-len={8} --max-pred={9} --max-patience={10} --beam-size={11} --plot ' \
								  '--lstm-layers={12} --models-to-save={13} {14} {15} {16}' \
		.format(train, validation, test, ext, model, args.epochs if args.epochs else config.getint('DyNmt', 'epochs'),
				config.getint('DyNmt', 'batch_size'), config.getint('DyNmt', 'eval_after'),
				config.getint('DyNmt', 'max_len'), config.getint('DyNmt', 'max_pred'),
				config.getint('DyNmt', 'max_patience'), 1 if args['train'] else args['num_translations'],
				config.getint('DyNmt', 'lstm_layers'), config.getint('DyNmt', 'models_to_save'),
				'--eval' if args['translate'] else '--override', ('--seed=%d' % args['seed']) if args['seed'] else '',
				'&> /dev/null' if args['silent'] else '', vocabs)
	command = command.strip()
	if args['train']:
		os.system(command)
	if args['translate']:
		import subprocess
		import re
		with open(test + '.corpus.' + str(args['num_translations']) + '.out', 'w') as f:
			translations = False
			current = None
			for line in subprocess.Popen(command.split(' '), stdout=subprocess.PIPE).stdout:
				print line,
				line = line.strip()
				if not translations:
					if line == 'predicting...':
						translations = True
				else:
					if re.match('^[0-9]+/[0-9]+$', line):
						current = line[:line.find('/')]
					if re.match('^[0-9]+\-best\: ', line):
						f.write(current + ' ||| ' + line[line.find(':') + 1:].strip() + ' ||| \n')
	if args['cleanup']:
		import glob
		files = filter(os.path.isfile, glob.glob(model + '*[0-9].*txt'))
		for f in files:
			os.remove(f)
		files = filter(os.path.isfile, glob.glob(model + '*[0-9].*png'))
		for f in files:
			os.remove(f)


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Train and test translation model")
	parser.add_argument('training_dataset', type=str, help="dataset for training")
	parser.add_argument('validation_dataset', type=str, help="dataset for validation")
	parser.add_argument('test_dataset', type=str, help="dataset for evaluation")
	parser.add_argument('vocabs', type=str, help="vocabularies for datasets")
	parser.add_argument('-m', '--model_path', type=str, default='model',
						help="name of trained model (default: \'%(default)s\')")
	parser.add_argument('-po', '--post-order', help="use post order c code (instead of regular c code)", action='count')
	parser.add_argument('--train', help="train a new model", action='count')
	parser.add_argument('--translate', help="translate using an existing model", action='count')
	parser.add_argument('-n', '--num_translations', type=int, default=5,
						help="number of translations for each input (default: %(default)s)")
	parser.add_argument('-c', '--config', type=str, default='configs/dynmt.config',
						help="configuration file (default: \'%(default)s\')")
	parser.add_argument('--cleanup', help="remove all intermediate files after training", action='count')
	parser.add_argument('--silent', help="hide all output", action='count')
	parser.add_argument('-s', '--seed', type=int, help="random seed")
	parser.add_argument('-e', '--epochs', type=int, help="number of epochs to train")
	args = parser.parse_args()

	if (args.train and args.translate) or not (args.train or args.translate):
		parser.error('You should choose either --train or --translate (exactly one, not both)')

	main(vars(args))