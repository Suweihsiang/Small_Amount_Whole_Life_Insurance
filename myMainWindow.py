from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel
from PyQt5.QtCore import pyqtSlot,QRect,Qt

from ui_MainWindow import Ui_MainWindow                             #GUI
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['ytick.labelcolor'] = 'white'
plt.rcParams['text.color'] = 'white'
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

class QmyMainWindow(QMainWindow):                                   #this class is inherit from QMainWindow

    def __init__(self,parent=None):
        super().__init__(parent)                                    #use QMainWindow inititialize function 
        self.ui=Ui_MainWindow()                                     #construct GUI
        self.ui.setupUi(self)
        width = QApplication.primaryScreen().size().width()
        height = QApplication.primaryScreen().size().height()
        self.setFixedSize(width,height)
        self.ui.gridLayoutWidget.setGeometry(QRect(10, 20, width, int(height * 0.9)))
        self.ui.centralwidget.setStyleSheet('background:rgb(0,0,0)')
        self.ui.male.setStyleSheet('color:rgb(255,255,255)')
        self.ui.female.setStyleSheet('color:rgb(255,255,255)')
        self.ui.total.setStyleSheet('color:rgb(255,255,255)')
        self.ui.label.setStyleSheet('color:rgb(255,255,255)')
        self.feature = 'total'
        self.load_data()
        self.draw_geograph()
        self.draw_indicator_plot()
        
        
    
#=====================================由connectSlotByName()自動連結的槽函數===================================================
    @pyqtSlot(str)
    def on_City_box_currentIndexChanged(self,city):
        self.draw_geograph()
        self.draw_indicator_plot()
        
    
    @pyqtSlot(bool)
    def on_male_clicked(self,click):
        if(click):
            self.feature = 'male'
            self.draw_geograph()
    
    @pyqtSlot(bool)
    def on_female_clicked(self,click):
        if(click):
            self.feature = 'female'
            self.draw_geograph()

    @pyqtSlot(bool)
    def on_total_clicked(self,click):
        if(click):
            self.feature = 'total'
            self.draw_geograph()
        

#============================================自定義槽函數===================================================================


#==========================================自訂函數========================================================================
    def load_data(self):
        self.geo = gpd.read_file('Taiwan_map.json')
        self.geo = self.geo[['COUNTYNAME','geometry']]
        self.data = pd.read_csv('ratio_of_having_insurance_coverage.csv')
        self.indicator = pd.read_csv('indicator.csv')

    
    def draw_geograph(self):
        self.city = self.ui.City_box.currentText()
        if self.city != '全國': geo_selected = self.geo[self.geo['COUNTYNAME'] == self.city]
        else:                   geo_selected = self.geo

        geo_data = geo_selected.merge(self.data,left_on = 'COUNTYNAME', right_on = 'City', how = 'outer')
        fig = plt.Figure(dpi=123)
        ax = fig.add_subplot(111)
        geo_data.plot(ax=ax,column=self.feature, cmap = 'YlOrRd', vmin = 0, vmax = 0.09, legend=True,legend_kwds={'label': "小額終老保險投保率"})
        ax.set_yticks([])
        canvas = FigureCanvas(fig)
        pixmap = QPixmap(canvas.grab().toImage())
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.ui.gridLayout.addWidget(label,0,0,2,1)

        rate = self.data[self.data['City'] == self.city][self.feature]
        text = "<font style = 'font-size:85px;'>{}</font>\
                <br/>\
                <br/>\
                <font style = 'font-size:40px;'>投保率</font>\
                <br/>\
                <br/>\
                <font style = 'font-size:85px;'>{}</font>".format(self.city,str('%.2f%%'%(rate.iloc[0] * 100)))
        self.city_info = QLabel()
        self.city_info.setText(text)
        f = QFont()
        f.setFamily('Microsoft JhengHei')
        self.city_info.setFont(f)
        self.city_info.setStyleSheet('color : white')
        self.city_info.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.ui.gridLayout.addWidget(self.city_info,0,1)

    def draw_indicator_plot(self):
        gender = self.indicator[self.indicator['City'] == self.city][['male_ratio','female_ratio']]
        fig = plt.Figure(dpi=115)
        ax = fig.add_subplot(111)
        ax.pie(x = gender.iloc[0],labels=['男','女'],autopct='%.2f%%',colors = ['c','hotpink'])
        ax.set_title('人口性別比例')
        canvas = FigureCanvas(fig)
        pixmap = QPixmap(canvas.grab().toImage())
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.ui.gridLayout.addWidget(label,1,1)

        age = self.indicator[self.indicator['City'] == self.city][['Young_Age_ratio','Working_Age_ratio','Old_Age_ratio']]
        fig = plt.Figure(dpi=115)
        ax = fig.add_subplot(111)
        ax.pie(x = age.iloc[0],labels=['幼年人口','青壯年人口','老年人口'],autopct='%.2f%%',colors=['mediumturquoise','skyblue','tan'])
        ax.set_title('年齡人口比例')
        canvas = FigureCanvas(fig)
        pixmap = QPixmap(canvas.grab().toImage())
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.ui.gridLayout.addWidget(label,1,2)

        income = self.indicator[['City','disposable income']].head(22)
        y = np.arange(len(income))
        value = income['disposable income']
        labels = [l for l in income['City']]
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        color = ['cyan' for _ in y]
        if self.city != "全國" :
            idx = income.index[income['City'] == self.city][0]
            color[idx] = 'springgreen'
        ax.barh(y,value,color = color)
        ax.set_yticks(ticks = y,labels = labels,color = 'white')
        for a,b in zip(y,value):
            if labels[a] == self.city : c = 'springgreen'
            else:                       c = 'white'
            ax.text(b,a-0.15,format(b,','),color=c,ha='left',va='center')
        ax.set_title('各縣市平均每人每年可支配所得')
        canvas = FigureCanvas(fig)
        pixmap = QPixmap(canvas.grab().toImage())
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.ui.gridLayout.addWidget(label,0,2)