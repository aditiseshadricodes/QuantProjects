#include <iostream>
#include <string>

double calculate_pnl(
    double entry_price, 
    double current_price,
    int quantity
){
    double pnl = (current_price - entry_price) * quantity;
    return pnl;
}

int main(){

    double entry_price, current_price;
    int quantity;
    std::cout
        <<"Enter the entry_price: "
        <<'\n';
    std::cin
        >>entry_price;
    
    std::cout
        <<"Enter the current_price: "
        <<'\n';
    std::cin
        >>current_price;
    
    std::cout
        <<"Enter the quantity: "
        <<'\n';
    std::cin
        >>quantity;
    
    double pnl = calculate_pnl(entry_price, current_price, quantity);
    if (pnl>0){
        std::cout
            <<"The PnL is positive: "
            <<pnl
            <<'\n';
    }
    else if(pnl<0){
        std::cout
            <<"The PnL is negative: "
            <<pnl
            <<'\n';
    }
    else{
        std::cout
            <<"The PnL is : "
            <<pnl
            <<'\n';
    }
    return 0;
}