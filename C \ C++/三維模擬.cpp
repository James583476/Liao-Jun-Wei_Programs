#include <iostream>
#include <cmath>
using namespace std;

class Vec3 {
public:
	float vec3[3];

	Vec3() : vec3{0,0,0} {}

	Vec3(float x, float y, float z): vec3{ x,y,z } {}

	Vec3(const float vec[3]) : vec3{ vec[0],vec[1],vec[2] } {}
	
	float& x()
	{
		return vec3[0];
	}
	float& y()
	{
		return vec3[1];
	}
	float& z()
	{
		return vec3[2];
	}
	const float& x() const
	{
		return vec3[0];
	}
	const float& y() const
	{
		return vec3[1];
	}
	const float& z() const
	{
		return vec3[2];
	}

	Vec3 operator+(const Vec3& v) const
	{
		return Vec3(x() + v.x(), y() + v.y(), z() + v.z());
	}
	Vec3 operator-(const Vec3& v) const
	{
		return Vec3(x() - v.x(), y() - v.y(), z() - v.z());
	}
	Vec3 operator*(float scalar) const
	{
		return Vec3(x() * scalar, y() * scalar, z() * scalar);
	}
	Vec3 operator/(float scale) const
	{
		return Vec3(x() / scale,y() / scale,z() / scale);
	}
	float dot(const Vec3& v) const			// dot
	{
		return x() * v.x() + y() * v.y() + z() * v.z();
	}
	Vec3 cross(const Vec3& v) const		//cross
	{
		return Vec3(
			y() * v.z() - z() * v.y(),
			z() * v.x() - x() * v.z(),
			x() * v.y() - y() * v.x()
		);
	}
	float norm3() const
	{
		return sqrt( x() * x() + y() * y() + z() * z());
	}
};

class Vec4 {
public:
	float vec4[4];
	Vec4() : vec4{0,0,0,1} {}
	Vec4(float x, float y, float z, float w = 1) : vec4{x,y,z,w} {}
	Vec4(const float vec[4]) : vec4{vec[0],vec[1],vec[2],vec[3]} {}
	
	float& x()
	{
		return vec4[0];
	}
	float& y()
	{
		return vec4[1];
	}
	float& z()
	{
		return vec4[2];
	}
	float& w()
	{
		return vec4[3];
	}
	const float& x() const
	{
		return vec4[0];
	}
	const float& y() const
	{
		return vec4[1];
	}
	const float& z() const
	{
		return vec4[2];
	}
	const float& w() const
	{
		return vec4[3];
	}

	Vec3 trans2v3() const
	{
		return Vec3( x()/w(), y() / w(), z() / w());
	}
};

class Mat4 {
public	:
	float mat[4][4];
	Mat4() :mat{}
	{
		for (int i = 0; i < 4; i++)
			mat[i][i] = float(1);
	}
	Mat4(const float mat[4][4]) {
		for (int i = 0; i < 4; i++){
			for (int j = 0; j < 4; j++)
				this->mat[i][j] = mat[i][j];
		}
	}
	Vec4 operator*(const Vec4& v) const
	{
		float vec[4],temp;
		for (int i = 0; i < 4; i++){
			temp = 0;
			for (int j = 0; j < 4; j++)
				temp += mat[i][j] * v.vec4[j];
			vec[i] = temp;
		}
		return Vec4(vec);
	}
	Mat4 operator*(const Mat4& mat2) const
	{
		float back_mat[4][4] = {};
		for (int i = 0; i < 4; i++) {
			for (int j = 0; j < 4; j++){
				for (int k = 0; k < 4; k++)
					back_mat[i][j] += this->mat[i][k] * mat2.mat[k][j];
			}
		}
		return Mat4(back_mat);
	}
};

const float PI = 3.14159;
const int W = 50;
const int H = 50;
const float far = 100;
const float near = 0.1;
float FOV = 60;
Vec3 C_eye(0.0, 4.0, 8.0);
Vec3 C_target(0,0,0);
const Vec3 C_up(0, 1, 0);
int screen[H][W] = {};
Vec4 cube[8] = {
	Vec4(  1,-1,  1),
	Vec4(-1,-1,  1),
	Vec4(-1,-1,-1),
	Vec4(  1,-1,-1),
	Vec4(  1,  1,-1),
	Vec4(  1,  1,  1),
	Vec4(-1,  1,  1),
	Vec4(-1,  1,-1)
};
int run = 1;

