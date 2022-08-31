import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertTokenizer, BertModel

from src.table_encoder.gat import GATEncoder


class ClassificationModel(nn.Module):
    def __init__(self, num_classes, bert_dir='bert-base-uncased', do_lower_case=True, bert_size=768, gnn_output_size=300):
        super().__init__()
        self.tokenizer = BertTokenizer.from_pretrained(bert_dir, do_lower_case=do_lower_case)
        self.bert = BertModel.from_pretrained(bert_dir)

        self.gnn = GATEncoder(input_dim=300, output_dim=gnn_output_size, hidden_dim=300, layer_num=4,
                              activation=nn.LeakyReLU(0.2))

        self.project_table = nn.Sequential(
            nn.Linear(gnn_output_size, 300),
            nn.LayerNorm(300)
        )

        self.classifier = nn.Sequential(
            nn.Dropout(0.1),
            nn.Linear(300, 320),
            nn.LeakyReLU(0.2),
            nn.Linear(320, num_classes),
            nn.LogSoftmax(-1)
        )

    def forward(self, table, query, dgl_g, t_feat, q_feat):
        """table classification"""

        rep = self.transform(dgl_g, t_feat, q_feat)

        score = self.classifier(rep)

        return score

    def transform(self, dgl_graph, table_embs, query_emb):
        """table transform module"""
        creps = self.gnn(dgl_graph, table_embs)

        hidden = self.project_table(creps)
        
        hidden = torch.max(hidden, 0)[0]

        return hidden
