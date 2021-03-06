import numpy as np
from sklearn import pipeline, feature_extraction, svm, metrics
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import KFold
from traditional_methods import get_data
import time
import numpy as np
class Traditional_method:
    def __init__(self, model, model_name="unknown model"):
        '''
        Build tradition method class
        :param file: csv file
        :param model_name: string
        :param model: sckit learn model
        '''
        self.model = pipeline.Pipeline([
            ('counts', feature_extraction.text.CountVectorizer(
                min_df=5, stop_words="english",analyzer="word", ngram_range=(1,2)
            )
             ),
            ('tfidf', feature_extraction.text.TfidfTransformer()),
            (model_name, model),
        ])
        # self.data = data
        self.model_name = model_name

    def k_fold(self, data_type):
        print(data_type + " data")

        kfold = KFold(5, True, 1)
        # enumerate splits
        X = np.array(data["tweet"])
        y = np.array(data["class"])
        for train_index, test_index in kfold.split(X):
            X_train = X[train_index]
            y_train = y[train_index]

            X_test = X[test_index]
            y_test = y[test_index]
            self.model.fit(X_train, y_train)
            # fit_time = time.time()

            y_pred = self.model.predict(X_test)

            print('Accuracy of ' + self.model_name + '= {}'.format(
                np.mean(y_pred == y_test)))


            print(metrics.classification_report(
                y_test, y_pred, target_names=["hate_speech", "offensive_language", "neither"]))
    def classification_report(self, data, data_type="unbalanced"):
        # data= self.data
        X, y = data["tweet"], data["class"]
        clf = self.model
        scores = cross_val_score(clf, X, y, cv=5)
        # print("cross validation score", scores)
        X_train, X_test, y_train, y_test = train_test_split(data['tweet'], data['class'], random_state=0)
        start_time = time.time()
        self.model.fit(X_train, y_train)
        fit_time = time.time()

        y_pred = self.model.predict(X_test)

        print(self.model_name + " with " + data_type)
        print(metrics.classification_report(
                y_test, y_pred, target_names=["hate_speech", "offensive_language", "neither"]))

        print("time comsume to fit model", fit_time - start_time)
        print()
        print('Accuracy of '+ self.model_name + 'on test sets= {}'.format(
            np.mean(y_pred == y_test)))
        print()
        X_pred = self.model.predict(X_train)
        print("Accuracy on training set", np.mean(y_train == X_pred))
        print(0)
        print("cross validation score", scores)
        print()


        # print("time consume to predict results", time.time() - fit_time)
        # print("upsampling")
        #
        # X_train, X_test, y_train, y_test = train_test_split(data1['tweet'], data1['class'], random_state=0)
        # self.model.fit(X_train, y_train)
        # y_pred = self.model.predict(X_test)
        #
        # print('Accuracy of '+ self.model_name + '= {}'.format(
        #     np.mean(y_pred == y_test)))
        #
        # print(metrics.classification_report(
        #     y_test, y_pred, target_names=["hate_speech", "offensive_language", "neither"]))
        #
        # print("downsampling")
        # X_train, X_test, y_train, y_test = train_test_split(data2['tweet'], data2['class'], random_state=0)
        # self.model.fit(X_train, y_train)
        # y_pred = self.model.predict(X_test)
        #
        # # print('Accuracy of SVM= {}'.format(
        # #     np.mean(y_pred == y_test)))
        # print('Accuracy of ' + self.model_name + '= {}'.format(
        #     np.mean(y_pred == y_test)))
        # print(metrics.classification_report(
        #     y_test, y_pred, target_names=["hate_speech", "offensive_language", "neither"]))
if __name__ == '__main__':
    # data = clean_text(df)
    # data1 = upsampling(clean_text((df)))
    # data2 = downsampling(clean_text(df))
    data = get_data.read_file("labeled_data.csv")

    svm = Traditional_method( svm.LinearSVC(), "LinearSVC")
    svm.classification_report(get_data.upsampling(data), "upsampling data")

