小額終老保險投保率
===================================================================================  

## 1.全台灣各縣市小額終老保險投保率儀表板
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/Taiwan_coverage_rate.png)
(相關程式碼請見：[ui_MainWindow.py](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/ui_MainWindow.py)、[myMainWindow.py](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/myMainWindow.py)、[main.py](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/main.py))  
### 在儀表板中設置了五個區塊  
(1)左邊區塊顯示的是台灣地圖，各縣市顏色的深淺表示該縣市投保率高低，投保率越高紅色越深，越低則黃色越淺。若選擇某一縣市時，則會顯示該縣市之地圖。  
(2)中間上方區塊顯示目前所選擇的地區及性別之投保率，例如當選擇全國之合計投保率時，則如圖片所示。  
(3)中間下方區塊顯示目前所選擇縣市之人口性別比例  
(4)右邊下方區塊顯示目前所選擇縣市之年齡人口比例  
(5)右邊上方區塊顯示各縣市平均每人每年可支配所得，若選擇某一縣市時，該縣市會顯示與其他縣市不同之顏色  
儀表板左上方有一個Combo Box可以選擇縣市，預設為「全國」，另有三個Radio Button可以選擇性別，以呈現所選縣市之某性別之投保率  
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/Hsinchu_coverage_rate.png)  
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/Hsinchu_female_coverage_rate.png)  
  
  
## 2.小額終老保險全國各縣市投保率分析  
(相關程式碼請見：[analysis.ipynb](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/analysis.ipynb))  
為了要找出與各縣市投保率相關之原因，我使用了內政部人口速報、縣市重要指標網有關家庭收入之檔案，並使用爬蟲程式爬取各縣市郵局間數，以及參考壽險公會年報之各縣市保險機構間數，建構出特徵：郵局間數、保險機構間數、郵局+保險機構間數、男性人口比例、女性人口比例、幼年人口比例、青壯年人口比例、老年人口比例、平均每人每年可支配所得、平均每戶全年經常性支出、平均每戶全年經常性收入、平均每戶可支配所得、平均每戶消費支出、每戶可支配所得中位數，並看各個特徵與投保率之相關係數，以及個別特徵與投保率之散點圖，觀察個別特徵與投保率之間是否存在某種規律。  
  
由於建模之需求，我先將資料進行標準化，再透過Lasso演算法，使用不同alpha產生其所對應之係數，並將其繪製成折線圖，可以觀察到最後被篩選掉的特徵為平均每人每年可支配所得，前面相關係數圖也是該項特徵與投保率最為相關，故可知此項特徵與投保率之間存有反向之相關性。  
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/corr.png)  
  
最後使用Lasso之最小角回歸算法進行特徵選擇，該算法並參考BIC進行模型選擇，最後選擇的模型為BIC最小者，被選擇之特徵為郵局間數、女性人口比例、青壯年人口比例，平均每人每年可支配所得、平均每戶全年經常性支出，並藉由這些特徵對投保率建構多元線性回歸模型，該模型之score約0.7089。  
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/Lasso_coef.png)  
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/Alpha_BIC.png)  
  
綜上所述，小額終老保險作為建構國人基本壽險保障，發揮普惠金融之特性，使預算有限之國人亦可享有基本之壽險保障，此項特性反映在平均每人每年可支配所得與投保率之負相關上，且為所有特徵中最相關者，可知小額終老保險確有發揮原先預期之效用。另一方面，小額終老保險建構基本保障，適合年幼之小朋友，且小額終老保險免體檢之特性，使想補足壽險基本保障之中高齡人口亦可輕鬆投保，故青壯年即非本保險之主要客群，與投保率呈現負相關，該係數為負。而從儀表板性別選擇之操作可以發現，各縣市女性投保率皆高於男性，故女性人口比例與投保率呈現正相關，該係數為正。最後，郵局較保險公司更可深入全台灣各村里，為最容易接觸到購買小額終老保險之客群之機構，故透過模型亦可發現郵局間數與投保率呈現正相關，該係數亦為正。