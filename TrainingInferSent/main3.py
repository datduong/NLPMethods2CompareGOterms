
''' 
added weight 
'''

import util, data, helper, train2, torch, os, numpy
from torch import optim
from classifier import SentenceClassifier

args = util.get_args()
# if output directory doesn't exist, create it
if not os.path.exists(args.save_path):
    os.makedirs(args.save_path)

# set the random seed manually for reproducibility.
numpy.random.seed(args.seed)
torch.manual_seed(args.seed)
if torch.cuda.is_available():
    if not args.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")
    else:
        torch.cuda.manual_seed(args.seed)

###############################################################################
# Load data
###############################################################################

dictionary = data.Dictionary()
train_corpus = data.Corpus(dictionary)
dev_corpus = data.Corpus(dictionary)
test_corpus = data.Corpus(dictionary)

train_corpus.parse(args.data, 'sent.train', args.tokenize, args.max_example) # @args.data folder where raining data is kept. 
print('train set size = ', len(train_corpus.data))
dev_corpus.parse(args.data, 'sent.dev', args.tokenize)
print('development set size = ', len(dev_corpus.data))
test_corpus.parse(args.data, 'sent.test', args.tokenize)
print('test set size = ', len(test_corpus.data))

print('vocabulary size = ', len(dictionary))

# save the dictionary object to use during testing
helper.save_object(dictionary, args.save_path + 'gene_dictionary.p')

embeddings_index = helper.load_word_embeddings(args.word_vectors_directory, args.word_vectors_file, dictionary.word2idx)
# helper.save_word_embeddings(args.word_vectors_directory, 'glove.840B.300d.gene.txt', embeddings_index) ## why do we need to save the word vectors ? 
# embeddings_index = helper.load_word_embeddings(args.word_vectors_directory, 'glove.840B.300d.gene.txt',
#                                                dictionary.word2idx)

print('number of OOV words = ', len(dictionary) - len(embeddings_index))

# ###############################################################################
# # Build the model
# ###############################################################################

model = SentenceClassifier(dictionary, embeddings_index, args, select_method='max')
optim_fn, optim_params = helper.get_optimizer(args.optimizer)
optimizer = optim_fn(filter(lambda p: p.requires_grad, model.parameters()), **optim_params)
best_acc = 0

# for training on multiple GPUs. use CUDA_VISIBLE_DEVICES=0,1 to specify which GPUs to use
if 'CUDA_VISIBLE_DEVICES' in os.environ:
    cuda_visible_devices = [int(x) for x in os.environ['CUDA_VISIBLE_DEVICES'].split(',')]
    if len(cuda_visible_devices) > 1:
        model = torch.nn.DataParallel(model, device_ids=cuda_visible_devices)
if args.cuda:
    model = model.cuda()

if args.resume:
    if os.path.isfile(args.resume):
        print("=> loading checkpoint '{}'".format(args.resume))
        checkpoint = torch.load(args.resume)
        args.start_epoch = checkpoint['epoch']
        best_acc = checkpoint['best_acc']
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        print("=> loaded checkpoint '{}' (epoch {})"
              .format(args.resume, checkpoint['epoch']))
    else:
        print("=> no checkpoint found at '{}'".format(args.resume))

# ###############################################################################
# # Train the model
# ###############################################################################

train = train2.Train(model, optimizer, dictionary, embeddings_index, args, best_acc)
train.train_epochs(train_corpus, dev_corpus, args.start_epoch, args.epochs)
