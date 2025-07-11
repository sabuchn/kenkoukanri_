import streamlit as st
import pandas as pd
import numpy as np

st.title("健康的な食事管理をしよう！")

#摂取カロリーの算出
num_hight=st.number_input("身長を入力してください:",min_value=0,max_value=200,step=0)
st.write("結果:",num_hight)
num_weight=st.number_input("体重を入力してください:",min_value=0,max_value=150,step=0)
st.write("結果：",num_weight)
selectbox=st.selectbox("選んでください:",["あんまり運動しない","運動するよ","めっちゃ運動する"])
st.write("結果：",selectbox)
selectbox_moku=st.selectbox("あなたの目的は:",["体型維持","痩せたい！"])
st.write("結果:",selectbox_moku)

if selectbox=="あんまり運動しない":
    move_today=32.5
elif selectbox=="運動するよ":
    move_today=37.5
else:
    move_today=40
#摂取目標の計算
kcal_moku=num_weight*move_today
st.write("一日の摂取カロリーの目標:",kcal_moku)
#PFCバランスの計算
p_gram=int((kcal_moku*0.2)/4)
F_gram=int((kcal_moku*0.25)/9)
C_gram=int((kcal_moku*0.55)/4)
st.write(f"p: {p_gram}F:{F_gram}C:{C_gram}")

#実際の摂取量、コメント表示
P_today=st.number_input("今日一日で実際に、摂取したプロテイン量を入力してください(P):",min_value=0,max_value=200,step=0)
F_today=st.number_input("今日一日で実際に、摂取した脂質を入力してください(f):",min_value=0,max_value=200,step=0)
C_today=st.number_input("今日一日で実際に、摂取した炭水化物を入力してください(C):",min_value=0,max_value=200,step=0)
d = p_gram -P_today
e = F_gram - F_today
f = C_gram - C_today
a1 = int(P_today /p_gram*100)
b1 = int(F_today/F_gram*100)
c1 = int(C_today/C_gram*100)
st.write(f" p残り{d}g,達成率{a1}%, f残り{e}g,達成率{b1}%, c残り{f}g,達成率{c1}%")

def calculate_pfc_balance(P_today, F_today, C_today, total_calories=None):
 #PFCバランスの計算式
    protein_kcal = P_today* 4
    fat_kcal = F_today * 9
    carb_kcal = C_today * 4
 
    # 総カロリーが未入力ならP+F+Cの合計から計算
    if total_calories is None:
        total_calories = protein_kcal + fat_kcal + carb_kcal
 
    # 割合を計算
    protein_ratio = (protein_kcal / 2600) * 100
    fat_ratio = (fat_kcal / 2600) * 100
    carb_ratio = (carb_kcal / 2600) * 100

    return total_calories,protein_kcal,fat_kcal,carb_kcal,protein_ratio,fat_ratio,carb_ratio
 
# 結果を表示
total_calories,protein_kcal,fat_kcal,carb_kcal,protein_ratio,fat_ratio,carb_ratio=calculate_pfc_balance(P_today, F_today, C_today, total_calories=None)
    
st.write("===== PFCバランス結果 =====")
st.write(f"総カロリー: {total_calories:.2f} kcal")
st.write(f"たんぱく質: {P_today}g ({protein_kcal} kcal, {protein_ratio:.1f}%)")
st.write(f"脂質: {F_today}g ({fat_kcal} kcal, {fat_ratio:.1f}%)")
st.write(f"炭水化物: {C_today}g ({carb_kcal} kcal, {carb_ratio:.1f}%)")

#達成率棒グラフの表示
data=pd.DataFrame({'達成率':['p','F','C'],'count':[P_today,F_today,C_today]})
st.bar_chart(data.set_index('達成率'))

#円グラフ
import matplotlib.pyplot as plt
 
plt.rcParams['font.family'] = 'BIZ UDGothic'
plt.rcParams['font.weight'] = 'bold'
 
labels = ["たんぱく質", "脂肪", "炭水化物"]
sizes = [20, 25, 55]  # 割合（合計100になるように）
 
plt.figure(figsize=(6,6))  
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  
plt.title("PFCバランス")

plt.savefig("plot_image.png",dpi=300)
st.image("plot_image.png")