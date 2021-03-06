export const extensions = [
  ".csv",
  ".txt",
  ".xlsx",
  ".xlsm",
  ".pickle",
  ".feather",
  ".parquet",
  ".hdf",
  ".hdf5",
  ".h5"
];
export const defaultExtension = ".parquet";

function isValidDatasetExtension(extension) {
  return extensions.includes(extension);
}

export function isDatasetNameValid(datasetName) {
  if (!datasetName) return false;

  const index = datasetName.lastIndexOf(".");
  if (index == -1) return false;

  const name = datasetName.substr(0, index);
  const extension = datasetName.substr(index);

  if (extension.length == 0) return false;

  return name.length > 0 && isValidDatasetExtension(extension);
}
