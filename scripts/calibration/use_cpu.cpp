// compile with g++ -fopenmp ./use_cpu.cpp -o use_cpu
#include <time.h>
#include <omp.h>

void use_cpu(double secs){
	time_t start = time(0);

	while (difftime(time(0),start) < secs)
		int a = 1 + 1;
}

int main(){
	// the way we call the function is the textbook example of how to
	// NOT use OpenMP because each available processor will start to
	// run the same function. However, since the program is meant to
	// serve as a piece of code that uses the all the available cpu,
	// this is a good way to achieve our goal.
	#pragma omp parallel
	use_cpu(5.0);
	return 0;
}
