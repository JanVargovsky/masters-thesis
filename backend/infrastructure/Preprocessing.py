from sklearn.model_selection import train_test_split as split


def train_test_split(dataset, ratio, shuffle):
    train, test = split(dataset, train_size=ratio, random_state=42, shuffle=shuffle)
    return train, test
