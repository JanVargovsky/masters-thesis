from infrastructure import preprocessing_configuration_path
from sklearn.model_selection import train_test_split as split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import json


def train_test_split(dataset, ratio, shuffle):
    train, test = split(dataset, train_size=ratio, random_state=42, shuffle=shuffle)
    return train, test


def modify(columns, df):
    for column in columns:
        name = column['name']
        if column['remove']:
            df.drop(name, axis=1, inplace=True)
        else:
            if column['na']:
                na_method = column['naMethod']
                if na_method == 'zero':
                    na_value = 0
                elif na_method == 'average':
                    na_value = df[name].mean()
                elif na_method == 'common':
                    na_value = df[name].value_counts().idxmax()
                elif na_method == 'custom':
                    na_value = column['naCustomValue']
                else:
                    raise Exception(f"Column '{name}' invalid na method")
                df[name].fillna(na_value, inplace=True)
            if column['normalize']:
                normalize_min, normalize_max = column['normalizeRange']['min'], column['normalizeRange']['max']
                if normalize_min >= normalize_max:
                    raise Exception(f"Column '{name}' has invalid normalize range {normalize_min} < {normalize_max}")
                scaler = MinMaxScaler(feature_range=(normalize_min, normalize_max))
                df[name] = scaler.fit_transform(df[[name]])
            if column['encode']:
                encode_method = column['encodeMethod']
                if encode_method == 'label':
                    df[name] = df[name].factorize()[0]
                elif encode_method == 'oneHot':
                    dummies = pd.get_dummies(df[name], prefix=name)
                    df.drop(name, axis=1, inplace=True)
                    df[dummies.columns] = dummies
                else:
                    raise Exception(f"Column '{name}' has invalid encode method")


def save_configuration(data, name):
    # TODO: prune
    with open(f"{preprocessing_configuration_path}{name}.json", 'x') as f:
        json.dump(data, f, indent=2)


def load_configuration(name):
    with open(f"{preprocessing_configuration_path}{name}.json", 'r') as f:
        return json.load(f)
