import matplotlib.pyplot as plt
import io
import base64


def plot_to_base64():
    image = io.BytesIO()
    plt.savefig(image, format='png', dpi=150, transparent=False, bbox_inches='tight')
    plt.clf()
    result = base64.b64encode(image.getvalue()).decode()
    return result


def plot_histogram(series, column_name, is_numeric):
    plt.xlabel(column_name)
    if is_numeric:
        plt.title(f"{column_name} cumulative histogram")
        plt.ylabel("Cumulative frequency")
        plt.hist(series.dropna(), bins='auto', density=True, cumulative=True)
    else:
        plt.title(f"{column_name} histogram")
        plt.ylabel("Frequency")
        value_counts = series.value_counts(dropna=False)
        for value, count in value_counts.iteritems():
            plt.bar(str(value), count)
