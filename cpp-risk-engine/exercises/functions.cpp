#include <iostream>
#include <string>

double calc_average(int n1, int n2){

    double average = (n1+n2)/2.0;
    return average;
}

double calculate_pnl(
    double entry_price, 
    double current_price,
    int quantity
){
    double pnl = (current_price - entry_price) * quantity;
    return pnl;
}

int main(){

    int n1 = 4, n2 = 5;
    double average = calc_average(n1,n2);
    std::cout
        <<"The average of "<<n1<<" and "<<n2<<" is: "
        <<average
        <<'\n';
    
    double entry_price = 10, current_price = 15;
    int quantity = 10;
    double pnl = calculate_pnl(entry_price, current_price, quantity);
    std::cout
        <<"The profit is: "
        <<pnl
        <<'\n';
    
    current_price = 9.9;
    pnl = calculate_pnl(entry_price, current_price, quantity);
    std::cout
        <<"The profit is: "
        <<pnl
        <<'\n';
    return 0;
}