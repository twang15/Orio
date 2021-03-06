#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

#define ceild(n,d)  ceil(((double)(n))/((double)(d)))
#define floord(n,d) floor(((double)(n))/((double)(d)))
#define max(x,y)    ((x) > (y)? (x) : (y))
#define min(x,y)    ((x) < (y)? (x) : (y))

double L[N][N];
double U[N][N];
double A[N][N+13];

void print_array()
{
  int i, j;

  for (i=0; i<N; i++) {
    for (j=0; j<N; j++) {
      fprintf(stderr, "%lf ", round(A[i][j]));
      if (j%80 == 79) fprintf(stderr, "\n");
    }
    fprintf(stderr, "\n");
  }
  fprintf(stderr, "\n");
}

void init_arrays()
{
  int i, j, k;

  /* have to initialize this matrix properly to prevent                                              
   * division by zero                                                                                 
   */
  for (i=0; i<N; i++) {
    for (j=0; j<N; j++) {
      L[i][j] = 0.0;
      U[i][j] = 0.0;
    }
  }

  for (i=0; i<N; i++) {
    for (j=0; j<=i; j++) {
      L[i][j] = i+j+1;
      U[j][i] = i+j+1;
    }
  }

  for (i=0; i<N; i++) {
    for (j=0; j<N; j++) {
      for (k=0; k<N; k++) {
	A[i][j] += L[i][k]*U[k][j];
      }
    }
  }
}

double rtclock()
{
  struct timezone tzp;
  struct timeval tp;
  int stat;
  gettimeofday (&tp, &tzp);
  return (tp.tv_sec + tp.tv_usec*1.0e-6);
}

