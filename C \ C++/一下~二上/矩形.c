# include <stdio.h>

int XY1(int x,int y);			//第一象限 
int XY2(int x,int y);			//第二象限  
int XY3(int x,int y);			//第三象限 
int XY4(int x,int y);			//第四象限 

int main(int x,int y){
	int i=-1;
	printf("平面座標(整數,空格分隔): ");
	for(;;){
		scanf("%i %i",&x,&y);
		printf("\n=======================\n");
		if(x >= 0 && y >= 0) XY1(x,y);
		if(x <= 0 && y >= 0) XY2(x,y);
		if(x <= 0 && y <= 0) XY3(x,y);
		if(x >= 0 && y <= 0) XY4(x,y);
		printf("\n\n重複執行? bool :");
		scanf("%i",&i);
		if(i!=0){
			printf("(x,y) :");
			continue;
		}
		else break;
	}
	return 0;
}

//第一象限 
int XY1(int x,int y){
	int i = y;
	int j;
	printf(" Y\n\n");
	for(i;i>0;i--){
		if(i%5==0) printf("%02i ",i/5);
		else printf("   ");
		for(j=1;j<=x;j++){	//|幾 
			printf("# ");	//|何
		}					//|輸
		printf("\n");		//|出
	} 
	for(i=0;i<=x;i++){
		if(i%5==0 && i!=0) printf("%02i",i/5);
		else {
			if(i==0) printf("00 "); 
			else printf("  ");
		}
	}
	printf(" X");
	return 0;
}
 
//第二象限
int XY2(int x,int y){
	int i;
	int j;
	for(i=0;i>x;i--){
		printf("  ");
	}
	printf("   Y\n\n");
	for(i=y;i>0;i--){
		printf("   ");		//負號緩衝 
		for(j=-1;j>=x;j--){	//|幾
			printf("# ");	//|何
		}					//|輸出 
		if(i%5==0) printf("%02i",i/5);
		printf("\n");
	} 
	printf("X ");
	for(i=x;i<=0;i++){
		if(i%5==0 && i!=0) printf("\b%03i",i/5);
		else {
			if(i==0) printf(" 00");
			else printf("  ");
		}
	}
	return 0;
}

//第三象限 
int XY3(int x,int y){
	int i,j;
	printf("X ");
	 for(i=x;i<=0;i++){
		if(i%5==0 && i!=0) printf("\b%03i",i/5);
		else {
			if(i==0) printf(" 00");
			else printf("  ");
		}
	}
	printf("\n");
	for(i=-1;i>=y;i--){
		printf("   ");
		for(j=-1;j>=x;j--){	//|幾 
			printf("# ");	//|何
		}					//|輸出 
		if(i%5==0) printf("%03i",i/5);
		else printf("   "); 
		printf("\n");
	}
	printf("\n");
	for(i=0;i>x;i--){
		printf("  ");
	}
	printf("   Y");
	return 0;
}

//第四象限 
int XY4(int x,int y){
	int i,j;
	printf(" "); 			//負號緩衝 
	 for(i=0;i<=x;i++){
		if(i%5==0) printf("%02i",i/5);
		else printf("  ");
	}
	printf(" X\n");
	for(i=-1;i>=y;i--){
		if(i%5==0) printf("%03i",i/5);
		else printf("   "); 
		for(j=1;j<=x;j++){	//|幾 
			printf("# ");	//|何
		}					//|輸
		printf("\n");		//|出
	}
	printf("\n Y");
	return 0;
}  
