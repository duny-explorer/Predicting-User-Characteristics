import torch
import pytorch_lightning as pl
from predprocessing import *
import os
import pandas as pd
import pickle
import datetime
from ptls.nn import TrxEncoder, RnnSeqEncoder
from ptls.frames.supervised import SequenceToTarget
from ptls.data_load.datasets import inference_data_loader


DATA_PATH=''
test = pd.read_csv(DATA_PATH)
target = pd.read_csv('train_targets.csv')
info = pd.read_csv('video_info_v2.csv')

with open('preprocessor.p', 'rb') as f:
    preprocessor = pickle.load(f)


agg_features, coles_data, target = feauture_engineering(info, test, target)
test['event_timestamp'] = test['event_timestamp'].apply(lambda x: datetime.strptime(x.replace('+00:00', ''), '%Y-%m-%d %H:%M:%S').timestamp())
dataset = preprocessor.transform(coles_data)
dataset = sorted(dataset, key=lambda x: x['viewer_uid'])


trx_encoder_params = dict( # инициализация энкодера фичей айтемов
    embeddings_noise=0.003,
    numeric_values={'how_many_times_watche': 'identity',
                    'duration': 'identity',
                    'latitude': 'identity',
                    'longitude': 'identity',
                    'time_zone': 'identity'},
    embeddings={
        'ua_device_type': {'in': 80, 'out': 16},
        'ua_client_type': {'in': 80, 'out': 16},
        'category': {'in': 80, 'out': 16},
        'duration': {'in': 80, 'out': 16},
        'latitude': {'in': 80, 'out': 16},
        'longitude': {'in': 80, 'out': 16},
        'event_timestamp': {'in': 80, 'out': 16},
        'time of day': {'in': 80, 'out': 16},
        'Day Type': {'in': 80, 'out': 16}
    },
)

seq_encoder = RnnSeqEncoder( # инициализация энкодера последовательности
    trx_encoder=TrxEncoder(**trx_encoder_params),
    hidden_size=256,
    type='gru',
)

seq_encoder.load_state_dict(torch.load('coles-emb_1.pt'))

model = SequenceToTarget(seq_encoder)
model.eval()

trainer = pl.Trainer(gpus=1 if torch.cuda.is_available() else 0)

dl = inference_data_loader(dataset, num_workers=0, batch_size=256)
embeds = torch.vstack(trainer.predict(model, tdl))

result = pd.concat([pd.DataFrame([i['viewer_uid'] for i in dataset], columns=['viewer_uid']), pd.DataFrame(embeds)], axis=1)
result = result.merge(agg_features, on='viewer_uid')

model_sex = joblib.load('model_age.pkl')
model_age = joblib.load('model_sex.pkl')

##TODO
