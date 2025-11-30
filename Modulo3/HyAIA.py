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

    
    @staticmethod
    def train_test_split(X, y, test_size=0.2):
        """
        Divide los datos en conjuntos de entrenamiento y prueba.
        Args:
            X (pd.DataFrame): Características.
            y (pd.DataFrame): Etiquetas.
            test_size (float): Proporción para el conjunto de prueba.
        Returns:
            X_train, X_test, y_train, y_test
        """
        import numpy as np
        n = len(X)
        idx = np.arange(n)
        np.random.shuffle(idx)
        split = int(n * (1 - test_size))
        train_idx, test_idx = idx[:split], idx[split:]
        X_train = X.iloc[train_idx].reset_index(drop=True)
        X_test = X.iloc[test_idx].reset_index(drop=True)
        y_train = y.iloc[train_idx].reset_index(drop=True)
        y_test = y.iloc[test_idx].reset_index(drop=True)
        return X_train, X_test, y_train, y_test

    # remover signos de puntuación
    @staticmethod
    def remove_punctuation(x):
        try:
            x = ''.join(ch for ch in x if ch not in string.punctuation)
        except:
            print(f'{x} no es una cadena de caracteres')
            pass
        return x



