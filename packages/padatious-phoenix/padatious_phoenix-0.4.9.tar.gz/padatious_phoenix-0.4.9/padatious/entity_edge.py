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
from padatious.util import StrEnum, resolve_conflicts

class Ids(StrEnum):
    end = ':end'

class EntityEdge(object):
    def __init__(self,  direction, token, intent_name):
        self.ids = IdManager(Ids)
        self.intent_name = intent_name
        self.token = token
        self.dir = direction
        self.model = make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(3,), activation='logistic'))

    def get_end(self, sent):
        return len(sent) if self.dir > 0 else -1

    def vectorize(self, sent, pos):
        unknown = 0
        vector = [0] * len(self.ids)
        end_pos = self.get_end(sent)
        for i in range(pos + self.dir, end_pos, self.dir):
            if sent[i] in self.ids:
                idx = self.ids[sent[i]]
                vector[idx] = 1.0 / abs(i - pos)
            else:
                unknown += 1
        vector[self.ids.end] = 1.0 / abs(end_pos - pos)
        return vector

    def match(self, sent, pos):
        vector = self.vectorize(sent, pos)
        return self.model.predict([vector])[0]

    def train(self, train_data):
        inputs = []
        outputs = []

        def add(vec, out):
            inputs.append(vec)
            outputs.append(out)

        def pollute(sent, i, out_val):
            for j, check_token in enumerate(sent

