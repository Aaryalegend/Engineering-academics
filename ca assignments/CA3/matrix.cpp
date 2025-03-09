//program by 22610017 batch T4
#include <iostream>
#include <vector>
#include <omp.h>
#include <cstdlib>
#include <ctime>
#include <fstream>

using namespace std;


vector<vector<int>> multiplyMatrix(const vector<vector<int>> &mat1, const vector<vector<int>> &mat2) {
    int rows1 = mat1.size();        
    int cols1 = mat1[0].size();     
    int cols2 = mat2[0].size();     

    vector<vector<int>> resultMatrix(rows1, vector<int>(cols2, 0));

    #pragma omp parallel for collapse(2)
    for (int x = 0; x < rows1; x++) {
        for (int y = 0; y < cols2; y++) {
            // Multiply corresponding elements and accumulate the result
            for (int z = 0; z < cols1; z++) {
                resultMatrix[x][y] += mat1[x][z] * mat2[z][y];
            }
        }
    }

    return resultMatrix; 
}

int main() {
    srand(time(0)); // Seed for random number generation

    // Define two 1024x1024 matrices
    vector<vector<int>> mat1(1024, vector<int>(1024));
    vector<vector<int>> mat2(1024, vector<int>(1024));

    // Initialize matrices with random values between 0 and 99
    for (int i = 0; i < 1024; i++) {
        for (int j = 0; j < 1024; j++) {
            mat1[i][j] = rand() % 100;
            mat2[i][j] = rand() % 100;
        }
    }

    
    ofstream outputFile("times.csv");
    outputFile << "Threads,Time(s)" << endl;

    const int maxThreads = 8; 

    for (int threads = 1; threads <= maxThreads; threads++) {
        omp_set_num_threads(threads); // Set the number of threads for OpenMP
        double start = omp_get_wtime(); // Get the start time

        // Perform matrix multiplication
        vector<vector<int>> result = multiplyMatrix(mat1, mat2);

        double end = omp_get_wtime(); // Get the end time
        double elapsed = end - start; 

        outputFile << threads << "," << elapsed << endl;

        
        cout << "Thread " << threads << " completed in " << elapsed << " seconds" << endl;
    }

    outputFile.close(); 
    cout << "Matrix Multiplication Completed" << endl; 

    return 0;
}
