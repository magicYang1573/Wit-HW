
module fsm_16(
    clk,
    reset,
    input1,
    input2,
    state
);

input clk;
input reset;
input input1;
input input2;
output [3:0] state;

wire clk;
wire reset;
wire input1;
wire input2;
reg [3:0] state;

localparam S0 = 4'b0000, S1 = 4'b0001, S2 = 4'b0010, S3 = 4'b0011,
           S4 = 4'b0100, S5 = 4'b0101, S6 = 4'b0110, S7 = 4'b0111,
           S8 = 4'b1000, S9 = 4'b1001, S10 = 4'b1010, S11 = 4'b1011,
           S12 = 4'b1100, S13 = 4'b1101, S14 = 4'b1110, S15 = 4'b1111;

always @(posedge clk) begin
    if (reset) begin
        state <= S0;  
    end else begin
            if(state==S0)  
                if(input1 & input2) begin
                    state <= S1;
                end else begin
                    state <= S2;
                end
            else if(state==S1)    
                if(!input1 & input2) begin
                    state <= S3;
                end else begin
                    state <= S4;
                end
            else if(state==S2)    
                if(input1 & !input2) begin
                    state <= S5;
                end else begin
                    state <= S6;
                end
            else if(state==S3)    
                if(!input1 & !input2) begin
                    state <= S7;
                end else begin
                    state <= S8;
                end
            else if(state==S4) 
                if(input1 | input2) begin
                    state <= S9;
                end else begin
                    state <= S10;
                end
            else if(state==S5)     
                if(!input1 | input2) begin
                    state <= S11;
                end else begin
                    state <= S12;
                end
            else if(state==S6)    
                if(input1 | !input2) begin
                    state <= S13;
                end else begin
                    state <= S14;
                end
            else if(state==S7)   
                if(!input1 | !input2) begin
                    state <= S15;
                end else begin
                    state <= S0;
                end
            else if(state==S8)    
                if(input1 & input2) begin
                    state <= S1;
                end else begin
                    state <= S2;
                end
            else if(state==S9)   
                if(!input1 & input2) begin
                    state <= S3;
                end else begin
                    state <= S4;
                end
            else if(state==S10)   
                if(input1 & !input2) begin
                    state <= S5;
                end else begin
                    state <= S6;
                end
            else if(state==S11)   
                if(!input1 & !input2) begin
                    state <= S7;
                end else begin
                    state <= S8;
                end
            else if(state==S12)   
                if(input1 | input2) begin
                    state <= S9;
                end else begin
                    state <= S10;
                end
            else if(state==S13)   
                if(!input1 | input2) begin
                    state <= S11;
                end else begin
                    state <= S12;
                end
            else if(state==S14)   
                if(input1 | !input2) begin
                    state <= S13;
                end else begin
                    state <= S14;
                end
            else 
                if(!input1 | !input2) begin
                    state <= S15;
                end else begin
                    state <= S0;
                end
    end
end

endmodule