int main()
{
  init_arrays();

  double annot_t_start=0, annot_t_end=0, annot_t_total=0;
  int annot_i;

  for (annot_i=0; annot_i<REPS; annot_i++)
    {
      annot_t_start = rtclock();


/*@ begin PerfTuning (         
  def build 
  { 
    arg build_command = 'icc -O3 -openmp -I/usr/local/icc/include -lm'; 
  } 
    
  def performance_counter          
  { 
    arg repetitions = 1; 
  }

  def performance_params 
  {
#    param T1_1[] = [1,16,32,64,128];
#    param T1_2[] = [1,16,32,64,128];
#    param T1_3[] = [1,16,32,64,128];
#    param T2_1[] = [1,4,8,16,32];
#    param T2_2[] = [1,4,8,16,32];
#    param T2_3[] = [1,4,8,16,32];

    param T1_1[] = [64];
    param T1_2[] = [256];
    param T1_3[] = [64];
    param T2_1[] = [1];
    param T2_2[] = [1];
    param T2_3[] = [1];

    constraint c1 = (T1_1*T2_1<=1024 and T1_1*T2_1<=1024 and T1_1*T2_1<=1024);
    constraint c2 = ((T1_1 == T1_3) and (T2_1 == T2_3));

    param U1[] = [1];
    param U2[] = [1];
    param U3[] = [7];

    constraint c3 = (U1*U2*U3<=512);

    param PERM[] = [
      #[0,1,2],
      #[0,2,1],
      #[1,0,2],
      #[1,2,0],
      [2,0,1],
      #[2,1,0],
      ];

    param PAR[] = [True];
    param SCREP[] = [False];
    param IVEC[] = [True];
  }

  def search 
  { 
    arg algorithm = 'Exhaustive'; 
#    arg algorithm = 'Simplex'; 
#    arg time_limit = 5;
#    arg total_runs = 1;
  } 
   
  def input_params 
  {
    param N[] = [1024];
  }

  def input_vars
  {
    arg decl_file = 'decl_code.h';
    arg init_file = 'init_code.c';
  }
) @*/

/**-- (Generated by Orio) 
Best performance cost: 
  0.201184 
Tuned for specific problem sizes: 
  N = 1024 
Best performance parameters: 
  IVEC = True 
  PAR = True 
  PERM = [2, 0, 1] 
  SCREP = False 
  T1_1 = 64 
  T1_2 = 256 
  T1_3 = 64 
  T2_1 = 1 
  T2_2 = 1 
  T2_3 = 1 
  U1 = 1 
  U2 = 1 
  U3 = 7 
--**/

 

register int i,j,k;
register int c1t, c2t, c3t, c4t, c5t, c6t, c7t, c8t, c9t, c10t, c11t, c12t;
register int newlb_c1, newlb_c2, newlb_c3, newlb_c4, newlb_c5, newlb_c6,
  newlb_c7, newlb_c8, newlb_c9, newlb_c10, newlb_c11, newlb_c12;
register int newub_c1, newub_c2, newub_c3, newub_c4, newub_c5, newub_c6,
  newub_c7, newub_c8, newub_c9, newub_c10, newub_c11, newub_c12;


/*@ begin PolySyn(    
  parallel = PAR;
  tiles = [T1_1,T1_2,T1_3,T2_1,T2_2,T2_3];
  permut = PERM;
  unroll_factors = [U1,U2,U3];
  scalar_replace = SCREP;
  vectorize = IVEC;
    
  profiling_code = 'lu_profiling.c';
  compile_cmd = 'gcc';
  compile_opts = '-lm';
  ) @*/

#include <math.h>
#include <assert.h>

#define ceild(n,d)  ceil(((double)(n))/((double)(d)))
#define floord(n,d) floor(((double)(n))/((double)(d)))
#define max(x,y)    ((x) > (y)? (x) : (y))
#define min(x,y)    ((x) < (y)? (x) : (y))

		
	int c1, c2, c3, c4, c5, c6, c7, c8, c9;

	register int lb, ub, lb1, ub1, lb2, ub2;
/* Generated from PLuTo-produced CLooG file by CLooG v0.14.1 64 bits in 0.05s. */
for (c1=-1;c1<=floord(5*N-9,256);c1++) {
	lb1=max(max(ceild(32*c1-127,160),ceild(64*c1-N+2,64)),0);
	ub1=min(floord(64*c1+63,64),floord(N-1,256));
#pragma omp parallel for shared(c1,lb1,ub1) private(c2,c3,c4,c5,c6,c7,c8,c9)
	for (c2=lb1; c2<=ub1; c2++) {
    for (c3=max(ceild(32*c1-32*c2-1953,2016),ceild(32*c1-32*c2-31,32));c3<=floord(N-1,64);c3++) {
      if (c1 == c2+c3) {
        for (c7=max(64*c3,0);c7<=min(min(N-2,64*c3+62),256*c2+254);c7++) {
          for (c8=max(c7+1,256*c2);c8<=min(N-1,256*c2+255);c8++) {
            A[c7][c8]=A[c7][c8]/A[c7][c7] ;
            for (c9=c7+1;c9<=min(N-1,64*c3+63);c9++) {
              A[c9][c8]=A[c9][c8]-A[c9][c7]*A[c7][c8] ;
            }
          }
        }
      }
/*@ begin Loop(
transform Composite(
permut = [['c9', 'c7', 'c8']],
  regtile = (['c7', 'c8', 'c9'],[1, 1, 7]),
  scalarreplace = (False, 'double'),
  vector = (True, ['ivdep','vector always']))

      for (c7=max(0,64*c1-64*c2);c7<=min(min(256*c2+254,64*c1-64*c2+63),64*c3-1);c7++) {
        for (c8=max(c7+1,256*c2);c8<=min(256*c2+255,N-1);c8++) {
          for (c9=64*c3;c9<=min(N-1,64*c3+63);c9++) {
            A[c9][c8]=A[c9][c8]-A[c9][c7]*A[c7][c8] ;
          }
        }
      }

) @*/{
  for (c9t=64*c3; c9t<=min(N-1,64*c3+63)-6; c9t=c9t+7) {
    for (c7=max(0,64*c1-64*c2); c7<=min(min(256*c2+254,64*c1-64*c2+63),64*c3-1); c7++ ) {
      register int cbv_1, cbv_2;
      cbv_1=max(c7+1,256*c2);
      cbv_2=min(256*c2+255,N-1);
#pragma ivdep
#pragma vector always
      for (c8=cbv_1; c8<=cbv_2; c8++ ) {
        A[c9t][c8]=A[c9t][c8]-A[c9t][c7]*A[c7][c8];
        A[(c9t+1)][c8]=A[(c9t+1)][c8]-A[(c9t+1)][c7]*A[c7][c8];
        A[(c9t+2)][c8]=A[(c9t+2)][c8]-A[(c9t+2)][c7]*A[c7][c8];
        A[(c9t+3)][c8]=A[(c9t+3)][c8]-A[(c9t+3)][c7]*A[c7][c8];
        A[(c9t+4)][c8]=A[(c9t+4)][c8]-A[(c9t+4)][c7]*A[c7][c8];
        A[(c9t+5)][c8]=A[(c9t+5)][c8]-A[(c9t+5)][c7]*A[c7][c8];
        A[(c9t+6)][c8]=A[(c9t+6)][c8]-A[(c9t+6)][c7]*A[c7][c8];
      }
    }
  }
  for (c9=c9t; c9<=min(N-1,64*c3+63); c9=c9+1) {
    for (c7=max(0,64*c1-64*c2); c7<=min(min(256*c2+254,64*c1-64*c2+63),64*c3-1); c7++ ) {
      register int cbv_3, cbv_4;
      cbv_3=max(c7+1,256*c2);
      cbv_4=min(256*c2+255,N-1);
#pragma ivdep
#pragma vector always
      for (c8=cbv_3; c8<=cbv_4; c8++ ) {
        A[c9][c8]=A[c9][c8]-A[c9][c7]*A[c7][c8];
      }
    }
  }
}
/*@ end @*/

      if ((-c1 == -c2-c3) && (c1 <= min(floord(320*c2+191,64),floord(64*c2+N-65,64)))) {
        for (c8=max(256*c2,64*c1-64*c2+64);c8<=min(256*c2+255,N-1);c8++) {
          A[64*c1-64*c2+63][c8]=A[64*c1-64*c2+63][c8]/A[64*c1-64*c2+63][64*c1-64*c2+63] ;
        }
      }
    }
  }
}
/* End of CLooG code */

/*@ end @*/
/*@ end @*/




      annot_t_end = rtclock();
      annot_t_total += annot_t_end - annot_t_start;
    }

  annot_t_total = annot_t_total / REPS;

#ifndef TEST
  printf("%f\n", annot_t_total);
#else
  {
    int i, j;
    for (i=0; i<N; i++) {
      for (j=0; j<N; j++) {
        if (j%100==0)
          printf("\n");
        printf("%f ",A[i][j]);
      }
      printf("\n");
    }
  }
#endif

  return ((int) A[0][0]);

}
