# importing dataset
from mil.data.datasets import musk1
# importing bag_representation
from mil.bag_representation import MILESMapping
# importing validation strategy
from mil.validators import LeaveOneOut
# importing final model, which in this case is the SVC classifier from sklearn
from mil.models import SVC
# importing mil models
from mil.models import APR, AttentionDeepPoolingMil, MILES
# importing sklearn models
from mil.models import RandomForestClassifier, SVC

# importing trainer
from mil.trainer import Trainer
# importing preprocessing
from mil.preprocessing import StandarizerBagsList
# importing metrics, which in this case are from tf keras metrics
from mil.metrics import Precision
from mil.metrics import Recall

# loading dataset
(bags_train, y_train), (bags_test, y_test) = musk1.load()

# instantiate trainer
trainer = Trainer()

# preparing trainer
metrics = ['acc', Precision, Recall]
model = RandomForestClassifier(kernel='linear', C=1, class_weight='balanced')
#model = APR()

pipeline = [('scale', StandarizerBagsList()), ('disc_mapping', MILESMapping())]
trainer.prepare(model, preprocess_pipeline=pipeline ,metrics=metrics)

# fitting trainer
valid = LeaveOneOut()
#history = trainer.fit(bags_train, y_train, sample_weights='balanced', validation_strategy=valid, verbose=1)
history = trainer.fit(bags_train, y_train, sample_weights='balanced', validation_strategy=valid, verbose=1)
# printing validation results for each fold
print(history['metrics_val'])

# predicting metrics for the test set
trainer.predict_metrics(bags_test, y_test)
trainer.get_positive_instances()



