import base64
import io

import matplotlib.pyplot as plt
import numpy as np
# noinspection PyUnresolvedReferences
from mpl_toolkits.mplot3d import Axes3D  # Register Axes3D as 3d projection


def plot_to_base64():
    image = io.BytesIO()
    plt.savefig(image, format='png', dpi=150, transparent=False, bbox_inches='tight')
    plt.clf()
    result = base64.b64encode(image.getvalue()).decode()
    return result


def plot_histogram(series, column_name, is_numeric):
    plt.xlabel(column_name)
    if is_numeric:
        plt.title("{} cumulative histogram".format(column_name))
        plt.ylabel("Cumulative frequency")
        plt.hist(series.dropna(), bins='auto', density=True, cumulative=True)
    else:
        plt.title("{} histogram".format(column_name))
        plt.ylabel("Frequency")
        value_counts = series.value_counts(dropna=False)
        for value, count in value_counts.iteritems():
            plt.bar(str(value), count)


def plot_box_and_violin(series):
    series = series.dropna()
    plt.violinplot(series)
    plt.boxplot(series)
    plt.title("{} boxplot".format(series.name))
    plt.xticks([])
    plt.ylabel(series.name)


def plot_history_accuracy(history):
    plt.plot(history.history['acc'], label="Train")
    if "val_acc" in history.history:
        plt.plot(history.history['val_acc'], label="Validation")
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()


def plot_history_loss(history):
    plt.plot(history.history['loss'], label="Train")
    if "val_loss" in history.history:
        plt.plot(history.history['val_loss'], label="Validation")
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()


def plot_classification_predictions(expected_predictions, actual_predictions,
                                    orientation='vertical', stacked=False):
    classes = np.sort(expected_predictions.unique())
    predicted_classes_correct = np.zeros(classes.size, dtype=int)
    predicted_classes_incorrect = np.zeros(classes.size, dtype=int)

    for expected, actual in zip(expected_predictions, actual_predictions):
        if expected == actual:
            predicted_classes_correct[expected] += 1
        else:
            predicted_classes_incorrect[expected] += 1

    if orientation == 'vertical':
        x = np.arange(classes.size)
        plt.xlabel(expected_predictions.name)
        plt.ylabel("Count")
        plt.xticks(x, classes)

        if stacked:
            w = 0.2
            plt.bar(x, predicted_classes_correct, width=w, color='tab:green', label='Correct')
            plt.bar(x, predicted_classes_incorrect, width=w, color='tab:red', label='Incorrect',
                    bottom=predicted_classes_correct)
        else:
            w = 0.4
            plt.bar(x - w / 2, predicted_classes_correct, width=w, color='tab:green', label='Correct')
            plt.bar(x + w / 2, predicted_classes_incorrect, width=w, color='tab:red', label='Incorrect')
    elif orientation == 'horizontal':
        y = np.arange(classes.size)
        plt.xlabel("Count")
        plt.ylabel(expected_predictions.name)
        plt.yticks(y, classes)

        if stacked:
            h = 0.2
            plt.barh(y, predicted_classes_correct, height=h, color='tab:green', label='Correct')
            plt.barh(y, predicted_classes_incorrect, height=h, color='tab:red', label='Incorrect',
                     left=predicted_classes_correct)
        else:
            h = 0.4
            plt.barh(y + h / 2, predicted_classes_correct, height=h, color='tab:green', label='Correct')
            plt.barh(y - h / 2, predicted_classes_incorrect, height=h, color='tab:red', label='Incorrect')
    else:
        raise Exception("unknown orientation '{}'".format(orientation))

    plt.title("Predictions")
    plt.legend()


def plot_generated_dataset(x, y):
    dim = x.shape[1]
    # 1d or 2d
    if dim == 1 or dim == 2:
        plt.title("Preview")
        plt.xlabel('X')
        x0 = x[:, 0]
        if dim == 1:
            x1 = np.zeros_like(x0)
            plt.yticks([])
        else:
            x1 = x[:, 1]
            plt.ylabel("Y")
        plt.scatter(x0, x1, marker='o', c=y, s=25, edgecolor='k')
    # 3d
    else:
        ax = plt.axes(projection='3d')
        ax.scatter(x[:, 0], x[:, 1], x[:, 2], marker='o', c=y, s=25, edgecolor='k')
        ax.set_title("Preview")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
