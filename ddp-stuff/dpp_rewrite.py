import pickle
import torch
import torch.optim as optim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dynamic_disease_network_ddp import data_loader
from dynamic_disease_network_ddp import models
from torch import nn
import torch.nn.functional as F

def max_likelihood_one_step(likelihood, opt):
    loss = -1.0 * likelihood
    loss.backward()
    opt.step()
    opt.zero_grad()


def cross_ent_one_step(ent_loss, opt):
    ent_loss.backward()
    opt.step()
    opt.zero_grad()


class DDP(GraphHawkes):
    """
    DDP model
    """ 
    def __init__(self, n_event_type, n_context_dim, first_occurrence_only=False, mu_vec_np=None, alpha_mat_np=None,
                 lambda_mat_np=None, embedding_size=10, rnn_hidden_size=10, gap_mean=0, gap_scale=1):
        super().__init__(n_event_type, n_context_dim,first_occurrence_only, mu_vec_np, alpha_mat_np, lambda_mat_np)
        self.gap_mean = gap_mean
        self.gap_scale = gap_scale
        self.embeding = nn.Embedding(n_event_type, embedding_size)
        # + 1 for time gap
        self.rnn = nn.LSTM(embedding_size + 1, rnn_hidden_size)
        self.rnn_lin = nn.Linear(rnn_hidden_size, 1)
        self.graph_weights_to_current = None
        self.graph_weights_seq = None

    def _update_graph_weights(self):
        seq_type_event = self.seq_type_event
        seq_mask_to_current = self.seq_mask_to_current
        seq_time_to_end = self.seq_time_to_end

        # n_event_type: T * batch_size
        # event_embedding: T * batch_size * K
        event_embedding = self.embeding(seq_type_event)
        # time_gap: T * batch_size
        # (T - 1) * batch_size
        time_diff = (seq_time_to_end[:-1, :] - seq_time_to_end[1:, :] - self.gap_mean) / self.gap_scale
        init_time_diff = time_diff.new_zeros((1, time_diff.shape[1]))
        time_diff_input = torch.cat((init_time_diff, time_diff))
        rnn_input = torch.cat((event_embedding, time_diff_input[:, :, None]), dim=2)

        # rnn_output: T * batch_size * rnn_hidden_size
        rnn_output, _ = self.rnn(rnn_input)
        # graph_weights: T * batch_size
        # activation function
        graph_weights = torch.sigmoid(self.rnn_lin(rnn_output)).reshape(rnn_output.shape[:2])
        self.graph_weights_seq = graph_weights
        self.graph_weights_to_current = graph_weights[None, :, :] * seq_mask_to_current