Mat4 Model_matrix(const Vec3& trans = Vec3(), const float scale = 1, const Vec3& rad = Vec3());
Mat4 View_matrix(const Vec3&, const Vec3&, const Vec3&);
Mat4 Project_matrix(const float, const float, const float, const float);
void update(const Vec4&,const Mat4&);
void Print_screen();

int main()
{
	int rad = 45*PI/180.0;
	while (run)
	{
		Mat4 PVM = Mat4(Project_matrix(near, far, FOV, float(W) / float(H)) * View_matrix(C_eye,C_target,C_up) * Model_matrix(Vec3(),1,Vec3(0,rad,0)));
		for (int i = 0; i < 8; i++)
			update(cube[i], PVM);
		Print_screen();
		run--;
		rad += 10*PI/180.0;
	}
	return 0;
}

Mat4 Model_matrix(const Vec3& trans, const float scale, const Vec3& rad)
{
	float matS[4][4] = {
		{scale,0,0,0},
		{0,scale,0,0},
		{0,0,scale,0},
		{0,0,0,1}
	};
	Mat4 S(matS);
	float matT[4][4] = {
		{1,0,0,trans.x()},
		{0,1,0,trans.y()},
		{0,0,1,trans.z()},
		{0,0,0,1}
	};
	Mat4 T(matT);
	float mat0[4][4] = {
		{1,0,0,0},
		{0, cos(rad.x()), -sin(rad.x()), 0},
		{0, sin(rad.x()),   cos(rad.x()), 0},
		{0,0,0,1}
	};
	float mat1[4][4] = {
		{ cos(rad.y()), 0,  sin(rad.y()), 0},
		{0,1,0,0},
		{-sin(rad.y()), 0, cos(rad.y()), 0},
		{0,0,0,1}
	};
	float mat2[4][4] = {
		{cos(rad.z()), -sin(rad.z()), 0, 0},
		{sin(rad.z()),   cos(rad.z()), 0, 0},
		{0,0,1,0},
		{0,0,0,1}
	};
	Mat4 Rx(mat0);
	Mat4 Ry(mat1);
	Mat4 Rz(mat2);
	Mat4 R(Rx * Ry * Rz);			// the firm structure, do not change arrange until using "4 element model"
	return T * R * S;
}

Mat4 View_matrix(const Vec3& eye, const Vec3& target, const Vec3& up)
{
	Vec3 vz((eye - target)/ (eye - target).norm3());		// right hand law
	Vec3 up_cross_z(up.cross(vz));
	Vec3 vx(up_cross_z / up_cross_z.norm3());
	Vec3 z_cross_x(vz.cross(vx));
	Vec3 vy(z_cross_x / z_cross_x.norm3());
	float mat[4][4] = {
		{vx.x(), vx.y(), vx.z(), -vx.dot(eye)},
		{vy.x(), vy.y(), vy.z(), -vy.dot(eye)},
		{vz.x(), vz.y(), vz.z(), -vz.dot(eye)},
		{0,0,0,1}
	};
	return Mat4(mat);
}

Mat4 Project_matrix(const float near, const float far, const float fov, const float aspect)
{
	float fov_rad = fov * PI / 180;
	float t = near * tan(fov_rad / 2);
	float r = t * aspect;
	float mat[4][4] = {
		{near/r,0,0,0},
		{0,near/t,0,0},
		{0,0,-(far + near) / (far - near),-2 * far * near / (far - near)},
		{0,0,-1,0}		// right hand law
	};
	return Mat4(mat);
}

void update(const Vec4& pos,const Mat4& PVM)
{
	Vec4 new_pos = PVM * pos;
	if (new_pos.w() <= 0)
		return;
	Vec3  ndc = new_pos.trans2v3();
	int x = int((ndc.x() + 1.0f) * 0.5f * W);
	int y = int((1.0f - ndc.y()) * 0.5f * H);
	if (x < 0 || x >= W || y < 0 || y >= H)		//	edge check
		return;
	screen[y][x] = 1;
}

void Print_screen()
{
	//system("cls");
	for (int i = 0; i < H; i++) {
		for (int j = 0; j < W; j++) {
			(screen[i][j] == 1) ? cout << "#" : cout << " ";
			screen[i][j] = 0;
		}
		cout << endl;
	}
}
