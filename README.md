小額終老保險投保率  

1.有關全台灣各縣市小額終老保險投保率儀表板
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/Taiwan_coverage_rate.png)
在儀表板中設置了五個區塊  
(1)左邊區塊顯示的是台灣地圖，各縣市顏色的深淺表示該縣市投保率高低，投保率越高紅色越深，越低則黃色越淺。  
(2)中間上方區塊顯示目前所選擇的地區及性別之投保率，例如當選擇全國之合計投保率時，則如圖片所示。  
(3)中間下方區塊顯示目前所選擇縣市之人口性別比例  
(4)右邊下方區塊顯示目前所選擇縣市之年齡人口比例  
(5)右邊上方區塊顯示各縣市平均每人每年可支配所得，若選擇某一縣市時，該縣市會顯示與其他縣市不同之顏色  
儀表板左上方有一個Combo Box可以選擇縣市，預設為「全國」，另有三個Radio Button可以選擇性別，以呈現所選縣市之某性別之投保率  
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/Hsinchu_coverage_rate.png)  
![image](https://github.com/Suweihsiang/Small_Amount_Whole_Life_Insurance/blob/main/image/Hsinchu_female_coverage_rate.png)  
  
  
2.小額終老保險全國各縣市投保率分析  
  
為了要找出與各縣市投保率相關之原因，我使用了內政部人口速報、縣市重要指標網有關家庭收入之檔案，並使用爬蟲程式爬取各縣市郵局間數，以及參考壽險公會年報之各縣市保險機構間數，建構出特徵：郵局間數、保險機構間數、郵局+保險機構間數、男性人口比例、女性人口比例、幼年人口比例、青壯年人口比例、老年人口比例、平均每人每年可支配所得、平均每戶全年經常性支出、平均每戶全年經常性收入、平均每戶可支配所得、平均每戶消費支出、每戶可支配所得中位數，並看各個特徵與投保率之相關係數，以及個別特徵與投保率之散點圖，觀察個別特徵與投保率之間是否存在某種規律。  
  
由於建模之需求，我先將資料進行正規化，再透過Lasso演算法，使用不同alpha產生其所對應之係數，並將其繪製成折線圖，可以觀察到最後被篩選掉的特徵為平均每人每年可支配所得，前面相關係數圖也是該項特徵與投保率最為相關，故可知此項特徵與投保率之間存有反向之相關性。  
  
最後使用Lasso之最小角回歸算法進行特徵選擇，該算法並參考BIC進行模型選擇，最後選擇的模型為BIC最小者，被選擇之特徵為郵局間數、女性人口比例、青壯年人口比例，平均每人每年可支配所得、平均每戶全年經常性支出，並藉由這些特徵對投保率建構多元線性回歸模型，該模型之score約0.7089。