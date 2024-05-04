#Определение газовой постоянной газа. Định nghĩa Rg
import numpy as np
import pandas as pd
import math
try:
	Stand=pd.read_csv('data\Standard_Atm.csv')
	Teplo_Prod=pd.read_csv('data\Teplo_Product.csv')
	Teplo_Voz=pd.read_csv('data\Teplo_Vozdux.csv')
except:
	Stand=pd.read_csv('AGTEPyth\data\Standard_Atm.csv')
	Teplo_Prod=pd.read_csv('AGTEPyth\data\Teplo_Product.csv')
	Teplo_Voz=pd.read_csv('AGTEPyth\data\Teplo_Vozdux.csv')
def R_g(alpha_local,L0):
	R_al1=0.2901
	R_B=0.287
	R_g=(alpha_local-1)*L0*R_B/(1+alpha_local*L0)+(1+L0)*R_al1/(1+alpha_local*L0)
	return R_g

#Định nghĩa CpmiB() - hàm nhiệt dung riêng đẳng tích trung bình của không khí trong khoảng nhiệt độ xác định từ 0 đến giá trị t(0C) bằng PP nội suy tuyến tính
def CpmiB(t_0C):
	for t_j in Teplo_Voz['t(0C)']:
		if 0<=t_0C-t_j<50:
			n=list(Teplo_Voz['t(0C)']).index(t_j)
			CpmiB_j=Teplo_Voz['CpmiB'][n]
			CpmiB_j1=Teplo_Voz['CpmiB'][n+1]
			CpmiB=CpmiB_j+(CpmiB_j1-CpmiB_j)*(t_0C-t_j)/50
			return CpmiB

#Định nghĩa CpmsB() - hàm nhiệt dung riêng đẳng tích trung bình logarit của không khí trong khoảng nhiệt độ xác định từ 0 đến giá trị T(K) bằng PP nội suy tuyến tính
def CpmsB(T_K):
	for T_j in Teplo_Voz['T(K)']:
		if 0<=T_K-T_j<50:
			n=list(Teplo_Voz['T(K)']).index(T_j)
			CpmsB_j=Teplo_Voz['CpmsB'][n]
			CpmsB_j1=Teplo_Voz['CpmsB'][n+1]
			CpmsB=CpmsB_j+(CpmsB_j1-CpmsB_j)*(T_K-T_j)/50
			return CpmsB

#Định nghĩa Cpmi_al1() - hàm nhiệt dung riêng đẳng tích trung bình của SP cháy trong khoảng nhiệt độ xác định từ 0 đến giá trị t(0C) bằng PP nội suy tuyến tính
def Cpmi_al1(t_0C):
	for t_j in Teplo_Prod['t(0C)']:
		if 0<=t_0C-t_j<50:
			n=list(Teplo_Prod['t(0C)']).index(t_j)
			Cpmi_j=Teplo_Prod['Cpmi_al1'][n]
			Cpmi_j1=Teplo_Prod['Cpmi_al1'][n+1]
			Cpmi=Cpmi_j+(Cpmi_j1-Cpmi_j)*(t_0C-t_j)/50
			return Cpmi

#Định nghĩa Cpms_al1() - hàm nhiệt dung riêng đẳng tích trung bình logarit của SP cháy trong khoảng nhiệt độ xác định từ 0 đến giá trị T(K) bằng PP nội suy tuyến tính
def Cpms_al1(T_K):
	for T_j in Teplo_Prod['T(K)']:
		if 0<=T_K-T_j<50:
			n=list(Teplo_Prod['T(K)']).index(T_j)
			Cpms_j=Teplo_Prod['Cpms_al1'][n]
			Cpms_j1=Teplo_Prod['Cpms_al1'][n+1]
			Cpms=Cpms_j+(Cpms_j1-Cpms_j)*(T_K-T_j)/50
			return Cpms

#Định nghĩa C_pmiB() - hàm nhiệt dung riêng đẳng tích trung bình của không khí trong khoảng nhiệt độ bất kỳ từ t1(0C) đến giá trị t2(0C) bằng PP nội suy tuyến tính

