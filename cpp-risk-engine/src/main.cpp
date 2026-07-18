#include <iostream>
#include <string>

class Position {
    public:
        Position(
            const std::string& symbol,
            int quantity,
            double price
        )
            : symbol_(symbol),
              quantity_(quantity),
              price_(price) {}

        double market_value() const {
            return quantity_ * price_;
        }
    
    private:
        std::string symbol_;
        int quantity_;
        double price_;
};

int main() {
    const Position position("AAPL",10, 230.50);
    std::cout
        << "Market Value: "
        <<position.market_value()
        <<'\n';
    
    return 0;
}