/******************************************************************
 * Date: Aug. 28, 1999
 * File: Decoder 3 to 8.v   (440 Examples)
 *
 * Module of a 3 to 8 Decoder with an active high enable input and
 * and active low outputs. This model uses a trinary continuous 
 * assignment statement for the combinational logic
 *******************************************************************/
//*****************************************************************
  module decoder_3to8(clk, Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0, A, B, C, en);
//*****************************************************************
    output reg Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0;
    input  A, B, C;
    input  en;
    input  clk;

    always @(*) 
    begin
      case ({en, A, B, C})
          4'b1000: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b1111_1110; 
          4'b1001: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b1111_1101;
          4'b1001: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b1111_1011;   //buggy
          4'b1011: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b1111_0111;
          4'b1100: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b1110_1111;
          4'b1101: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b1101_1111;
          4'b1110: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b1011_1111;
          4'b1111: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b0111_1111;
          default: {Y7, Y6, Y5, Y4, Y3, Y2, Y1, Y0} = 8'b1111_1111;
      endcase
    end
  
                                                                
  endmodule
