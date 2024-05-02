from finter.api import SymbolApi  # noqa: E501
from finter.settings import get_api_client
from finter.data import ModelData

from datetime import datetime
import pandas as pd

class Evaluator:
    @staticmethod
    def top_n_assets(position, n, start = None, end = None, universe=0):
        """
        Calculates and returns a DataFrame of the top n assets based on their returns,
        including negative returns unless the total position is zero.
        
        Parameters:
            position (str, pd.DataFrame): Position of the model or a specific model name.
            n (int): Number of assets with the highest returns to be returned.
            start (int): Start date of target period. (optional)
            end (int): End date of target period. (optional)
            universe (int): 0 for KRX universe, 1 for US universe. (optional)
            
        Returns:
            pd.DataFrame: DataFrame listing the top n assets with their returns and entity names,
            sorted by returns in descending order.
            
        Raises:
            ValueError: If the position parameter is not of type str or pd.DataFrame.
            ValueError: If the start or end parameter is not of type int.
        """
        if not isinstance(position, (str, pd.DataFrame)):
            raise ValueError("The 'position' parameter must be either a string or a pandas DataFrame.")

        
        # Load and preprocess position data
        if isinstance(position, str):
            position = ModelData.load(position)
        if isinstance(position.columns[0], str):
            position.columns = position.columns.astype(int)
        
        # Define the period
        if start:
            if isinstance(start, int):
                start = str(start)
                date_object = datetime.strptime(start, "%Y%m%d")
                start = date_object.strftime("%Y-%m-%d")
            else:
                raise ValueError("The 'start' parameter must be integers in YYYYMMDD format. For example, 20000101.")
            position = position.loc[start:]
        if end:
            if isinstance(end, int):
                end = str(end)
                date_object = datetime.strptime(end, "%Y%m%d")
                end = date_object.strftime("%Y-%m-%d")
            else:
                raise ValueError("The 'end' parameter must be integers in YYYYMMDD format. For example, 20000101.")
            position = position.loc[:end]

        position = position.shift(1)

        # Load price and adjustment factor data
        raw = ModelData.load('content.handa.dataguide.price_volume.krx-spot-price_close.1d')
        adj = ModelData.load('content.handa.dataguide.cax.krx-spot-adjust_factor.1d')
        
        # Calculate daily returns
        chg = ((raw * adj).pct_change()).loc[start:end]
        
        # Apply position weights
        mask = position / 1e8
        chg *= mask
        chg.fillna(0, inplace=True)
        
        # Calculate sum of returns and filter only assets with non-zero total position
        sum_chg = chg.sum()
        
        # Filter only assets with non-zero total position
        valid_assets = position.sum()[position.sum() > 0].index
        sum_chg = sum_chg[sum_chg.index.isin(valid_assets)]   
        
        # Select top n assets
        top_n_indices = sum_chg.nlargest(min(n, len(sum_chg))).index
        
        # Convert symbol IDs to entity names
        mapped = SymbolApi(get_api_client()).id_convert_retrieve(_from='id', to='entity_name', source=",".join(map(str, top_n_indices)))
        mapped = mapped.code_mapped
        
        # Create result DataFrame
        top = sum_chg.loc[list(map(int, mapped.keys()))]
        df_sorted = pd.DataFrame(top, columns=['ret']).sort_values(by='ret', ascending=False)
        df_sorted.index = df_sorted.index.map(str)
        df_sorted['entity_name'] = df_sorted.index.map(mapped)
        df_sorted['ccid'] = df_sorted.index
        df_sorted.set_index('entity_name', inplace=True)

        return df_sorted

    @staticmethod
    def bottom_n_assets(position, n, start = None, end = None, universe=0):
        """
            position (str, pd.DataFrame): Position of the model or a specific model name.
            n (int): Number of assets with the lowest returns to be returned.
            start (int): Start date of target period. (optional)
            end (int): End date of target period. (optional)
            universe (int): 0 for KRX universe, 1 for US universe. (optional)
            
        Returns:
            pd.DataFrame: DataFrame listing the bottom n assets with their returns and entity names,
            sorted by returns in descending order.
            
        Raises:
            ValueError: If the position parameter is not of type str or pd.DataFrame.
            ValueError: If the start or end parameter is not of type int.
        """
        # Validate position parameter type
        if not isinstance(position, (str, pd.DataFrame)):
            raise ValueError("The 'position' parameter must be either a string or a pandas DataFrame.")

        # Load and preprocess position data
        if isinstance(position, str):
            position = ModelData.load(position)
        if isinstance(position.columns[0], str):
            position.columns = position.columns.astype(int)
            
        # Define the period
        if start:
            if isinstance(start, int):
                start = str(start)
                date_object = datetime.strptime(start, "%Y%m%d")
                start = date_object.strftime("%Y-%m-%d")
            else:
                raise ValueError("The 'start' parameter must be integers in YYYYMMDD format. For example, 20000101.")
            position = position.loc[start:]
        if end:
            if isinstance(end, int):
                end = str(end)
                date_object = datetime.strptime(end, "%Y%m%d")
                end = date_object.strftime("%Y-%m-%d")
            else:
                raise ValueError("The 'end' parameter must be integers in YYYYMMDD format. For example, 20000101.")
            position = position.loc[:end]

        position = position.shift(1)
        
        # Load price and adjustment factor data
        raw = ModelData.load('content.handa.dataguide.price_volume.krx-spot-price_close.1d')
        adj = ModelData.load('content.handa.dataguide.cax.krx-spot-adjust_factor.1d')
        
        # Calculate daily returns
        chg = ((raw * adj).pct_change()).loc[start:end]
        
        # Apply position weights
        mask = position / 1e8
        chg *= mask
        chg.fillna(0, inplace=True)
        
        # Calculate sum of returns
        sum_chg = chg.sum()

        # Filter only assets with non-zero total position
        valid_assets = position.sum()[position.sum() > 0].index
        sum_chg = sum_chg[sum_chg.index.isin(valid_assets)]
        
        # Select bottom n assets
        bottom_n_indices = sum_chg.nsmallest(min(n, len(sum_chg))).index
        
        # Convert symbol IDs to entity names
        mapped = SymbolApi(get_api_client()).id_convert_retrieve(_from='id', to='entity_name', source=",".join(map(str, bottom_n_indices)))
        mapped = mapped.code_mapped
        
        # Create result DataFrame
        bottom = sum_chg.loc[list(map(int, mapped.keys()))]
        df_sorted = pd.DataFrame(bottom, columns=['ret']).sort_values(by='ret', ascending=True)
        df_sorted.index = df_sorted.index.map(str)
        df_sorted['entity_name'] = df_sorted.index.map(mapped)
        df_sorted['ccid'] = df_sorted.index
        df_sorted.set_index('entity_name', inplace=True)
        
        return df_sorted
