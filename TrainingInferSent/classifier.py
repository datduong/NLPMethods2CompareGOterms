###############################################################################
# Author: Wasi Ahmad
# Project: Quora Duplicate Question Classification
# Date Created: 7/25/2017
#
# File Description: This script contains code related to quora duplicate
# question classifier.
###############################################################################

import torch
import torch.nn as nn
from collections import OrderedDict
from nn_layer import EmbeddingLayer, Encoder


class SentenceClassifier(nn.Module):
	"""Class that classifies question pair as duplicate or not."""

	def __init__(self, dictionary, embeddings_index, args, select_method='max'):
		""""Constructor of the class."""
		super(SentenceClassifier, self).__init__()
		self.config = args
		self.feature_select_method = select_method
		self.num_directions = 2 if args.bidirection else 1
		print ("finish sending in arg")
		self.embedding = EmbeddingLayer(len(dictionary), self.config)
		print ("finish embed. layer")
		self.embedding.init_embedding_weights(dictionary, embeddings_index, self.config.emsize)
		self.encoder = Encoder(self.config.emsize, self.config.nhid, self.config.bidirection, self.config)
		print ("finish encoder")

		if args.nonlinear_fc:
			self.ffnn = nn.Sequential(OrderedDict([
				('dropout1', nn.Dropout(self.config.dropout_fc)),
				('dense1', nn.Linear(self.config.nhid * self.num_directions * 4, self.config.fc_dim)),
				('tanh', nn.Tanh()),
				('dropout2', nn.Dropout(self.config.dropout_fc)),
				('dense2', nn.Linear(self.config.fc_dim, self.config.fc_dim)),
				('tanh', nn.Tanh()),
				('dropout3', nn.Dropout(self.config.dropout_fc)),
				('dense3', nn.Linear(self.config.fc_dim, 2))
			]))
		else:
			self.ffnn = nn.Sequential(OrderedDict([
				('dropout1', nn.Dropout(self.config.dropout_fc)),
				('dense1', nn.Linear(self.config.nhid * self.num_directions * 4, self.config.fc_dim)),
				('dropout2', nn.Dropout(self.config.dropout_fc)),
				('dense2', nn.Linear(self.config.fc_dim, self.config.fc_dim)),
				('dropout3', nn.Dropout(self.config.dropout_fc)),
				('dense3', nn.Linear(self.config.fc_dim, 2))
			]))

	def forward(self, batch_sentence1, sent_len1, batch_sentence2, sent_len2):
		""""Defines the forward computation of the question classifier."""
		# print ('embedding sent num 1')
		# print (batch_sentence1)
		embedded1 = self.embedding(batch_sentence1)
		# print (embedded1)
		
		# print ('embedding sent num 2')
		# print (batch_sentence2)
		embedded2 = self.embedding(batch_sentence2)
		# print (embedded2)
		
		# For the first sentences in batch
		output1 = self.encoder(embedded1, sent_len1)
		# For the second sentences in batch
		output2 = self.encoder(embedded2, sent_len2)

		if self.feature_select_method == 'max':
			encoded_questions1 = torch.max(output1, 1)[0].squeeze()
			encoded_questions2 = torch.max(output2, 1)[0].squeeze()
		elif self.feature_select_method == 'average':
			encoded_questions1 = torch.sum(output1, 1).squeeze() / batch_sentence1.size(1)
			encoded_questions2 = torch.sum(output2, 1).squeeze() / batch_sentence2.size(1)
		elif self.feature_select_method == 'last':
			encoded_questions1 = output1[:, -1, :]
			encoded_questions2 = output2[:, -1, :]

		assert encoded_questions1.size(0) == encoded_questions2.size(0)

		if encoded_questions1.data.dim() == 1: 
			encoded_questions1 = encoded_questions1.unsqueeze(0)
		if encoded_questions2.data.dim() == 1:
			encoded_questions2 = encoded_questions2.unsqueeze(0)
		
		# compute angle between question representation
		angle = torch.mul(encoded_questions1, encoded_questions2)
		# compute distance between question representation
		distance = torch.abs(encoded_questions1 - encoded_questions2)
		# combined_representation = batch_size x (hidden_size * num_directions * 4)
		combined_representation = torch.cat((encoded_questions1, encoded_questions2, angle, distance), 1)

		return self.ffnn(combined_representation)