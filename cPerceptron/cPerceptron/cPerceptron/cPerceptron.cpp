#include "cPerceptron.h"

DLLEXPORT double calculate(struct cPerceptron *pc){
	double total = 0;

	for(int i = 0; i < pc->numInput; i++){
		total += pc->dataX[pc->indexes[i]]*pc->weights[i];
	}
		
	if((total < 1.0/((double)pc->numInput+1.0)) == pc->region){
		return 0.0;
	}
	else{
		return 1.0;
	}
}