###############################################################################
# Author: Wasi Ahmad
# Project: Quora Duplicate Question Classification
# Date Created: 7/25/2017
#
# File Description: This is the main script from where all experimental
# execution begins.
###############################################################################

from argparse import ArgumentParser


def get_args():
	parser = ArgumentParser(description='quora_duplicate_question_detection')
	parser.add_argument('--data', type=str, default='../data/',
						help='location of the training data')
	parser.add_argument('--max_example', type=int, default=-1,
						help='number of training examples (-1 = all examples)')
	parser.add_argument('--tokenize', action='store_true',
						help='tokenize instances using word_tokenize')
	parser.add_argument('--model', type=str, default='LSTM',
						help='type of recurrent net (RNN_Tanh, RNN_RELU, LSTM, GRU)')
	parser.add_argument("--optimizer", type=str, default="sgd,lr=0.1",
						help="adam or sgd,lr=0.1")
	parser.add_argument("--lrshrink", type=float, default=5,
						help="shrink factor for sgd")
	parser.add_argument("--minlr", type=float, default=1e-5,
						help="minimum lr")
	parser.add_argument('--bidirection', action='store_true',
						help='use bidirectional recurrent unit')
	parser.add_argument('--emsize', type=int, default=300,
						help='size of word embeddings')
	parser.add_argument('--emtraining', action='store_true',
						help='train embedding layer')
	parser.add_argument('--nhid', type=int, default=2048,
						help='number of hidden units per layer')
	parser.add_argument('--nlayers', type=int, default=1,
						help='number of layers')
	parser.add_argument('--lr_decay', type=float, default=.99,
						help='decay ratio for learning rate')
	parser.add_argument("--nonlinear_fc", action='store_true',
						help="use nonlinear fully connected layers")
	parser.add_argument("--fc_dim", type=int, default=512,
						help="nhid of fc layers")
	parser.add_argument('--dropout_fc', type=float, default=0,
						help='dropout applied to fully connected layers (0 = no dropout)')
	parser.add_argument('--dropout', type=float, default=0.2,
						help='dropout applied to layers (0 = no dropout)')
	parser.add_argument('--clip', type=float, default=5.0,
						help='gradient clipping')
	parser.add_argument('--epochs', type=int, default=10,
						help='upper limit of epoch')
	parser.add_argument('--start_epoch', default=0, type=int, metavar='N',
						help='manual epoch number (useful on restarts)')
	parser.add_argument('--batch_size', type=int, default=128, metavar='N',
						help='batch size')
	parser.add_argument('--seed', type=int, default=1111,
						help='random seed for reproducibility')
	parser.add_argument('--cuda', action='store_true',
						help='use CUDA for computation')
	parser.add_argument('--print_every', type=int, default=50, metavar='N',
						help='training report interval')
	parser.add_argument('--plot_every', type=int, default=20,
						help='plotting interval')
	parser.add_argument('--resume', default='', type=str, metavar='PATH',
						help='resume from last checkpoint (default: none)')
	parser.add_argument('--save_path', type=str, default='../gene_output/',
						help='path to save the final model')
	parser.add_argument('--word_vectors_file', type=str, default='w2vModel1Gram11Nov2017NoHeader.txt',
						help='GloVe word embedding version')
	parser.add_argument('--word_vectors_directory', type=str, default='/u/flashscratch/d/datduong/w2vModel1Gram11Nov2017/',
						help='Path of GloVe word embeddings')
	parser.add_argument('--scoreOutput',type=str,default="none",help='where to save score file for 2 sets of GO')
	parser.add_argument('--pairStartIndex',type=int,default=0,help='what is the first pair of GO terms indexing')
	parser.add_argument('--pairEndIndex',type=int,default=0,help='what is the last pair of GO terms indexing')
	parser.add_argument('--nameExpression',type=str,default='none',help='random/real pairing')
	parser.add_argument('--pairs2test',type=str,default='none',help='file contains the gene pairs')
	parser.add_argument('--geneAnnotationFile',type=str,default='none',help='go term annotation for the genes (BP,CC,MF)')
	parser.add_argument('--goAnnotationFile',type=str,default='none',help='gene ontology description (BP,CC,MF)')
	args = parser.parse_args()
	return args
