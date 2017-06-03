from builtins import range
from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.rnn_layers import *


class CaptioningRNN(object):
    """
    A CaptioningRNN produces captions from image features using a recurrent
    neural network.

    The RNN receives input vectors of size D, has a vocab size of V, works on
    sequences of length T, has an RNN hidden dimension of H, uses word vectors
    of dimension W, and operates on minibatches of size N.

    Note that we don't use any regularization for the CaptioningRNN.
    """

    def __init__(self, word_to_idx, input_dim=512, wordvec_dim=128,
                 hidden_dim=128, cell_type='rnn', dtype=np.float32):
        """
        Construct a new CaptioningRNN instance.

        Inputs:
        - word_to_idx: A dictionary giving the vocabulary. It contains V entries,
          and maps each string to a unique integer in the range [0, V).
        - input_dim: Dimension D of input image feature vectors.
        - wordvec_dim: Dimension W of word vectors.
        - hidden_dim: Dimension H for the hidden state of the RNN.
        - cell_type: What type of RNN to use; either 'rnn' or 'lstm'.
        - dtype: numpy datatype to use; use float32 for training and float64 for
          numeric gradient checking.
        """
        if cell_type not in {'rnn', 'lstm'}:
            raise ValueError('Invalid cell_type "%s"' % cell_type)

        self.cell_type = cell_type
        self.dtype = dtype
        self.word_to_idx = word_to_idx
        self.idx_to_word = {i: w for w, i in word_to_idx.items()}
        self.params = {}

        vocab_size = len(word_to_idx)

        self._null = word_to_idx['<NULL>']
        self._start = word_to_idx.get('<START>', None)
        self._end = word_to_idx.get('<END>', None)

        # Initialize word vectors
        self.params['W_embed'] = np.random.randn(vocab_size, wordvec_dim)
        self.params['W_embed'] /= 100

        # Initialize CNN -> hidden state projection parameters
        self.params['W_proj'] = np.random.randn(input_dim, hidden_dim)
        self.params['W_proj'] /= np.sqrt(input_dim)
        self.params['b_proj'] = np.zeros(hidden_dim)

        # Initialize parameters for the RNN
        dim_mul = {'lstm': 4, 'rnn': 1}[cell_type]
        self.params['Wx'] = np.random.randn(wordvec_dim, dim_mul * hidden_dim)
        self.params['Wx'] /= np.sqrt(wordvec_dim)
        self.params['Wh'] = np.random.randn(hidden_dim, dim_mul * hidden_dim)
        self.params['Wh'] /= np.sqrt(hidden_dim)
        self.params['b'] = np.zeros(dim_mul * hidden_dim)

        # Initialize output to vocab weights
        self.params['W_vocab'] = np.random.randn(hidden_dim, vocab_size)
        self.params['W_vocab'] /= np.sqrt(hidden_dim)
        self.params['b_vocab'] = np.zeros(vocab_size)

        # Cast parameters to correct dtype
        for k, v in self.params.items():
            self.params[k] = v.astype(self.dtype)


    def loss(self, features, captions):
        """
        Compute training-time loss for the RNN. We input image features and
        ground-truth captions for those images, and use an RNN (or LSTM) to compute
        loss and gradients on all parameters.

        Inputs:
        - features: Input image features, of shape (N, D)
        - captions: Ground-truth captions; an integer array of shape (N, T) where
          each element is in the range 0 <= y[i, t] < V

        Returns a tuple of:
        - loss: Scalar loss
        - grads: Dictionary of gradients parallel to self.params
        """
        # Cut captions into two pieces: captions_in has everything but the last word
        # and will be input to the RNN; captions_out has everything but the first
        # word and this is what we will expect the RNN to generate. These are offset
        # by one relative to each other because the RNN should produce word (t+1)
        # after receiving word t. The first element of captions_in will be the START
        # token, and the first element of captions_out will be the first word.
        captions_in = captions[:, :-1]
        captions_out = captions[:, 1:]

        # You'll need this
        mask = (captions_out != self._null)

        # Weight and bias for the affine transform from image features to initial
        # hidden state
        W_proj, b_proj = self.params['W_proj'], self.params['b_proj']

        # Word embedding matrix
        W_embed = self.params['W_embed']

        # Input-to-hidden, hidden-to-hidden, and biases for the RNN
        Wx, Wh, b = self.params['Wx'], self.params['Wh'], self.params['b']

        # Weight and bias for the hidden-to-vocab transformation.
        W_vocab, b_vocab = self.params['W_vocab'], self.params['b_vocab']

        loss, grads = 0.0, {}
        ############################################################################
        # TODO: Implement the forward and backward passes for the CaptioningRNN.   #
        # In the forward pass you will need to do the following:                   #
        # (1) Use an affine transformation to compute the initial hidden state     #
        #     from the image features. This should produce an array of shape (N, H)#
        # (2) Use a word embedding layer to transform the words in captions_in     #
        #     from indices to vectors, giving an array of shape (N, T, W).         #
        # (3) Use either a vanilla RNN or LSTM (depending on self.cell_type) to    #
        #     process the sequence of input word vectors and produce hidden state  #
        #     vectors for all timesteps, producing an array of shape (N, T, H).    #
        # (4) Use a (temporal) affine transformation to compute scores over the    #
        #     vocabulary at every timestep using the hidden states, giving an      #
        #     array of shape (N, T, V).                                            #
        # (5) Use (temporal) softmax to compute loss using captions_out, ignoring  #
        #     the points where the output word is <NULL> using the mask above.     #
        #                                                                          #
        # In the backward pass you will need to compute the gradient of the loss   #
        # with respect to all model parameters. Use the loss and grads variables   #
        # defined above to store loss and gradients; grads[k] should give the      #
        # gradients for self.params[k].                                            #
        ############################################################################
        pass
    
        h0 = np.dot(features, W_proj) + b_proj #h0 has dimensions (N, H)
