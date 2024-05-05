import torch
from packaging import version

if version.parse(torch.__version__) >= version.parse('2.0.0'):
    from einops._torch_specific import allow_ops_in_compiled_graph
    allow_ops_in_compiled_graph()

from audiolm_superfeel.audiolm_superfeel import AudioLM
from audiolm_superfeel.soundstream import SoundStream, AudioLMSoundStream, MusicLMSoundStream
from audiolm_superfeel.encodec import EncodecWrapper

from audiolm_superfeel.audiolm_superfeel import SemanticTransformer, CoarseTransformer, FineTransformer
from audiolm_superfeel.audiolm_superfeel import FineTransformerWrapper, CoarseTransformerWrapper, SemanticTransformerWrapper

from audiolm_superfeel.vq_wav2vec import FairseqVQWav2Vec
from audiolm_superfeel.hubert_kmeans import HubertWithKmeans

from audiolm_superfeel.trainer import SoundStreamTrainer, SemanticTransformerTrainer, FineTransformerTrainer, CoarseTransformerTrainer

from audiolm_superfeel.audiolm_superfeel import get_embeds
