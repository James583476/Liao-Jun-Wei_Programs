#include <iostream>
using namespace std;

const int ARRAY_SIZE = 3;
int run = 1;
int Array[ARRAY_SIZE][ARRAY_SIZE] = { {0,0,0},{0,0,0},{0,0,0} };

void PrintArray(const int list[ARRAY_SIZE][ARRAY_SIZE]);
bool PlayerEvent(const int pos[2],int player);
void Msg_get_pos(int player,int pos[]);
int CheckWin(void);

int main() {
	int player;
	int winer;
	while(true){
		PrintArray(Array);
		(run % 2 == 1) ? player = 1 : player = -1;
		int pos[2];
		Msg_get_pos(player,pos);
		if (!PlayerEvent(pos,player)){
			cout << "position error" << endl;
			continue;
		}
		winer = CheckWin();
		if (!(winer == 2)) {
			if (winer == 1)
				cout << "Player O win!" << endl;
			else if (winer == -1)
				cout << "Player X win!" << endl;
			else
				cout << "Draw!" << endl;
			break;
		}
		run++;
	}
	return 0;
}

void PrintArray(const int list[ARRAY_SIZE][ARRAY_SIZE]) {
	cout  << endl; 
	for (int i = 0; i < ARRAY_SIZE; i++) {
		cout << " ";
		for (int j = 0; j < ARRAY_SIZE; j++) {
			if (list[i][j] == 0)
				cout << "+";
			else if (list[i][j] == 1)
				cout << "O";
			else
				cout << "X";
			cout << " ";
		}
		cout << endl;
	}
	cout << endl;
}

bool PlayerEvent(const int pos[2],int player){
	if (!(0 <= pos[0] && pos[0] <= 2 && 0 <= pos[1] && pos[1] <= 2 && Array[pos[1]][pos[0]] == 0))
		return false;
	Array[pos[1]][pos[0]] = player;
	return true;
}

void Msg_get_pos(int player,int pos[]) {
	if (player == 1)
		cout << "Player O turn, please input position (x, y): ";
	else
		cout << "Player X turn, please input position (x, y): ";
	cin >> pos[0] >> pos[1];
}

int CheckWin(void) {
	int row[3],col[3],m[2];
	for (int i = 0;i < ARRAY_SIZE; i++) {
		row[i] = Array[i][0] + Array[i][1] + Array[i][2];
		col[i] = Array[0][i] + Array[1][i] + Array[2][i];
	}
	m[0] = Array[0][0] + Array[1][1] + Array[2][2];
	m[1] = Array[0][2] + Array[1][1] + Array[2][0];
	for (int i = 0; i < ARRAY_SIZE; i++) {
		if (row[i] == 3 || col[i] == 3)
			return 1;
		else if (row[i] == -3 || col[i] == -3)
			return -1;
	}
	if (m[0] == 3 || m[1] == 3)
		return 1;
	else if (m[0] == -3 || m[1] == -3)
		return -1;
	if (run >= 9)
		return 0;
	return 2;
}
