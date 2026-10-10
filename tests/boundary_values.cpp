#include <iostream>
#include <limits>

int main() {
    const int low = std::numeric_limits<int>::min();
    const int high = std::numeric_limits<int>::max();
    std::cout << (low < 0) << '\n';
    std::cout << (high > 0) << '\n';
    std::cout << (low == high) << '\n';
    return 0;
}
