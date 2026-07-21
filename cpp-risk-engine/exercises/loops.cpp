#include <iostream>
#include <string>

int main(){
    double pnl[5];
    std::cout
        <<"Enter 5 numbers: "
        <<'\n';
    for (int i=0; i<5; i++){
        std::cin
            >>pnl[i];
    }
    int count_pos = 0;
    int count_neg = 0;
    int count_zero = 0;
    double sum = 0.0;
    double avg = 0.0;
    for (int j=0;j<5;j++){
        if (pnl[j]>0){
            count_pos++;
            std::cout
                <<"The PnL is positive: "
                <<pnl[j]
                <<'\n';
        }
        else if(pnl[j]<0){
            count_neg++;
            std::cout
                <<"The PnL is negative: "
                <<pnl[j]
                <<'\n';
        }
        else{
            count_zero++;
            std::cout
                <<"The PnL is : "
                <<pnl[j]
                <<'\n';
        }
        sum+=pnl[j];
    }
    avg = sum / 5;
    std::cout
        <<"The total count of positive pnl: "
        <<count_pos
        <<", negative pnl: "
        <<count_neg
        <<", and pnl of value 0: "
        <<count_zero
        <<"."
        <<'\n';
    std::cout
        <<"The sum of PnL series is "
        <<sum
        <<" and the average is "
        <<avg
        <<'\n';
    return 0;
}
    
