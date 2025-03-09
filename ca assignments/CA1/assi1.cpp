#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>

using namespace std;

void generateRandomNumbers(vector<int>& numbers);
void printNumbers(const vector<int>& numbers);
void checkOddEven(const vector<int>& numbers);
void checkPrime(const vector<int>& numbers);
void computeFactorials(const vector<int>& numbers, vector<unsigned long long>& factorials);
void computePrefixSums(const vector<int>& numbers, vector<unsigned long long>& prefixSums);
double computeAverage(const vector<int>& numbers);

bool isPrime(int num);

int main() {
    srand(time(0));

    vector<int> numbers(100);  
    vector<unsigned long long> factorials(numbers.size());
    vector<unsigned long long> prefixSums(numbers.size());

    generateRandomNumbers(numbers);

    printNumbers(numbers);

    checkOddEven(numbers);

    checkPrime(numbers);

    computeFactorials(numbers, factorials);
    computePrefixSums(numbers, prefixSums);

    cout << "Factorials:" << endl;
    for (size_t i = 0; i < factorials.size(); ++i) {
        cout << "Factorial of " << numbers[i] << " is " << factorials[i] << endl;
    }

    cout << "Prefix Sums:" << endl;
    for (size_t i = 0; i < prefixSums.size(); ++i) {
        cout << "Prefix sum at index " << i << " is " << prefixSums[i] << endl;
    }

    double average = computeAverage(numbers);
    cout << "Average: " << average << endl;

    return 0;
}

void generateRandomNumbers(vector<int>& numbers) {
    for (int& num : numbers) {
        num = rand() % 10000 + 1;
    }
}

void printNumbers(const vector<int>& numbers) {
    cout << "Generated numbers: ";
    for (const int& num : numbers) {
        cout << num << " ";
    }
    cout << endl;
}

void checkOddEven(const vector<int>& numbers) {
    cout << "Odd/Even check:" << endl;
    for (const int& num : numbers) {
        if (num % 2 == 0) {
            cout << num << " is even." << endl;
        } else {
            cout << num << " is odd." << endl;
        }
    }
}

void checkPrime(const vector<int>& numbers) {
    cout << "Prime check:" << endl;
    for (const int& num : numbers) {
        if (isPrime(num)) {
            cout << num << " is prime." << endl;
        } else {
            cout << num << " is not prime." << endl;
        }
    }
}

void computeFactorials(const vector<int>& numbers, vector<unsigned long long>& factorials) {
    for (size_t i = 0; i < numbers.size(); ++i) {
        unsigned long long factorial = 1;
        for (int j = 1; j <= (numbers[i] % 20) + 1; ++j) {  
            factorial *= j;
        }
        factorials[i] = factorial;
    }
}

void computePrefixSums(const vector<int>& numbers, vector<unsigned long long>& prefixSums) {
    prefixSums[0] = numbers[0];
    for (size_t i = 1; i < numbers.size(); ++i) {
        prefixSums[i] = prefixSums[i - 1] + numbers[i];
    }
}

double computeAverage(const vector<int>& numbers) {
    unsigned long long sum = 0;
    for (const int& num : numbers) {
        sum += num;
    }
    return static_cast<double>(sum) / numbers.size();
}

bool isPrime(int num) {
    if (num <= 1) return false;
    if (num == 2 || num == 3) return true;
    if (num % 2 == 0 || num % 3 == 0) return false;
    for (int i = 5; i * i <= num; i += 6) {
        if (num % i == 0 ) return false;
    }
    return true;
}
