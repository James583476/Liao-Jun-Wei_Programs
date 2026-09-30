#include <stdio.h>
#include <math.h>
#include <conio.h>

float x(int num,float list[]);
float s(int num,float list[],float x);
float u(int num,float s);
float X(float x,float u);
int n(float u);

//----------------------------------------------------
int main(void){
	
	int i,j;
	printf("A類不確定度計算\n\n");
	printf("數據數量:");
	scanf("%i",&i);
	printf("\n");
	float list[i];
	for(j=0;j<i;j++){
		printf("數據 %i : ",j+1); 
		scanf("%f",&list[j]);
	}                         //  ^數據紀錄^ 
	
	float xx = x(i,list);
	float ss = s(i,list,xx);
	float uu = u(i,ss);
	float XX = X(xx,uu);
	int nn = n(uu);
	
	printf("\n　　平均值(x):\t%f\n樣本標準差(s):\t%f\n\n　不確定度(u):\t%.*f\n最佳估計值(X):\t%.*f\n\n　　 測量結果:\t%.*f ±%.*f",xx,ss,nn,uu,nn,XX,nn,XX,nn,uu);
	getch();
	return 0;
} 

//----------------------------------------------平均值
float x(int num,float list[]){
	float total=0;
	for(int i=0;i<num;i++){
		total+=list[i];
	}
	return total/num;
}

//------------------------------------------樣本標準差
float s(int num,float list[],float x){
	if(num<2) return 0;
	float total = 0;
	for(int i=0;i<num;i++){
		total+=(list[i]-x)*(list[i]-x);
	}
	total /= (num-1);
	return sqrtf(total);
}

//--------------------------------------------不確定度
float u(int num,float s){
	float uu = s/sqrtf(float(num));
	float i,j;
	for(i=1;;i/=10){
		j=i;
		if(uu/i>=1) break;
	}
	j*=0.01;
	uu/=j;
	if(int(uu)%10!=0) return j*((int(uu)/10)*10+10);
	else return j*((int(uu)/10)*10);
}

//------------------------------------------最佳估計值
float X(float x,float u){
	float i,j;
	for(i=1;;i/=10){
		j=i;
		if(u/i>=1) break;
	}
	j*=0.01;
	x/=j;
	if(int(x)%10>=5) return j*(int(x)+10);
	else return j*(int(x));
}

//--------------------------------------------保留位數
int n(float u){
	float i;
	int j=-1;
	for(i=10;;i/=10){
		if(u/i>=1) break;
		j+=1;
	}
	j+=1;
	return j;
}
