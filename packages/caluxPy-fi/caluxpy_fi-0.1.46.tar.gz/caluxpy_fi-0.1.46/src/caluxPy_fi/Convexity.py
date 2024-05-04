import numpy as np, pandas as pd, matplotlib.pyplot as plt, logging, os
from pathlib import Path
import sys
#sys.path.append(str(Path(__file__).resolve().parent.parent))
from caluxPy_fi.FixedIncome import FixedIncome
from caluxPy_fi.Support import Support

class Convexity(FixedIncome):

    def __init__(self, settlement_date, issuance_date, maturity_date, coupon, ytm, face_value, issuer, methodology, periodicity, payment_type, coupon_type, 
                 forward_date, amortization_start_date, amortization_periods, amortization_periodicity, amortizable_percentage, date_format = '', multiple = False, bps = 100, lang = 'eng'):
        super().__init__(settlement_date, issuance_date, maturity_date, coupon, ytm, face_value, issuer, methodology, periodicity, payment_type, coupon_type, 
                         forward_date, amortization_start_date, amortization_periods, amortization_periodicity, amortizable_percentage, date_format = '', multiple = False, lang = 'eng')

        desktop = Support.get_folder_path()
        logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(desktop, 'convex'), mode = 'w', encoding = 'utf-8')
        fileHandler.setFormatter(logFormatter)
        self._logger.addHandler(fileHandler)

        self._lang = lang
        self.tipo_valoracion = 'convexity'
        self.bps = bps

        self.max_gain, self.max_loss, self.avg_gain, self.avg_loss, self.std_gain, self.std_loss = 0, 0, 0, 0, 0, 0
        self.chart_data = {}

        if self._lang == 'eng':
            self._logger.info(f'Settlement Date -> {settlement_date}')
            self._logger.info(f'Issuance Date -> {issuance_date}')
            self._logger.info(f'Maturity Date -> {maturity_date}')
            self._logger.info(f'Coupon Rate -> {coupon}')
            self._logger.info(f'Yield to Maturity -> {ytm}')
            self._logger.info(f'Face Value -> {face_value}')
            self._logger.info(f'Issuer -> {issuer}')
            self._logger.info(f'Methodology -> {methodology}')
            self._logger.info(f'Periodicity -> {periodicity}')
            self._logger.info(f'Payment Type -> {payment_type}')
            self._logger.info(f'Coupon Type -> {coupon_type}')
            self._logger.info(f'Forward Date -> {forward_date}')
            self._logger.info(f'Amortization Start Date -> {amortization_start_date}')
            self._logger.info(f'Amortization Periods -> {amortization_periods}')
            self._logger.info(f'Amortization Periodicity -> {amortization_periodicity}')
            self._logger.info(f'Amortizable Percentage -> {amortizable_percentage}\n--------------------------------------------------------------------------------------------------------------------------------------\n')
            try:
                self._logger.info(f'Current Coupon -> {self.current_coupon}')
                self._logger.info(f'NPER -> {self._nper}')
                self._logger.info(f'w Coupon -> {self.w_coupon}')
                self._logger.info(f'Discrepancy -> {self._discrepancy}')
                self._logger.info(f'Coupon Type -> {self.coupon_type}')
                self._logger.info(f'Maturity Date -> {self.maturity_date}')
                self._logger.info(f'Expected Maturity -> {self.expected_maturity}')
                self._logger.info(f'Coupon Days -> {self.coupon_days}')
                self._logger.info(f'Yield yo Maturity -> {self.ytm}')
                self._logger.info(f'Periodicity -> {self.periodicity}')
                self._logger.info(f'Coupon Flow -> {self.coupon_flow}')
                self._logger.info(f'Payment Type -> {self.payment_type}')
                self._logger.info(f'Issuer -> {self.issuer}')
                self._logger.info(f'Notional Value -> {self.notional_value}')
                self._logger.info(f'Earned Coupon -> {self.gained_coupon}')
                self._logger.info(f'Basis Points -> {bps}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
                
                self.convexityValuationType(self.current_coupon, self._nper, self.w_coupon, self._discrepancy, self.coupon_type, self.maturity_date, self.expected_maturity, self.coupon_days, 
                                              self.ytm, self.periodicity, self.coupon_flow, self.payment_type, self.issuer, self.notional_value, self.gained_coupon, bps)
                self._logger.info('SUCCESS: Calculation finished..')
            except Exception as e:
                self._logger.exception(e)
        elif self._lang == 'esp':
            self._logger.info(f'Fecha Liquidación -> {settlement_date}')
            self._logger.info(f'Fecha Emisión -> {issuance_date}')
            self._logger.info(f'Fecha Vencimiento -> {maturity_date}')
            self._logger.info(f'Cupón -> {coupon}')
            self._logger.info(f'Rendimiento -> {ytm}')
            self._logger.info(f'Monto -> {face_value}')
            self._logger.info(f'Emisor -> {issuer}')
            self._logger.info(f'Metodología -> {methodology}')
            self._logger.info(f'Periodicidad -> {periodicity}')
            self._logger.info(f'Tipo de Pago -> {payment_type}')
            self._logger.info(f'Tipo de Cupones -> {coupon_type}')
            self._logger.info(f'Fecha Forward -> {forward_date}')
            self._logger.info(f'Fecha de Inicio de Amortizaciones -> {amortization_start_date}')
            self._logger.info(f'Cantidad de Amortizaciones -> {amortization_periods}')
            self._logger.info(f'Periodicidad de Amortizaciones -> {amortization_periodicity}')
            self._logger.info(f'Porcentaje Amortizable -> {amortizable_percentage}\n--------------------------------------------------------------------------------------------------------------------------------------\n')

            try:
                self._logger.info(f'Cupón Actual -> {self.current_coupon}')
                self._logger.info(f'NPER -> {self._nper}')
                self._logger.info(f'w Cupón -> {self.w_coupon}')
                self._logger.info(f'Discrepancia -> {self._discrepancy}')
                self._logger.info(f'Tipo de Cupones -> {self.coupon_type}')
                self._logger.info(f'Fecha de Vencimiento -> {self.maturity_date}')
                self._logger.info(f'Vencimiento Esperado -> {self.expected_maturity}')
                self._logger.info(f'Días Cupón -> {self.coupon_days}')
                self._logger.info(f'Rendimiento -> {self.ytm}')
                self._logger.info(f'Periodicidad -> {self.periodicity}')
                self._logger.info(f'Flujo Cupón -> {self.coupon_flow}')
                self._logger.info(f'Tipo de Pago -> {self.payment_type}')
                self._logger.info(f'Emisor -> {self.issuer}')
                self._logger.info(f'Valor Nocional -> {self.notional_value}')
                self._logger.info(f'Cupón Corrido -> {self.gained_coupon}')
                self._logger.info(f'Puntos Básicos -> {bps}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
                
                self.convexityValuationType(self.current_coupon, self._nper, self.w_coupon, self._discrepancy, self.coupon_type, self.maturity_date, self.expected_maturity, self.coupon_days, 
                                              self.ytm, self.periodicity, self.coupon_flow, self.payment_type, self.issuer, self.notional_value, self.gained_coupon, bps)
                self._logger.info('SUCCESS: Cálculo realizado..')
            except Exception as e:
                self._logger.exception(e)

        self._logger.removeHandler(fileHandler)
        fileHandler.close()

    def convexityValuationType(self, current_coupon, nper, w_coupon, discrepancy, coupon_type, maturity_date, expected_maturity, coupon_days, ytm, periodicity, 
                                 coupon_flow, payment_type, issuer, notional_value, gained_coupon, bps):
        
        listPBS, listytms, listCleanPrice, listDirtyPrice, listDuracion, listModDuration, listDV01, listConvexity, listDuration2 = [], [], [], [], [], [], [], [], []
        dicDV01 = {}
        
        y = -int(bps)
        while y <= int(bps):
            ytm2 = ytm + (y / 10000)
            resValuation = self.presentValue(current_coupon, nper, w_coupon, discrepancy, coupon_type, maturity_date, expected_maturity, coupon_days, ytm2, periodicity, coupon_flow, payment_type, issuer, notional_value, gained_coupon)
            listPBS.append(y)
            listytms.append(ytm2)
            listCleanPrice.append(resValuation[4] * 100)
            listDirtyPrice.append(resValuation[1] * 100)
            listDuracion.append(resValuation[3])
            listModDuration.append(resValuation[5])
            #dv01 = (resValuation[5] / 100) * (resValuation[1]) * (notional_value / 100)
            #listDV01.append(dv01)
            #dicDV01[y] = dv01
            y += 1
        listPBS = np.array(listPBS)
        listytms = np.array(listytms)
        listCleanPrice = np.array(listCleanPrice)
        listDirtyPrice = np.array(listDirtyPrice)
        listDuracion = np.array(listDuracion)
        listModDuration = np.array(listModDuration)
        #listDV01 = np.array(listDV01)
        self.df_convex = pd.DataFrame({'pbs': listPBS, 'Price': listDirtyPrice})
        
        # Treatment of the negatives in the df
        negatives = self.df_convex[self.df_convex['pbs'] <= 0].copy()
        negatives.sort_values(by = 'pbs', ascending = False, inplace = True)
        negatives['dv01'] = negatives['Precio Sucio'].diff().fillna(0) * 10000
        negatives['accum'] = negatives['dv01'].cumsum()
        negatives.sort_values(by = 'pbs', ascending = True, inplace = True)
        first_neg = negatives.iloc[-2]['dv01']
        
        # Treatment of the positives in the df
        positives = self.df_convex[self.df_convex['pbs'] >= 0].copy()
        positives.sort_values(by = 'pbs', ascending = True, inplace = True)
        positives['dv01'] = positives['Precio Sucio'].diff().fillna(0) * -10000
        positives['accum'] = positives['dv01'].cumsum()
        first_pos = positives.iloc[1]['dv01']   
        
        # Getting the average
        avg = (first_neg + first_pos) / 2
        
        #Concatenating the dfs to form the complete one
        final = pd.concat([negatives, positives])
        final.reset_index(drop = True, inplace = True)
        self.df_convex['dv01'] = final['dv01']
        
        final['Negative'] = final['Stress Pbs'] < 0
        max_values_by_category = final.groupby('Negative')['dv01'].max()
        avg_values_by_category = final.groupby('Negative')['dv01'].mean()
        std_values_by_category = final.groupby('Negative')['dv01'].std()

        #self.neg_vals = final.groupby('Negative')

        self._logger.info(f'{self.df_convex}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
        if self._lang == 'eng':
            self._logger.info(f'Max Values by Category -> {max_values_by_category}')
            self._logger.info(f'Average Values by Category -> {max_values_by_category}')
            self._logger.info(f'Standard Deviations by Category -> {max_values_by_category}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
        elif self._lang == 'esp':
            self._logger.info(f'Máximos Valores por Categoría -> {max_values_by_category}')
            self._logger.info(f'Valores Promedio por Categoría -> {max_values_by_category}')
            self._logger.info(f'Desviaciones Estándar por Categoría -> {max_values_by_category}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')

        self.max_gain = max_values_by_category[True]
        self.max_loss = max_values_by_category[False]
        self.avg_gain = avg_values_by_category[True]
        self.avg_loss = avg_values_by_category[False]
        self.std_gain = std_values_by_category[True]
        self.std_loss = std_values_by_category[False]

        if self._lang == 'eng':
            self._logger.info(f'Max Gain -> {self.max_gain}')
            self._logger.info(f'Max Loss -> {self.max_loss}')
            self._logger.info(f'Average Gain -> {self.avg_gain}')
            self._logger.info(f'Average Loss -> {self.avg_loss}')
            self._logger.info(f'Standard Deviation of Gains -> {self.std_gain}')
            self._logger.info(f'Standard Deviation of Losses -> {self.std_loss}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
        elif self._lang == 'esp':
            self._logger.info(f'Max Ganancia -> {self.max_gain}')
            self._logger.info(f'Max Perdida -> {self.max_loss}')
            self._logger.info(f'Ganancia Promedio -> {self.avg_gain}')
            self._logger.info(f'Perdida Promedio -> {self.avg_loss}')
            self._logger.info(f'Desviación Estándar en Ganancias -> {self.std_gain}')
            self._logger.info(f'Desviación Estándar en Perdidas -> {self.std_loss}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
    
        i = 0
        while i <= int(bps):
            if i == 0:
                listConvexity.append(0)
            else:
                listConvexity.append(listConvexity[i - 1] - final['dv01'][i])
            i += 1
        i = -1
        while i >= -int(bps):
            if i == -1:
                listConvexity.append(final['dv01'][i])
            else:
                listConvexity.append(listConvexity[-1] + final['dv01'][i])
            i -= 1
        listConvexity = np.array(listConvexity)
        listConvexity[::-1].sort()
        i = -int(bps)
        while i <= int(bps):
            listDuration2.append(final['dv01'][0] * (0 - i))
            i += 1
        listDuration2 = np.array(listDuration2)

        self.chart_data['x'] = listPBS
        self.chart_data['y1'] = listDuration2
        self.chart_data['y2'] = listConvexity

    def showGraph(self):
        plt.figure(figsize=(10,6))
        plt.plot(self.chart_data['x'], self.chart_data['y1'])
        plt.plot(self.chart_data['x'], self.chart_data['y2'], linestyle='--')
        title = 'Gráfico de Duración-Convexidad' if self._lang == 'esp' else 'Duration-Convexity Graph' if self._lang == 'eng' else ''
        basis_points = 'Puntos Básicos' if self._lang == 'esp' else 'Basis Points' if self._lang == 'eng' else ''
        values = 'Valores Duración y Convexidad' if self._lang == 'esp' else 'Duration and Convexity Values' if self._lang == 'eng' else ''
        plt.ylabel(values)
        plt.xlabel(basis_points)
        plt.title(title)
        
        return plt.show()

    def saveGraph(self, filename):
        plt.savefig(filename, bbox_inches = 'tight', dpi = 300)
        plt.close()
    
    def getResults(self):
        if self._lang == 'eng':
            results = {'Max Gain': self.max_gain, 'Max Loss': self.max_loss, 'Average Gain': self.avg_gain, 'Average Loss': self.avg_loss, 'Deviations in Gains': self.std_gain, 
                    'Deviations in Losses': self.std_loss}
        elif self._lang == 'esp':
            results = {'Max Ganancia': self.max_gain, 'Max Perdida': self.max_loss, 'Ganancia Promedio': self.avg_gain, 'Perdida Promedio': self.avg_loss, 'Desviacion Ganancias': self.std_gain, 
                    'Desviacion Perdidas': self.std_loss}
        return results

    def __str__(self):
        if self._lang == 'eng':
            return f'\
Max Gain: {self.max_gain} \n \
Max Loss: {self.max_loss} \n \
Average Gain: {self.avg_gain} \n \
Average Loss: {self.avg_loss} \n \
Deviation in Gains: {self.std_gain} \n \
Deviation in Losses: {self.std_loss}'
        elif self._lang == 'esp':
            return f'\
Max Ganancia: {self.max_gain} \n \
Max Perdida: {self.max_loss} \n \
Ganancia Prom: {self.avg_gain} \n \
Perdida Prom: {self.avg_loss} \n \
Desviacion Ganancias: {self.std_gain} \n \
Desviacion Perdidas: {self.std_loss}'


