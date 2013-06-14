/*This first C++ program is a testcase for the common method 
 that we mean to use when timing parallel threads that are
 working with openmp.

 The code randomly generates a number of nrRand random numbers
 and sums them up.


 When calling the programme from the command line, the syntax will
 be

 <OBJECT> NUMBER_OF_NUMBERS NUMBER_OF_THREADS CHOICE_OF_FUNCTION
 **/
#include <stdlib.h>
#include <omp.h>
#include <stdio.h>
#include <time.h>
#include <string>

void sum(int nrRand) {
  int a[nrRand], theSum, i;
#pragma omp parallel for
  for (i = 0; i < nrRand; i++) {
    theSum += a[i];
  }
}

void genSum(int nrRand) {
  int a[nrRand], theSum, i;
  srand (time(NULL));

#pragma omp parallel for
for(  i=0;i<nrRand;i++) {
    a[i]=rand()%10000;
    theSum+=a[i];
  }
}

int main(int argc, char * argv[]) {
  int nrRand = atoi(argv[1]);
  int nrThreads = atoi(argv[2]);
  std::string option(argv[3]);

  omp_set_num_threads(nrThreads);
  double time;

  if (option == "sum") {
    time = omp_get_wtime();
    sum(nrRand);
    time = omp_get_wtime() - time;
  } else if (option == "genSum") {
    time = omp_get_wtime();
    genSum(nrRand);
    time = omp_get_wtime() - time;
  }

  printf("%d %d %lf\n", nrRand, nrThreads, time);

  return 0;

}
