import torch
import torch.nn as nn
from quant.layers.normalization import RMSNorm
from quant.layers.swiglu_ffn import SwiGLUFFN


class STNetV1(nn.Module):

    def __init__(self, in_features, hidden_features, out_features, **kwargs):
        super().__init__()
        n_layers = kwargs.get("n_layers", 1)
        bias = kwargs.get("bias", True)
        drop = kwargs.get("drop", 0.)

        self.enable_skip = kwargs.get("enable_skip", False)

        self.stem = nn.Sequential(
            nn.Linear(in_features, hidden_features, bias=bias),
            nn.SiLU(),
        )
        self.layers = nn.ModuleList()
        for _ in range(n_layers):
            self.layers.append(nn.Sequential(
                nn.LayerNorm(hidden_features),
                nn.Linear(hidden_features, hidden_features, bias=bias),
                nn.SiLU(),
                nn.Dropout(drop) if drop > 0. else nn.Identity(),
            ))
        self.norm = nn.LayerNorm(hidden_features)
        self.head = nn.Linear(hidden_features, out_features, bias=bias)
        self.class_name = self.__class__.__name__

    def forward(self, x):
        x = self.stem(x)
        for layer in self.layers:
            if self.enable_skip:
                x = x + layer(x)
            else:
                x = layer(x)
        x = self.head(self.norm(x))
        return x


class STNetV2(nn.Module):

    def __init__(self, in_features, hidden_features, out_features, **kwargs):
        super().__init__()
        n_layers = kwargs.get("n_layers", 1)
        bias = kwargs.get("bias", True)
        drop = kwargs.get("drop", 0.)

        self.enable_skip = kwargs.get("enable_skip", False)

        self.stem = nn.Sequential(
            nn.Linear(in_features, hidden_features, bias=bias),
            nn.SiLU(),
        )
        self.layers = nn.ModuleList()
        for _ in range(n_layers):
            self.layers.append(nn.Sequential(
                RMSNorm(hidden_features),
                SwiGLUFFN(hidden_features, bias=bias),
                nn.SiLU(),
                nn.Dropout(drop) if drop > 0. else nn.Identity(),
            ))
        self.norm = RMSNorm(hidden_features)
        self.head = nn.Linear(hidden_features, out_features, bias=bias)
        self.class_name = self.__class__.__name__

    def forward(self, x):
        x = self.stem(x)
        for layer in self.layers:
            if self.enable_skip:
                x = x + layer(x)
            else:
                x = layer(x)
        x = self.head(self.norm(x))
        return x


class STNetV3(nn.Module):

    def __init__(self, in_features, hidden_features, out_features, **kwargs):
        super().__init__()
        num_embeddings = kwargs.get("num_embeddings", 1000)
        embedding_dim = kwargs.get("embedding_dim ", 100)

        in_features = embedding_dim * 2 + in_features

        n_layers = kwargs.get("n_layers", 1)
        bias = kwargs.get("bias", True)
        drop = kwargs.get("drop", 0.)

        self.enable_skip = kwargs.get("enable_skip", False)
        self.embedding = nn.Embedding(num_embeddings, embedding_dim)

        self.stem = nn.Sequential(
            nn.Linear(in_features, hidden_features, bias=bias),
            nn.SiLU(),
        )
        self.layers = nn.ModuleList()
        for _ in range(n_layers):
            self.layers.append(nn.Sequential(
                RMSNorm(hidden_features),
                SwiGLUFFN(hidden_features, bias=bias),
                nn.SiLU(),
                nn.Dropout(drop) if drop > 0. else nn.Identity(),
            ))
        self.norm = RMSNorm(hidden_features)
        self.head = nn.Linear(hidden_features, out_features, bias=bias)
        self.class_name = self.__class__.__name__

    def forward(self, x):
        x_home, x_away, x_features = x
        x_home, x_away = self.embedding(x_home), self.embedding(x_away)
        x = torch.cat([x_home, x_away, x_features], dim=1)

        x = self.stem(x)
        for layer in self.layers:
            if self.enable_skip:
                x = x + layer(x)
            else:
                x = layer(x)
        x = self.head(self.norm(x))
        return x


class STNetV4(nn.Module):

    def __init__(self, in_features, hidden_features, out_features, **kwargs):
        super().__init__()
        season_embeddings = kwargs.get("season_embeddings", 4096)
        season_embedding_dim = kwargs.get("season_embedding_dim", 100)

        team_embeddings = kwargs.get("team_embeddings", 4096)
        team_embedding_dim = kwargs.get("team_embedding_dim", 100)

        in_features = season_embedding_dim + team_embedding_dim * 2 + in_features

        n_layers = kwargs.get("n_layers", 1)
        bias = kwargs.get("bias", True)
        drop = kwargs.get("drop", 0.)

        self.enable_skip = kwargs.get("enable_skip", False)
        self.season_embedding = nn.Embedding(season_embeddings, season_embedding_dim)
        self.team_embedding = nn.Embedding(team_embeddings, team_embedding_dim)

        self.stem = nn.Sequential(
            nn.Linear(in_features, hidden_features, bias=bias),
            nn.SiLU(),
        )
        self.layers = nn.ModuleList()
        for _ in range(n_layers):
            self.layers.append(nn.Sequential(
                RMSNorm(hidden_features),
                SwiGLUFFN(hidden_features, bias=bias),
                nn.SiLU(),
                nn.Dropout(drop) if drop > 0. else nn.Identity(),
            ))
        self.norm = RMSNorm(hidden_features)
        self.head = nn.Linear(hidden_features, out_features, bias=bias)
        self.class_name = self.__class__.__name__

    def forward(self, x):
        x_season, x_home, x_away, x_features = x
        x_season = self.season_embedding(x_season)
        x_home, x_away = self.team_embedding(x_home), self.team_embedding(x_away)
        x = torch.cat([x_season, x_home, x_away, x_features], dim=1)

        x = self.stem(x)
        for layer in self.layers:
            if self.enable_skip:
                x = x + layer(x)
            else:
                x = layer(x)
        x = self.head(self.norm(x))
        return x
