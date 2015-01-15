#ifndef C_PERCEPTRON_FOR_PYTHON
#define C_PERCEPTRON_FOR_PYTHON

#define DLLEXPORT extern "C" __declspec(dllexport)

struct cPerceptron{
	double* dataX;
	int numInput;
	double* weights;
	int* indexes;
	bool region;
};

DLLEXPORT double calculate(struct cPerceptron *pc);

#endif