#        print(h0.shape)
        
#        Inputs:
#        - x: Integer array of shape (N, T-1) giving indices of words. Each element idx
#          of x muxt be in the range 0 <= idx < V.
#        - W: Weight matrix of shape (V, W) giving word vectors for all words.
#    
#        Returns a tuple of:
#        - out: Array of shape (N, T, W) giving word vectors for all input words.
#        - cache: Values needed for the backward pass        
        
        out_wordembedding, cache_wordembedding = word_embedding_forward(captions_in, W_embed) # x has dimension (N,T,W)
#        print(out_wordembedding.shape)
        
#        Inputs:
#        - x: Input data for the entire timeseries, of shape (N, T, W).
#        - h0: Initial hidden state, of shape (N, H)
#        - Wx: Weight matrix for input-to-hidden connections, of shape (W, H)
#        - Wh: Weight matrix for hidden-to-hidden connections, of shape (H, H)
#        - b: Biases of shape (H,)

#        Returns a tuple of:
#        - h: Hidden states for the entire timeseries, of shape (N, T, H).
#        - cache: Values needed in the backward pass

        if(self.cell_type == "rnn"):
            h_rnn, cache_rnn = rnn_forward(out_wordembedding, h0, Wx, Wh, b)
        elif(self.cell_type == "lstm"):
            h_rnn, cache_rnn = lstm_forward(out_wordembedding, h0, Wx, Wh, b)
    
#        Inputs:
#        - x: Input data of shape (N, T, H)
#        - w: Weights of shape (H, V)
#        - b: Biases of shape (V,)

#        Returns a tuple of:
#        - out: Output data of shape (N, T, V)
#        - cache: Values needed for the backward pass
    
        out_temporalaffine, cache_temporalaffine = temporal_affine_forward(h_rnn, W_vocab, b_vocab)

