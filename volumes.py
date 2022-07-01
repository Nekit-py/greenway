import pandas as pd
from utils import timeit


class TotalPartnerVolume:
    def __init__(self, partners_path: str, orders_path: str):
        self.partners_path = partners_path
        self.orders_path = orders_path

    def _get_merged_data(self) -> None:
        orders = pd.read_csv(self.orders_path, memory_map=True, usecols=('item_vol', 'RECIPIENT'))
        partners = pd.read_csv(self.partners_path, memory_map=True)
        partners = partners[partners['SPONSOR'].notna()]
        self.merged_data = partners.merge(
            orders, how='left', left_on='ID',
            right_on='RECIPIENT', suffixes=('_PARTNER', None)
        )
        self.merged_data = self.merged_data[self.merged_data['item_vol'].notna()]
        del self.merged_data['ID']

    @timeit
    def get_total_sales_volume(self, footer=True) -> pd.DataFrame:
        self._get_merged_data()
        #issue_1
        if footer:
            result = self.merged_data.groupby('SPONSOR')['item_vol'].sum().reset_index()
            return result
        else:
        #issue_2
            footer = self.merged_data.groupby('SPONSOR')['RECIPIENT'].max()\
                .reset_index()['RECIPIENT'].to_list()
            result_without_footer = self.merged_data[~self.merged_data.isin(footer)]\
                .groupby('SPONSOR')['item_vol'].sum().reset_index()
            return result_without_footer