def C_pmiB(T1,T2):
	if T1==T2:
		T2+=0.0000001	
	C_pmiB=((CpmiB(T1-273.15))*(T1-273.15)-(CpmiB(T2-273.15))*(T2-273.15))/(T1-T2)
	return C_pmiB

#Định nghĩa C_pmsB() - hàm nhiệt dung riêng đẳng tích trung bình logarit của không khí trong khoảng nhiệt độ bất kỳ từ T1(K) đến giá trị T2(K) bằng PP nội suy tuyến tính

def C_pmsB(T1,T2):
	if T1==T2:
		T2+=0.0000001
	C_pmsB=(CpmsB(T1)*(math.log(T1/273.15))-CpmsB(T2)*(math.log(T2/273.15)))/(math.log(T1/T2))
	return C_pmsB

#Định nghĩa C_pmi_al1() - hàm nhiệt dung riêng đẳng tích trung bình của SP cháy trong khoảng nhiệt độ bất kỳ từ T1(K) đến giá trị T2(K) bằng PP nội suy tuyến tính
def C_pmi_al1(T1,T2):
	if T1==T2:
		T2+=0.0000001
	C_pmi_al1=(Cpmi_al1(T2-273.15)*(T2-273.15)-Cpmi_al1(T1-273.15)*(T1-273.15))/(T2-T1)
	return C_pmi_al1

#Định nghĩa C_pms_al1() - hàm nhiệt dung riêng đẳng tích trung bình logarit của SP cháy trong khoảng nhiệt độ bất kỳ từ T1(K) đến giá trị T2(K) bằng PP nội suy tuyến tính
def C_pms_al1(T1,T2):
	if T1==T2:
		T2+=0.0000001
	C_pms_al1=(Cpms_al1(T2)*math.log(T2/273.15)-Cpms_al1(T1)*math.log(T1/273.15))/(math.log(T2/T1))
	return C_pms_al1

#Định nghĩa C_pmig() - hàm nhiệt dung riêng đẳng tích trung bình của khí công tác trong khoảng nhiệt độ bất kỳ từ T1(K) đến giá trị T2(K) bằng PP nội suy tuyến tính
def C_pmig(T1,T2,alpha_local,L0):
	C_pmig=(alpha_local-1)*L0*C_pmiB(T1,T2)/(1+alpha_local*L0)+(1+L0)*C_pmi_al1(T1,T2)/(1+alpha_local*L0)
	return C_pmig

#Định nghĩa C_pmsg() - hàm nhiệt dung riêng đẳng tích trung bình logarit của khí công tác trong khoảng nhiệt độ bất kỳ từ T1(K) đến giá trị T2(K) bằng PP nội suy tuyến tính
def C_pmsg(T1,T2,alpha_local,L0):
	C_pmsg=(alpha_local-1)*L0*C_pmsB(T1,T2)/(1+alpha_local*L0)+(1+L0)*C_pms_al1(T1,T2)/(1+alpha_local*L0)
	return C_pmsg

'''
print('CpmiB = '+str(CpmiB(260)))#In kiểm tra
print('CpmsB = '+str(CpmsB(500)))#In kiểm tra
print('Cpmi_al1 = '+str(Cpmi_al1(260)))#In kiểm tra
print('Cpms_al1 = '+str(Cpms_al1(500)))#In kiểm tra
print('C_pmiB = '+str(C_pmiB(300,600)))#In kiểm tra so sánh kết quả tính với công thức trong khoảng nhiệt độ xác định
print('C_pmsB = '+str(C_pmsB(288,445)))#In kiểm tra so sánh kết quả tính với công thức trong khoảng nhiệt độ xác định
print('C_pmi_al1 = '+str(C_pmi_al1(300,500)))#In kiểm tra so sánh kết quả tính với công thức trong khoảng nhiệt độ xác định
print('C_pms_al1 = '+str(C_pms_al1(300,500)))#In kiểm tra so sánh kết quả tính với công thức trong khoảng nhiệt độ xác định
print('C_pmig = '+str(C_pmig(300,500,3,15)))#In kiểm tra so sánh kết quả tính với công thức trong khoảng nhiệt độ xác định
print('C_pmsg = '+str(C_pmsg(300,500,3,15)))#In kiểm tra so sánh kết quả tính với công thức trong khoảng nhiệt độ xác định'''
