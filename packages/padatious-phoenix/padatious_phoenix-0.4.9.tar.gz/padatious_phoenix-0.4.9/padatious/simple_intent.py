# Copyright 2017 Mycroft AI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from padatious.id_manager import IdManager
from padatious.util import resolve_conflicts, StrEnum

class Ids(StrEnum):
    unknown_tokens = ':0'
    w_1 = ':1'
    w_2 = ':2'
    w_3 = ':3'
    w_4 = ':4'

class SimpleIntent(object):
    LENIENCE = 0.6

    def __init__(self, name=''):
        self.name = name
        self.ids = IdManager(Ids)
        self.model = make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(10,), activation='logistic'))

    def match(self, sent):
        vector = self.vectorize(sent)
        return max(0, self.model.predict([vector])[0])

    def vectorize(self, sent):
        vector = [0] * len(self.ids)
        unknown = 0
        for token in sent:
            if token in self.ids:
                idx = self.ids[token]
                vector[idx] = 1.0
            else:
                unknown += 1
        total_tokens = len(sent)
        if total_tokens > 0:
            vector[self.ids.unknown_tokens] = unknown / float(total_tokens)
            vector[self.ids.w_1] = total_tokens / 1
            vector[self.ids.w_2] = total_tokens / 2.
            vector[self.ids.w_3] = total_tokens / 3.
            vector[self.ids.w_4] = total_tokens / 4.
        return vector

    def train(self, train_data):
        inputs = []
        outputs = []

        def add(vec, out):
            inputs.append(vec)
            outputs.append(out)

        def pollute(sent, p):
            sent = sent[:]
            for _ in range(int((len(sent) + 2) / 3)):
                sent.insert(p, ':null:')
            add(self.vectorize(sent), self.LENIENCE)

        def weight(sent):
            total_weight = sum(len(word) ** 3.0 for word in sent)
            for word in sent:
                weight = 0 if word.startswith('{') else len(word) ** 3.0
                add(self.vectorize([word]), weight / total_weight)

        for sent in train_data.my_sents(self.name):
            add(self.vectorize(sent), 1.0)
            weight(sent)

            if not any(word[0] == ':' and word != ':' for word in sent):
                pollute(sent, 0)
                pollute(sent, len(sent))

        for sent in train_data.other_sents(self.name):
            add(self.vectorize(sent), 0.0)
        add(self.vectorize([':null:']), 0.0)
        add(self.vectorize([]), 0.0)

        for sent in train_data.my_sents(self.name):
            without_entities = [':null:' if token.startswith('{') else token for token in sent]
            if without_entities != sent:
                add(self.vectorize(without_entities), 0.0)

        inputs, outputs = resolve_conflicts(inputs, outputs)

        self.model.fit(inputs, outputs)

    def save(self, prefix):
        # Implement save method if needed
        pass

    @classmethod
    def from_file(cls, name, prefix):
        # Implement loading from file if needed
        pass

