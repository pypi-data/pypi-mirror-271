from pyspark.sql import DataFrame, SparkSession


def input(path: str) -> DataFrame:
    """
    Carrega o arquivo inicial para load e carga na bronze.

    Args:
        path: diretorio origem

    Returns:
        Um dataframe com metadados do arquivo consumido.

    Raises:
        ValueError: Caso path esteja vazio.

    Examples:
        >>> input('path/origem/account.csv')
        DataFrame[age: bigint, name: string]
    """

    if path == '':
        raise ValueError(f'path is required')

    spark = SparkSession.builder.appName(
        'Testing PySpark Example'
    ).getOrCreate()
    sample_data = [
        {'name': 'John    D.', 'age': 30},
        {'name': 'Alice   G.', 'age': 25},
    ]

    df = spark.createDataFrame(sample_data)

    return df
