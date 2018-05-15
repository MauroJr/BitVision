# alichtman

import os
from pprint import pprint

import matplotlib.pyplot as plt
import preprocessing as pp
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC as SupportVectorClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


PARENT_DIR = os.path.dirname(os.getcwd())


# Main #


class SentimentModel(object):
	def __init__(self, estimator, train_set, test_set, select_features=None, optimize=False):
		self.x_train, self.y_train = train_set
		self.x_test, self.y_test = test_set

		# print("\nPRINTING SELF.X_TRAIN")
		# print(len(self.x_train))
		# print(len(self.x_train[0]))
		# pprint(self.x_train)

		self.optimize, self.estimator = optimize, estimator

		self.__fit_model()

		self.y_pred = self.model.predict(self.x_test)

	# Private Methods #

	def __fit_rand_forest(self):
		print("\tFitting a random forest algorithm")

		# GRID SEARCH NOT WORKING PROPERLY
		if self.optimize:
			return None
			# print("\t\tFinding optimal hyperparameter values")

			# grid = {"n_estimators": [250, 500, 750, 1000]}
			# models = []
			# for n in grid["n_estimators"]:
			# 	rand_forest = RandomForestClassifier(n_estimators=n)
			# 	rand_forest.fit(self.x_train, self.y_train)

			# 	y_pred = rand_forest.predict(self.x_test)

			# 	models.append({"model"          : rand_forest, "accuracy": accuracy_score(y_pred, self.y_test),
			# 	               "hyperparameters": {"n_estimators": n}})

			# best_model = max(models, key=lambda model: model["accuracy"])

			# print("\t\t\tNumber of estimators: " + str(best_model["hyperparameters"]["n_estimators"]))

			# return best_model["model"]
		else:
			rand_forest = RandomForestClassifier(n_estimators=500, verbose=1)
			rand_forest.fit(self.x_train, self.y_train)

			return rand_forest

	def __fit_grad_boost(self):
		print("\tFitting a gradient boosting machine")

		# GRID SEARCH NOT WORKING PROPERLY
		if self.optimize:
			return None
			# print("\t\tFinding optimal hyperparameter values")

			# grid = {"n_estimators" : [250, 500, 750, 1000],
			#         "learning_rate": [1, .1, .05, .01],
			#         "max_depth"    : [3, 8, 12, 15],
			#         }
			# models = []
			# for n in grid["n_estimators"]:
			# 	for lr in grid["learning_rate"]:
			# 		for d in grid["max_depth"]:
			# 			grad_boost = GradientBoostingClassifier(n_estimators=n, learning_rate=lr, max_depth=d)
			# 			grad_boost.fit(self.x_train, self.y_train)

			# 			y_pred = grad_boost.predict(self.x_test)

			# 			models.append({"model"          : grad_boost, "accuracy": accuracy_score(y_pred, self.y_test),
			# 			               "hyperparameters": {"n_estimators": n, "learning_rate": lr, "max_depth": d}})

			# best_model = max(models, key=lambda model: model["accuracy"])

			# hyperparam_vals = best_model["hyperparameters"]
			# print("\t\t\tNumber of estimators: " + str(hyperparam_vals["n_estimators"]))
			# print("\t\t\tLearning rate: " + str(hyperparam_vals["learning_rate"]))
			# print("\t\t\tMax depth: " + str(hyperparam_vals["max_depth"]))

			# return best_model["model"]
		else:
			grad_boost = GradientBoostingClassifier(n_estimators=500, learning_rate=.01, max_depth=8, verbose=1)
			grad_boost.fit(self.x_train, self.y_train)

			return grad_boost

	def __fit_support_vector_classifier(self):
		print("\tFitting a support vector classifier")

		# GRID SEARCH NOT WORKING PROPERLY
		if self.optimize:
			return None
			# print("\t\tFinding optimal hyperparameter values")

			# grid = {"kernel"     : ["linear", "poly", "rbf", "sigmoid", "precomputed"],
			#         "probability": [True, False],
			#         "tol"        : [1e-5, 1e-4, 1e-3],
			#         }
			# models = []
			# for ker in grid["kernel"]:
			# 	for prob in grid["probability"]:
			# 		for tolerance in grid["tol"]:
			# 			svc = SVC(kernel=ker, probability=prob, tol=tolerance)
			# 			svc.fit(self.x_train, self.y_train)

			# 			y_pred = svc.predict(self.x_test)

			# 			models.append({"model"          : svc, "accuracy": accuracy_score(y_pred, self.y_test),
			# 			               "hyperparameters": {"kernel": ker, "probability": prob, "tol": tolerance}})

			# best_model = max(models, key=lambda model: model["accuracy"])

			# hyperparam_vals = best_model["hyperparameters"]
			# print("\t\t\tNumber of estimators: " + str(hyperparam_vals["n_estimators"]))
			# print("\t\t\tLearning rate: " + str(hyperparam_vals["learning_rate"]))
			# print("\t\t\tMax depth: " + str(hyperparam_vals["max_depth"]))

			# return best_model["model"]
		else:
			svc = SupportVectorClassifier(kernel="poly", probability=True, tol=1e-5, verbose=1)
			svc.fit(self.x_train, self.y_train)

			return svc

	def __fit_model(self):
		if self.estimator == "RandomForest":
			self.model = self.__fit_rand_forest()
			joblib.dump(self.model, PARENT_DIR + "/models/RandomForest.pkl")
		elif self.estimator == "GradientBoosting":
			self.model = self.__fit_grad_boost()
			joblib.dump(self.model, PARENT_DIR + "/models/GradientBoosting.pkl")
		elif self.estimator == "SupportVectorClassifier":
			self.model = self.__fit_support_vector_classifier()
			joblib.dump(self.model, PARENT_DIR + "/models/SupportVector.pkl")
		else:
			print("\tError: Invalid model type")

	def __holdout_test(self):
		"""Calculates the model's classification accuracy, recall, precision, and specificity."""
		print("\t\tHoldout Validation Results:")

		print("\t\t\tAccuracy: ", accuracy_score(self.y_test, self.y_pred))
		print("\t\t\tPrecision: ", precision_score(self.y_test, self.y_pred, average="weighted"))
		print("\t\t\tRecall: ", recall_score(self.y_test, self.y_pred, average="weighted"))
		print("\t\t\tF1: ", f1_score(self.y_test, self.y_pred, average="weighted"))

	def __rolling_window_test(self, data, window_size, test_size, step=1):
		print("\t\tRolling Window Validation Results:")

		# TODO: Hide the STDOUT of pp.split() and __fit_model(), and prevent __fit_model() from saving a .pkl on each run

		windows = [data.loc[idx * step:(idx * step) + round(window_size * len(data))] for idx in
		           range(int((len(data) - round(window_size * len(data))) / step))]
		decoupled_windows = [pp.split(window, test_size=test_size, balanced=False) for window in windows]

		results = {"accuracy": [], "precision": [], "f1": [], "recall": []}
		for feature_set in decoupled_windows:
			self.x_train, self.x_test, self.y_train, self.y_test = feature_set

			self.__fit_model()

			self.y_pred = self.model.predict(self.x_test)

			results["accuracy"].append(accuracy_score(self.y_test, self.y_pred))
			results["precision"].append(precision_score(self.y_test, self.y_pred, average="weighted"))
			results["recall"].append(recall_score(self.y_test, self.y_pred, average="weighted"))
			results["f1"].append(f1_score(self.y_test, self.y_pred, average="weighted"))

		print("\t\t\tAccuracy: ", str(sum(results["accuracy"]) / float(len(results["accuracy"]))))
		print("\t\t\tPrecision: ", str(sum(results["precision"]) / float(len(results["precision"]))))
		print("\t\t\tRecall: ", str(sum(results["recall"]) / float(len(results["recall"]))))
		print("\t\t\tF1: ", str(sum(results["f1"]) / float(len(results["f1"]))))

	# Public Methods #

	def cross_validate(self, method, data=None, window_size=.9, test_size=.1, step=1):
		if method == "Holdout":
			self.__holdout_test()
		elif method == "RollingWindow":
			self.__rolling_window_test(data, window_size, test_size, step)
		else:
			print("\t\tError: Invalid cross-validation method")
