#include <iostream>

int main() {
    for (int value : {-3, 0, 4, 9}) {
        if (value < 0) {
            std::cout << "negative\n";
        } else if (value == 0) {
            std::cout << "zero\n";
        } else if (value % 2 == 0) {
            std::cout << "positive-even\n";
        } else {
            std::cout << "positive-odd\n";
        }
    }
    return 0;
}
