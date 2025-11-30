import pandas as pd
import numpy as np
import string

class HyAIA:
    def __init__(self, df):
        self.data = df
        self.columns = df.columns
        self.data_binarios, self.binarios_columns = self.get_binarios()
        self.data_cuantitativos, self.cuantitativos_columns = self.get_cuantitativos()
        self.data_categoricos, self.categoricos_columns = self.get_categoricos()
        self.df_dqr = self.get_dqr()
        
    ##% Métodos para Análisis de Datos 
    #Método para obtener las columnas y dataframe binarios
    def get_binarios(self):
        col_bin = []
        for col in self.data.columns:
            if self.data[col].nunique() == 2:
                col_bin.append(col)
        return self.data[col_bin], col_bin
        
    #Método para obtener columnas y dataframe cuantitativos
    def get_cuantitativos(self):
        col_cuantitativas = self.data.select_dtypes(include='number').columns
        return self.data[col_cuantitativas], col_cuantitativas
        
    #Método para obtener columnas y dataframe categóricos
    def get_categoricos(self):
        col_categoricos = self.data.select_dtypes(exclude='number').columns
        col_cat = []
        for col in col_categoricos:
            if self.data[col].nunique()>2:
                col_cat.append(col)
        return self.data[col_cat], col_cat
        
    def get_dqr(self):
        #% Lista de variables de la base de datos
        columns = pd.DataFrame(list(self.data.columns.values), columns=['Columns_Names'], 
                               index=list(self.data.columns.values))
        
        #Lista de tipos de datos del dataframe
        data_dtypes = pd.DataFrame(self.data.dtypes, columns=['Dtypes'])
        
        #Lista de valores presentes
        present_values = pd.DataFrame(self.data.count(), columns=['Present_values'])
        
        #Lista de valores missing (Valores faltantes/nulos nan)
        missing_values = pd.DataFrame(self.data.isnull().sum(), columns=['Missing_values'])
        
        #Valores unicos de las columnas
        unique_values = pd.DataFrame(columns=['Unique_values'])
        for col in list(self.data.columns.values):
            unique_values.loc[col] = [self.data[col].nunique()]
        
        # Información estadística
        #Lista de valores máximos
        max_values = pd.DataFrame(columns=['Max_values'])
        for col in list(self.data.columns.values):
            try:
                max_values.loc[col] = [self.data[col].max()]
            except:
                max_values.loc[col] = ['N/A']
                pass
        
        #Lista de valores mínimos
        min_values = pd.DataFrame(columns=['Min_values'])
        for col in list(self.data.columns.values):
            try:
                min_values.loc[col] = [self.data[col].min()]
            except:
                min_values.loc[col] = ['N/A']
                pass
        #Lista de valores con su desviación estandar
        
        #Lista de valores con los percentiles
        
        #Lista de valores con la media
           
        return columns.join(data_dtypes).join(present_values).join(missing_values).join(unique_values).join(max_values).join(min_values)

    
  #  def categoricos_limpieza(self):
  #      for col in self.categoricos_columns:
  #          self.data_categoricos[col] = self.data_categoricos[col].apply(remove_punctuation)
            
    # remover signos de puntuación
    @staticmethod
    def remove_punctuation(x):
        try:
            x = ''.join(ch for ch in x if ch not in string.punctuation)
        except:
            print(f'{x} no es una cadena de caracteres')
            pass
        return x

    



    def dqr(self):
        """
        Reporte de Calidad de Datos (DQR)
        - is_categorical
        - categories (<=10)
        - max, min, mean, std solo para numéricas
        """

        df = self.data

        # Tipo de dato
        tipos = df.dtypes

        # Nulos
        nulos = df.isnull().sum()
        pct_nulos = round((df.isnull().sum() / len(df)) * 100, 2)

        # Identificar columnas categóricas
        is_categorical = df.apply(lambda col: col.dtype == 'object' or col.dtype.name == 'category')

        # Categorias
        categorias = []
        for col in df.columns:
            if is_categorical[col]:
                vals = df[col].dropna().unique()
                if len(vals) <= 10:
                    categorias.append(list(vals))
                else:
                    categorias.append("Más de 10 categorías")
            else:
                categorias.append(None)

        # Estadísticos numéricos
        max_vals = df.apply(lambda col: col.max() if pd.api.types.is_numeric_dtype(col) else None)
        min_vals = df.apply(lambda col: col.min() if pd.api.types.is_numeric_dtype(col) else None)
        mean_vals = df.apply(lambda col: col.mean() if pd.api.types.is_numeric_dtype(col) else None)
        std_vals = df.apply(lambda col: col.std() if pd.api.types.is_numeric_dtype(col) else None)

        dqr_df = pd.DataFrame({
            'tipo_dato': tipos,
            'nulos_total': nulos,
            'porcentaje_nulos': pct_nulos,
            'is_categorical': is_categorical,
            'categories': categorias,
            'max': max_vals,
            'min': min_vals,
            'mean': mean_vals,
            'std': std_vals
        })

        return dqr_df