#        Inputs:
#        - x: Input scores, of shape (N, T, V)
#        - y: Ground-truth indices, of shape (N, T-1) where each element is in the range
#             0 <= y[i, t] < V
#        - mask: Boolean array of shape (N, T) where mask[i, t] tells whether or not
#          the scores at x[i, t] should contribute to the loss.
#    
#        Returns a tuple of:
#        - loss: Scalar giving loss
#        - dx: Gradient of loss with respect to scores x.

        loss, dout_temporalaffine = temporal_softmax_loss(out_temporalaffine, captions_out, mask, verbose=False)


        dh_rnn, dW_vocab, db_vocab = temporal_affine_backward(dout_temporalaffine, cache_temporalaffine)
        
        if(self.cell_type == "rnn"):
            dout_wordembedding, dh0, dWx, dWh, db = rnn_backward(dh_rnn, cache_rnn)
        else:
            dout_wordembedding, dh0, dWx, dWh, db = lstm_backward(dh_rnn, cache_rnn)
            
        dW_embed = word_embedding_backward(dout_wordembedding, cache_wordembedding)



        grads['W_embed'] = dW_embed
        grads['W_proj'] = np.dot(features.T, dh0)
        grads['b_proj'] = sum(dh0)
        grads['Wx'] = dWx
        grads['Wh'] = dWh
        grads['b'] = db
        grads['W_vocab'] = dW_vocab
        grads['b_vocab'] = db_vocab
        
        
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


    def sample(self, features, max_length=30):
        """
        Run a test-time forward pass for the model, sampling captions for input
        feature vectors.

        At each timestep, we embed the current word, pass it and the previous hidden
        state to the RNN to get the next hidden state, use the hidden state to get
        scores for all vocab words, and choose the word with the highest score as
        the next word. The initial hidden state is computed by applying an affine
        transform to the input image features, and the initial word is the <START>
        token.

        For LSTMs you will also have to keep track of the cell state; in that case
        the initial cell state should be zero.

        Inputs:
        - features: Array of input image features of shape (N, D).
        - max_length: Maximum length T of generated captions.

        Returns:
        - captions: Array of shape (N, max_length) giving sampled captions,
          where each element is an integer in the range [0, V). The first element
          of captions should be the first sampled word, not the <START> token.
        """
        N = features.shape[0]
        captions = self._null * np.ones((N, max_length), dtype=np.int32)

        # Unpack parameters
        W_proj, b_proj = self.params['W_proj'], self.params['b_proj']
        W_embed = self.params['W_embed']
        Wx, Wh, b = self.params['Wx'], self.params['Wh'], self.params['b']
        W_vocab, b_vocab = self.params['W_vocab'], self.params['b_vocab']

        ###########################################################################
        # TODO: Implement test-time sampling for the model. You will need to      #
        # initialize the hidden state of the RNN by applying the learned affine   #
        # transform to the input image features. The first word that you feed to  #
        # the RNN should be the <START> token; its value is stored in the         #
        # variable self._start. At each timestep you will need to do to:          #
        # (1) Embed the previous word using the learned word embeddings           #
        # (2) Make an RNN step using the previous hidden state and the embedded   #
        #     current word to get the next hidden state.                          #
        # (3) Apply the learned affine transformation to the next hidden state to #
        #     get scores for all words in the vocabulary                          #
        # (4) Select the word with the highest score as the next word, writing it #
        #     to the appropriate slot in the captions variable                    #
        #                                                                         #
        # For simplicity, you do not need to stop generating after an <END> token #
        # is sampled, but you can if you want to.                                 #
        #                                                                         #
        # HINT: You will not be able to use the rnn_forward or lstm_forward       #
        # functions; you'll need to call rnn_step_forward or lstm_step_forward in #
        # a loop.                                                                 #
        ###########################################################################
        pass
        
        h0 = np.dot(features, W_proj) + b_proj
    
        prev_h = h0
        prev_c = np.zeros_like(prev_h)
        
        _, D = W_embed.shape
        
        prev_word = self._start * np.ones(N, dtype=np.int32)
        
        for t in range(max_length):
        
            #Inputs:
            #- x: Input data for this timestep, of shape (N, D).
            #- prev_h: Hidden state from previous timestep, of shape (N, H)
            #- Wx: Weight matrix for input-to-hidden connections, of shape (D, H)
            #- Wh: Weight matrix for hidden-to-hidden connections, of shape (H, H)
            #- b: Biases of shape (H,)
            #
            #Returns a tuple of:
            #- next_h: Next hidden state, of shape (N, H)
            #- cache: Tuple of values needed for the backward pass.

            x = np.zeros((N, D))
            for i in range(N):
                x[i] = W_embed[prev_word[i]]
            
            if(self.cell_type == "rnn"):
                next_h , _ = rnn_step_forward(x, prev_h, Wx, Wh, b)
            elif(self.cell_type == "lstm"):
                next_h, next_c, _ = lstm_step_forward(x, prev_h, prev_c, Wx, Wh, b)
                prev_c = next_c
                
            scores = np.dot(next_h, W_vocab) + b_vocab
        
            highest_score_idx = np.argmax(scores, axis=1)
            captions[:, t] = highest_score_idx
        
            prev_h = next_h
            prev_word = captions[:, t]
            
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################
        return captions
