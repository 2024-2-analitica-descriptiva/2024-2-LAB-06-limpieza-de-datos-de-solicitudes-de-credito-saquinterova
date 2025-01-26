"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import pandas as pd
    import os

    def preprocess_column(df, column_name, transformations):
        for transformation in transformations:
            df[column_name] = transformation(df[column_name])

    def replace_characters(series, chars_to_replace, replacement):
        for char in chars_to_replace:
            series = series.str.replace(char, replacement)
        return series


    df = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';', index_col=0)
    df.dropna(inplace=True)
    
    preprocess_column(df, 'sexo', [lambda x: x.str.upper()])

    preprocess_column(df, 'tipo_de_emprendimiento', [lambda x: x.str.upper(), lambda x: x.str.strip()])

    preprocess_column(df, 'barrio', [
        lambda x: x.str.upper(), 
        lambda x: replace_characters(x, ["_", "-"], " ")
    ])

    preprocess_column(df, 'idea_negocio', [
        lambda x: x.str.upper(), 
        lambda x: replace_characters(x, ["_", "-"], " "), 
        lambda x: x.str.strip()
    ])

    df['monto_del_credito'] = df['monto_del_credito'].str.strip().str.replace("$", "").str.replace(",", "").str.replace(".00", "").astype(int)

    preprocess_column(df, 'línea_credito', [
        lambda x: x.str.upper(), 
        lambda x: replace_characters(x, ["_", "-"], " "), 
        lambda x: x.str.strip()
    ])

    df['fecha_homologada'] = pd.to_datetime(df['fecha_de_beneficio'], dayfirst=True, errors='coerce')
    df['fecha_homologada'] = df['fecha_homologada'].fillna(
        pd.to_datetime(df['fecha_de_beneficio'], format="%Y/%m/%d", errors='coerce')
    )
    
    df.drop(columns='fecha_de_beneficio', inplace=True)
    df.rename(columns={'fecha_homologada': 'fecha_de_beneficio'}, inplace=True)

    df.drop_duplicates(inplace=True)

    output_directory = os.path.join('files', 'output')
    os.makedirs(output_directory, exist_ok=True)
    df.to_csv(os.path.join(output_directory, 'solicitudes_de_credito.csv'), sep=';')


    return df

print(pregunta_01())